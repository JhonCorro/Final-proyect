from firebase import firebase
from tkinter import *

firebase = firebase.FirebaseApplication('https://proyecto-b2674.firebaseio.com/')

def pushed():
    lbl.configure(text="you clicked")
    result = firebase.post('/user', {'admin': {'name': 'admin'}})
    print(result)

'''Main Window'''
window = Tk()
# Window title
window.title("RED (Raspberry pi Extracted Data)")
# Window size
window.geometry('800x600')


# Labels
lbl = Label(window, text="Push Data")
lb2 = Label(window, text="Get Data")

# Buttons
btn = Button(window, text="Do the thing", bg="red", fg="black", command=pushed)

# Grid
lbl.grid(column=0, row=0)
lb2.grid(column=0, row=1)
btn.grid(column=1, row=0)

# Window loop, must be at the end
window.mainloop()
