import logging
import sys
import time
import unittest
from threading import Thread
from datetime import datetime

import xmlrunner

from azureml.telemetry import AML_INTERNAL_LOGGER_NAMESPACE
from azureml.telemetry import INSTRUMENTATION_KEY
from azureml.telemetry.logging_handler import get_appinsights_log_handler, \
    AppInsightsLoggingHandler, _RetrySynchronousSender
from tests.appinsightslogginghandler_mock import AppInsightsLoggingHandlerMock
from tests.notifyhandler import NotifyHandler


class AppInsightTests(unittest.TestCase):
    """
    App insight tests
    """

    def __init__(self, *args, **kwargs):
        super(AppInsightTests, self).__init__(*args, **kwargs)

    def test_appinsight_handler(self):
        """
        Test method for validating adding app insight to parent logger
        :return: None
        """
        logger = self.getBasicLogger()
        appInsightHandler = get_appinsights_log_handler(INSTRUMENTATION_KEY, self.getAppinsightLogger(), 'test')
        logger.addHandler(appInsightHandler)

        appInsightHandler1 = get_appinsights_log_handler(INSTRUMENTATION_KEY, self.getAppinsightLogger())
        logger.addHandler(appInsightHandler1)
        self.assertEqual(logger.handlers.count(appInsightHandler), 1)
        self.assertEqual(logger.handlers.count(appInsightHandler1), 1)
        self.cleanup(logger)

    def test_appinsight_faulty(self):
        """
        Test method for invalid key, expectation is no exception should be thrown from app insight
        :return: None
        """
        logger = self.getBasicLogger()
        properties = {'foo': 'bar'}
        appInsightHandler = get_appinsights_log_handler(INSTRUMENTATION_KEY + 'junk',
                                                        self.getAppinsightLogger(), properties=properties)
        logger.addHandler(appInsightHandler)

        self.assertEqual(logger.handlers.count(appInsightHandler), 1)

        logger.info('info message')
        logger.warning('Warning message')
        logger.exception('exception message')

        time.sleep(1)
        self.cleanup(logger)

    def test_emit(self):
        """
        test method for validating app insight emit
        :return: None
        """
        logger = self.getBasicLogger()

        notifyHandler = NotifyHandler()
        properties = {'foo': 'bar', 'prop1': 'val1'}
        appInsightHandler = AppInsightsLoggingHandlerMock(INSTRUMENTATION_KEY, self.getAppinsightLogger(),
                                                          notify=notifyHandler, properties=properties)
        logger.addHandler(appInsightHandler)

        logger.info('info message')
        logger.warning('Warning message')
        logger.exception('exception message')

        self.assertEqual(3, notifyHandler.queue.qsize())
        self.cleanup(logger)

    def test_emit_verbosity(self):
        """
        Test for validating different level of verbosity from parent
        :return: None
        """
        logger = self.getBasicLogger()

        notifyHandler = NotifyHandler()
        appInsightHandler = AppInsightsLoggingHandlerMock(INSTRUMENTATION_KEY, self.getAppinsightLogger(),
                                                          notify=notifyHandler)
        logger.addHandler(appInsightHandler)

        appInsightHandler.setLevel(logging.WARNING)

        logger.info('info message')
        logger.warning('Warning message')
        logger.exception('exception message')

        self.assertEqual(2, notifyHandler.queue.qsize())
        self.cleanup(logger)

    def test_flush(self):
        """
        Test for validating flush
        :return: None
        """
        logger = self.getBasicLogger()

        appInsightHandler = get_appinsights_log_handler(INSTRUMENTATION_KEY, self.getAppinsightLogger())
        logger.addHandler(appInsightHandler)

        start_time = datetime.now()
        for c in range(10):
            logger.info('info message {}'.format(c))
            logger.warning('Warning message')
            appInsightHandler.flush()

        end_time = datetime.now()
        runtime1 = (end_time - start_time).total_seconds()
        self.assertTrue(runtime1 < 1, "time taken {}, start {},end {}".format(runtime1, start_time, end_time))

        self.cleanup(logger)

    def test_flush_multi_threaded(self):
        """
        Test for validating flush with multi-threaded
        :return: None
        """
        logger = self.getBasicLogger()
        properties = {'foo': 'bar', 'prop1': 'val1'}

        appInsightHandler = get_appinsights_log_handler(INSTRUMENTATION_KEY, self.getAppinsightLogger(),
                                                        properties=properties)
        logger.addHandler(appInsightHandler)

        thread_flush1 = Thread(target=self._call_flush, args=(self, "thread1", appInsightHandler, .1))
        thread_flush2 = Thread(target=self._call_flush, args=(self, "thread2", appInsightHandler, .1))
        thread_logging = Thread(target=self._log_message, args=(self, "thread3", logger, .1))
        thread_logging_exception = Thread(target=self._log_exception_message, args=(self, "thread4", logger, .1))

        threads = {thread_flush1, thread_flush2, thread_logging, thread_logging_exception}
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # flush
        appInsightHandler.flush()
        self.cleanup(logger)

    def test_bad_host(self):
        """
        Test for validating invalid host
        :return: None
        """
        logger = self.getBasicLogger()

        appInsightHandler = AppInsightsLoggingHandler(INSTRUMENTATION_KEY, self.getAppinsightLogger(),
                                                      _RetrySynchronousSenderMock)
        logger.addHandler(appInsightHandler)
        appInsightHandler.setLevel(logging.INFO)

        for c in range(5):
            logger.exception('exception message')
            appInsightHandler.flush()

        self.cleanup(logger)

    @staticmethod
    def _call_flush(self, name, appinsight_handler, delay):
        for i in range(100):
            print('calling flush {}'.format(name))
            appinsight_handler.flush()
            time.sleep(delay)

    @staticmethod
    def _log_message(self, name, logger, delay):
        for i in range(20):
            logger.info('info message {}'.format(i))
            time.sleep(delay)

    @staticmethod
    def _log_exception_message(self, name, logger, delay):
        for i in range(20):
            logger.exception('exception message {}'.format(i))
            time.sleep(delay)

    @staticmethod
    def getBasicLogger():
        logger = logging.getLogger(AML_INTERNAL_LOGGER_NAMESPACE).getChild(__name__)
        logger.setLevel(logging.DEBUG)
        stdout_logger = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_logger)
        logger.propagate = False
        return logger

    @staticmethod
    def getAppinsightLogger():
        logger = logging.getLogger('AppInsight').getChild(__name__)
        logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def cleanup(logger):
        count = len(logger.handlers)
        while count > 0:
            logger.handlers.pop()
            count = count - 1


class _RetrySynchronousSenderMock(_RetrySynchronousSender):
    def __init__(self, logger, timeout=10, retry=3):
        super(_RetrySynchronousSenderMock, self).__init__(logger, timeout, retry)
        self.service_endpoint_uri = 'http://localhost:1234'


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
