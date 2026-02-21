import pyttsx3
# Initialize the text-to-speech engine


engine = pyttsx3.init()
language_code = "de_DE"
gender = "VoiceGenderMale" # Beispiel: "VoiceGenderFemale" für weibliche Stimme

# Verfügbare Stimmen ausgeben
voices = engine.getProperty('voices')
for voice in voices:
    print(f"Stimme: {voice.name}")
    print(f"ID: {voice.id}")
    print(f"Sprachen: {voice.languages}")
    print(f"Geschlecht: {voice.gender}")
    print(f"Alter: {voice.age}")
    print("-" * 20)

# Deutsche Stimme auswählen (falls verfügbar)
for voice in voices:
    if language_code.lower() in voice.languages[0].lower(): # Suche nach "german" oder "deutsch"
        engine.setProperty('voice', voice.id)
        break  # Beende die Schleife, sobald eine deutsche Stimme gefunden wurde

# Text sprechen
engine.say("Hallo, dies ist ein Test auf Deutsch.")
engine.runAndWait()
