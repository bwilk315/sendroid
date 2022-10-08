
from    plyer   import audio
from    .sensor import Sensor
import  logging


class Audio(Sensor):
    """
        Management class for audio sensor.
    """

    def __init__(self, file_path=None) -> None:
        super().__init__(file_path=file_path)

    def on_disable(self) -> None:
        audio.stop()

    def on_enable(self) -> bool:
        try:
            audio.start()
        except Exception as e:
            logging.error('Failed to enable the audio sensor on device: %s', e)
            return False
        else:
            logging.info('Enabled audio sensor on device.')
            return True

    def record(self) -> None:
        """
            Starts recording audio (using the sensor).
        """
        audio.start()

    def finish(self) -> None:
        """
            Finishes recording and saves data as specified file, if no path to target file
            was specified in class constructor data will remain untill next recording starts.
        """
        audio.stop()

    def play(self) -> None:
        """
            Plays audio using file specified in constructor, or lastly recorded (cached) data.
        """
        audio.play()
