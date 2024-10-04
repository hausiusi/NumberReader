#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import pygame

audio_path_root = "data"
audio_language = "ka"


def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def play_sequence(sequence):
    for audio_path in sequence:
        play_audio(audio_path)


def create_sequence_to_99(num: int, audio_seq: list):
    if num <= 20:
        audio_seq.append(os.path.join(audio_path_root, audio_language, f"{str(num)}.mp3"))
        return

    tens = num // 10
    num %= 10

    if num == 0 and tens % 2 == 0:
        audio_seq.append(os.path.join(audio_path_root, audio_language, f"{str(tens)}0.mp3"))
    else:
        audio_seq.append(os.path.join(audio_path_root, audio_language, f"{str(tens - tens % 2)}_.mp3"))
        num += tens % 2 * 10
        audio_seq.append(os.path.join(audio_path_root, audio_language, f"{str(num)}.mp3"))


def create_sequence_for_hundreds(num: int, audio_seq: list):
    if len(str(num)) < 3:
        create_sequence_to_99(num, audio_seq)
        return

    if int(str(num)[1:]) == 0:
        audio_seq.append(os.path.join(audio_path_root, audio_language, f"{str(num)}.mp3"))
        return

    hundreds = num // 100
    num %= 100

    if hundreds > 0:
        audio_seq.append(os.path.join(audio_path_root, audio_language, f"{str(hundreds)}__.mp3"))

    create_sequence_to_99(num, audio_seq)


def create_sequence_ka(num: int, zeroes_in_min: int, audio_seq: list):
    min_number = 10 ** zeroes_in_min
    max_num_len = zeroes_in_min + 3
    min_number_len = zeroes_in_min + 1
    if len(str(num)) < zeroes_in_min + 1 and zeroes_in_min >= 3:
        create_sequence_ka(num, zeroes_in_min - 3, audio_seq)
    elif num == min_number:
        audio_seq.append(os.path.join(audio_path_root, audio_language, f"{min_number}.mp3"))
    elif max_num_len >= len(str(num)) >= min_number_len:
        # ensure exceptional saying numbers for 1*** in Georgian
        if zeroes_in_min >= 3 and (int(str(num)[0]) != 1 or len(str(num)) > 4):
            create_sequence_for_hundreds(int(str(num)[:-zeroes_in_min]), audio_seq)
        elif zeroes_in_min == 3 and int(str(num)[0]) == 1:
            pass
        elif zeroes_in_min < 3:
            create_sequence_for_hundreds(num, audio_seq)
        if int(str(num)[-zeroes_in_min:]) == 0 and num != 0:
            audio_seq.append(os.path.join(audio_path_root, audio_language, f"{min_number}.mp3"))
        elif zeroes_in_min >= 3:
            audio_seq.append(os.path.join(audio_path_root, audio_language, f"1{'_' * zeroes_in_min}.mp3"))
            create_sequence_ka(int(str(num)[-zeroes_in_min:]), zeroes_in_min - 3, audio_seq)


def read(num: int):
    audio_seq = []
    create_sequence_ka(num, 18, audio_seq)
    play_sequence(audio_seq)


if __name__ == '__main__':
    while True:
        user_input = input("Input the number:")
        if user_input == "exit":
            exit()

        try:
            number = int(user_input)
        except:
            print("Please, provide the number")
            continue

        read(number)
