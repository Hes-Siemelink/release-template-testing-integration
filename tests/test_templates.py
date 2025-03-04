import unittest
import subprocess

class TestMyTemplate(unittest.TestCase):

    def test_script_success(self):

        process = subprocess.run(['xl', 'apply', '-f', 'tests/run-test-release.yaml'], capture_output=True, text=True, check=False)

        self.assertEqual(process.returncode, 0, f"Script failed with exit code {process.returncode}. Output:\n{process.stdout}\n{process.stderr}")

