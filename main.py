import tkinter as tk 
from tkinter import ttk,messagebox
import json
import utils
import studying_vocabulary as study

def add():
    words = [word_dict["Word"] for word_dict in utils.listing()]
    word = word_entry.get().capitalize()
    meaning = meaning_entry.get().capitalize()
    turkish = turkish_entry.get().capitalize()
    example = example_entry.get().capitalize()
    
    if word and meaning and turkish and example:
        if word in words:
            messagebox.showwarning("Warning","There is word alrady in list")
        else:
            vocab = utils.add_json(word, meaning, turkish, example) 
            tree.insert("","end",values=(vocab["id"],vocab["Word"],vocab["Meaning"],vocab["Turkish"],vocab["Example"]))
        
        word_entry.delete(0,tk.END)
        meaning_entry.delete(0,tk.END)
        turkish_entry.delete(0,tk.END)
        example_entry.delete(0,tk.END)
    else:
        messagebox.showwarning("Warning","The boxes is empty")

def add_tree():
    words = utils.listing()
    for word in words:
        tree.insert("","end",values=(word["id"],word["Word"],word["Meaning"],word["Turkish"],word["Example"]))

def right_selection(event):
    selected = tree.selection()
    if selected:
        datas = tree.item(selected[0])["values"]
        word_entry.delete(0,tk.END)
        turkish_entry.delete(0,tk.END)
        meaning_entry.delete(0,tk.END)
        example_entry.delete(0,tk.END)
        word_entry.insert(0,datas[1])
        meaning_entry.insert(0,datas[2])
        turkish_entry.insert(0,datas[3])
        example_entry.insert(0,datas[4])

def double_selection(event):
    selected = tree.selection()
    if selected:
        data = tree.item(selected[0])["values"]
        top_level = tk.Toplevel(window)
        top_level.title("Word Review")

        word_label = ttk.Label(top_level,font=("Arial",10),text=f"Word: {data[1]}")
        meaning_label = ttk.Label(top_level,font=("Arial",10),text=f"Meaning: {data[2]}")
        turkish_label = ttk.Label(top_level,font=("Arial",10),text=f"Turkish: {data[3]}")
        example_label = ttk.Label(top_level,font=("Arial",10),text=f"Example: {data[4]}")

        word_label.pack()
        meaning_label.pack()
        turkish_label.pack()
        example_label.pack()

def update():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning","No word selected")
        return
    
    file = utils.file
    try:
        with open(file,"r",encoding="utf-8") as f:
            vocabularies = json.load(f)
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        vocabularies = []
        return 
    
    word = word_entry.get().capitalize()
    turkish = turkish_entry.get().capitalize()
    meaning = meaning_entry.get().capitalize()
    example = example_entry.get().capitalize()

    if not (word and turkish and meaning and example):
        messagebox.showerror("Error","Text boxes cannot be left empty")
        return
    
    old_data = tree.item(selected[0])["values"]
    old_id = int(old_data[0]) 

    for vocab in vocabularies:
        if vocab["id"] == old_id:
            vocab.update({
                "Word": word,
                "Meaning": meaning,
                "Turkish": turkish,
                "Example": example
            })
            break

    with open(file,"w",encoding="utf-8") as f:
        json.dump(vocabularies,f,ensure_ascii=False,indent=2)

    tree.delete(*tree.get_children())
    add_tree()
    word_entry.delete(0,tk.END)
    meaning_entry.delete(0,tk.END)
    turkish_entry.delete(0,tk.END)
    example_entry.delete(0,tk.END)

def search():
    data = search_entry.get()
    if data:
        words = [word for word in utils.listing()]
        tree.delete(*tree.get_children())
        isfound = False
        for word in words:
            if data in word["Word"].lower():
                tree.insert("","end",values=(word["id"],word["Word"],word["Meaning"],word["Turkish"],word["Example"]))
                isfound = True
        if not isfound:
            add_tree()
            messagebox.showwarning("Warning","Cannot results found")
            search_entry.delete(0,tk.END)
    else:
        tree.delete(*tree.get_children())
        add_tree()

def back(event):
    search_entry.delete(0,tk.END)
    tree.delete(*tree.get_children())
    add_tree()

def on_mousewheel(event):
    tree.yview_scroll(int(-1*(event.delta/120)), "units")

def on_return(event):
    if event.keysym == "Return":
        print("Bastın")
        word = word_entry.get()
        meaning = meaning_entry.get()
        turkish = turkish_entry.get()
        example = example_entry.get()
        data = search_entry.get()

        if data:
            search()
        elif word and meaning and turkish and example:
            add()

window = tk.Tk()
window.title("Home Page")

frame = ttk.Frame(window)
frame.pack(fill="x")

columns = ["id","word","meaning","turkish","example"]
tree = ttk.Treeview(frame,show="headings",columns=columns,height=25)
tree.pack(side="left",fill="both",expand=True)

for column in columns:
    if column != "id": 
        if column == "word":
            tree.heading(column,text= column.capitalize())
            tree.column(column=column,width=50,anchor="center")
        else:    
            tree.heading(column,text= column.capitalize())
            tree.column(column=column,width=150,anchor="center")
    else:
        tree.column(column, width=0, stretch=False)

scrollbar = ttk.Scrollbar(frame,command=tree.yview)
scrollbar.pack(side="right",fill="y")

tree.config(yscrollcommand=scrollbar.set)

alt_frame = ttk.Frame(window)
alt_frame.pack()

labels = [("Word:",0,0),("Meaning:",0,2),("Turkish:",0,4),("Example:",0,6),("Search:",1,4  )]

for label,r,c in labels:
    ttk.Label(alt_frame,text=label,font=("Arial",10)).grid(row=r,column=c,padx=3)

word_entry = ttk.Entry(alt_frame)
meaning_entry = ttk.Entry(alt_frame)
turkish_entry = ttk.Entry(alt_frame)
example_entry = ttk.Entry(alt_frame)
search_entry = ttk.Entry(alt_frame)

word_entry.grid(row=0,column=1,padx=3)
meaning_entry.grid(row=0,column=3,padx=3)
turkish_entry.grid(row=0,column=5,padx=3)
example_entry.grid(row=0,column=7,padx=3)
search_entry.grid(row=1,column=5)

add_btn = ttk.Button(alt_frame,text="Add",command=add)
update_btn = ttk.Button(alt_frame,text="Update",command=update)
start_to_asking = ttk.Button(alt_frame,text="Asking",command= lambda : study.studying(window))
search_btn = ttk.Button(alt_frame,text="Search",command=search)
back_btn = ttk.Button(alt_frame,text="Back",command=back)

add_btn.grid(row=0,column=8,padx=3)
update_btn.grid(row=0,column=9,padx=3)
start_to_asking.grid(row=0,column=10)
search_btn.grid(row=1,column=6)
back_btn.grid(row=1,column=7)

tree.bind("<Double-Button-1>",double_selection)
tree.bind("<Button-3>",right_selection)
tree.bind("<MouseWheel>",on_mousewheel)
window.bind_all("<Enter>",on_return)
window.bind("<Escape>",back)

add_tree()
window.mainloop()