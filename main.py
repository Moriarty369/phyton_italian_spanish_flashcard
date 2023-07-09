from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/italian_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # Datos orientados como record para obtener una lista de diccionarios separados por cada fila
    # (pares italiano-español)
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    # Cancelamos el flip timer en caso de que se haya pasado manualmente a la siguiente palabra
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    # Asociamos con el .csv
    current_card["Italiano"]
    # Modificamos el titulo de la card en cada slice
    canvas.itemconfig(card_title, text="Italiano", fill="black")
    # Modificamos la palabra en cada slice
    canvas.itemconfig(card_word, text=current_card["Italiano"], fill="black")
    canvas.itemconfig(card_bg, image=card_front_img)
    # Reiniciar el fliptimer
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="Español", fill="white")
    canvas.itemconfig(card_word, text=current_card["Español"], fill="white")
    canvas.itemconfig(card_bg, image=card_back_img)


def is_know():
    to_learn.remove(current_card)
    next_card()
    # Creamos un nuevo csv para las palabras NO acertadas y así al reiniciar la app empezamos con ese archivo (para guardar progresos)
    data_to_learn = pandas.DataFrame(to_learn)
    # Eliminando el index del dataframe generado por pandas
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Parla")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# Temporizador para switch cards y mostar palabra en español
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
know_button = Button(image=check_image, highlightthickness=0, command=is_know)
know_button.grid(row=1, column=1)

next_card()
window.mainloop()