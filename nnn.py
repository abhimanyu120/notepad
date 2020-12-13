from tkinter import  *
import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, messagebox, filedialog
import Controller
import traceback



class Notepad:

    def __init__(self, root):

        self.root = root
        self.url =''
        self.text_changed = False
        self.notepadController = Controller.Controller()
        self.root.geometry('1000x600')
        self.root.title('MyNotepad')
        #self.root.wm_iconbitmap('icon.ico')
        self.set_icons()
        self.set_menu_bar()
        self.set_file_sub_menu()
        self.set_edit_sub_menu()
        self.set_canvas()
        self.Set_status_bar()
        self.set_file_menu_event_bindings()
        self.root.protocol("WM_DELETE_WINDOW",self.exit_func)

    def set_icons(self):
        self.new_icon = tk.PhotoImage(file='icons/new.png')
        self.open_icon = tk.PhotoImage(file='icons/open.png')
        self.save_icon = tk.PhotoImage(file='icons/save.png')
        self.save_as_icon = tk.PhotoImage(file='icons/save_as.png')
        self.exit_icon = tk.PhotoImage(file='icons/exit.png')
        self.copy_icon = tk.PhotoImage(file='icons/copy.png')
        self.paste_icon = tk.PhotoImage(file='icons/paste.png')
        self.cut_icon = tk.PhotoImage(file='icons/cut.png')
        self.clear_icon = tk.PhotoImage(file='icons/clear_all.png')
        self.find_icon = tk.PhotoImage(file='icons/find.png')
        self.tool_bar_icon = tk.PhotoImage(file='icons/tool_bar.png')

    def set_menu_bar(self):
        self.main_menu = tk.Menu()
        self.file = tk.Menu(self.main_menu, tearoff=False)
        self.edit = tk.Menu(self.main_menu, tearoff=False)
        self.view = tk.Menu(self.main_menu, tearoff=False)
        self.color_theme = tk.Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label='File', menu=self.file)
        self.main_menu.add_cascade(label='Edit', menu=self.edit)
        self.main_menu.add_cascade(label='View', menu=self.view)
        self.main_menu.add_cascade(label='Color Theme', menu=self.color_theme)
        self.root.config(menu=self.main_menu)


    def set_file_sub_menu(self):
        self.file.add_command(label='New', image=self.new_icon, compound=tk.LEFT, accelerator='Ctrl+N', command=self.new_file)
        self.file.add_command(label='Open', image=self.open_icon, compound=tk.LEFT, accelerator='Ctrl+O', command=self.open_file)
        self.file.add_command(label='Save', image=self.save_icon, compound=tk.LEFT, accelerator='Ctrl+S', command=self.save_file)
        self.file.add_command(label='Save_as', image=self.save_as_icon, compound=tk.LEFT, accelerator='Ctrl+S', command=self.save_as)
        self.file.add_command(label='Exit', image=self.exit_icon, compound=tk.LEFT, accelerator='Ctrl+Q', command=self.exit_func)

    def set_canvas(self):
        self.text_editor = tk.Text(self.root)
        self.text_editor.config(wrap='word',relief = tk.FLAT)
        self.text_editor.focus_set()
        self.scroll_bar = tk.Scrollbar(self.root)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.pack(fil=tk.BOTH, expand=True)
        self.scroll_bar.config(command= self.text_editor.yview)
        self.text_editor.config(yscrollcommand= self.scroll_bar.set)

        self.text_changed=False
        self.text_editor.bind('<<Modified>>',self.changed)

    def Set_status_bar(self):
        self.set_status_bar = tk.Label(self.root, text='Status Bar')
        self.set_status_bar.pack(side=tk.BOTTOM)
        self.count= 1



    def set_file_menu_event_bindings(self):
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-N>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-O>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-S>", self.save_file)
        self.root.bind("<Alt-s>", self.save_as)
        self.root.bind("<Alt-S>", self.save_as)
        self.root.bind("<Control-q>", self.exit_func)
        self.root.bind("<Control-Q>", self.exit_func)

    def save_file(self, event= None):

        try:
            content = self.text_editor.get(1.0,"end-1c")
            if self.url == "":
                self.save_dialog()
                self.notepadController.save_file(content, self.url)
                self.text_changed = False

            else:
                self.notepadController.save_file(content,self.url)
                self.text_changed = False

        except Exception:
            messagebox.showerror("Error!","Please Select A file to Save")
            print(traceback.format_exc())

    def save_dialog(self):
        self.url = filedialog.asksaveasfile(mode='w', defaultextension= '.ntxt', filetypes= ([("ALL Files", "."),("Text Documents","*.txt")]))


    def open_file(self):

        try:
            self.open_dialog()
            self.msg, self.base = self.notepadController.read_file(self.url)
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, self.msg)
            self.root.title(self.base)
            self.text_editor.edit_modified(False)
        except FileNotFoundError:
            messagebox.showerror("Error", "Please Select a File First! ")
            print(traceback.format_exc())

    def open_dialog(self):
        self.url = filedialog.askopenfilename(title='Select File', filetypes = [("Text Documenets", ".")])

    def save_as(self):
        try:
            content = self.text_editor.get(1.0, "end-1c")

            self.save_dialog()
            self.notepadController.save_as(content, self.url)

        except Exception:
            messagebox.showerror("Error", "Please Enter File Name")
            print(traceback.format_exc())

    def new_file(self):
        self.url=""
        self.text_editor.delete(1.0, tk.END)
        self.root.title("My_notepad")

    def changed(self, event=None):
        words= len(self.text_editor.get(1.0,'end-1c').split())
        characters= len(self.text_editor.get(1.0,'end-1c'))
        self.set_status_bar.config(text=f'Characters : {characters} word : {words}')
        if self.text_editor.edit_modified():
            self.text_changed= True
        self.text_editor.edit_modified(False)

    def exit_func(self):
        result = messagebox.askyesno("App Closing!!!", "Do you want to quit")
        if result == False:
            return
        try:
            if self.url=='':
                if len(self.text_editor.get("1.0",'end-1c'))== 0:
                    self.text_changed = False

                if self.text_changed:
                    mbox = messagebox.askokcancel('Warning', 'Do you want to Save this File')
                    if mbox == True:
                        content = self.text_editor.get(1.0,"end-1c")
                        if self.url == "":
                            self.save_dialog()
                            self.notepadController.save_file(content,self.url)
                        else:
                            self.notepadController.save_file(content,self.url)

            messagebox.showinfo("Have a Good Day!","Thank you for using \"MyNotePad\"")
            self.root.destroy()

        except:
            messagebox.showerror("Error","Plese Select File to Save")
            print(traceback.format_exc())


    def set_edit_sub_menu(self):
        self.edit.add_command(label='Copy', image=self.copy_icon, compound= tk.LEFT, accelerator= 'Ctrl+C', command=lambda  :self.text_editor.event_generate("<<Copy>>"))
        self.edit.add_command(label='Paste', image=self.paste_icon, compound= tk.LEFT, accelerator= 'Ctrl+V', command=lambda :self.text_editor.event_generate("<<Paste>>"))
        self.edit.add_command(label='Cut', image=self.cut_icon, compound= tk.LEFT, accelerator= 'Ctrl+X', command=lambda :sel----------------------------------------------------------------------------------------------------f.text_editor.event_generate("<<Cut>>"))
        self.edit.add_command(label='Clear All', image=self.clear_icon, compound=tk.LEFT, accelerator= 'Ctrl+X', command=lambda :self.text_editor.delete(1.0, tk.END))
        self.edit.add_command(label='Find', image=self.find_icon, compound= tk.LEFT, accelerator= 'Ctrl+C', command=self.find_func)

    def find_func(self, event=None):
        self.find_dialogue = tk.Toplevel()
        self.find_dialogue.geometry('450x250+500+200')
        self.find_dialogue.title('Find')
        self.find_dialogue.resizable(0,0)

        #frame
        self.find_frame = ttk.LabelFrame(self.find_dialogue, text = 'Find/Replace')
        self.find_frame.pack(pady=20)

        #labels
        self.text_find_label = ttk.Label(self.find_frame, text='Find : ')
        self.text_replace_label =ttk.Label(self.find_frame, text='Replace')

        ## entry
        self.find_input = ttk.Entry(self.find_frame, width=30)
        self.replace_input = ttk.Entry(self.find_frame, width=30)
        ## button
        self.find_button = ttk.Button(self.find_frame, text='Find', command=self.find)
        self.replace_button = ttk.Button(self.find_frame, text='Replace', command=self.replace)

        ## labelgrid
        self.text_find_label.grid(row=0, column=0, padx=4, pady=4)
        self.text_replace_label.grid(row=1, column=0, padx=4, pady=4)

        ## entry grid
        self.find_input.grid(row=0, column=1, padx=4, pady=4)
        self.replace_input.grid(row=1, column=1, padx=4, pady=4)

        ## button grid
        self.find_button.grid(row=2, column=0, padx=8, pady=4)
        self.replace_button.grid(row=2, column=1, padx=8, pady=4)

        self.find_dialogue.mainloop()
    def find(self):
        T = tk.Text()
        T.pack()
        str=T.get()
        print(type(str))
        #T.insert(END, "Hello User Bye User")
        #start_pos = T.search("se", "1.0", stopindex=END)
        #T.tag_add('', "1.0", "1.2")
        #T.tag_config("here", background='red', foreground='blue')



        char=self.find_input.get()


    def replace(self):
            pass

root = tk.Tk()
obj = Notepad(root)
root.mainloop()