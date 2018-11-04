import datetime
import random
from tkinter.ttk import Combobox

from firebase import firebase
import matplotlib.pyplot as p
import numpy as np
from tkinter import *

variables = []
corr_p, p_oil, p_ev, p_con, s_con, s_ev, temph_i, temph_s, tempc_i, tempc_s, temp_d, temp_a = [], [], [], [], [], [], \
                                                                                              [], [], [], [], [], []
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


def get_data(corrp, poil, pev, pcon, scon, sev, temphi, temphs, tempci, tempcs, tempd, tempa):
    # Here we clear the array
    variables.clear()
    data_dict = firebase.get("/data", None)
    print(combo1.get())

    if combo1.get() == "Ultimas 24 horas":
        length = 10  # value of the radio button for time lapse
    elif combo1.get() == 'Ultimas 72 horas':
        length = 50
    else:
        length = 100

    count = 0  # This counter indicates how much variables we are gonna get
    for i, j in data_dict.items():
        count += 1
        if count > length:
            break
        for x, y in j.items():
            if x == "% de Corriente a Plena Carga":
                corrp.append(y)
            elif x == "Presión de Aceite":
                poil.append(y)
            elif x == "Presión del Evaporador":
                pev.append(y)
            elif x == "Presión en Condesador":
                pcon.append(y)
            elif x == "Saturación en Condesador":
                scon.append(y)
            elif x == "Saturación en Evaporador":
                sev.append(y)
            elif x == "Temperatura de Agua Helada":
                for z, w in y.items():
                    if z == "Introduciendo":
                        temphi.append(w)
                    else:
                        temphs.append(w)
            elif x == "Temperatura de Agua de Condensación":
                for z, w in y.items():
                    if z == "Introduciendo":
                        tempci.append(w)
                    else:
                        tempcs.append(w)
            elif x == "Temperatura de Descarga":
                tempd.append(y)
            else:
                tempa.append(y)
    print("Contador: ", count)
    corrp = np.array(corrp)
    poil = np.array(poil)
    pev = np.array(pev)
    pcon = np.array(pcon)
    scon = np.array(scon)
    sev = np.array(sev)
    temphi = np.array(temphi)
    temphs = np.array(temphs)
    tempci = np.array(tempci)
    tempcs = np.array(tempcs)
    tempd = np.array(tempd)
    tempa = np.array(tempa)

    # Here we return all variables as a dictionary
    variables.extend((corrp, poil, pev, pcon, scon, sev, temphi, temphs, tempci, tempcs, tempd, tempa))


def plot(x, y, x_label, y_label):
    p.figure(x_label + " vs " + y_label)
    print("x:", x)
    print("y:", y)
    p.plot(x, y, ".r")
    p.xlabel(x_label)
    p.ylabel(y_label)
    p.show()


# Lets_plot allows to get the list of data and the respective label for the radio buttons selected
def lets_plot(name1, name2):
    if name1 == '1x':
        print("1 good")
        x = variables[0]
        x_label = 'Presion aceite'
    elif name1 == '2x':
        x = variables[1]
    else:
        x = variables[5]
    if name2 == '1y':
        y = variables[0]
    elif name2 == '2y':
        y = variables[1]
    else:
        print("2 good")
        y = variables[5]
        y_label = 'Temperatura'
    plot(x, y, x_label, y_label)


def check_for_correlation():
    amount = 0
    print("cantidad variables: ", len(variables))
    for i in range(0, len(variables)):  # len(variables) to get all data
        for j in range(i, len(variables)):
            if i != j:
                amount += 1
                corr = np.corrcoef(variables[i], variables[j])
                corr = corr[0][1]
                if corr >= 0.8:
                    print("Relevant correlation")
                print("Coeficiente de correlación: {}".format(corr))
    print(amount)
    """# Insert values into textbox
    txt_1.configure(state='normal')
    txt_1.insert("end", str(corr[0][1]))
    txt_1.configure(state='disabled')"""


if __name__ == "__main__":

    '''Main Window'''
    window = Tk()
    # Window title
    window.title("DSRED (Display System for Raspberry pi Extracted Data)")
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
    btn_2 = Button(window, text="Get data", bg="gray", fg="black", command=lambda: get_data(corr_p, p_oil, p_ev, p_con,
                                                                                            s_con, s_ev, temph_i,
                                                                                            temph_s, tempc_i, tempc_s,
                                                                                            temp_d, temp_a))
    # Graph variables
    btn_3 = Button(window, text="Graph", bg="gray", fg="black", command=lambda: lets_plot(combo2.get(), selected3.get()))
    # Check correlation
    btn_4 = Button(window, text="Check", bg="gray", fg="black", command=lambda: check_for_correlation())

    '''Combo boxes'''
    # Radio buttons values must be different from each other
    selected2 = StringVar()  # Selected for x axis
    selected3 = StringVar()  # Selected for y axis
    combo1 = Combobox(window, state='readonly')
    combo2 = Combobox(window, state='readonly')
    combo3 = Combobox(window, state='readonly')

    combo1['values'] = ('Ultimas 24 horas', 'Ultimas 72 horas', 'Ultima semana')
    combo2['values'] = ('Temperatura de Descarga', '% de Corriente a Plena Carga', 'Temp Introduciendo Agua de condensación',
                        'Temp Introduciendo agua de condensación','Temperatura del Depósito de Aceite', 'Presión de Aceite',
                        'Temp Introduciendo Agua Helada' 'Temp Salida Agua Helada')
    combo3['values'] = (1, 2, 3, 4, 5, "Text")


    # Graph x axis
    rad1x = Radiobutton(window, text='Temperatura de Descarga', value='1x', variable=selected2)
    rad2x = Radiobutton(window, text='% de Corriente a Plena Carga', value='2x', variable=selected2)
    rad3x = Radiobutton(window, text='Presion aceite', value='3x', variable=selected2)
    rad4x = Radiobutton(window, text='Presion aceite', value='4x', variable=selected2)
    rad5x = Radiobutton(window, text='Presion aceite', value='5x', variable=selected2)
    rad6x = Radiobutton(window, text='Presion aceite', value='6x', variable=selected2)
    rad7x = Radiobutton(window, text='Presion aceite', value='7x', variable=selected2)
    rad8x = Radiobutton(window, text='Presion aceite', value='8x', variable=selected2)
    rad9x = Radiobutton(window, text='Presion aceite', value='9x', variable=selected2)
    rad10x = Radiobutton(window, text='Presion aceite', value='10x', variable=selected2)
    rad11x = Radiobutton(window, text='Presion aceite', value='11x', variable=selected2)
    rad12x = Radiobutton(window, text='Presion aceite', value='12x', variable=selected2)

    # Graph x axis
    rad1y = Radiobutton(window, text='Presion aceite', value='1y', variable=selected3)
    rad2y = Radiobutton(window, text='Presion aceite', value='2y', variable=selected3)
    rad3y = Radiobutton(window, text='Presion aceite', value='3y', variable=selected3)
    rad4y = Radiobutton(window, text='Presion aceite', value='4y', variable=selected3)
    rad5y = Radiobutton(window, text='Presion aceite', value='5y', variable=selected3)
    rad8y = Radiobutton(window, text='Presion aceite', value='6y', variable=selected3)
    rad6y = Radiobutton(window, text='Presion aceite', value='7y', variable=selected3)
    rad7y = Radiobutton(window, text='Presion aceite', value='8y', variable=selected3)
    rad9y = Radiobutton(window, text='Presion aceite', value='9y', variable=selected3)
    rad10y = Radiobutton(window, text='Presion aceite', value='10y', variable=selected3)
    rad11y = Radiobutton(window, text='Presion aceite', value='11y', variable=selected3)
    rad12y = Radiobutton(window, text='Presion aceite', value='12y', variable=selected3)

    '''Textboxes'''
    # Correlation Coefficient
    txt_1 = Text(window, state='disabled', width=20, height=1)

    """-------------------------------------------------GRID--------------------------------------------------------"""
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
    # Time lapse
    combo1.grid(column=20, row=5)
    combo2.grid(column=21, row=5)
    combo3.grid(column=22, row=5)

    # Graph x axis
    rad1x.grid(column=3, row=10)
    rad2x.grid(column=3, row=11)
    rad3x.grid(column=3, row=12)
    rad4x.grid(column=3, row=13)
    rad5x.grid(column=3, row=14)
    rad6x.grid(column=3, row=15)
    rad7x.grid(column=3, row=16)
    rad8x.grid(column=3, row=17)
    rad9x.grid(column=3, row=18)
    rad10x.grid(column=3, row=19)
    rad11x.grid(column=3, row=20)
    rad12x.grid(column=3, row=21)

    # Graph x axis
    rad1y.grid(column=4, row=10)
    rad2y.grid(column=4, row=11)
    rad3y.grid(column=4, row=12)
    rad4y.grid(column=4, row=13)
    rad5y.grid(column=4, row=14)
    rad6y.grid(column=4, row=15)
    rad7y.grid(column=4, row=16)
    rad8y.grid(column=4, row=17)
    rad9y.grid(column=4, row=18)
    rad10y.grid(column=4, row=19)
    rad11y.grid(column=4, row=20)
    rad12y.grid(column=4, row=21)

    '''Textboxes grid'''
    # Correlation Coefficient
    txt_1.grid(column=4, row=3)

    # Window loop, must be at the end
    window.mainloop()
