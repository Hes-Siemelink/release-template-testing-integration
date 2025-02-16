from digitalai.release.integration import BaseTask
from digitalai.release.v1.api.release_api import ReleaseApi, Release


class EchoAndWait(BaseTask):

    def execute(self) -> None:

        # Get input properties
        input = self.input_properties['input']
        delay = int(self.input_properties['delay'])

        # Wait
        import time;
        time.sleep(delay)

        # Set output
        self.set_output_property('output', input)

