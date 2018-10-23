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
    #firebase.post('/RPi', data_dict)
    firebase.put('RPi', "NombreX" ,data_dict)

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

    return p_oil, p_ev, p_con, s_con, s_ev, temp

def plot(oil, pev, pcon, scon, sev, tem):
    p.figure("Temperatura vs tiempo")
    p.plot(oil, tem, ".r")
    p.xlabel("Tiempo")
    p.ylabel("Temperatura")
    p.show()

def check_for_correlation(data_1, data_2):
    corr = np.corrcoef(data_1, data_2)
    print("Coeficiente de correlación: {}".format(corr[0][1]))
    txt_1.configure(state='normal')
    txt_1.insert("end", str(corr[0][1]))
    txt_1.configure(state='disabled')

if __name__ == "__main__":

    p_oil, p_ev, p_con, s_con, s_ev, temp = [], [], [], [], [], []

    '''Main Window'''
    window = Tk()
    # Window title
    window.title("RED (Raspberry pi Extracted Data)")
    # Window size
    window.geometry('800x600')


    # Labels
    lbl_1 = Label(window, text="Push Data")
    lbl_2 = Label(window, text="Get Data")
    lbl_3 = Label(window, text="Graph variables")
    lbl_4 = Label(window, text="Check for correlation")
    lbl_5 = Label(window, text="Correlation coefficient")

    # Buttons
    btn_1 = Button(window, text="Push data", bg="gray", fg="black", command=pushed)
    btn_2 = Button(window, text="Get data", bg="gray", fg="black", command=get_data)
    btn_3 = Button(window, text="Graph", bg="gray", fg="black",
                  command= lambda: plot(p_oil,p_ev, p_con, s_con, s_ev, temp))
    btn_4 = Button(window, text="Check", bg="gray", fg="black",
                  command= lambda: check_for_correlation(p_oil, temp))

    # Textboxes
    txt_1 = Text(window, state='disabled', width = 20, height=1)

    # Labels' Grid
    lbl_1.grid(column=0, row=0)
    lbl_2.grid(column=0, row=1)
    lbl_3.grid(column=0, row=2)
    lbl_4.grid(column=0, row=3)
    lbl_5.grid(column=3, row=3)

    # Buttons' grid
    btn_1.grid(column=1, row=0)
    btn_2.grid(column=1, row=1)
    btn_3.grid(column=1, row=2)
    btn_4.grid(column=1, row=3)

    # Textboxes' grid
    txt_1.grid(column=4, row=3)

    # Window loop, must be at the end
    window.mainloop()
