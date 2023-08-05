# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
The helper module to restrict the training time on windows
platform.
"""
from multiprocessing import Process, Queue, freeze_support


def process_start_fn(fn, queue, **kwargs):
    """
    Process start function used in creating the new windows
    process
    :param fn: the actual function to be called
    :param queue:  the queue where result will be placed from the fn.
    :param kwargs:  arguments to the fn
    :return:
    """
    result = None, None
    try:
        result = fn(**kwargs)
    finally:
        queue.put((result))


def kill_process(proc):
    """
    terminates the process and all its children.
    :param proc:  the process to terminate
    :return:
    """
    try:
        import psutil
        target = psutil.Process(proc.pid)
        for child in target.children(recursive=True):
            child.kill()
        target.kill()
    except Exception:
        raise


def enforce_time_limit(max_time_in_sec, fn, kwargs):
    """
    function to limited on the execution time
    :param max_time_in_sec: allowed time for the fn.
    :param fn:  the fn to be restricted.
    :param kwargs: arguments for the fn.
    :return:
    """
    if __name__ == "__main__":
        freeze_support()
    q = Queue()
    out = None
    subproc = Process(target=process_start_fn, args=(fn, q), kwargs=kwargs)
    try:
        subproc.start()
        out = q.get(timeout=max_time_in_sec)
    except Exception as e:
        # pid is set only after a process is started successfully.
        try:
            import psutil
            if subproc.pid and psutil.Process().pid != subproc.pid:
                kill_process(subproc)
                subproc.join()
        except Exception:
            raise
        finally:
            if str(e) == "":
                out = None, TimeoutError()
            else:
                out = None, e
            assert (not subproc.is_alive())
    finally:
        return out
