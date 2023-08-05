"""Limit function calls to specified resource constraints.

Adapted from:
 https://github.com/sfalkner/pynisher
"""
import logging
import multiprocessing
import os

try:

    import resource
    import signal
    import sys
    import time

    from automl.client.core.common import constants
    from automl.client.core.common import killable_subprocess

    class CpuTimeoutException(Exception):
        """
        Exception to raise when the cpu time exceeded.
        """

        def __init__(self):
            """
            default constructor.
            """
            super(CpuTimeoutException, self).__init__(
                constants.ClientErrors.EXCEEDED_TIME_CPU)

    class TimeoutException(Exception):
        """
        Exception to raise when the total execution time exceeded.
        """

        def __init__(self, value=None):
            """
            the time out exception
            :param value: time consumed
            """
            super(TimeoutException, self).__init__(
                constants.ClientErrors.EXCEEDED_TIME)
            self.value = value

    class MemorylimitException(Exception):
        """
        Exception to raise when memory exceeded.
        """

        def __init__(self, value=None):
            """
            memory exception
            :param value:  the memory consumed.
            """
            super(MemorylimitException, self).__init__(
                constants.ClientErrors.EXCEEDED_MEMORY)
            self.value = value

    class SubprocessException(Exception):
        """
         Exception to raise when subprocess terminated.
        """

        def __init__(self):
            """
            construtor
            """
            super(SubprocessException, self).__init__(
                constants.ClientErrors.SUBPROCESS_ERROR)

    class AnythingException(Exception):
        """
         Exception to raise for all other exceptoms
        """

        def __init__(self):
            """
            default constructor.
            """
            super(AnythingException, self).__init__(
                constants.ClientErrors.GENERIC_ERROR)

    def subprocess_func(func, pipe, logger, mem_in_mb, cpu_time_limit_in_s,
                        wall_time_limit_in_s, num_procs,
                        grace_period_in_s, *args, **kwargs):
        """
        create the function the subprocess can execute
        :param func: the functiom to enforce limit on
        :param pipe: the pipe to communicate the result
        :param logger:
        :param mem_in_mb:
        :param cpu_time_limit_in_s:
        :param wall_time_limit_in_s:
        :param num_procs:
        :param grace_period_in_s:
        :param args: the args fot the functiom
        :param kwargs: the kwargs for function
        :return:
        """

        # simple signal handler to catch the signals for time limits
        def handler(signum, frame):
            # logs message with level debug on this logger
            logger.debug("signal handler: %i" % signum)
            if (signum == signal.SIGXCPU):
                # when process reaches soft limit --> a SIGXCPU signal is
                # sent (it
                # normally terminats the process)
                raise CpuTimeoutException()
            elif (signum == signal.SIGALRM):
                # SIGALRM is sent to process when the specified time limit to
                # an alarm function elapses (when real or clock time elapses)
                logger.debug("timeout")
                raise TimeoutException()
            raise AnythingException()

        # catching all signals at this point turned out to interfere with the
        # subprocess (e.g. using ROS)
        signal.signal(signal.SIGALRM, handler)
        signal.signal(signal.SIGXCPU, handler)
        signal.signal(signal.SIGQUIT, handler)

        # code to catch EVERY catchable signal (even X11 related ones ... )
        # only use for debugging/testing as this seems to be too intrusive.
        """
        for i in [x for x in dir(signal) if x.startswith("SIG")]:
            try:
                signum = getattr(signal,i)
                print("register {}, {}".format(signum, i))
                signal.signal(signum, handler)
            except:
                print("Skipping %s"%i)
        """

        # set the memory limit
        if mem_in_mb is not None:
            # byte --> megabyte
            mem_in_b = mem_in_mb * 1024 * 1024
            # the maximum area (in bytes) of address space which may be taken
            # by the process.
            resource.setrlimit(resource.RLIMIT_AS, (mem_in_b, mem_in_b))

        # for now: don't allow the function to spawn subprocesses itself.
        # resource.setrlimit(resource.RLIMIT_NPROC, (1, 1)) Turns out, this is
        # quite restrictive, so we don't use this option by default
        if num_procs is not None:
            resource.setrlimit(resource.RLIMIT_NPROC, (num_procs, num_procs))

        # schedule an alarm in specified number of seconds
        if wall_time_limit_in_s is not None:
            signal.alarm(wall_time_limit_in_s)

        if cpu_time_limit_in_s is not None:
            # From the Linux man page: When the process reaches the soft
            # limit, it is sent a SIGXCPU signal. The default action for this
            # signal is to  terminate the process. However, the signal can
            # be caught, and the handler can return control to the main
            # program. If the process continues to consume CPU time, it will
            # be sent SIGXCPU once per second until the hard limit is
            # reached, at which time it is sent SIGKILL.
            resource.setrlimit(
                resource.RLIMIT_CPU, (cpu_time_limit_in_s,
                                      cpu_time_limit_in_s + grace_period_in_s))

        # the actual function call
        try:
            logger.debug("call function")
            return_value = ((func(*args, **kwargs), 0))
            logger.debug("function returned properly: {}".format(return_value))
        except MemoryError as e:
            return_value = (None, MemorylimitException())

        except OSError as e:
            if (e.errno == 11):
                return_value = (None, SubprocessException())
            else:
                return_value = (None, AnythingException())

        except CpuTimeoutException as e:
            return_value = (None, CpuTimeoutException())

        except TimeoutException as e:
            return_value = (None, TimeoutException())

        except AnythingException as e:
            return_value = (None, AnythingException())
        except Exception as e:
            return_value = (None, e)
            logger.error("Unexpected Error", exc_info=True)

        finally:
            try:
                logger.debug("return value: {}".format(return_value))

                pipe.send(return_value)
                pipe.close()

            except Exception:
                # this part should only fail if the parent process is already
                # dead, so there is not much to do anymore :)
                pass
            finally:
                # recursively kill all children
                pid = os.getpid()
                killable_subprocess.kill_process_tree_in_linux(pid)

    class enforce_limits(object):
        """
        The class to enforce the resourse limit on Linux.
        """

        def __init__(self, mem_in_mb=None, cpu_time_in_s=None,
                     wall_time_in_s=None, num_processes=None,
                     grace_period_in_s=None, logger=None,
                     log_function_parameters=False):
            """
            The resource limit to be enforced.
            :param mem_in_mb:
            :param cpu_time_in_s:
            :param wall_time_in_s:
            :param num_processes:
            :param grace_period_in_s:
            :param logger:
            :param log_function_parameters:
            """
            self.mem_in_mb = mem_in_mb
            self.cpu_time_in_s = cpu_time_in_s
            self.num_processes = num_processes
            self.wall_time_in_s = wall_time_in_s
            self.grace_period_in_s = (
                0 if grace_period_in_s is None else grace_period_in_s)
            self.logger = (
                logger if logger is not None else multiprocessing.get_logger())
            self.log_function_parameters = log_function_parameters

            if self.mem_in_mb is not None:
                self.logger.debug(
                    "Restricting your function to {} mb memory."
                    .format(self.mem_in_mb))
            if self.cpu_time_in_s is not None:
                self.logger.debug(
                    "Restricting your function to {} seconds cpu time."
                    .format(self.cpu_time_in_s))
            if self.wall_time_in_s is not None:
                self.logger.debug(
                    "Restricting your function to {} seconds wall time."
                    .format(self.wall_time_in_s))
            if self.num_processes is not None:
                self.logger.debug(
                    "Restricting your function to {} threads/processes."
                    .format(self.num_processes))
            if self.grace_period_in_s is not None:
                self.logger.debug(
                    "Allowing a grace period of {} seconds."
                    .format(self.grace_period_in_s))

        def __call__(self, func):
            """
            executes the functions with the resource constarints
            :param func: the function to be restricted.
            :return:
            """

            class function_wrapper(object):
                def __init__(self2, func):
                    self2.func = func
                    self2.result = None
                    self2.exit_status = None

                def __call__(self2, *args, **kwargs):

                    # create a pipe to retrieve the return value
                    parent_conn, child_conn = multiprocessing.Pipe()

                    # create and start the process
                    subproc = multiprocessing.Process(
                        target=subprocess_func, name="pynisher function call",
                        args=(
                            self2.func,
                            child_conn,
                            self.logger,
                            self.mem_in_mb,
                            self.cpu_time_in_s,
                            self.wall_time_in_s,
                            self.num_processes,
                            self.grace_period_in_s) + args,
                        kwargs=kwargs)

                    if self.log_function_parameters:
                        self.logger.debug(
                            "Function called with argument: {}, {}".format(
                                args, kwargs))

                    # start the process

                    start = time.time()
                    subproc.start()
                    child_conn.close()

                    try:
                        # read the return value
                        if (self.wall_time_in_s is not None):
                            if parent_conn.poll(
                                    self.wall_time_in_s +
                                    self.grace_period_in_s):
                                (self2.result,
                                 self2.exit_status) = parent_conn.recv()
                            else:
                                subproc.terminate()
                                self2.exit_status = TimeoutException()

                        else:
                            self2.result, self2.exit_status = \
                                parent_conn.recv()

                    except EOFError as e:
                        # Don't see that in the unit tests :(
                        self.logger.error(
                            "Your function call closed the pipe prematurely ->"
                            " Subprocess probably got an uncatchable signal.",
                            exc_info=True)

                        self2.resources_function = resource.getrusage(
                            resource.RUSAGE_CHILDREN)
                        self2.resources_pynisher = resource.getrusage(
                            resource.RUSAGE_SELF)
                        self2.exit_status = AnythingException()

                    except Exception as e:
                        self.logger.error(
                            "Something else went wrong, sorry.", exc_info=True)
                    finally:
                        self2.wall_clock_time = time.time() - start
                        self2.exit_status = (
                            5 if self2.exit_status is None
                            else self2.exit_status)
                        # don't leave zombies behind

                        # subproc.join hangs in mac, due to empty queue
                        # deadlock join with timeout doesn't work either,
                        # so forcing terminate. finally is called only after
                        # the timeout period
                        if subproc.is_alive() and sys.platform == 'darwin':
                            subproc.terminate()
                        else:
                            subproc.join()

                    return (self2.result)

            return (function_wrapper(func))

except ImportError as e:
    logging.warn("Could not import resource package. Resource management "
                 "is only supported on Unix-derived OSes.")
