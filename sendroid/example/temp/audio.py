
from    plyer       import audio
from    plyer       import tts
from    plyer       import stt
from    threading   import Thread
from    time        import time, sleep
from    .sensor     import Sensor


class Audio(Sensor):
    CALLBACKS_PREC  = .01   # Speech recognition callbacks precision in seconds [s].
    RECOG_ERR_LEN   = .5    # Length in seconds [s] which is the minimum time of proper recognition operation.
    # Errors.
    LANG_ERROR      = 100   # Language is not installed on the device.
    # Audio states.
    STATE_UNKNOWN   = 0
    STATE_RECORDING = 1
    STATE_READY     = 2
    STATE_PLAYING   = 3
    # Languages.
    LANG_EN         = 'en-US'
    LANG_PL         = 'pl-PL'

    listening       = False  # Boolean indicating if the speech is being recognized now.

    def __init__(self, data_path: str = None, **kwargs):
        """
            Initializes the 'Audio' class instance.
            @param data_path:   Path to file which will contain the data recorded.
        """
        self.data_path          = data_path # Path under which data will be written.
        # Callbacks used to catch speech recognition events.
        self.on_recognize_start = kwargs.get('on_recognize_start',  lambda: None)
        self.on_recognize_end   = kwargs.get('on_recognize_end',    lambda: None)
        self.__recog_start      = .0  # Time in seconds [s] in which speech recognition started.
        # Pass required permissions to the superclass constructor.
        super().__init__(
            # buildozer.spec: RECORD_AUDIO, WAKE_LOCK, [INTERNET].
            req_perms   = [
                'RECORD_AUDIO',
                'WAKE_LOCK',
                'READ_EXTERNAL_STORAGE',
                'WRITE_EXTERNAL_STORAGE'
            ],
            **kwargs
        )

    @property
    def state(self) -> int:
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

    @property
    def speech_support(self):
        """
            Returns whether current device supports the speech recognition.
        """
        return stt.exist()

    @property
    def listening(self):
        """
            Returns if speech is being recognized now.
        """
        return stt.listening

    @property
    def results(self) -> list:
        """
            Returns the results of voice recognition as list of sentences which may be a properly
            recognized versions. You should then take user accent in account to match the sentence.
        """
        return stt.results

    def speak(self, msg: str):
        """
            Speaks the message given.
            @param msg: Text to speak.
        """
        tts.speak(msg)

    def recognize(self, lang: str = LANG_EN):
        """
            Starts the recognization of voice if it is supported.
            @param lang:    Language to recognize.
        """
        if self.speech_support:
            stt.language = lang
            stt.start()
            # Start recognization cycle which will manage stt callbacks invocation.
            Thread(target = self._recognization_cycle).start()

    def finish(self):
        """
            Finishes speech recognition if it is active, or finishes recording and stops the data stream,
            data is playable until new recording starts.
        """
        if self.listening:
            stt.stop()
            self.on_recognize_end()
        elif self.active and self.state != Audio.STATE_READY:
            audio.stop()

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

    def play(self) -> None:
        """
            Plays audio using file specified in constructor, or lastly recorded (cached) data.
        """
        if self.active:
            self.finish()  # Stop the current playback if it exists.
            if self.state == Audio.STATE_READY:
                audio.play()

    def _recognization_cycle(self):
        """
            Cycle of recognization, it works in another thread due to blocking loops used to forcely
            wait for specified moment where callbacks can be invoked.
        """
        # Wait for the recognization start using loop.
        while not self.listening:
            sleep(Audio.CALLBACKS_PREC)
        self.on_recognize_start()  # Call start.
        self.__recog_start = time()  # Set recognition start time.
        # Wait for the recognization end with empty loop.
        while self.listening:
            sleep(Audio.CALLBACKS_PREC)
        # If process length was very small it means recognition failed.
        if time() - self.__recog_start < Audio.RECOG_ERR_LEN:
            self.on_error(Audio.LANG_ERROR, "Device's voice recognition system does not support language chosen.")
        else:
            self.on_recognize_end()  # Call end.

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return all(grants)

    def _on_enable(self):
        self.speak('')  # It initializes the TTS module now to avoid collision with STT later.
        self.on_enable()

    def _on_disable(self):
        self.finish()
        self.on_disable()

