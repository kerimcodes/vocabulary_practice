import tkinter as tk 
from tkinter import ttk
import random 
import utils

asked_words = []
wrong_answers = []

words = [word["Word"] for word in utils.listing()]
def studying(window):
    current_word = None
    def ask():
        global asked_words,words,current_word
        label_control.config(text="")
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
        global current_word,wrong_answers
        data = entry.get().lower().strip()
        if data:
            listes = utils.listing()
            for list in listes:
                if list["Word"] == current_word:
                    turkihes = [x.strip() for x in list["Turkish"].lower().split(",")]
                    user_words = [x.strip() for x in data.split(",")]

                    if all(word in turkihes for word in user_words):
                        label_control.config(
                            text=f"Congratulations, It's True! -> {list['Turkish']}",
                            background="yellow"
                        )
                    else:
                        label_control.config(
                            text=f"Unfortunately wrong...\nThe truth is {list['Turkish']}",
                            background="red")
                        wrong_answers.append(current_word)
                        if len(wrong_answers) == 10:
                            ask_btn.config(state="disabled")
                    entry.delete(0, tk.END)
        else:
            label_control.config(text="The Turkish of the word has not been written")

    def listing():
        new_top = tk.Toplevel(top)
        new_top.title("incorrect answers")
        for i,wrong in enumerate(wrong_answers,start=1):
            tk.Label(new_top,text=f"{i}- {wrong}").pack()
        
        ask_btn.config(state="normal")

        new_top.mainloop()

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

    listing_btn = ttk.Button(frame,text="Listing the incorrect answers",command=listing)
    listing_btn.grid(row=1,column=3,padx=0)

    top.mainloop()