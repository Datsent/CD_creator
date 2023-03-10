import ctypes
import glob
import os
import shutil
import time
from tkinter import *
from tkinter import messagebox
from Utils.Utils import *
from datetime import datetime

def eject_disk():
    messagebox.showinfo('information', 'הצריבה הסתיימה ')
    time.sleep(3)
    ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None)

ws = Tk()
ws.title('CD-Creator')
ws.geometry('300x200')
width = 300
height = 150
x = int(ws.winfo_screenwidth() / 2 - width / 2)
y = int(ws.winfo_screenheight() / 2 - height / 2)
ws.geometry("+{}+{}".format(x, y))
ws.config(bg='#5FB691')

def format_cd(driver):
    os.system(f'cmd /c "format {driver}: /y"')

def copy_file(src, des):
    shutil.copy2(src, des)

def msg1():
    messagebox.showinfo('information', 'Hi! You got a prompt.')
    messagebox.showerror('error', 'Something went wrong!')
    messagebox.showwarning('warning', 'accept T&C')
    messagebox.askquestion('Ask Question', 'Do you want to continue?')
    messagebox.askokcancel('Ok Cancel', 'Are You sure?')
    messagebox.askyesno('Yes|No', 'Do you want to proceed?')
    messagebox.askretrycancel('retry', 'Failed! want to try again?')

def find_file(sn, wo):
    now = datetime.now()
    datetime_string = now.strftime("%d-%m-%Y %H:%M:%S")
    for folder in glob.glob(f'{DSC_PATH}\\*{wo}*\\CD*'):
        print(folder)
        if glob.glob(f'{DSC_PATH}\\*{wo}*\\CD*\\*{sn}*'):
            for file in glob.glob(f'{DSC_PATH}\\*{wo}*\\CD*\\*{sn}*'):
                print('Coping...')
                print(file)
                copy_file(file, f'{CD_LETTER}:\\')
                with open("Utils\\log.txt", "a") as file1:
                    file1.write(f"{datetime_string} - {file}\n")
        else:
            messagebox.showinfo('information', f' {sn} אין קבצים עבור מעגל:')
            with open("Utils\\log.txt", "a") as file1:
                file1.write(f"{datetime_string} - {wo} - {sn} - NOT FOUND\n")

def find_sn():

    with open(FILE, 'r') as file1:
        #file1 = open(FILE, 'r')
        Lines = file1.readlines()
        print(Lines[0].strip())
        if glob.glob(f'{DSC_PATH}\\*{Lines[0].strip()}*\\CD*'):
            for line in Lines[1:]:
                if line != '\n':
                    print(line.strip())
                    find_file(line.strip(), Lines[0].strip())

        else:
            messagebox.showinfo('information', f' {Lines[0].strip()} אין קבצים עבור פק"ע:')

def main():
    path = f'{CD_LETTER}:\\'
    format_cd(CD_LETTER)
    isExist = os.path.exists(path)
    print(isExist)
    while not os.path.exists(path):
        if messagebox.askquestion('Ask Question', 'No Disk, want try again?') == 'yes':
            format_cd(CD_LETTER)
        else:
            quit()
    find_sn()
    print('waiting...')
    print('ejecting...')
    eject_disk()

if __name__ == '__main__':
    main()
