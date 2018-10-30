import datetime
import random

from firebase import firebase
import matplotlib.pyplot as p
import numpy as np
from tkinter import *

firebase = firebase.FirebaseApplication('https://proyecto-b2674.firebaseio.com/')


def pushed():
    date = datetime.datetime.now()

    data_dict = {"Temperatura del Déposito de Aceite": "1",
                 "Presión de Aceite": "2",
                 "Presión en Condesador": "3",
                 "Saturación en Condesador": "4",
                 "Presión del Evaporador": "5",
                 "Saturación en Evaporador": "6"}
    firebase.post('/RPi', data_dict)
    #firebase.put('RPi', "NombreX", data_dict)

    lbl_1.configure(text="you clicked")


def get_data():
    global p_oil, p_ev, p_con, s_con, s_ev, temp
    data_dict = firebase.get("/RPi", None)
    for i, j in data_dict.items():
        for x, y in j.items():
            if x == "Presión de Aceite":
                p_oil.append(y)
            elif x == "Presión del Evaporador":
                p_ev.append(y)
            elif x == "Presión en Condesador":
                p_con.append(y)
            elif x == "Saturación en Condesador":
                s_con.append(y)
            elif x == "Saturación en Evaporador":
                s_ev.append(y)
            else:
                temp.append(y)

    p_oil = np.array(p_oil)
    p_ev = np.array(p_ev)
    p_con = np.array(p_con)
    s_con = np.array(s_con)
    s_ev = np.array(s_ev)
    temp = np.array(temp)
    variables.extend((p_oil, p_ev, p_con, s_con, s_ev, temp))
    return variables


def plot(oil, pev, pcon, scon, sev, tem):
    p.figure("Temperatura vs tiempo")
    p.plot(oil, tem, ".r")
    p.xlabel("Tiempo")
    p.ylabel("Temperatura")
    p.show()


def check_for_correlation():
    amount = 0
    for i in range(0, len(variables)):
        for j in range(i, len(variables)):
            if i != j:
                amount += 1
                corr = np.corrcoef(variables[i], variables[j])
                print("Coeficiente de correlación: {}".format(corr[0][1]))
    print(amount)
    """# Insert values into textbox
    txt_1.configure(state='normal')
    txt_1.insert("end", str(corr[0][1]))
    txt_1.configure(state='disabled')"""


if __name__ == "__main__":
    variables = []
    p_oil, p_ev, p_con, s_con, s_ev, temp = [], [], [], [], [], []

    '''Main Window'''
    window = Tk()
    # Window title
    window.title("RES (Raspberry pi Extraction System)")
    # Window size
    window.geometry('800x600')

    """-------------------------------------------------------GUI----------------------------------------------------"""
    '''Labels'''
    lbl_1 = Label(window, text="Push Data")
    lbl_2 = Label(window, text="Get Data")
    lbl_3 = Label(window, text="Graph variables")
    lbl_4 = Label(window, text="Check for correlation")
    lbl_5 = Label(window, text="Correlation coefficient")

    '''Buttons actions'''
    # Push data
    btn_1 = Button(window, text="Push data", bg="gray", fg="black", command=pushed)
    # Get data
    btn_2 = Button(window, text="Get data", bg="gray", fg="black", command=get_data)
    # Graph variables
    btn_3 = Button(window, text="Graph", bg="gray", fg="black", command=lambda: plot(p_oil, p_ev, p_con, s_con, s_ev,
                                                                                     temp))
    # Check correlation
    btn_4 = Button(window, text="Check", bg="gray", fg="black", command=lambda: check_for_correlation())

    '''Radio buttons'''
    selected = IntVar()

    # Radio buttons values must be different from each other
    rad1 = Radiobutton(window, text='Ultimas 24 horas', value=1, variable=selected)
    rad2 = Radiobutton(window, text='Ultimas 72 horas', value=2, variable=selected)
    rad3 = Radiobutton(window, text='Ultima semana', value=3, variable=selected)

    '''Textboxes'''
    # Correlation Coefficient
    txt_1 = Text(window, state='disabled', width=20, height=1)

    """----------------------------------------------------GRID------------------------------------------------------"""
    '''Labels Grid'''
    # Push data
    lbl_1.grid(column=0, row=0)
    # Get data
    lbl_2.grid(column=0, row=1)
    # Graph variables
    lbl_3.grid(column=0, row=2)
    # Check correlation
    lbl_4.grid(column=0, row=3)
    # Correlation Coefficient
    lbl_5.grid(column=3, row=3)

    '''Buttons grid'''
    # Push data
    btn_1.grid(column=1, row=0)
    # Get data
    btn_2.grid(column=1, row=1)
    # Graph variables
    btn_3.grid(column=1, row=2)
    # Check correlation
    btn_4.grid(column=1, row=3)

    '''Radio buttons grid'''
    rad1.grid(column=0, row=5)
    rad2.grid(column=0, row=6)
    rad3.grid(column=0, row=7)
    '''Textboxes grid'''
    # Correlation Coefficient
    txt_1.grid(column=4, row=3)

    # Window loop, must be at the end
    window.mainloop()
