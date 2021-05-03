from tkinter import *
from tkinter import ttk
import random
global canvas_lines, letters_buttons1, letters_buttons2
canvas_lines, letters_buttons1, letters_buttons2 = [], [], []


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


def get_cables_from_canvas(canvas):
    uppers = [i[0] for i in canvas_lines]
    lowers = [i[1] for i in canvas_lines]
    offset = 16
    if len(canvas_lines) < 6:
        for i in range(6 - len(canvas_lines)):
            while True:
                upper_button_index = random.randint(0, 25)
                if (upper_button_index not in uppers) and (upper_button_index not in lowers):
                    break
            while True:
                lower_button_index = random.randint(0, 25)
                if (lower_button_index not in lowers) and (lower_button_index not in uppers) \
                        and (lower_button_index != upper_button_index):
                    break
            uppers.append(upper_button_index)
            lowers.append(lower_button_index)
            line = canvas.create_line(upper_button_index * 700/26 + offset, 2, lower_button_index * 700/26 + offset, 78)
            canvas_lines.append([upper_button_index, lower_button_index, line])
    disable_buttons()
    return [(chr(97+i[0]),chr(97+i[1])) for i in canvas_lines]


def disable_buttons():
    uppers = [i[0] for i in canvas_lines]
    lowers = [i[1] for i in canvas_lines]
    for index in range(26):
        letters_buttons1[index].config(state='normal')
        letters_buttons2[index].config(state='normal')
    for index in range(26):
        if index in uppers:
            letters_buttons2[index].config(state='disable')
        if index in lowers:
            letters_buttons1[index].config(state='disable')


def before_encrypt(textbox, encrypted_text, rotors, letters, canvas):
    first_position = letters[0].get() + letters[1].get() + letters[2].get()
    rotors_order = [int(rotors[0].get()), int(rotors[1].get()), int(rotors[2].get())]
    cables = get_cables_from_canvas(canvas)
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


def grid_all(button1, button2, rotors, text1, text2, frame2, letters, frame3, root_frame, settings_frame, settings, canvas):
    text1.grid(row=2, pady=5)
    button1.grid(row=3, pady=5)
    button1.config(command=lambda: before_encrypt(text1, text2, rotors, letters, canvas))
    text2.grid(row=5, pady=5)
    button2.config(command=lambda: settings.deiconify())
    button2.grid(row=6, pady=5)
    root_frame.grid()
    ################
    for i in range(3):
        rotors[i].grid(row=0, column=i, padx=5, pady=5)
    for i in range(3):
        letters[i].grid(row=0, column=i, padx=5, pady=5)
    frame2.grid(row=1, pady=5)
    frame3.grid(row=3, pady=5)
    settings_frame.grid()


def button_press(row_button_index, row, canvas):
    second_row = int(not row)
    offset = 16
    letters_buttons = [letters_buttons1, letters_buttons2]
    row_button = letters_buttons[row][row_button_index]
    second_row_button_list = [(letters_buttons[second_row][i], i) for i in range(len(letters_buttons[second_row]))
                              if letters_buttons[second_row][i]['relief'] == 'sunken']
    if len(second_row_button_list) == 1 and second_row_button_list[0][1] == row_button_index:
        second_row_button_list[0][0].config(relief='raised')
        return None
    if row_button['relief'] == 'raised':
        for button in letters_buttons[row]:
            button.config(relief='raised')
        row_button.config(relief='sunken')

        if len(second_row_button_list) == 1:
            second_row_button = second_row_button_list[0][0]
            second_row_button_index = second_row_button_list[0][1]
            to_delete = []
            same_line = False
            if row == 0:
                for can_line in canvas_lines:
                    if second_row_button_index == can_line[1] and row_button_index == can_line[0]:
                        to_delete.append(can_line)
                        same_line = True
                    else:
                        if row_button_index == can_line[0]:
                            to_delete.append(can_line)
                        if second_row_button_index == can_line[1]:
                            to_delete.append(can_line)
                upper_button_index, lower_button_index = row_button_index, second_row_button_index
            else:
                for can_line in canvas_lines:
                    if row_button_index == can_line[1] and second_row_button_index == can_line[0]:
                        to_delete.append(can_line)
                        same_line = True
                    else:
                        if row_button_index == can_line[1]:
                            to_delete.append(can_line)
                        if second_row_button_index == can_line[0]:
                            to_delete.append(can_line)
                upper_button_index, lower_button_index = second_row_button_index, row_button_index
            for can_line_to_delete in to_delete:
                canvas_lines.remove(can_line_to_delete)
                canvas.delete(can_line_to_delete[2])
            if same_line is False:
                line = canvas.create_line(upper_button_index*700/26 + offset, 2, lower_button_index*700/26 + offset, 78)
                canvas_lines.append([upper_button_index, lower_button_index, line])
                if len(canvas_lines) > 6:
                    canvas.delete(line)
                    canvas_lines.pop()
            disable_buttons()
            row_button.config(relief='raised')
            second_row_button.config(relief='raised')
    elif row_button['relief'] == 'sunken':
        row_button.config(relief='raised')


def main():
    font1 = ('Arial', 18)
    font2 = ('Arial', 30)
    font3 = ('Arial', 14)
    root = Tk()
    root.wm_title('Enigma')
    root_frame = Frame(root)
    Label(root_frame, text='Enigma', font=font2).grid(row=0, pady=5)
    Label(root_frame, text='Text to encrypt (English letters only):', font=font1).grid(row=1, sticky='W')
    text1 = Text(root_frame, height=10, width=40)
    button1 = Button(root_frame, text='encrypt', font=font3)
    Label(root_frame, text='Encrypted text:', font=font1).grid(row=4, sticky='W')
    text2 = Text(root_frame, height=10, width=40, state='disabled')
    button2 = Button(root_frame, text='Settings')
    ###############################
    settings = Toplevel(root)
    settings.wm_title('settings')
    settings.withdraw()
    settings.protocol('WM_DELETE_WINDOW', lambda: settings.withdraw())
    settings_frame = Frame(settings)
    Label(settings_frame, text='Rotors order:', font=font1).grid(row=0, sticky='W')
    frame2 = Frame(settings_frame)
    rotors_list = [1, 2, 3]
    rotors = []
    for i in range(3):
        rotors.append(ttk.Combobox(frame2, values=rotors_list, width=3, state='readonly'))
        rotors[i].set(1)
    Label(settings_frame, text='First rotors position:', font=font1).grid(row=2, sticky='W')
    frame3 = Frame(settings_frame)
    letters_list = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    letters = []
    for i in range(3):
        letters.append(ttk.Combobox(frame3, values=letters_list, width=3, state='readonly'))
        letters[i].set('a')
    Label(settings_frame, text='Cables (must be 6):', font=font1).grid(row=4, sticky='W')
    frame4 = Frame(settings_frame)
    frame5 = Frame(settings_frame)
    for i in letters_list:
        index = ord(i) - 97
        letters_buttons1.append(Button(frame4, text=i, command=(lambda x:
                                                                lambda: button_press(x, 0, canvas))(index)))
        letters_buttons1[index].grid(row=0, column=index, padx=5)

    canvas = Canvas(settings_frame, width=700, height=80, bg='white')
    for i in letters_list:
        index = ord(i) - 97
        letters_buttons2.append(Button(frame5, text=i, command=(lambda x: lambda: button_press(x, 1, canvas))(index)))
        letters_buttons2[index].grid(row=0, column=index, padx=5)
    frame4.grid(row=5, padx=5)
    canvas.grid(row=6)
    frame5.grid(row=7, padx=5)
    grid_all(button1, button2, rotors, text1, text2, frame2, letters, frame3, root_frame, settings_frame, settings, canvas)
    root.mainloop()


if __name__ == "__main__":
    main()
