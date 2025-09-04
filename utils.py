import os
import sys
import json
from tkinter import messagebox

def get_data_file():
    if getattr(sys, 'frozen', False):
        data_dir = r"C:\Users\lenovo\OneDrive\Ekler\data"
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_path, "data")
    
    os.makedirs(data_dir, exist_ok=True)  
    return os.path.join(data_dir, "vocabularies.json")

file = get_data_file()

def add_json(word, meaning, turkish, example):
    try:
        with open(file, "r", encoding="utf-8") as tobe_read:
            word_list = json.load(tobe_read)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        word_list = []

    if word_list:
        id = word_list[-1]["id"] + 1
    else:
        id = 1

    vocab = {"id": id, "Word": word, "Meaning": meaning, "Turkish": turkish, "Example": example}

    for word in word_list:
        if word["Word"] == vocab["Word"] and word["Turkish"] == vocab["Turkish"]:
            messagebox.showwarning("Warning", "There is already this word in list")
            return None

    word_list.append(vocab)
    with open(file, "w", encoding="utf-8") as tobe_written:
        json.dump(word_list, tobe_written, ensure_ascii=False, indent=2)

    return vocab

def listing():
    try:
        with open(file, "r", encoding="utf-8") as tobe_read:
            return json.load(tobe_read)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []