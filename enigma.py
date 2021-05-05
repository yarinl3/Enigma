from tkinter import *
from tkinter import ttk
import random
global canvas_lines, letters_buttons1, letters_buttons2
canvas_lines, letters_buttons1, letters_buttons2 = [], [], []


def get_defaults():
    rotor1 = ['k', 'y', 'p', 'j', 't', 'x', 'r', 'b', 'w', 'o', 'g', 'i', 'l', 'h', 'n', 'q', 'f', 'd', 'v', 'e', 'c',
              'z', 'u', 'a', 'm', 's']
    rotor2 = ['m', 'v', 'k', 'e', 'o', 'x', 'd', 't', 'c', 'y', 'j', 'a', 'g', 'z', 'f', 'l', 'q', 'n', 'i', 'r', 'w',
              'h', 'p', 'u', 'b', 's']
    rotor3 = ['n', 'b', 'g', 's', 'z', 'f', 'c', 'j', 'y', 'r', 'l', 'q', 'u', 'd', 'p', 'o', 't', 'k', 'e', 'v', 'w',
              'a', 'm', 'i', 'x', 'h']
    reflector1 = [('r', 'k'), ('y', 'd'), ('c', 'u'), ('z', 'i'), ('e', 'n'), ('s', 'h'), ('g', 'a'), ('m', 'l'),
        ('o', 'p'), ('f', 'b'), ('t', 'j'), ('v', 'x'), ('w', 'q')]
    return rotor1, rotor2, rotor3, reflector1


def fix_offset(letter, first_position):
    new_position = ord(letter) - 97 + first_position
    if new_position > 25:
        new_position -= 26
    if new_position < 0:
        new_position += 26
    return new_position


def reverse_rotor(rotor, letter, first_position):
    new_position = rotor.index(letter) + first_position * (-1)
    if new_position < 0:
        new_position += 26
    return chr(new_position + 97)


def find_pair(pairs, char):
    for pair in pairs:
        if char == pair[0]:
            return pair[1]
        if char == pair[1]:
            return pair[0]


def encrypt(settings, text, encode_or_decode):
    new_text = ''
    first_position, rotors_order, cables = settings
    if encode_or_decode == 1:
        for cable in cables:
            text = text.replace(cable[0], '*')
            text = text.replace(cable[1], cable[0])
            text = text.replace('*', cable[1])

    first_position = first_position.lower()
    rotor1, rotor2, rotor3, reflector_pairs = get_defaults()
    rotors = [rotor1, rotor2, rotor3]
    rotors = [rotors[rotors_order[0] - 1], rotors[rotors_order[1] - 1], rotors[rotors_order[2] - 1]]
    rotor1_first_position = ord(first_position[0]) - 97
    rotor2_first_position = ord(first_position[1]) - 97
    rotor3_first_position = ord(first_position[2]) - 97

    for inx, val in enumerate(text):
        stage1 = rotors[0][fix_offset(val, rotor1_first_position)]
        stage2 = rotors[1][fix_offset(stage1, rotor2_first_position)]
        stage3 = rotors[2][fix_offset(stage2, rotor3_first_position)]
        stage4 = chr(fix_offset(stage3, rotor3_first_position * (-1)) + 97)
        stage5 = find_pair(reflector_pairs, stage4)
        stage6 = chr(fix_offset(stage5, rotor3_first_position) + 97)
        stage7 = reverse_rotor(rotors[2], stage6, rotor3_first_position)
        stage8 = reverse_rotor(rotors[1], stage7, rotor2_first_position)
        stage9 = reverse_rotor(rotors[0], stage8, rotor1_first_position)
        new_text += stage9
        print(val, stage1, stage2, stage3, stage4, stage5, stage6, stage7, stage8, stage9)
        # rotors movements
        rotor3_first_position += 1
        if rotor3_first_position == 26:
            rotor3_first_position = 0
            rotor2_first_position += 1
        if rotor2_first_position == 26:
            rotor2_first_position = 0
            rotor1_first_position += 1
        if rotor1_first_position == 26:
            rotor1_first_position = 0
    if encode_or_decode == 2:
        for cable in cables:
            new_text = new_text.replace(cable[0], '*')
            new_text = new_text.replace(cable[1], cable[0])
            new_text = new_text.replace('*', cable[1])
    return new_text


def get_cables_from_canvas(canvas):
    upper_buttons_indexes = [i[0] for i in canvas_lines]
    lower_buttons_indexes = [i[1] for i in canvas_lines]
    offset = 16
    if len(canvas_lines) < 6:
        for i in range(6 - len(canvas_lines)):
            while True:
                upper_button_index = random.randint(0, 25)
                if (upper_button_index not in upper_buttons_indexes) and (upper_button_index not in lower_buttons_indexes):
                    break
            while True:
                lower_button_index = random.randint(0, 25)
                if (lower_button_index not in lower_buttons_indexes) and (lower_button_index not in upper_buttons_indexes)\
                        and (lower_button_index != upper_button_index):
                    break
            upper_buttons_indexes.append(upper_button_index)
            lower_buttons_indexes.append(lower_button_index)
            line = canvas.create_line(upper_button_index * 700/26 + offset, 2, lower_button_index * 700/26 + offset, 78)
            canvas_lines.append([upper_button_index, lower_button_index, line])
    disable_buttons()
    return [(chr(97+i[0]), chr(97+i[1])) for i in canvas_lines]


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


def before_encrypt(decrypted_textbox, encrypted_textbox, rotors, letters, canvas, radio):
    first_position = letters[0].get() + letters[1].get() + letters[2].get()
    rotors_order = [int(rotors[0].get()), int(rotors[1].get()), int(rotors[2].get())]
    cables = get_cables_from_canvas(canvas)
    settings = [first_position, rotors_order, cables]
    decrypted_text = decrypted_textbox.get('1.0', END).lower()
    encrypted_text = encrypted_textbox.get('1.0', END).lower()

    new_decrypted_text = ''
    for letter in decrypted_text:
        if (ord(letter) >= ord('a')) and (ord(letter) <= ord('z')):
            new_decrypted_text += letter
    new_encrypted_text = ''
    for letter in encrypted_text:
        if (ord(letter) >= ord('a')) and (ord(letter) <= ord('z')):
            new_encrypted_text += letter

    if len(new_decrypted_text) != 0 and radio.get() == '1':
        encrypted_textbox.delete(1.0, END)
        encrypted_textbox.insert(1.0, encrypt(settings, new_decrypted_text, 1))

    if len(new_encrypted_text) != 0 and radio.get() == '2':
        decrypted_textbox.delete(1.0, END)
        decrypted_textbox.insert(1.0, encrypt(settings, new_encrypted_text, 2))


def grid_all(button1, button2, rotors, text1, text2, frame2, letters, frame3, root_frame, settings_frame, settings, canvas, radio):
    text1.grid(row=2, pady=5)
    button1.config(command=lambda: before_encrypt(text1, text2, rotors, letters, canvas, radio))
    button1.grid(row=4)
    text2.grid(row=6, pady=5)
    button2.config(command=lambda: settings.deiconify())
    button2.grid(row=7, pady=5)
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
                for canvas_line in canvas_lines:
                    if second_row_button_index == canvas_line[1] and row_button_index == canvas_line[0]:
                        to_delete.append(canvas_line)
                        same_line = True
                    else:
                        if row_button_index == canvas_line[0]:
                            to_delete.append(canvas_line)
                        if second_row_button_index == canvas_line[1]:
                            to_delete.append(canvas_line)
                upper_button_index, lower_button_index = row_button_index, second_row_button_index
            else:
                for canvas_line in canvas_lines:
                    if row_button_index == canvas_line[1] and second_row_button_index == canvas_line[0]:
                        to_delete.append(canvas_line)
                        same_line = True
                    else:
                        if row_button_index == canvas_line[1]:
                            to_delete.append(canvas_line)
                        if second_row_button_index == canvas_line[0]:
                            to_delete.append(canvas_line)
                upper_button_index, lower_button_index = second_row_button_index, row_button_index
            for canvas_line_to_delete in to_delete:
                canvas_lines.remove(canvas_line_to_delete)
                canvas.delete(canvas_line_to_delete[2])
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


def change(button, text1, text2, rotors, letters, canvas, radio):
    if radio.get() == '2':
        button['text'] = 'Decrypt'
        button['command'] = lambda: before_encrypt(text1, text2, rotors, letters, canvas, radio)
    else:
        button['text'] = 'Encrypt'
        button['command'] = lambda: before_encrypt(text1, text2, rotors, letters, canvas, radio)


def main():
    font1 = ('Arial', 18)
    font2 = ('Arial', 30)
    font3 = ('Arial', 14)
    root = Tk()
    root.wm_title('Enigma')
    root_frame = Frame(root)
    Label(root_frame, text='Enigma', font=font2).grid(row=0, pady=5)
    Label(root_frame, text='Text before encrypt (English letters only):', font=font1).grid(row=1, sticky='W')
    text1 = Text(root_frame, height=10, width=40)
    encrypt_frame = Frame(root_frame)
    radio = StringVar()
    radio.set(1)
    encrypt_radio = Radiobutton(encrypt_frame, text="Encrypt", command=lambda: change(button1, text1, text2, rotors, letters, canvas, radio), variable=radio, value=1)
    encrypt_radio.grid(row=0, pady=5)
    decrypt_radio = Radiobutton(encrypt_frame, text="Decrypt", command=lambda: change(button1, text1, text2, rotors, letters, canvas, radio), variable=radio, value=2)
    decrypt_radio.grid(row=1,pady=5)
    button1 = Button(root_frame, text='Encrypt', font=font3)
    Label(root_frame, text='Encrypted text:', font=font1).grid(row=5, sticky='W')
    text2 = Text(root_frame, height=10, width=40)
    button2 = Button(root_frame, text='Settings')
    encrypt_frame.grid(row=4, column=0, sticky='W')
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
    for letter in letters_list:
        index = ord(letter) - 97
        letters_buttons1.append(Button(frame4, text=letter, command=(lambda x:
                                                                     lambda: button_press(x, 0, canvas))(index)))
        letters_buttons1[index].grid(row=0, column=index, padx=5)

    canvas = Canvas(settings_frame, width=700, height=80, bg='white')
    for letter in letters_list:
        index = ord(letter) - 97
        letters_buttons2.append(Button(frame5, text=letter, command=(lambda x:
                                                                     lambda: button_press(x, 1, canvas))(index)))
        letters_buttons2[index].grid(row=0, column=index, padx=5)
    frame4.grid(row=5, padx=5)
    canvas.grid(row=6)
    frame5.grid(row=7, padx=5)
    grid_all(button1, button2, rotors, text1, text2, frame2, letters, frame3, root_frame, settings_frame, settings, canvas, radio)
    root.mainloop()


if __name__ == "__main__":
    main()
