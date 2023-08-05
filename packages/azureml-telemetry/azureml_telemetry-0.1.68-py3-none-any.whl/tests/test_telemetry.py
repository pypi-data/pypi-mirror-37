import logging
import sys
import unittest
import time
import xmlrunner

from threading import Thread
from azureml.telemetry import set_diagnostics_collection, get_diagnostics_collection_info, \
    get_telemetry_log_handler, add_diagnostics_properties, global_diagnostics_properties, set_diagnostics_properties, \
    AML_INTERNAL_LOGGER_NAMESPACE
from azureml.telemetry.logging_handler import AppInsightsLoggingHandler


class TestTelemetry(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTelemetry, self).__init__(*args, **kwargs)

    def test_enable_usage_statistics_collection(self):
        set_diagnostics_collection(send_diagnostics=True, verbosity=logging.INFO)
        send_diagnostics, verbosity = get_diagnostics_collection_info()
        self.assertTrue(send_diagnostics)
        self.assertEqual(verbosity, logging.getLevelName(logging.INFO))
        set_diagnostics_collection(send_diagnostics=False, verbosity=logging.NOTSET)
        send_diagnostics, verbosity = get_diagnostics_collection_info()
        self.assertFalse(send_diagnostics)
        self.assertEqual(verbosity, logging.getLevelName(logging.NOTSET))

    def test_get_telemetry_log_handler(self):
        set_diagnostics_collection(send_diagnostics=True, verbosity=logging.INFO)
        telemetry_handler = get_telemetry_log_handler()
        self.assertTrue(type(telemetry_handler) is AppInsightsLoggingHandler)
        set_diagnostics_collection(send_diagnostics=False, verbosity=logging.INFO)
        telemetry_handler = get_telemetry_log_handler()
        self.assertTrue(type(telemetry_handler) is logging.NullHandler)

    def test_add_diagnostics_properties(self):
        add_diagnostics_properties({'foo': 'bar', 'foo1': 'bar1'})
        add_diagnostics_properties({'foo2': 'bar2', 'foo12': 'bar2'})
        self.assertTrue(len(global_diagnostics_properties.items()) is 4)

    def test_set_diagnostics_properties(self):
        add_diagnostics_properties({'foo': 'bar', 'foo1': 'bar1'})
        set_diagnostics_properties({'new1': 'val1'})
        self.assertTrue(len(global_diagnostics_properties.items()) is 1)
        self.assertEqual(global_diagnostics_properties['new1'], 'val1')

    def test_multithreaded_telemetry_log_handler(self):
        set_diagnostics_collection(send_diagnostics=True, verbosity=logging.INFO)

        logger = logging.getLogger(AML_INTERNAL_LOGGER_NAMESPACE).getChild(__name__)
        logger.setLevel(logging.DEBUG)
        stdout_logger = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_logger)

        appInsightHandler = get_telemetry_log_handler()
        self.assertTrue(type(appInsightHandler) is AppInsightsLoggingHandler)
        logger.addHandler(appInsightHandler)
        thread_get_handler1 = Thread(target=self._get_telemetry_log_handler, args=("thread1", logger,
                                                                                   appInsightHandler, .1))
        thread_get_handler2 = Thread(target=self._get_telemetry_log_handler, args=("thread2", logger,
                                                                                   appInsightHandler, .1))
        threads = {thread_get_handler1, thread_get_handler2}

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        appInsightHandler.flush()
        set_diagnostics_collection(send_diagnostics=False, verbosity=logging.INFO)

    def _get_telemetry_log_handler(self, name, logger, app_insights_handler, delay):
        print("Thread {}", name)
        for i in range(100):
            handler = get_telemetry_log_handler()
            logger.info('test message')
            time.sleep(delay)
            self.assertTrue(type(app_insights_handler) is AppInsightsLoggingHandler)
            self.assertTrue(type(handler) is AppInsightsLoggingHandler)


if __name__ == "main":
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
