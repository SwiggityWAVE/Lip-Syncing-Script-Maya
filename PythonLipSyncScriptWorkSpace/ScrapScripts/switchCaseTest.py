#https://developer.oculus.com/documentation/unity/audio-ovrlipsync-viseme-reference/
#15 cases


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
undefinedChars = []

for c in alphabet:
    case = c
    if (case == 'ɓ') or (case == 'ɱ') or (case == 'ɯ') or (case == 'ɰ') or (case == 'ʘ') or (case == 'p') or (case == 'b') or (case == 'm'):
        #Viseme:    PP                       Phonemes:      p, b, m                         Word example:           put, bat, mat
        print("1")

    elif (case == 'β') or (case == 'φ') or (case == 'ɸ') or (case == 'ʋ') or (case == 'ʍ') or (case == 'ŵ') or (case == 'ɯ') or (case == 'ɰ') or (case == 'ŵ') or (case == 'ẃ') or (case == 'f') or (case == 'v'):
        #Viseme:    FF                       Phonemes:      f, v                            Word example:           fat, vat
        print("2")

    elif (case == 'ð') or (case == 'θ') or (case == 'þ') or (case == 'w') or (case == 'ʷ'):
        #Viseme:    TH                       Phonemes:      th                              Word example:           think, that
        print("3")

    elif (case == 'ɖ') or (case == 'ḍ') or (case == 'ɗ') or (case == 'ʄ') or (case == 'ʈ') or (case == 'ṭ') or (case == 'd') or (case == 't') or (case == '') or (case == ''):
        #Viseme:    DD                       Phonemes:      t, d                            Word example:           tip, doll
        print("4")

    elif (case == 'ɟ') or (case == 'γ') or (case == 'ɣ') or (case == 'ɠ') or (case == 'ǰ') or (case == 'ʝ') or (case == 'ʲ') or (case == 'ʲ') or (case == 'ɟ') or (case == 'ɥ') or (case == 'ŷ') or (case == 'y') or (case == 'ɰ') or (case == 'ỹ') or (case == 'ȳ') or (case == 'k') or (case == 'g') or (case == 'j') or (case == 'q')or (case == 'x'):
        #Viseme:    kk                       Phonemes:      k, g                            Word example:           call, gas
        print("5")

    elif (case == 'ç') or (case == 'č') or (case == 'ʃ') or (case == 'ʂ') or (case == 'χ') or (case == 'c'):
        #Viseme:    CH                       Phonemes:      tS, dZ, S                       Word example:           chair, join, she
        print("6")

    elif (case == 'ɕ') or (case == 'š') or (case == 'ś') or (case == 'ṣ') or (case == 'ẓ') or (case == 'ʒ') or (case == 'ž') or (case == 'ʑ') or (case == 'ʐ') or (case == 's') or (case == 'z'):
        #Viseme:    SS                       Phonemes:      s, z                            Word example:           sir, zeal
        print("7")

    elif (case == 'ɫ') or (case == 'l') or (case == 'λ') or (case == 'ɭ') or (case == 'ʎ') or (case == 'ɭ') or (case == 'ḷ') or (case == 'ɬ') or (case == 'ɮ') or (case == 'ñ') or (case == 'ŋ') or (case == 'ɲ') or (case == 'ɳ') or (case == 'ṇ') or (case == 'n') or (case == 'l'):
        #Viseme:    nn                       Phonemes:      n, l                            Word example:           lot, not
        print("8")

    elif (case == 'ɹ') or (case == 'r') or (case == 'ʁ') or (case == 'ř') or (case == 'ɾ') or (case == 'ɽ') or (case == 'ṛ') or (case == 'ɻ'):
        #Viseme:    RR                       Phonemes:      r                               Word example:           red
        print("9")

    elif (case == 'æ') or (case == 'ɑ') or (case == 'ɐ') or (case == 'ɒ') or (case == 'α') or (case == 'ã') or (case == 'ă') or (case == 'ʌ') or (case == 'a'):
        #Viseme:    aa                       Phonemes:      A:                              Word example:           car
        print("10")

    elif (case == 'ə') or (case == 'ε') or (case == 'ɛ') or (case == 'ẹ') or (case == 'ɜ') or (case == 'ɚ') or (case == 'ɘ') or (case == 'ẽ') or (case == 'ĕ') or (case == 'e'):
        #Viseme:    E                       Phonemes:      e                                Word example:           bed
        print("11")

    elif (case == 'ɪ') or (case == 'i') or (case == 'ɨ') or (case == 'ĩ') or (case == 'ĭ') or (case == '') or (case == '') or (case == '') or (case == '') or (case == 'i'):
        #Viseme:    I                       Phonemes:      ih                               Word example:           tip
        print("12")

    elif (case == 'ħ') or (case == 'ɦ') or (case == 'h') or (case == 'ʰ') or (case == 'ɥ') or (case == 'ḥ') or (case == 'ɧ') or (case == 'ø') or (case == 'œ') or (case == 'œ') or (case == 'œ') or (case == 'ö') or (case == 'ɔ') or (case == 'ọ') or (case == 'ɵ') or (case == 'õ') or (case == 'ŏ') or (case == 'o'):
        #Viseme:    O                       Phonemes:      oh                               Word example:           toe
        print("13")

    elif (case == 'ʊ') or (case == 'ü') or (case == 'u') or (case == 'ʉ') or (case == 'ɞ') or (case == 'ũ') or (case == 'ŭ') or (case == 'u'):
        #Viseme:    U                       Phonemes:      ou                               Word example:           book
        print("14")

    else:
        print("Shit is undefined")
        undefinedChars.append(case)

print("undefined Chars: ")

for c in undefinedChars:
    print(c)


















"""
import random

def do_thing():
    print("does thing")

def do_other_thing():
    print("does other thing")

idk = {
    "case1": {
        "values": [1, 2, 3],
        "execute": do_thing
    },
    "case2": {
        "values": [4, 5, 6],
        "execute": do_other_thing
    },
    "case3": {
        "values": [7, 8, 9],
        "execute": do_thing
    }
}


num = random.randint(1, len(idk))
idk["case" + str(num)]["execute"]()
"""