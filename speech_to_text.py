import speech_recognition as sr

def sprache_zu_text():
    erkenner = sr.Recognizer()
    
    with sr.Microphone() as quelle:
        print("Ich höre zu... Bitte sprechen Sie jetzt.")
        audio = erkenner.listen(quelle)
    
    try:
        text = erkenner.recognize_google(audio, language="de-DE")
        print("Sie haben gesagt:", text)
        return text
    except sr.UnknownValueError:
        print("Entschuldigung, ich konnte das nicht verstehen.")
    except sr.RequestError:
        print("Entschuldigung, es gab einen Fehler mit dem Spracherkennungsdienst.")

# Funktion aufrufen, um die Spracherkennung zu starten
sprache_zu_text()
