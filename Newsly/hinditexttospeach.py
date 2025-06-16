from gtts import gTTS
import pygame
import tempfile
import os
import time
import threading
import re
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup

pygame.mixer.init()

stop_flag = False  # Global flag to stop playback

def change_speed(sound, speed=1.0):
    if speed == 1.0:
        return sound
    return speedup(sound, playback_speed=speed)

def play_sentence(sentence, speed=1.0):
    global stop_flag
    try:
        tts = gTTS(text=sentence, lang='hi')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        # Load and modify speed
        audio = AudioSegment.from_file(temp_path, format="mp3")
        modified_audio = change_speed(audio, speed=speed)

        # Save new temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as out_fp:
            out_path = out_fp.name
            modified_audio.export(out_path, format="wav")

        # Play using pygame
        pygame.mixer.music.load(out_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if stop_flag:
                pygame.mixer.music.stop()
                break
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(temp_path)
        os.remove(out_path)

    except Exception as e:
        print(f"Error playing sentence: {e}")

def speak_summary_streaming(text, speed=1.0):
    global stop_flag
    stop_flag = False

    sentences = re.split(r'[।.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    def run():
        for sentence in sentences:
            if stop_flag:
                break
            print(f"Speaking: {sentence}")
            play_sentence(sentence, speed=speed)

    threading.Thread(target=run).start()

def stop_playback():
    global stop_flag
    stop_flag = True
    pygame.mixer.music.stop()
    print("Playback stopped.")

# --- Example usage ---
# summary = """Royal Challengers Bengaluru (RCB) IPL 2025 jeet gayi! Unhone Punjab Kings (PBKS) ko final mein haraya. RCB ka pehla IPL title tha yeh.
#    Final match Ahmedabad mein hua tha.
#    Kuch important players aur moments:
#        Virat Kohli bahut khush hua finally RCB ke saath title jeet kar.
#        Krunal Pandya ne final mein bahut achi bowling ki.
#        Shreyas Iyer ne PBKS ke performance aur future ke baare mein baat ki.
#    Ek IPL Owners Meeting bhi hui thi jismein players ke rules aur business ke baare mein discuss hua.
#    Playoff games ke reports available hain, jaise final, Qualifier 1, Qualifier 2, aur Eliminator."""
# speak_summary_streaming(summary, speed=1.3)  # Try 0.8 for slow, 1.5 for fast

# Stop after 6 seconds for demo
# time.sleep(6)
# stop_playback()
