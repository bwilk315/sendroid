
from threading  import Thread
from .sensor    import Sensor
from plyer      import audio
from plyer      import tts
from plyer      import stt
from time       import time, sleep
from jnius      import autoclass, cast  # Briliant.


class Audio(Sensor):
    # Errors.
    LANG_ERROR          = 100   # Language is not installed on the device.
    # Audio states.
    STATE_UNKNOWN       = 200
    STATE_RECORDING     = 201
    STATE_READY         = 202
    STATE_PLAYING       = 203
    STATE_SPEAKING      = 204
    STATE_RECOGNIZING   = 205
    # Languages.
    LANG_EN             = 'en-US'
    LANG_PL             = 'pl-PL'
    # Class-specific.
    RECOG_INTERVAL      = .1    # Interval in seconds [s] between next frame-skippings.
    SPK_INTERVAL        = .1    # Interval for speaking.
    RECOG_ERR_LEN       = .333  # Length in seconds [s] which is the minimum time of proper recognition operation.

    # TODO: Create module which will manage jnius, better than plyer did.
    # Everything done below is required to change brightness level since this level is a system settings and is restricted.
    # Get python activity class from kivy application.
    PythonActivity  = autoclass('org.kivy.android.PythonActivity')
    # Import 'Intent', 'Settings' and 'System' class to the Python Universe.
    Intent          = autoclass('android.content.Intent')
    Settings        = autoclass('android.provider.Settings')
    System          = autoclass('android.provider.Settings$System')
    TextToSpeech    = autoclass('android.speech.tts.TextToSpeech')
    # Create special intent class instance for opening an activity for granting permissions to write system settings.
    intent          = Intent()
    intent.setAction(Settings.ACTION_MANAGE_WRITE_SETTINGS)
    # Cast the python activity to the common 'Activity' class in order to get its context later.
    currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    # Cast got application context to the common 'Context' class to use it as actual context object.
    context         = cast('android.content.Context', currentActivity.getApplicationContext())
    tts = None  # TextToSpeech class instance.

    def __init__(self, data_path: str = None, **kwargs):
        """
            Initializes the 'Audio' class instance.
            @param data_path:   Path to file which will contain the data recorded.
        """
        self.data_path          = data_path # Path under which data will be written.
        # Callbacks used to catch speech recognition events.
        self.on_recognize_start = kwargs.get('on_recognize_start',  lambda:             None)
        self.on_recognize       = kwargs.get('on_recognize',        lambda sentence:    None)
        self.on_recognize_end   = kwargs.get('on_recognize_end',    lambda matches:     None)
        self.on_speak_start     = kwargs.get('on_speak_start',      lambda:             None)
        self.on_speak_end       = kwargs.get('on_speak_end',        lambda:             None)
        self.__recog_start      = .0  # Time in seconds [s] in which speech recognition started.
        self.__is_speaking      = False
        self.__is_recognizing   = False
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
            Returns the state of audio sensor (recording, ready, playing, speaking, recognizing or unknown).
        """
        if self.__is_speaking:
            return Audio.STATE_SPEAKING
        elif self.__is_recognizing:
            return Audio.STATE_RECOGNIZING
        elif audio.state == 'recording':
            return Audio.STATE_RECORDING
        elif audio.state == 'ready':
            return Audio.STATE_READY
        elif audio.state == 'playing':
            return Audio.STATE_PLAYING
        else:
            return Audio.STATE_UNKNOWN

    @property
    def speech_support(self) -> bool:
        """
            Returns whether current device supports the speech recognition.
        """
        return stt.exist()

    @property
    def listening(self) -> bool:
        """
            Returns if speech is being recognized now.
        """
        return stt.listening

    def speak(self, msg: str):
        """
            Speaks the message given.
            @param msg: Text to speak.
        """
        tts.speak(msg)
        Thread(target = self.__speaking_cycle).start()

    def recognize(self, lang: str = LANG_EN):
        """
            Starts the recognization of voice if it is supported.
            @param lang:    Language to recognize.
        """
        if self.speech_support:
            stt.language = lang
            stt.start()
            # Start recognization cycle which will manage stt callbacks invocation.
            Thread(target = self.__recognization_cycle).start()

    def finish(self):
        """
            Finishes speech recognition if it is active, or finishes recording and stops the data stream,
            data is playable until new recording starts.
        """
        if self.listening:
            stt.stop()
            self.on_recognize_end(stt.result)
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

    def __speaking_cycle(self):
        # TODO: Recreate it so it will use the jnius-based module.
        """
            Cycle of speaking, it detects start and end of the device TTS speaking.
        """
        while not Audio.tts.isSpeaking():
            sleep(Audio.SPK_INTERVAL)
        self.on_speak_start()
        self.__is_speaking = True

        while Audio.tts.isSpeaking():
            sleep(Audio.SPK_INTERVAL)

        self.__is_speaking = False
        self.on_speak_end()

    def __recognization_cycle(self):
        """
            Cycle of recognization, it works in another thread due to blocking loops used to forcely
            wait for specified moment where callbacks can be invoked.
        """
        # Wait for the recognization start using loop.
        while not self.listening:
            sleep(Audio.RECOG_INTERVAL)

        self.on_recognize_start()  # Call start.
        self.__is_recognizing   = True
        self.__recog_start      = time()  # Set recognition start time.

        # Wait for the recognization end with empty loop.
        while self.listening:
            sleep(Audio.RECOG_INTERVAL)
            # Make sentence using partial results.
            pr = stt.partial_results
            self.on_recognize(pr[-1] if len(pr) else '')
        
        results = stt.results  # Actual matching sentences.
        # Call the recognition loop callback with the final sentence (first element is the most accurate).
        if len(results):
            self.on_recognize(results[0])
        # If process length was very small it means recognition failed.
        if time() - self.__recog_start < Audio.RECOG_ERR_LEN:
            self.on_error(Audio.LANG_ERROR, "Device's voice recognition system does not support language chosen.")
        else:
            self.__is_recognizing = False
            self.on_recognize_end(results)  # Call end.

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        grants = all(grants)
        if grants:
            # Instantiate TTS class instance.
            Audio.tts = Audio.TextToSpeech(Audio.context, lambda status: None)
        return grants

    def _on_enable(self):
        self.speak('')  # It initializes the TTS module now to avoid collision with STT later.
        self.on_enable()

    def _on_disable(self):
        self.finish()
        self.on_disable()

