from azureml.telemetry.logging_handler import AppInsightsLoggingHandler


class AppInsightsLoggingHandlerMock(AppInsightsLoggingHandler):
    """
    Mock class for AppInsightsLoggingHandler
    """

    def __init__(self, instrumentationKey, *args, **kwargs):
        self.notify = None

        if 'notify' in kwargs:
            self.notify = kwargs.pop('notify')

        super(AppInsightsLoggingHandlerMock, self).__init__(instrumentationKey, *args, **kwargs)

    def emit(self, record):
        """Emit a record.

        Args:
            record (:class:`logging.LogRecord`). the record to format and send.
        """
        if self.notify is not None:
            self.notify.emit(record)

        super(AppInsightsLoggingHandlerMock, self).emit(record)
