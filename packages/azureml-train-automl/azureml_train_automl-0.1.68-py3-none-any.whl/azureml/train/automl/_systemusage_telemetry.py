# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""_systemusage_telemetry.py, A file system usage telemetry classes"""

import abc
import os
import subprocess
import sys

from ._timer_utilities import TimerCallback


class SystemResourceUsageTelemetryFactory:
    """System resource usage telemetry collection factory class"""
    @staticmethod
    def get_system_usage_telemetry(logger, interval=10, **kwargs):
        """
        gets system usage telemetry object based on platform
        :param logger: logger
        :param interval: interval in sec
        :return: SystemResourceUsageTelemetry : platform specific object
        """
        if sys.platform == "win32":
            return _WindowsSystemResourceUsageTelemetry(logger, interval=interval, **kwargs)

        return _NonWindowsSystemResourceUsageTelemetry(logger, interval=interval, **kwargs)


class SystemResourceUsageTelemetry:
    """System usage telemetry abstract class"""
    def __init__(self, logger, interval=10, **kwargs):
        """
        initializes system resource usage telemetry class
        :param logger: logger
        :param interval: interval in sec
        :param kwargs: kwargs
        """
        self.logger = logger
        self.interval = interval
        self.kwargs = kwargs
        self._timer = None

    def start(self):
        """
        starts usage collection
        :return:
        """
        pass

    def stop(self):
        """
        stops collection
        :return:
        """
        pass

    def __del__(self):
        """
        cleanup
        :return:
        """
        pass

    def _log_memory_usage(self, mem_usage, prefix_message=''):
        """
        log memory usage
        """
        extra_info = {'properties': {'Type': 'MemoryUsage', 'Usage': mem_usage}}
        if prefix_message is None:
            prefix_message = ''
        self.logger.info("{}memory usage {}".format(prefix_message, mem_usage), extra=extra_info)

    def _log_cpu_usage(self, cpu_time, cores, system_time=None, prefix_message=''):
        """
        log cpu usage
        """
        extra_info = {'properties': {'Type': 'CPUUsage', 'CPUTime': cpu_time, 'Cores': cores}}
        if system_time is not None:
            extra_info['properties']["SystemTime"] = system_time
        if prefix_message is None:
            prefix_message = ''
        self.logger.info("{}cpu time {}".format(prefix_message, cpu_time), extra=extra_info)

    def send_usage_telemetry_log(self, prefix_message=None, is_sending_telemetry=True):
        """
        send the usage telemetry log based on automl settings with message.

        :param telemetry_logger: Object of SystemResourceUsageTelemetry.
        :param prefix_message: The prefix of logging message.
        :param is_sending_telemetry: the switch controls whether send log or not.
        :return: None
        """
        if not is_sending_telemetry:
            return

        try:
            self._get_usage(prefix_message)
        except Exception:
            pass  # do nothing

    @abc.abstractmethod
    def _get_usage(self, prefix_message=None):
        raise NotImplementedError


class _WindowsSystemResourceUsageTelemetry(SystemResourceUsageTelemetry):
    """
    Telemetry Class for collecting system usage
    """

    def __init__(self, logger, interval=10, **kwargs):
        """
        Constructor
        :param logger: logger
        :param interval: collection frequency in seconds
        :param kwargs:
        """
        self._cmd = "tasklist /v /fi \"pid eq {}\" /fo csv".format(os.getpid())
        super(_WindowsSystemResourceUsageTelemetry, self).__init__(logger, interval=interval, **kwargs)

    def start(self):
        """
        starts usage collection
        :return:
        """
        self.logger.info("Starting usage telemetry collection")
        self._timer = TimerCallback(interval=self.interval, logger=self.logger, callback=self._get_usage)

    def _get_usage(self, prefix_message=None):
        """
        gets usage
        :return:
        """
        try:
            import csv
            from io import StringIO

            proc = subprocess.Popen(self._cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            data = out.decode('utf-8')

            csv_reader = csv.reader(StringIO(data))
            mem_index = -1
            cpu_index = -1
            lines = 0
            for row in csv_reader:
                lines += 1

                if lines == 1:  # header
                    mem_index = row.index('Mem Usage')
                    cpu_index = row.index('CPU Time')
                    continue

                if mem_index != -1:
                    self._log_memory_usage(row[mem_index], prefix_message)

                if cpu_index != -1:
                    self._log_cpu_usage(row[cpu_index], os.cpu_count(), prefix_message=prefix_message)
        except Exception as e:
            self.logger.info(e)

    def stop(self):
        """
        stops timer
        :return:
        """
        if self._timer is not None:
            self._timer.stop()

    def __del__(self):
        """
        destructor
        :return:
        """
        self.stop()


class _NonWindowsSystemResourceUsageTelemetry(SystemResourceUsageTelemetry):
    """Linux, Mac & other os"""

    def __init__(self, logger=None, interval=10, **kwargs):
        self.logger = logger
        self.interval = interval
        self.kwargs = kwargs
        self._timer = None
        super(_NonWindowsSystemResourceUsageTelemetry, self).__init__(logger=logger, interval=interval, **kwargs)

    def start(self):
        """
        starts usage collection
        :return:
        """
        self.logger.info("Starting usage telemetry collection")
        self._timer = TimerCallback(interval=self.interval, logger=self.logger, callback=self._get_usage)

    def _get_usage(self, prefix_message=None):
        """
        gets usage
        :return:
        """
        try:
            import resource
            res = resource.getrusage(resource.RUSAGE_SELF)

            self._log_memory_usage(res.ru_maxrss, prefix_message)

            self._log_cpu_usage(res.ru_utime, os.cpu_count(), res.ru_stime, prefix_message)
        except Exception as e:
            self.logger.info(e)

    def stop(self):
        """
        stops timer
        :return:
        """
        if self._timer is not None:
            self._timer.stop()

    def __del__(self):
        """
        destructor
        :return:
        """
        self.stop()
