import tkinter as tk 
from tkinter import ttk
import random 
import utils

asked_words = []
wordss = utils.listing()
words = [word["Word"] for word in wordss]
def studying(window):
    current_word = None
    def ask():
        global asked_words,words,current_word
        while True:
            asked = random.choice(words)
            if len(asked_words) == 10:
                asked_words.pop(-1)
            if asked in asked_words:
                continue
            else:
                label_ask.config(text=f"Word: {asked}")
                asked_words.insert(0,asked)
                break
        current_word = asked    
    def control():
        global current_word
        data = entry.get().capitalize()
        if data:
            listes = utils.listing()
            for list in listes:
                if list["Word"] == current_word:
                    turkihes = list["Turkish"].strip().split(",")
                    if data in turkihes:
                        label_control.config(text=f"Congrulations,It's True! ->{list['Turkish']}",background="yellow")
                    else:
                        label_control.config(text="Unfortunately wrong...\n" \
                        f"The truth is {list['Turkish']}"
                        ,background="red")
                    entry.delete(0,tk.END)
        else:
            label_control.config(text="the turkish of word had not written")

    top = tk.Toplevel(window)

    frame = ttk.Frame(top)
    frame.pack(anchor="center")

    alt_frame = ttk.Frame(top)
    alt_frame.pack(anchor="center")

    label_ask = ttk.Label(frame,text="Let's start!",font=("Arial",10))
    label_ask.grid(row=0,column=0)
    label_control = ttk.Label(alt_frame,text="",font=("Arial",10))
    label_control.grid(row=2,column=0)

    entry = ttk.Entry(frame)
    entry.grid(row=0,column=1,padx=2,)

    ask_btn = ttk.Button(frame,text="Ask",command=ask)
    ask_btn.grid(row=1,column=0,padx=2)

    control_btn = ttk.Button(frame,text="Control",command=control)
    control_btn.grid(row=1,column=1,padx=2)

    top.mainloop()