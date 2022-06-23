import re
from tkinter import Tk, StringVar, Label, Button, Entry
import tkinter as tk
from PIL import ImageTk, Image
from EIA96 import index, multipler

patterns = ('^\d{4}$', '^\d{3}$', '^[R]+\d{1,3}$', '^\d{,2}[R]\d{1,3}$',
            '^\d{2}[A-F H R-S X-Z]$', '^[0]$')

types = ('4digits', '3digits', 'R+digits', 'digitsRdigits',
         'EIA-96', 'zero')


def calculate(e=None):
    r_code = entry.get().upper().strip()
    entry.delete(0, tk.END)
    entry.insert(0, r_code)
    r_type = resistorCodeTypeCheker(r_code)
    if r_type is None:
        wrongResistorCode()
        return
    resistance = resistanceСalculate(r_type, r_code)
    if r_type == "EIA-96" and resistance == 0:
        wrongResistorCode()
        return
    resistance_value = unitAbbreviationsHandler(round(resistance, 3))
    r_label.configure(text='Resistance:')
    message_label.configure(text='Enter Resistor Code:', fg='black')
    output_label.configure(text=resistance_value, fg='black')


def clearEntry():
    entry.delete(0, tk.END)
    r_label.configure(text='')
    output_label.configure(text='')
    message_label.configure(text='Enter Resistor Code:', fg='black')


def unitAbbreviationsHandler(value):
    if value < 1000:
        answer = str(value) + " Ohms"
        return(answer)
    value = value/1000
    answer = str(value) + " kOhms"
    if value >= 1000:
        value = value/1000
        answer = str(value) + " MOhms"
    return(answer)


def entryMaxCharacters():
    entry.delete(4, tk.END)


def resistorCodeTypeCheker(r_code):
    for index, pattern in enumerate(patterns):
        if re.match(pattern, r_code):
            return types[index]


def wrongResistorCode():
    message_label.configure(text='Wrong Resistor Code!', fg='red')
    r_label.configure(text='')
    output_label.configure(text='')


def resistanceСalculate(r_type, r_code):
    match r_type:
        case '3digits':
            value = r_code[0] + r_code[1]
            power = r_code[2]
            resistance = int(value)*(10**int(power))
            return resistance
        case '4digits':
            value = r_code[0] + r_code[1] + r_code[2]
            power = r_code[3]
            resistance = int(value)*(10**int(power))
            return resistance
        case 'EIA-96':
            value = index[r_code[0] + r_code[1]]
            power = str(r_code[2])
            resistance = int(value)*multipler[power]
            return resistance
        case 'R+digits':
            value = r_code.replace('R', '.')
            resistance = "0" + str(value)
            return float(resistance)
        case 'digitsRdigits':
            value = r_code.replace('R', '.')
            return float(value)
        case 'zero':
            return 0


# Window elements initialization
main_window = Tk()
entry_text = StringVar()
main_window.resizable(0, 0)
main_window.minsize(300, 325)
r_label = Label(font=('Courier', 16))
main_window.bind('<Return>', calculate)
main_window.title("SMD Code Calculator")
ico = ImageTk.PhotoImage(Image.open("icon.ico"))
main_window.wm_iconphoto(False, ico)
output_label = Label(font=('Courier', 16), justify=tk.CENTER)
resistor_image = ImageTk.PhotoImage(Image.open("resistor.png"))
r_image = Label(image=resistor_image)
autor_label = Label(text='by CTL', font=('Courier', 8), fg='gray')
message_label = Label(text='Enter Resistor Code:', font=('Courier', 16))
clear_button = Button(text='Clear', font=('Courier', 16), command=clearEntry)
calc_button = Button(text='Calculate', font=('Courier', 16), command=calculate)
entry = Entry(font=('Courier', 21), width=4,  bg='black', fg='white',
              relief=tk.FLAT, textvariable=entry_text, justify=tk.CENTER)

# Window elements placement
clear_button.place(x=107, y=175)
message_label.place(x=18, y=10)
calc_button.place(x=82, y=125)
output_label.place(x=76, y=266)
r_image.place(x=101, y=50)
r_label.place(x=76, y=246)
autor_label.place(x=0, y=307)
entry.place(x=115, y=62)

entry_text.trace("w", lambda *args: entryMaxCharacters())
main_window.mainloop()
