import unittest
import xmlrunner

from azureml.telemetry.logging_handler import AppInsightsLoggingHandler
from azureml.train.telemetry_logger import TelemetryLogger


class TelemetryTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TelemetryTests, self).__init__(*args, **kwargs)

    def test_telemetry_logger(self):
        logger = TelemetryLogger.get_telemetry_logger()
        self.assertEqual(len(logger.handlers), 1)
        self.assertTrue(isinstance(logger.handlers[0], AppInsightsLoggingHandler))


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner())
