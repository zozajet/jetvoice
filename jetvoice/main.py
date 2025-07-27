# jetvoice/main.py

import sys
import time

from loguru import logger
from jetvoice.stt import stt
# from jetvoice.llm import llm
# from jetvoice.tts import tts

def main():
    """
    The main function that runs the JetVoice application loop.
    """
    # Configure Loguru
    # This removes the default handler and adds a new one that formats
    # the output, making it colorful and including the timestamp.
    logger.remove()
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    logger.info("Starting JetVoice application... ")
    
    try:
        while True:
            # logger.info("Listening for your command...")
            
            # The application will block here, waiting for speech.
            recognized_text = stt.recognize_from_microphone()
            
            if recognized_text:
                logger.success(f"Recognized text: \"{recognized_text}\"")
                
                # --- Add your core application logic here ---
                # For example, pass the text to the LLM and get a response.
                # logger.info("Sending text to LLM...")
                # llm_response = llm.query(recognized_text)
                
                # Then, have the TTS engine speak the response.
                # logger.success(f"LLM Response: \"{llm_response}\"")
                # tts.speak(llm_response)
                # ----------------------------------------------
                
            else:
                logger.warning("Could not recognize speech, listening again...")
            
            # A small delay can be useful to prevent tight loops on errors.
            time.sleep(0.1)

    except KeyboardInterrupt:
        # This block allows you to stop the loop with Ctrl+C.
        logger.info("Gracefully shutting down JetVoice.")
        
    except Exception as e:
        # Catching other potential errors with a detailed error log.
        logger.error(f"An unexpected error occurred: {e}")
        logger.exception("Traceback:")

if __name__ == "__main__":
    # The CMD in your Dockerfile executes the module, which runs this block.
    main()