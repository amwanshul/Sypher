import sys
import unittest
from unittest.mock import patch
from actions.cmd_control import _run_silent

class TestCommandInjection(unittest.TestCase):
    @patch("actions.cmd_control._get_platform")
    def test_injection_mitigation(self, mock_platform):
        mock_platform.return_value = "linux"

        malicious_command = "echo hello; echo injected"
        output = _run_silent(malicious_command)

        # When passed as a list without shell=True, "echo" will receive "hello;" "echo" "injected"
        # as arguments, rather than executing "echo injected" as a separate command.
        # So the output should contain "injected", but "hello; echo injected" should be on one line
        # since it's just the echo command echoing everything.
        print("Output:", repr(output))
        self.assertIn("hello;", output)
        self.assertIn("injected", output)

        # Testing another common injection technique
        malicious_command2 = "ls -la & echo hacked"
        output2 = _run_silent(malicious_command2)
        print("Output2:", repr(output2))

        # Depending on if 'ls' exists or fails with those arguments, we just want to make sure it didn't
        # execute 'echo hacked'. If it didn't use shell=True, ls will look for a file named '&' and 'echo' and 'hacked'.
        # The output shouldn't just be "hacked"
        self.assertNotIn("hacked\n", output2)
        # Even if 'hacked' is in output because ls prints error about file 'hacked' not found
        # it shouldn't execute the command `echo hacked`.

if __name__ == "__main__":
    unittest.main()
