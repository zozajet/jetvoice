import pyttsx3
import os

def speak(text):
    try:
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        
        # Check for user-specified voice first
        user_voice = os.getenv("TTS_VOICE_ID")
        selected_voice = None
        
        if user_voice:
            # Try to find exact user-specified voice
            for voice in voices:
                if user_voice == voice.id:
                    selected_voice = voice.id
                    break
        
        # If no user voice or not found, use default preferences
        if not selected_voice:
            voice_preference = [
                'english-us',      # American English
                'english_rp',      # British English (RP)
                'english',         # Standard English
                'default'          # Fallback
            ]
            
            # Try to find and set preferred voice
            for preferred in voice_preference:
                for voice in voices:
                    if preferred in voice.id.lower():
                        selected_voice = voice.id
                        break
                if selected_voice:
                    break
        
        if selected_voice:
            engine.setProperty('voice', selected_voice)
            print(f"[TTS] Using voice: {selected_voice}")
        
        # Set speech rate (words per minute) - default is usually 200
        # Lower = slower and clearer, Higher = faster
        rate = int(os.getenv("TTS_RATE", "150"))  # Slower for clarity
        engine.setProperty('rate', rate)
        
        # Set volume (0.0 to 1.0)
        volume = float(os.getenv("TTS_VOLUME", "0.9"))
        engine.setProperty('volume', volume)
        
        print(f"[TTS] Speaking: '{text}' (rate: {rate}, volume: {volume})")
        
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"[TTS Error]: {e}")
        # Fallback to simple espeak command
        try:
            import subprocess
            subprocess.run(['espeak', '-s', '150', '-v', 'en-us', text], 
                         capture_output=True, check=True)
            print("[TTS] Using espeak fallback")
        except Exception as fallback_error:
            print(f"[TTS Fallback Error]: {fallback_error}")
