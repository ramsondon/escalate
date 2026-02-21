import pyttsx3


class Text2Voice:

    def __init__(self):
        # init on mac
        self.engine = pyttsx3.init(driverName="nsss")  # "sapi5" for Windows, "espeak" for Linux, "nsss" for Mac

        self.language_code = "de_DE"
        self.gender = "VoiceGenderMale"  # Beispiel: "VoiceGenderFemale" für weibliche Stimme

    def get_voices(self):
        return self.engine.getProperty('voices')

    def select_language_voice(self, voices: list, language_code: str):
        # Deutsche Stimme auswählen (falls verfügbar)
        for voice in voices:
            if language_code.lower() in voice.languages[0].lower():  # Suche nach "german" oder "deutsch"
                self.engine.setProperty('voice', voice.id)
                break  # Beende die Schleife, sobald eine deutsche Stimme gefunden wurde

    def print_voices(self, voices: list, language_code: str):
        for voice in voices:
            if language_code.lower() in voice.languages[0].lower():
                print(f"Stimme: {voice.name}")
                print(f"ID: {voice.id}")
                print(f"Sprachen: {voice.languages}")
                print(f"Geschlecht: {voice.gender}")
                print(f"Alter: {voice.age}")
                print("-" * 20)

    def select_voice(self, id: str):
        self.engine.setProperty('voice', id)

    def say(self, value: str):
        self.engine.say(value)
        self.engine.runAndWait()