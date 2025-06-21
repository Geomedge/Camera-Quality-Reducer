# Theme Checker - SAU1.02
import os
import tkinter as tk
from tkinter import messagebox
import webbrowser
import json

sau_ver = 1.02
path = os.path.expanduser("~") + r"\Documents\Geomedge.inc"
path_2 = path + r"\Global-Theme.json"


#Very Important Variables!
try:
    title_font = ("Aptos", 18, "bold")
    default_font = ("Aptos", 12)
    credit_font = ("Aptos", 10)
except:
    title_font = ("Segoe UI", 18, "bold")
    default_font = ("Segoe UI", 11)
    credit_font = ("Segoe UI", 9)

default = {
    'font':default_font,
    'background':"#111",
    'foreground':"#FFF",
        }

button = {
    'font':default_font,
    'background':"#333",
    'foreground':"#FFF",
        }


combo = {
    'font':default_font,
    'background':"#111",
    'foreground':"#111",
    'width':40,
}

cred = {
    'font':credit_font,
    'bg':"#333",
    'fg':"#FFF",
}

scale = {
    'font':default_font,
    'bg':"#222",
    'fg':"#FFF",
    'highlightbackground':"#333",
    'troughcolor':"#333",
    'orient':"horizontal",
    'length':350,
    'width':15,
}

title = {
    'font':title_font,
    'bg':"#333",
    'fg':"#FFF",
}

window_ui = {
    'background':'#111',
    'fg':'#FFF',
}

#Checks

def check():
    #Check For Parent Folder
    folder_check = os.path.exists(path)
    if folder_check == True:
        print("Pass Program Folder!")
    else:
        os.mkdir(path)

    #Check For Theme File
    theme_check = os.path.exists(path_2) 
    if theme_check == True:
        print("Pass Theme File!")
    else:
        openfile = open(path_2, "w")
        json.dump([default, button, combo, cred, scale, title, window_ui], openfile)
        openfile.close()
    #JSON FILES 
    
    

def verify(ver):
    if ver != sau_ver:
        return "Error With Version!"
    else:
        return True



#Starting Modes - Default And Safe Mode

def start():
    c = 0
    openfile = open(path_2, "r")
    a = json.load(openfile)
    for item in a:
        c = c + 1
    if c != 6:
        print("Error, rebuilding")
        openfile = open(path_2, "w")
        json.dump([default, button, combo, cred, scale, title, window_ui], openfile)
        openfile = open(path_2, "r")
        a = json.load(openfile)
        openfile.close()
    return a

start()