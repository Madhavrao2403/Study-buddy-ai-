import speech_recognition as sr
from fastapi import HTTPException
from services.cohere_service import get_cohere_response
from services.translate_service import greeting, translate_to_machine
from services.tts_service import speak_response_lang
from deep_translator import GoogleTranslator

def handle_speak(lang, language2):
    greeting(lang)
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 250
    recognizer.pause_threshold = 0.8
    
    try:
        with sr.Microphone() as source:
            print("Listening to your response...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        
        try:
            response = recognizer.recognize_google(audio, language=lang)
            print(f"User said: {response}")
            translated = translate_to_machine(response)
            result = get_cohere_response(translated)
            translated_result = GoogleTranslator(source='en', target=language2).translate(result)
            speak_response_lang(translated_result,language2)
            return {"message": "Response received", "response_speech": result}
        
        except sr.UnknownValueError:
            return {"message": "Sorry, I couldn't understand the speech."}
        except sr.RequestError:
            return {"message": "Speech recognition service is unavailable."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Microphone or recognition failed: {str(e)}")
