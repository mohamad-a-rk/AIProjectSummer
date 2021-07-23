from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
from AI import *
from Human import *

title_font = ('Comic Sans MS', 23)
font_tuple = ('Comic Sans MS', 12)

EASY = 2
MEDIUM = 4
HARD = 5


def backward(main_label, widget):
    main_label.grid_forget()
    widget.place_forget()
    main_label.grid(column=1, row=0, sticky='N')


def choose_level(lev):
    if lev == 'Easy':
        play_game(EASY)
    elif lev == 'Medium':
        play_game(MEDIUM)
    else:
        play_game(HARD)


def show_levels_dialog(main_label):
    main_label.grid_forget()

    dlg = Label(width=25, height=15, bg='#ebdab4')

    title = Label(dlg, text='Select Level:', font=('Comic Sans MS', 14), bg='#ebdab4', padx='30', pady=5)
    title.pack()

    combo = Combobox(dlg, state='readonly')
    combo['values'] = ('Easy', 'Medium', 'Hard')
    combo.current(0)
    combo.pack(pady=5)

    ok = Button(dlg, text='OK', width=10, font=('Comic Sans MS', 10), bg='#ebdab4', cursor='hand2',
                command=lambda: choose_level(combo.get()))
    ok.pack(pady=5)

    back = Button(dlg, text='BACK', width=10, font=('Comic Sans MS', 10), bg='#ebdab4', cursor='hand2',
                  command=lambda: backward(main_label, dlg))
    back.pack()

    main_label.grid(column=1, row=0, sticky='N')

    dlg.place(x=75, y=100)


def run():
    # Main Window
    window = Tk()
    # window.geometry('660x560')
    window.title('Connect 4 Game')
    window.resizable(False, False)

    canvas = Canvas(window, width=320, height=420)
    canvas.grid(columnspan=3)  # WE USE COLUMN SPAN = 3 TO CENTRALIZE THE CONTENTS

    main_label = Label(bg='#2596be')

    title = Label(main_label, text='Play Connect4 Game', fg='#fec67c', bg='#2596be', font=title_font)
    title.pack(pady=10)

    logo = Image.open('Connect4.png').resize((320, 200))
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(main_label, image=logo)
    logo_label.pack()

    # Choose to play
    choose_label = Label(main_label, bg='#2596be')

    ai = Button(choose_label, text='Play With Computer', font=font_tuple, pady=2, cursor='hand2', width=20,
                command=lambda: show_levels_dialog(main_label))
    two_players = Button(choose_label, text='Play With Human', font=font_tuple, pady=2, cursor='hand2', width=20,
                         command=play_game_h)
    ai.grid(column=0, row=0, padx=10, pady=10)
    two_players.grid(column=0, row=1, padx=10, pady=10)

    choose_label.pack(pady=18)

    main_label.grid(column=1, row=0, sticky='N')

    window.mainloop()


if __name__ == '__main__':
    run()
