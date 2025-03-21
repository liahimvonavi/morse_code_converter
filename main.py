import time
import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

pygame.mixer.init(frequency=44100, size=-16, channels=2)

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': ' ', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    '!': '-.-.--', "'": '.----.', '"': '.-..-.', ';': '-.-.-.',
    ':': '---...', '(': '-.--.', ')': '-.--.-', '/': '-..-.',
    '-': '-....-', '+': '.-.-.'
}

def generate_tone(frequency, duration_ms, volume=0.5):
    sample_rate = 44100
    duration = duration_ms / 1000
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(frequency * 2 * np.pi * t)
    audio = (wave * volume * 32767).astype(np.int16)
    stereo_audio = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(stereo_audio)

# Smoother sound durations
DOT_DURATION = 0.1  # seconds
DASH_DURATION = 0.3
SYMBOL_GAP = 0.05
LETTER_GAP = 0.2
WORD_GAP = 0.6

DOT_SOUND = generate_tone(800, int(DOT_DURATION * 1000))
DASH_SOUND = generate_tone(800, int(DASH_DURATION * 1000))

def play_sound(symbol):
    if symbol == ".":
        DOT_SOUND.play()
        time.sleep(DOT_DURATION + SYMBOL_GAP)
    elif symbol == "-":
        DASH_SOUND.play()
        time.sleep(DASH_DURATION + SYMBOL_GAP)
    elif symbol == " ":
        time.sleep(WORD_GAP)

def string_to_morse(text):
    morse_code = ""
    pretty_code = ""
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_char = MORSE_CODE_DICT[char]
            morse_code += morse_char + " "
            pretty_code += morse_char.replace('.', '•').replace('-', '–') + " "
            for symbol in morse_char:
                play_sound(symbol)
            time.sleep(LETTER_GAP)
        else:
            morse_code += "? "
            pretty_code += "? "
    print()
    print("Morse code:")
    print(pretty_code.strip())
    return morse_code.strip()


while True:
    print("*" * 100)
    user_input = input("Enter text to convert to Morse Code or type quit! to close.\nEnter text here: ")
    if user_input.strip().lower() == "quit!":
        break
    result = string_to_morse(user_input)
    print()


