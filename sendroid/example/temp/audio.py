
from    plyer       import audio
from    .sensor     import Sensor


class Audio(Sensor):
    # Audio states.
    STATE_UNKNOWN   = 0
    STATE_RECORDING = 1
    STATE_READY     = 2
    STATE_PLAYING   = 3

    def __init__(self, data_path: str = None, **kwargs):
        """
            Initializes the 'Audio' class instance.
            @param data_path:           Path to file which will contain the data recorded.
            @kwarg ignore_platform:     Should platform checking be omitted?
            @kwarg on_error[int, str]:  Error callback, called with the error information.
            @kwarg on_enable[]:         Method called when sensor is enabled (accessible).
            @kwarg on_disable[]:        Method called if sensor is deactivated.
        """
        self.data_path  = data_path # Path under which data will be written.
        self.on_error   = kwargs.get('on_error', lambda code, info: None)
        self.on_enable  = kwargs.get('on_enable', lambda: None)
        self.on_disable = kwargs.get('on_disable', lambda: None)
        # Pass required permissions to the superclass constructor.
        super().__init__(
            ignore_platform=kwargs.get('ignore_platform', False),
            # buildozer.spec: RECORD_AUDIO, WAKE_LOCK.
            req_perms=[
                'RECORD_AUDIO',
                'WAKE_LOCK',
                'READ_EXTERNAL_STORAGE',
                'WRITE_EXTERNAL_STORAGE'
            ]
        )

    @property
    def state(self):
        """
            Returns the state of audio sensor (recording, ready, playing or unknown).
        """
        if audio.state == 'recording':
            return Audio.STATE_RECORDING
        elif audio.state == 'ready':
            return Audio.STATE_READY
        elif audio.state == 'playing':
            return Audio.STATE_PLAYING
        else:
            return Audio.STATE_UNKNOWN

    def record(self):
        """
            Starts recording audio using microhpone sensor.
        """
        if self.active:
            if self.state == Audio.STATE_PLAYING:
                self.finish()  # Stop the current playback if it exists.
            if self.state == Audio.STATE_READY:
                audio.file_path = self.data_path
                audio.start()

    def finish(self) -> None:
        """
            Finishes recording and stops the data stream. Data is playable until new recording starts.
        """
        if self.active and self.state != Audio.STATE_READY:
            audio.stop()

    def play(self) -> None:
        """
            Plays audio using file specified in constructor, or lastly recorded (cached) data.
        """
        if self.active:
            self.finish()  # Stop the current playback if it exists.
            if self.state == Audio.STATE_READY:
                audio.play()

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return all(grants)

    def _on_enable(self):
        self.on_enable()

    def _on_disable(self):
        self.finish()
        self.on_disable()

