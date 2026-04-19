import tkinter as tk
from tkinter import ttk
import pyperclip

# -----------------------------
# Arduino Snippet Komutları (Genişletilmiş)
# -----------------------------
CATEGORIES = {
    "Setup": {
        "Setup": "void setup() {\n    \n}",
        "Loop": "void loop() {\n    \n}",
        "Include Wire": "#include <Wire.h>",
        "Include SPI": "#include <SPI.h>",
        "Include Servo": "#include <Servo.h>",
        "Include EEPROM": "#include <EEPROM.h>"
    },
    "IO": {
        "pinMode": "pinMode(13, OUTPUT);",
        "digitalWrite HIGH": "digitalWrite(13, HIGH);",
        "digitalWrite LOW": "digitalWrite(13, LOW);",
        "digitalRead": "int val = digitalRead(2);",
        "analogRead": "int val = analogRead(A0);",
        "analogWrite": "analogWrite(9, 128);",
        "delay": "delay(1000);",
        "millis": "unsigned long t = millis();",
        "micros": "unsigned long t = micros();",
        "tone":"tone(pin,freqhz)",
        "tone2":"tone(pin,freqhz,duration_ms)",
        "noTone":"noTone(pin)"
    },
    "Serial": {
        "Serial.begin": "Serial.begin(300,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200);",
        "Serial.print": 'Serial.print("Mesaj");',
        "Serial.println": 'Serial.println("i ı İ ç ş ö ü ğ");',
        "Serial.available": "if (Serial.available()) {\n    \n}",
        "available":"int available()",
        "read":"int read()",
        "flush":"flush()",
        "print":"print()",
        "println":"println()",
        "write":"write()"
    },
    "Loops": {
        "if": "if (x == 1) {\n    \n}",
        "else": "else {\n    \n}",
        "for": "for (int i=0;i<10;i++) {\n    \n}",
        "while": "while (x < 10) {\n    \n}",
        "do while": "do {\n    \n} while(x<10);",
        "continue":"continue;",
        "return":"return x;",
        "goto":"goto",
        "switch":"switch(myvar){ case 1: break; case 2: break; default:}"
    },
    "Functions": {
        "Function": "void myFunction() {\n    \n}",
        "Return int": "int myFunction() {\n    return 0;\n}"
    },
    "Symbols": {
        "{ }": "{}",
        "[ ]": "[]",
        "( )": "()",
        "< >": "<>",
        ";": ";",
        ":": ":",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
        "=": "=",
        "==": "==",
        "!=": "!=",
        ">": ">",
        "<": "<",
        ">=": ">=",
        "<=": "<=",
        "++,+=,-=,*=,/=,&=,|=":"",
        " & and, | or, ~ not" :"",
        "&&(and),||(or),!(not)":"",
        "/*xx*/ multiline,// single":""
    },
    "Macros": {
        "#define": "#define LED 13",
        "#ifdef": "#ifdef DEBUG\n\n#endif",
        "#ifndef": "#ifndef MY_HEADER\n\n#endif",
        "#include": "#include <Arduino.h>"
    },
    "Extras": {
        "Servo attach": "myServo.attach(9);",
        "Servo write": "myServo.write(90);",
        "EEPROM write": "EEPROM.write(0, 123);",
        "EEPROM read": "int val = EEPROM.read(0);",
        "Reset Wacht Dog":" wdt_enable(WDTO_15MS); while (1) { }"  
    },
    "Conversion":{
        "char":"char()",
        "byte":"byte()",
        "int":"int()",
        "word":"word()",
        "long":"long()",
        "float":"float()"
    }
}

# -----------------------------
# Tkinter UI
# -----------------------------
root = tk.Tk()
root.title("Arduino Profesyonel Kod Klavyesi - Hafıza Tabanlı")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

btn_style = {"width": 25, "height": 3, "padx": 4, "pady": 4, "bg": "#3c3c3c", "fg": "white",
            "activebackground": "#2d2d2d", "activeforeground": "#00ffea", "font": ("Consolas", 11, "bold")}

# Hafızaya kopyalama
def copy_to_clipboard(text):
    pyperclip.copy(text)

# Her kategori için sekme ve butonlar
for cat_name, commands in CATEGORIES.items():
    frame = tk.Frame(notebook, bg="#1e1e1e")
    notebook.add(frame, text=cat_name)
    row, col = 0, 0
    for label, cmd in commands.items():
        def make_cmd(c=cmd):
            return lambda: copy_to_clipboard(c)
        tk.Button(frame, text=label, command=make_cmd(), **btn_style)\
            .grid(row=row, column=col, padx=6, pady=6)
        col += 1
        if col >= 3:
            col = 0
            row += 1

info = tk.Label(root, text="Butona tıkla → kod hafızaya alındı.\nİstediğin yere CTRL+V ile yapıştır.",
                fg="cyan", bg="#1e1e1e", font=("Consolas", 11))
info.pack(pady=6)

root.mainloop()
