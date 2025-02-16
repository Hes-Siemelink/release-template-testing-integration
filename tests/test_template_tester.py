import unittest

from src.template_tester import TestTemplate


class TestTestTemplate(unittest.TestCase):

    def test_run(self):

        # Given
        task = TestTemplate()
        task.input_properties = {
            'templateName': 'My Template',
        }

        # When
        task.execute_task()

        # Then
        # ...


if __name__ == '__main__':
    unittest.main()
