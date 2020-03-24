from pygame import mixer


class music:
    def __init__(self):
        mixer.music.load("../sounds/funky.wav")
        mixer.music.play(-1)

    def sound_handler(file, repeat):
        a_sound = mixer.Sound(file)
        a_sound.play(repeat)