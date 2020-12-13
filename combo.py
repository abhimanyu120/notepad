from tkinter import *
from tkinter import ttk
def fun():
    l2.configure(text=cb.get())
root=Tk()
root.geometry("200x100")
course=("java","python","c")
l1=Label(root,text="chhose your favourite language")
l1.grid(column=0,row=0)
cb=ttk.Combobox(root,value=course,width=10)
cb.grid(column=0,row=1)
cb.current(0)
b=Button(root,text="Click Here",command=fun)
b.grid(column=0,row=2)
l2=Label(root,text="")
l2.grid (row=3,column=0)
root.mainloop()