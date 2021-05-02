from tkinter import *
from tkinter import ttk


def foo(i, rotor_a):
    num = ord(i) - 97 + rotor_a
    if num > 25:
        num -= 26
    return num


def reflector(rotor, rotor_a, char):
    num = rotor.index(char) + rotor_a
    if num > 25:
        num -= 26
    return chr(num + 97)


def ref_pairs(pairs, char):
    for pair in pairs:
        if char == pair[0]:
            return pair[1]
        if char == pair[1]:
            return pair[0]


def encrypt(key, text):
    new_text = []
    for pair in key[2]:
        text = text.replace(pair[0], '*')
        text = text.replace(pair[1], pair[0])
        text = text.replace('*', pair[1])

    key[0] = key[0].lower()
    rotor1 = ['k', 'y', 'p', 'j', 't', 'x', 'r', 'b', 'w', 'o', 'g', 'i', 'l', 'h', 'n', 'q', 'f', 'd', 'v', 'e', 'c',
              'z', 'u', 'a', 'm', 's']
    rotor2 = ['m', 'v', 'k', 'e', 'o', 'x', 'd', 't', 'c', 'y', 'j', 'a', 'g', 'z', 'f', 'l', 'q', 'n', 'i', 'r', 'w',
              'h', 'p', 'u', 'b', 's']
    rotor3 = ['n', 'b', 'g', 's', 'z', 'f', 'c', 'j', 'y', 'r', 'l', 'q', 'u', 'd', 'p', 'o', 't', 'k', 'e', 'v', 'w',
              'a', 'm', 'i', 'x', 'h']
    reflector_pairs = [('r', 'k'), ('y', 'd'), ('c', 'u'), ('z', 'i'), ('e', 'n'), ('s', 'h'), ('g', 'a'), ('m', 'l'),
                    ('o', 'p'), ('f', 'b'), ('t', 'j'), ('v', 'x'), ('w', 'q')]
    rotors = [rotor1, rotor2, rotor3]
    rotors = [rotors[key[1][0] - 1], rotors[key[1][1] - 1], rotors[key[1][2] - 1]]
    rotor1_a, rotor2_a, rotor3_a = ord(key[0][0]) - 97, ord(key[0][1]) - 97, ord(key[0][2]) - 97
    for inx, val in enumerate(text):
        first = rotors[0][foo(val, rotor1_a)]
        second = rotors[1][foo(first, rotor2_a)]
        third = rotors[2][foo(second, rotor3_a)]
        # after reflector:
        rv_third = reflector(rotors[2], rotor3_a, ref_pairs(reflector_pairs, third))
        rv_second = reflector(rotors[1], rotor2_a, ref_pairs(reflector_pairs, rv_third))
        rv_first = reflector(rotors[0], rotor1_a, ref_pairs(reflector_pairs, rv_second))
        new_text.append(rv_first)
        rotor3_a += 1
        if rotor3_a == 26:
            rotor3_a = 0
            rotor2_a += 1
        if rotor2_a == 26:
            rotor2_a = 0
            rotor1_a += 1
        if rotor1_a == 26:
            rotor1_a = 0

    return ''.join(new_text)


def before_encrypt(textbox, encrypted_text, rotor1, rotor2, rotor3, first_letter, second_letter, third_letter):
    first_position = first_letter.get() + second_letter.get() + third_letter.get()
    rotors_order = [int(rotor1.get()), int(rotor2.get()), int(rotor3.get())]
    cables = [('a', 'g'), ('f', 'l'), ('w', 'q'), ('v', 'c'), ('z', 'x'), ('k', 'p')]

    settings = [first_position, rotors_order, cables]
    text = textbox.get('1.0', END)
    new_text = ''
    text = text.lower()
    for i in text:
        if (ord(i) >= ord('a')) and (ord(i) <= ord('z')):
            new_text += i
    if new_text.isspace() is False:
        encrypted_text.config(state='normal')
        encrypted_text.delete(1.0, 'end')
        encrypted_text.insert(1.0, encrypt(settings, new_text))
        encrypted_text.config(state='disabled')


def grid_all(button, rotor1, rotor2, rotor3, text1, text2, frame2,
             first_letter, second_letter, third_letter, frame3, frame1):
    text1.grid(row=2, pady=5)
    rotor1.grid(row=0, column=0, padx=5, pady=5)
    rotor2.grid(row=0, column=1, padx=5, pady=5)
    rotor3.grid(row=0, column=2, padx=5, pady=5)
    first_letter.grid(row=0, column=0, padx=5, pady=5)
    second_letter.grid(row=0, column=1, padx=5, pady=5)
    third_letter.grid(row=0, column=2, padx=5, pady=5)
    frame2.grid(row=4, pady=5)
    frame3.grid(row=6, pady=5)
    button.config(command=lambda: before_encrypt(text1, text2, rotor1, rotor2, rotor3, first_letter, second_letter,
                                                 third_letter))
    button.grid(row=7, pady=5)
    text2.grid(row=9, pady=5)
    frame1.grid()


def main():
    font1 = ('Arial', 18)
    font2 = ('Arial', 30)
    font3 = ('Arial', 14)
    root = Tk()
    root.wm_title('Enigma')
    frame1 = Frame(root)
    Label(frame1, text='Enigma', font=font2).grid(row=0, pady=5)
    Label(frame1, text='Text to encrypt (English letters only):', font=font1).grid(row=1, sticky='W')
    text1 = Text(frame1, height=10, width=40)
    Label(frame1, text='Rotors order:', font=font1).grid(row=3, sticky='W')
    frame2 = Frame(frame1)
    rotors_list = [1, 2, 3]
    rotor1 = ttk.Combobox(frame2, values=rotors_list, width=3, state='readonly')
    rotor1.set(1)
    rotor2 = ttk.Combobox(frame2, values=rotors_list, width=3, state='readonly')
    rotor2.set(1)
    rotor3 = ttk.Combobox(frame2, values=rotors_list, width=3, state='readonly')
    rotor3.set(1)
    Label(frame1, text='First rotors position:', font=font1).grid(row=5, sticky='W')
    frame3 = Frame(frame1)
    letters_list = [chr(i) for i in range(ord('a'), ord('z')+1)]
    first_letter = ttk.Combobox(frame3, values=letters_list, width=3, state='readonly')
    first_letter.set('a')
    second_letter = ttk.Combobox(frame3, values=letters_list, width=3, state='readonly')
    second_letter.set('a')
    third_letter = ttk.Combobox(frame3, values=letters_list, width=3, state='readonly')
    third_letter.set('a')
    button = Button(frame1, text='encrypt', font=font3)
    Label(frame1, text='Encrypted text:', font=font1).grid(row=8, sticky='W')
    text2 = Text(frame1, height=10, width=40, state='disabled')
    grid_all(button, rotor1, rotor2, rotor3, text1, text2, frame2,
             first_letter, second_letter, third_letter, frame3, frame1)
    root.mainloop()


if __name__ == "__main__":
    main()
