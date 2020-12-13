from tkinter import *
import traceback
from tkinter import font,messagebox,filedialog,colorchooser
import Controller
from tkinter import ttk
class View:
    def __init__(self,root):
        self.root = root
        self.url = ""
        self.text_changed = FALSE
        self.control = Controller.Controller()
        self.my_font = font.Font(family='Arial')
        self.root.geometry("1200x800")
        self.root.title("My NotePad")
        #self.root.wm_iconbitmap("icon.ico")
        self.set_icons()
        self.set_menu_bar()
        self.show_statusbar = BooleanVar()  # for show Status bar
        self.show_statusbar.set(True)
        self.show_toolbar = BooleanVar()  # for show tool bar
        self.show_toolbar.set(True)
        self.set_file_sub_menu()
        self.set_edit_sub_menu()
        self.set_view_sub_menu()
        self.set_color_theme_sub_menu()
        self.set_tool_bar()
        self.set_canvas()
        self.set_status_bar()
        self.set_file_menu_event_bindings()
        self.set_view_menu_event_bindings()
        self.set_tool_bar_event_bindings()
        self.b_count = False
        self.i_count = False
        self.u_count = False
        self.count = 0

        self.root.protocol("WM_DELETE_WINDOW", self.exit_func)

    def set_icons(self):
        self.new_icon = PhotoImage(file='icons/new.png')
        self.open_icon = PhotoImage(file='icons/open.png')
        self.save_icon = PhotoImage(file='icons/save.png')
        self.save_as_icon = PhotoImage(file='icons/save_as.png')
        self.exit_icon = PhotoImage(file='icons/exit.png')
        self.copy_icon=PhotoImage(file='icons/copy.png')
        self.cut_icon = PhotoImage(file='icons/cut.png')
        self.paste_icon = PhotoImage(file='icons/paste.png')
        self.clear_all_icon = PhotoImage(file='icons/clear_all.png')
        self.find_icon = PhotoImage(file='icons/find.png')
        self.tool_bar_icon = PhotoImage(file="icons/tool_bar.png")
        self.status_bar_icon = PhotoImage(file="icons/status_bar.png")
        self.light_default_icon = PhotoImage(file="icons/light_default.png")
        self.light_plus_icon = PhotoImage(file="icons/light_plus.png")
        self.dark_icon = PhotoImage(file="icons/dark.png")
        self.red_icon = PhotoImage(file="icons/red.png")
        self.monokai_icon = PhotoImage(file="icons/monokai.png")
        self.night_blue_icon = PhotoImage(file="icons/night_blue.png")

    def set_menu_bar(self):
        self.main_menu = Menu()

        self.file = Menu(self.main_menu, tearoff=FALSE)
        self.edit = Menu(self.main_menu, tearoff=FALSE)
        self.view = Menu(self.main_menu, tearoff=FALSE)
        self.color_theme = Menu(self.main_menu, tearoff=FALSE)

        self.main_menu.add_cascade(label="File", menu=self.file)
        self.main_menu.add_cascade(label="Edit", menu=self.edit)
        self.main_menu.add_cascade(label="View", menu=self.view)
        self.main_menu.add_cascade(label="Color Theme", menu=self.color_theme)
        self.root.config(menu=self.main_menu)

    def set_file_sub_menu(self):
        self.file.add_command(label="New", command=self.new_file, image=self.new_icon, compound=LEFT,
                              accelerator='Ctrl+N')
        self.file.add_command(label="Open", command=self.open_file, image=self.open_icon, compound=LEFT,
                              accelerator='Ctrl+O')
        self.file.add_command(label="Save", command=self.save, image=self.save_icon, compound=LEFT,
                              accelerator='Ctrl+S')
        self.file.add_command(label="Save as", command=self.save_as, image=self.save_as_icon, compound=LEFT,
                              accelerator='Ctrl+S')
        self.file.add_command(label="Exit", command=self.exit_func, image=self.exit_icon, compound=LEFT,
                              accelerator='Ctrl+Q')
    def set_edit_sub_menu(self):
        self.edit.add_command(label="Copy", command=lambda : self.text_editor.event_generate("<<Copy>>"), image=self.copy_icon, compound=LEFT,
                              accelerator='Ctrl+C')
        self.edit.add_command(label="Cut", command=lambda : self.text_editor.event_generate("<<Cut>>"), image=self.cut_icon, compound=LEFT,
                              accelerator='Ctrl+X')
        self.edit.add_command(label="Paste", command=lambda : self.text_editor.event_generate("<<Paste>>"), image=self.paste_icon, compound=LEFT,
                              accelerator='Ctrl+V')
        self.edit.add_command(label="Clear All", command=lambda : self.text_editor.delete(1.0,END), image=self.clear_all_icon, compound=LEFT,
                              accelerator='Alt+X')
        self.edit.add_command(label="Find", command=self.find_func, image=self.find_icon, compound=LEFT,
                              accelerator='Ctrl+F')
    def set_view_sub_menu(self):
        self.view.add_checkbutton(label="Tool Bar",image=self.tool_bar_icon,onvalue=True,offvalue=False,
                                  variable=self.show_toolbar,compound=LEFT,command=self.hide_toolbar)
        self.view.add_checkbutton(label="Status Bar", image=self.status_bar_icon, onvalue=True, offvalue=False,
                                  variable=self.show_statusbar, compound=LEFT, command=self.hide_statusbar)

    def set_color_theme_sub_menu(self):
        self.count = 0
        self.theme_choice = StringVar()
        self.color_icons = (self.light_default_icon,self.light_plus_icon,self.dark_icon,self.red_icon,self.monokai_icon,self.night_blue_icon)
        self.color_dict = {
            'Light Default' : ('#000000' , '#ffffff'),
            'Light Plus' : ('#474747' , '#e0e0e0'),
            'Dark' : ("#c4c4c4" , "#2d2d2d"),
            'Red' : ("#2d2d2d" , "#ffe8e8"),
            'Monokai' : ("#d3b774" , "#474747"),
            'Night Blue' : ("#ededed", "#6b9dc2")
        }
        for i in self.color_dict:
            self.color_theme.add_radiobutton(label = i, image =self.color_icons[self.count],variable = self.theme_choice,compound = LEFT,command = self.change_theme)
            self.count+=1


    def change_theme(self):
        theme = self.theme_choice.get()
        colors = self.color_dict[theme]
        self.text_editor.config(bg = colors[0],foreground = colors[1])



    def hide_toolbar(self):
        if self.show_toolbar:
            self.tool_bar.pack_forget()
            self.show_toolbar = False
        else:
            self.text_editor.pack_forget()
            self.status_bar.pack_forget()
            self.tool_bar.pack(side=TOP,fill=X)
            self.text_editor.pack(fill=BOTH,expand=True)
            self.status_bar.pack(side=BOTTOM)
            self.show_toolbar= True

    def hide_statusbar(self):

        if self.show_statusbar:
            self.status_bar.pack_forget()
            self.show_statusbar = False
        else:
            self.status_bar.pack(side=BOTTOM)
            self.show_statusbar = True

    def set_canvas(self):
        self.text_editor = Text(self.root)
        self.text_editor.config(wrap='word', relief=FLAT)
        self.text_editor.focus_set()
        self.scroll_bar = Scrollbar(self.root)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.text_editor.pack(fill=BOTH, expand=True)
        self.scroll_bar.config(command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=self.scroll_bar.set)
        self.text_changed = False
        self.text_editor.bind("<<Modified>>",self.changed)

    def set_status_bar(self):
        self.status_bar = Label(self.root, text='Status Bar')
        self.status_bar.pack(side=BOTTOM)


    def set_file_menu_event_bindings(self):
        self.root.bind("<Control-N>", self.new_file)
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-O>", self.open_file)
        self.root.bind("<Control-s>", self.save)
        self.root.bind("<Control-S>", self.save)
        self.root.bind("<Alt-s>", self.save_as)
        self.root.bind("<Alt-S>", self.save_as)
        self.root.bind("<Control-q>", self.exit_func)
        self.root.bind("<Control-Q>", self.exit_func)

    def set_view_menu_event_bindings(self):
        self.root.bind("<Control-F>", self.find_func)
        self.root.bind("<Control-f>", self.find_func)
        self.root.bind("<Alt-X>", lambda e : self.text_editor.delete(1.0,END))
        self.root.bind("<Alt-x>", lambda e : self.text_editor.delete(1.0,END))
    def set_tool_bar(self):
        self.tool_bar=ttk.Label(self.root)
        self.tool_bar.pack(side=TOP,fill=X)

        ##font Box
        self.font_tuple=font.families()
        self.font_family=StringVar()
        self.font_box=ttk.Combobox(self.tool_bar,width=30,textvariable=self.font_family,state='readonly')
        self.font_box['values']=self.font_tuple
        self.font_box.current(self.font_tuple.index('Arial'))
        self.font_box.grid(row=0,column=0,padx=5)

        ##Size box
        self.size_var=IntVar()
        self.font_size=ttk.Combobox(self.tool_bar,width=14,textvariable=self.size_var,state='readonly')
        self.font_size['values']=tuple(range(8,81))
        self.font_size.current(4)
        self.font_size.grid(row=0,column=1,padx=5)

        ##Bold button
        self.bold_icon=PhotoImage(file='icons/bold.png')
        self.bold_btn=ttk.Button(self.tool_bar,image=self.bold_icon)
        self.bold_btn.grid(row=0,column=2,padx=5)


        ##Itallic button
        self.italic_icon=PhotoImage(file='icons/italic.png')
        self.italic_btn = ttk.Button(self.tool_bar, image=self.italic_icon)
        self.italic_btn.grid(row=0, column=3, padx=5)

        ##underline button
        self.underline_icon = PhotoImage(file='icons/underline.png')
        self.underline_btn = ttk.Button(self.tool_bar, image=self.underline_icon)
        self.underline_btn.grid(row=0, column=4, padx=5)

        ##font_color button
        self.font_color_icon = PhotoImage(file='icons/font_color.png')
        self.font_color_btn = ttk.Button(self.tool_bar, image=self.font_color_icon)
        self.font_color_btn.grid(row=0, column=5, padx=5)

        ##align left
        self.align_left_icon = PhotoImage(file='icons/align_left.png')
        self.align_left_btn = ttk.Button(self.tool_bar, image=self.align_left_icon)
        self.align_left_btn.grid(row=0, column=6, padx=5)

        ##align center
        self.align_center_icon = PhotoImage(file='icons/align_center.png')
        self.align_center_btn = ttk.Button(self.tool_bar, image=self.align_center_icon)
        self.align_center_btn.grid(row=0, column=7, padx=5)

        ##align right
        self.align_right_icon = PhotoImage(file='icons/align_right.png')
        self.align_right_btn = ttk.Button(self.tool_bar, image=self.align_right_icon)
        self.align_right_btn.grid(row=0, column=8, padx=5)

        ##mike button
        self.mike_icon = PhotoImage(file='icons/cut.png')
        self.mike_btn = ttk.Button(self.tool_bar, image=self.mike_icon)
        self.mike_btn.grid(row=0, column=9, padx=5)

    def set_tool_bar_event_bindings(self):
        self.font_box.bind("<<ComboboxSelected>>", self.change_font)
        self.font_size.bind("<<ComboboxSelected>>", self.change_fontsize)

        self.bold_btn.config(command=self.change_bold)
        self.italic_btn.config(command=self.change_italic)
        self.underline_btn.config(command=self.change_underline)
        self.font_color_btn.config(command=self.change_font_color)
        self.align_left_btn.config(command=self.change_align_left)
        self.align_center_btn.config(command=self.change_align_center)
        self.align_right_btn.config(command=self.change_align_right)
        self.mike_btn.config(command=self.saySomething)

    def change_font(self, event):
        font_name = self.font_family.get()
        self.my_font.config(family=font_name)
        self.text_editor['font'] = self.my_font


    def change_fontsize(self, event):
        fsize = self.size_var.get()
        self.my_font.config(size=fsize)
        self.text_editor['font'] = self.my_font


    def change_bold(self):
        if self.b_count == False:
            self.my_font.config(weight='bold')
            self.b_count = True
        else:
            self.my_font.config(weight='normal')
            self.b_count = False
        self.text_editor['font'] = self.my_font

    def change_italic(self):
        if self.i_count == False:
            self.my_font.config(slant='italic')
            self.i_count = True
        else:
            self.my_font.config(slant='roman')
            self.i_count = False
        self.text_editor['font'] = self.my_font



    def change_underline(self):
        if self.u_count==False:
            self.my_font.config(underline=1)
            self.u_count=True
        else:
            self.my_font.config(underline=0)
            self.u_count=False
        self.text_editor['font'] = self.my_font


    def change_font_color(self):
        color=colorchooser.askcolor(title="Select Color",color='black')
        if type(color[0]) is tuple:
            self.text_editor.config(foreground=color[1])
        else:
            messagebox.showinfo("Color Selection","You didn't select any color")

    def change_align_left(self):
        print("aman")
        text_content=self.text_editor.get(1.0,END)
        self.text_editor.tag_config('left',justify=LEFT)
        self.text_editor.delete(1.0,END)
        self.text_editor.insert(INSERT,text_content,'left')


    def change_align_center(self):
        text_content=self.text_editor.get(1.0,END)
        self.text_editor.tag_config('center',justify=CENTER)
        self.text_editor.delete(1.0,END)
        self.text_editor.insert(1.0,text_content,'center')


    def change_align_right(self):
        text_content=self.text_editor.get(1.0,END)
        self.text_editor.tag_config('right',justify=RIGHT)
        self.text_editor.delete(1.0,END)
        self.text_editor.insert(1.0,text_content,'right')

    def new_file(self,event=None):
        self.url==""
        self.text_editor.delete(1.0,END)
        self.root.title("My NotePad")


    def open_file(self,event=0):
        try:
            self.open_dialog()
            self.msg,self.base=self.control.read_file(self.url)
            self.text_editor.delete(1.0, END)
            self.text_editor.insert(END,self.msg)
            self.root.title(self.base)
            self.text_editor.edit_modified(False)
        except FileNotFoundError:
            messagebox.showerror("Error!","please select a file to open")
            print(traceback.format_exc())
    def open_dialog(self):
        self.url=filedialog.askopenfilename(title="Select File",filetypes=[("text Documents","*.*")])

    def save(self,event=None):
        try:
            content=self.text_editor.get(1.0,"end-1c")
            if self.url=="":
                self.save_dialog()
                self.control.save_file(content,self.url)
                self.text_changed=False
            else:
                self.control.save_file(content,self.url)
                self.text_changed=False
        except Exception:
            messagebox.showerror("Error!","Please Select a file to Save")
            print(traceback.format_exc())
    def save_as(self,event=None):
        try:
            content=self.text_editor.get(1.0,"end-1c")
            self.save_dialog()
            self.control.save_as(content,self.url)
            self.text_changed=False
        except Exception:
            messagebox.showerror("!Error","Please Select File to save As")
            print (traceback.format_exc())


    def save_dialog(self):
        self.url=filedialog.asksaveasfile(mode="w",filetypes=[("All Files","*.*"),("Text documents","*.txt*")],defaultextension=".ntxt")

    def find_func(self,event=None):
        ##find Ui
        self.find_dialogue=Toplevel()
        self.find_dialogue.geometry("450x250+500+200")
        self.find_dialogue.title("Find")
        self.find_dialogue.resizable(0,0)

        ##frame
        self.find_frame=ttk.LabelFrame(self.find_dialogue,text="Find/Replace")
        self.find_frame.pack(pady=20)

        ## labels
        self.text_find_label=ttk.Label(self.find_frame,text="Find : ")
        self.text_replace_label = ttk.Label(self.find_frame, text="Replace : ")

        ## Entry
        self.find_input=ttk.Entry(self.find_frame,width=30)
        self.replace_input = ttk.Entry(self.find_frame, width=30)

        ##Button
        self.find_button=ttk.Button(self.find_frame,text="FIND",command=self.find)
        self.replace_button = ttk.Button(self.find_frame, text="REPLACE", command=self.replace)

        ## label grid
        self.text_find_label.grid(row=0,column=0,padx=4,pady=4)
        self.text_replace_label.grid(row=1, column=0, padx=4, pady=4)

        ## entry grid
        self.find_input.grid(row=0,column=1,padx=4,pady=4)
        self.replace_input.grid(row=1, column=1, padx=4, pady=4)

        ##button grid
        self.find_button.grid(row=2,column=0,padx=8,pady=4)
        self.replace_button.grid(row=2, column=1, padx=8, pady=4)

        self.find_dialogue.mainloop()


    def find(self):
        str=self.find_input.get()
        self.text_editor.tag_remove('match','1.0',END)
        matches=0
        if str:
            start_pos='1.0'
            while True:
                start_pos=self.text_editor.search(str,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos=f'{start_pos}+{len(str)}c'
                print(start_pos,end_pos)
                self.text_editor.tag_add('match',start_pos,end_pos)
                matches+=1
                start_pos=end_pos
                self.text_editor.tag_config('match',foreground='red',background='yellow')
        if matches:
            messagebox.showinfo("Word Count",f"{str} occurs {matches} times")

    def replace(self):
        word=self.find_input.get()
        rep=self.replace_input.get()
        content=self.text_editor.get(1.0,END)
        self.text_editor.delete(1.0,END)
        content=content.replace(word,rep)
        self.text_editor.insert(1.0,content)


    def saySomething(self):
        #messagebox.showinfo("make sure u have connect your mic","Say something")
        try:
            self.takeAudio=self.control.saysomething()
            if self.takeAudio == "":
                messagebox.showinfo("Say Again","Speech not recognized")
            elif self.takeAudio == "open file":
                self.open_file()
            elif self.takeAudio == "save file":
                self.save_as()
            elif self.takeAudio == "new file":
                self.new_file()
            elif self.takeAudio == 'file save':
                self.save_as()
            elif self.takeAudio == 'text bold':
                self.change_bold()
            elif self.takeAudio == 'text italic':
                self.change_italic()
            elif self.takeAudio == 'search':
                self.find_func()
            elif self.takeAudio == 'hide statusbar':
                self.hide_statusbar()
            elif self.takeAudio == 'hide toolbar':
                self.hide_toolbar()
            else:
                messagebox.showerror("Say Again","audio not matched")
        except Exception:
            messagebox.showerror("ERROR!!!","Some Problem in device")
            print(traceback.format_exc())






    def exit_func(self,event=None):
        answer = messagebox.askyesno("APP CLOSING!!!", "Do you really want to quit?")
        if answer == False:
            return
        try:
            if self.url=="":
                if len(self.text_editor.get(1.0,"end-1c"))==0:
                    self.text_changed=False
            if self.text_changed:
                mbox=messagebox.askyesnocancel("WARNING!!","Do you want to save the file?")
                if mbox==True:
                    content=self.text_editor.get(1.0,"end-1c")
                    if self.url=="":
                        self.save_dialog()
                        self.control.save_file(content,self.url)
                    else:
                        self.control.save_file(content,self.url)
            messagebox.showinfo("Have a good day","Thankyou for using \"MyNotepad\" ")
            self.root.destroy()
        except:
            messagebox.showerror("ERROR!","Please select a file to save")
            print(traceback.format_exc())

    def changed(self,e):
        words=len(self.text_editor.get(1.0,END).split())
        characters=len(self.text_editor.get(1.0,"end-1c"))
        self.status_bar.config(text=f"Characters : {characters} words : {words}")
        if self.text_editor.edit_modified():
            self.text_changed=True
        self.text_editor.edit_modified(False)

    def run(self):
        self.root.mainloop()
root=Tk()
obj=View(root)
obj.run()