#!/usr/bin/python
from Tkinter import *
from tkFileDialog import askopenfilename
import qrgenerator
def openfile():
   filename = askopenfilename(parent=root)
 #  f = open(filename)
#   f.read()
   text = entry.get()
   qrgenerator.create_qrcode(text, filename).show()

root = Tk()
root.wm_title("Create Your Own QRCode!")
root.resizable(width=FALSE, height=FALSE)
root.geometry('{}x{}'.format(500, 50))

entry = Entry(root, width=200)
entry.pack()
entry.delete(0,END)
entry.insert(0,"http://www.coronelbicaco.rs.gov.br")
b = Button(root, text="Create QRCode!", width=10, command=openfile)
b.pack()


root.mainloop()