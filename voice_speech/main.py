# pip install pipwin
# pip install speechrecognition 
# pip install --upgrade speechrecognition

import webbrowser
import speech_recognition as sr
r = sr.Recognizer() 
while True:
    with sr.Microphone() as source:
        print('Hola, soy tu asistente por voz: ')
        audio = r.listen(source)
 
        try:
            text = r.recognize_google(audio)
            print('Has dicho: {}'.format(text))
            print(text)
            if "Amazon" in text:
                webbrowser.open('http://amazon.es')
            if "noticias" in text:
                webbrowser.open('http://noticiasfinancieras.info')
            if "que tal" in text:
                print("Bien y tu?")
        except:
            print('No te he entendido')