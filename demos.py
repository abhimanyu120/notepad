import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, messagebox, filedialog
import Controller
import traceback

class Notepad:
    def exit_func(self):
        if self.text_changed == True:
            print("hello")
            d=messagebox.askyesno("Save","Is you Want to Save this")
            if d == True:
                self.save_file()
        c= messagebox.askyesno("quit","Are You Sure")
        if c==True:
            exit()

    def __init__(self,root):

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
        self.set_canvas()
        self.set_status_bar()
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
        #self.scroll_bar.config(Yscrollcommand=self.scroll_bar.set)

        self.text_changed=False
        self.text_editor.bind('<<Modified>>',self.text_changed)

    def set_status_bar(self):
        self.set_status_bar = tk.Label(self.root, text='Status Bar')
        self.set_status_bar.pack(side=tk.BOTTOM)
        self.count= 1
        print(self.count)

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

   # hw ::: at chsnged find character and word

root = tk.Tk()
#root.mainloop()
obj = Notepad(root)
root.mainloop()