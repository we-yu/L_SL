# coding: UTF-8
import sys
import tkinter as tk
import tkinter.messagebox as tkm # メッセージボックスに使用
import random
import PIL.ImageTk as pilimgtk
import PIL.Image as pilimg

# https://nnahito.gitbooks.io/tkinter/content/

WINDOW_WIDTH  = 400
WINDOW_HEIGHT = 800

def SetLabels(tk) :
    # Label text
    static1 = tk.Label(text=u'message A')
    static1.pack()

    # Label text with color
    static1 = tk.Label(text=u'message B', foreground='#FF0000')
    static1.pack()

    # Label text with color, background color
    static1 = tk.Label(text=u'message C', foreground='#FF0000', background='#90CAF9')
    static1.pack()

    # Label at specify place
    Static1 = tk.Label(text=u'test', foreground='#ff0000', background='#ffaacc')
    Static1.place(x=150, y=228)

    return

def SetEntry(tk) :
    # Set Entry
    Static1 = tk.Label(text=u'▼ This is Entry ▼')
    Static1.pack()
    Entry1 = tk.Entry()
    Entry1.pack()

    # Entry with Initial text
    Static1 = tk.Label(text=u'▼ This is Entry with Initial text ▼')
    Static1.pack()
    Entry1 = tk.Entry()
    Entry1.insert(tk.END, u'いろはにほへと')
    Entry1.pack()

    # Entry with Width
    Static1 = tk.Label(text=u'▼ This is Entry with specificated width ▼')
    Static1.pack()
    Entry1 = tk.Entry(width=50)
    Entry1.insert(tk.END, u'This is Width=50 Entry')
    Entry1.pack()

    # Get value from Entry
    Entry1_value = Entry1.get()
    print(Entry1_value)

    # Delete value from Entry
    Entry1.delete(0, tk.END)

    return

def DeleteEntry(ent1) :
    ent1.delete(0, tk.END)
    return

def SetButtion(tk) :

    Static1 = tk.Label(text=u'▼ Entry ▼')
    Static1.pack()

    Entry1 = tk.Entry(width=50)
    Entry1.insert(tk.END, u'Init msg')
    Entry1.pack()

    # Place button
    Button1 = tk.Button(text=u'No Action')
    Button1.pack()

    # Button with size
    Button1 = tk.Button(text=u'Size Change', width=50)
    Button1.pack()

    # Button for Erase
    Button1 = tk.Button(text=u'Erase', width=30)
    # Button1.bind("<Button-1>", DeleteEntry)
    Button1.bind("<Button-1>", lambda event, a=Entry1:DeleteEntry(a))
    Button1.pack()

    return

def ShowMessage(text) :
    tkm.showinfo('info', text)
    return

def SetDialog(tk) :
    Static1 = tk.Label(text=u'▼ Entry ▼')
    Static1.pack()

    Entry1 = tk.Entry(width=50)
    Entry1.insert(tk.END, u'取得メッセージ！')
    Entry1.pack()

    # Buttonを設置してみる
    Button1 = tk.Button(text=u'MessageBox Button', width=50,
                        command=lambda: ShowMessage(Entry1.get()))  # 関数に引数を渡す場合は、commandオプションとlambda式を使う
    Button1.pack()

    # 普通のダイアログ
    tkm.showinfo('Information', 'Informative Message')
    # ワーニングなダイアログ
    tkm.showwarning('Warning', 'Warning Message')
    # エラーな感じのダイアログ
    tkm.showerror('Error', 'Error Dialog')
    # tkm.showwarning('Error', 'Error Dialog', type=tkm.YESNOCANCEL)
    # # YES/NOなダイアログ（YESがクリックされたら戻り値がtrue、NOならfalse）
    # tkm.askyesno('ダイアログのタイトル', 'YES/NOなダイアログ')
    # # リトライキャンセルダイアログ（リトライがクリックされたら戻り値がtrue、キャンセルならfalse）
    # tkm.askretrycancel('ダイアログのタイトル', 'リトライキャンセルダイアログ')
    # # OK/NOダイアログ（リトライがクリックされたら戻り値が'yes'、キャンセルなら'no'）
    # tkm.askquestion('ダイアログのタイトル', 'OK/NOダイアログ')
    # # OK/CANCELダイアログ（OKがクリックされたら戻り値がtrue、キャンセルならfalse
    # tkm.askokcancel('ダイアログのタイトル', 'OK/CANCELダイアログ')

    return

def AddToList(tgtList, text) :
    tgtList.insert(tk.END, text)
    return

def DeleteFromList(tgtList, tgtLine) :
    selectedIndex = tgtLine
    tgtList.delete(selectedIndex)
    return

def SetListBox(tk) :
    Static1 = tk.Label(text=u'▼ Entry ▼')
    Static1.pack()

    Entry1 = tk.Entry(width=50)
    Entry1.insert(tk.END, u'取得メッセージ！')
    Entry1.pack()

    # Put ListBox
    ListBox1 = tk.Listbox()
    ListBox1.pack()

    # ListBox Size Change
    ListBox2 = tk.Listbox(width=55, height=15)
    ListBox2.pack()

    # Get text from Entry, Then insert to ListBox
    Button1 = tk.Button(text=u'Get&Add Text', width=50,
                        command=lambda: AddToList(ListBox2, Entry1.get()))  # 関数に引数を渡す場合は、commandオプションとlambda式を使う
    Button1.pack()

    Button2 = tk.Button(text=u'Remove Text', width=50,
                        command=lambda: DeleteFromList(ListBox2, tk.ACTIVE))  # 関数に引数を渡す場合は、commandオプションとlambda式を使う
    Button2.pack()

    return

def DrawOnCanvas(canv) :
    canv.create_rectangle(random.randint(0, 300), random.randint(0, 200), random.randint(0, 400), random.randint(0, 250),
                          tag="rectangle", fill='green', outline='#00f')
    return

def EraseOnCanvas(canv) :
    canv.delete("rectangle")
    return

def SetCanvas(tk, rt) :
    # Canvas Area
    canvas = tk.Canvas(rt, width = WINDOW_WIDTH, height = WINDOW_HEIGHT)
    canvas.place(x = 0, y = 0)

    # Create Filled Square (Filled by Green, Outline border is Red)
    canvas.create_rectangle(5, 5, 20, 20, fill = 'green', outline = 'red')

    button_draw = tk.Button(rt, text=u'Draw Square', width = 15, command=lambda : DrawOnCanvas(canvas))
    # button_draw.bind("<Button-1>", lambda : DrawOnCanvas(canvas))
    button_draw.place(x=50, y=260)

    button_draw = tk.Button(rt, text=u'Erase', width = 15, command=lambda : EraseOnCanvas(canvas))
    # button_draw.bind("<Button-1>", lambda : EraseOnCanvas(canvas))
    button_draw.place(x=200, y=260)


    return


class TkGraphic() :
    def SetGraphic(self, tk, rt) :
        self.cv = tk.Canvas(rt, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='white')
        # cv.create_rectangle(5, 5, 20, 20, fill = 'green', outline = 'red')
        self.cv.pack()

        filepath = '/Users/yuji/Documents/python/L_SL/img/landscape-559434_640.jpg'
        img = pilimg.open(filepath)
        self.tkimg = pilimgtk.PhotoImage(img)

        self.cv.create_image(100, 100, image=self.tkimg)
        return

def SetGraphic(tk, rt) :

    cv = tk.Canvas(rt, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg='white')
    # cv.create_rectangle(5, 5, 20, 20, fill = 'green', outline = 'red')
    cv.pack()

    filepath = '/Users/yuji/Documents/python/L_SL/img/landscape-559434_640.jpg'
    img = pilimg.open(filepath)
    tkimg = pilimgtk.PhotoImage(img)

    cv.create_image(100, 100, image = tkimg)

    return

root = tk.Tk()

# Set Window title
root.title(u'PyWindow')

# Window-size change
geometorySet = str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT)
root.geometry(geometorySet)

# Labels -----------------------------
# SetLabels(tk)

# Entries ----------------------------
# SetEntry(tk)

# Buttons ----------------------------
# SetButtion(tk)

# Dialog (Modal messagebox) ----------
# SetDialog(tk)

# ListBox ----------------------------
# SetListBox(tk)

# Canvas -----------------------------
# SetCanvas(tk, root)

# Show Graphic -----------------------
tkg = TkGraphic()
tkg.SetGraphic(tk, root)

root.mainloop()

