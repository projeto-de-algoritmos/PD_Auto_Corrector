from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from numpy import loadtxt
dictionary = loadtxt("Dicionario.txt", comments="#", unpack=False, dtype="str", encoding="utf8")
print (dictionary)
dictionary = list(set(dictionary))
i=0
thisfile=None

def set_input(value):
    text.delete(1.0, "END")
    text.insert("end-1c", value)

def get_words():
    words = text.get("1.0",END).split()
    print(words)

def editDistDP(str1, str2, m, n):
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1],
                                   dp[i-1][j],
                                   dp[i-1][j-1])
    return dp[m][n]

def Autocorrect(word):
    dists =  []
    for i in range(len(dictionary)):
        dists.append(editDistDP(word, dictionary[i], len(word), len(dictionary[i])))
    arr2 = sorted(dists)
    min_dist = arr2[0]
    for i in range(len(dists)):
        if min_dist == dists[i]:
            minpos=i
            break
    return dictionary[minpos]

def autocorrect():
    words = text.get("1.0",END).split()
    in_word = words[-1]
    
    out =Autocorrect(in_word)
    label.config(text = out)

def correctWord(event):
    words = text.get("1.0",END).split()
    if len(words)!=0:
        text.delete('1.0', END)
        for i in range(len(words)-1):
            text.insert("end-1c", words[i])
            text.insert("end-1c", " ")
        text.insert("end-1c", label.cget("text")+" ")

def checkSpelling(event):
    autocorrect()

def newLine(event):
    autocorrect()

def saveFile():
    global i
    if i==0:
        file = filedialog.asksaveasfile(initialdir="D:\\Main",
                                        defaultextension='.txt',
                                        filetypes=[
                                            ("Text file",".txt"),
                                            ("HTML file", ".html"),
                                            ("All files", ".*"),
                                        ])
        if file is None:
            return
        else:
            global thisfile
            thisfile = file
        filetext = str(text.get(1.0,END))
        file.write(filetext)
        i = i + 1
    else:
        currentFileSave()

def currentFileSave():
    global thisfile
    thisfile.truncate(0)
    filetext = str(text.get(1.0,END))
    thisfile.write(filetext)
    thisfile.close()

window = Tk()
window.title("Verificador de Ortografia")
def on_closing():
    if messagebox.askyesno("Sair", "Você deseja sair?"):
        global thisfile
        try:
            thisfile.close()
        except:
            pass
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

menubar = Menu(window)
window.config(menu=menubar)

fileMenu = Menu(menubar,tearoff=0,font=("Consolas",10))

label = Label(window,
              text="",
              font=('Arial',30,'bold'),
              fg='black',
              bg='white',
              relief="groove",
              bd=10,
              padx=10,
              pady=10,
              compound='bottom')
label.pack()
text = scrolledtext.ScrolledText(window,
            bg="white",
            font=("Consolas",25),
            height=10,
            width=30,
            padx=20,
            pady=20,
            fg="black",
            wrap=WORD)
text.pack()
button = Button(text='Salvar',command=saveFile)
button.pack()
window.bind('<KeyRelease>',checkSpelling)
window.bind("<Return>",newLine)
window.bind('<Insert>',correctWord)
window.mainloop()