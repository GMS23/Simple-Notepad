from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox    
from tkinter import filedialog
from tkfontchooser import askfont

opens = 0
files_path = ''
path = ''
font_size = 16
wrap_state = 0

root = Tk()
root.title("寄事本")
def read(path, mode, encoding='utf-8'):
    f = open(path, mode, encoding=encoding)
    return f.read()
def write(path, mode, str, encoding='utf-8'):
    f = open(path, mode, encoding=encoding)
    f.write(str)
    f.close()
def insert_photo():
    global photo
    photo = filedialog.askopenfilename()
    photo = photo.split()
    global path
    path = PhotoImage(file=photo[0])
    TXT.image_create(INSERT, image=path)
    
def new_files(event):
    global opens
    global opens
    global path
    c = TXT.get('1.0', 'end')
    print(c)
    if opens == 0:
        if c == '':
            TXT.delete('1.0', 'end')
        if c != '':
            static = messagebox.askyesnocancel("是否保存已编辑的文件?")
            if static:
                save_file(0)
                TXT.delete('1.0', 'end')
            if static == False:
                TXT.delete('1.0', 'end')
    if opens == 1:
        static = messagebox.askyesnocancel("是否保存已编辑的文件?")
        if static:
            write(path[0], "w+r", c)
        if static == False:
            TXT.delete('1.0', 'end')
    
def open_file(event):
    global files_path
    global opens
    global path
    c = TXT.get('1.0', 'end')
    if opens == 1 or c != "":
        static = messagebox.askyesnocancel("是否保存已编辑的文件?")
        if static:
            path = filedialog.asksaveasfilename()
            path = path.split()
            print(path)
            write(path[0], "w", c)
            TXT.delete('1.0', 'end')
        if static == False:
            TXT.delete('1.0', 'end')
            path = filedialog.askopenfilename()
            path = path.split()
            print(path)
            files_path = read(path[0], "r")
            print(files_path)
            opens = 1
            TXT.delete('1.0', 'end')
            TXT.insert('1.0', files_path)
            TXT.mark_set(INSERT, "1.0")
    else:
        path = filedialog.askopenfilename()
        path = path.split()
        print(path)
        files_path = read(path[0], "r")
        print(files_path)
        opens = 1
        TXT.delete('1.0', 'end')
        TXT.insert('1.0', files_path)
        TXT.mark_set(INSERT, "1.0")
def save_file(event):
    global files_path
    global opens
    global path
    c = TXT.get('1.0', 'end')
    if opens == 1:
        write(path[0], "w", c)
    else:
        path = filedialog.asksaveasfilename()
        path = path.split()
        print(path)
        write(path[0], "w", c)

def save_as_file(event):
    global files_path
    global opens
    global path
    c = TXT.get('1.0', 'end')
    path = filedialog.asksaveasfilename()
    path = path.split()
    print(path)
    write(path[0], "w", c)


def auto_wrap():
    global wrap_state
    if wrap_state == 0:
        wrap_state = 1
        TXT.configure(wrap='word')
    if wrap_state == 1:
        wrap_state = 0
        TXT.configure(wrap='none')
def font_chooser():
    font = askfont(root)
    if font:
        font['family'] = font['family'].replace(' ', '\ ')
        font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
        if font['underline']:
            font_str += ' underline'
        if font['overstrike']:
            font_str += ' overstrike'
        TXT.configure(font=font_str)
def about():
    messagebox.showinfo(1,"寄事本 1.0\n作者：qinch\n联系方式：BlueRect@outlook.com")


def undo():
    TXT.edit_undo()
root.bind("<Alt-n>", new_files)
root.bind("<Alt-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-Shift-s>", save_as_file)
root.bind("<Control-w>", auto_wrap)
root.bind("<Control-f>", font_chooser)
root.bind("<Control-a>", about)
menubar = Menu(root)
files_menu = Menu(menubar, tearoff=False)
files_menu.add_command(label="新建", accelerator='Alt+N', command=lambda: new_files(0))
files_menu.add_command(label="打开", accelerator='Alt+O', command=lambda: open_file(0))
files_menu.add_command(label="保存", accelerator='Ctrl+S', command=lambda: save_file(0))
files_menu.add_command(label="另存为", accelerator='Ctrl+Shift+S', command=lambda: save_as_file(0))
files_menu.add_separator()
files_menu.add_command(label="退出", command=root.destroy)
menubar.add_cascade(label="文件", menu=files_menu)

edit_menu = Menu(menubar, tearoff=False)
edit_menu.add_command(label="复制", accelerator='Ctrl+C', command=lambda: TXT.event_generate("<<Copy>>"))
edit_menu.add_command(label="粘贴", accelerator='Ctrl+V', command=lambda: TXT.event_generate("<<Paste>>"))
edit_menu.add_command(label="剪切", accelerator='Ctrl+X', command=lambda: TXT.event_generate("<<Cut>>"))
edit_menu.add_command(label="撤销", accelerator='Ctrl+Z', command=undo)
edit_menu.add_separator()
edit_menu.add_command(label="插入图片", command=insert_photo)
menubar.add_cascade(label="编辑", menu=edit_menu)

format_menu = Menu(menubar, tearoff=False)
format_menu.add_command(label="字体", command=font_chooser)
format_menu.add_command(label="自动换行", command=auto_wrap)
menubar.add_cascade(label="格式", menu=format_menu)


help_menu = Menu(menubar, tearoff=False)
help_menu.add_command(label="关于", command= about)
menubar.add_cascade(label="帮助", menu=help_menu)

root.config(menu=menubar)

TXT = Text(root, font=("微软雅黑", 16), relief="flat", undo=True, autoseparators=False)
TXT.focus()
TXT.pack(fill=BOTH, expand=YES)
root.mainloop()