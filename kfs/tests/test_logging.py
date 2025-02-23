import logging
from unittest import TestCase


class TestLoggingConfig(TestCase):

    def test_logging_capture(self):
        """Test that the log is captured in the correct format"""

        with self.assertLogs(level="INFO") as captured_logs:
            logging.info("Log message")

        self.assertEqual(len(captured_logs.output), 1)
        self.assertIn("INFO:root:Log message", captured_logs.output[0])
