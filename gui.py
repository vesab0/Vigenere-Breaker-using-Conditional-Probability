import tkinter as tk
from tkinter import messagebox
import random

import decrypt as vc
import encrypt as ve

EXAMPLES = [
    "Mathematics is the language in which the universe is written. Without understanding its grammar, we are forever lost in a foreign land, unable to read the signs around us or speak with precision about the world.",

    "Computer science is not just about writing code. It is about thinking clearly, breaking problems into smaller pieces, and building solutions that are elegant, efficient, and correct. Every algorithm is a small act of logic and creativity.",

    "UBT University in Prishtina has shaped a generation of engineers and computer scientists in Kosovo. Walking through its halls you feel the energy of people who genuinely believe that technology can transform a country.",

    "Discrete mathematics is the backbone of computer science. Graphs, sets, relations, combinatorics, and number theory are not abstract toys. They are the tools that let us reason about networks, algorithms, databases, and cryptography.",

    "The Euclidean algorithm is one of the oldest algorithms known to humanity, yet it remains one of the most elegant. With nothing more than repeated division, it finds the greatest common divisor of two numbers in logarithmic time.",

    "Kosovo has a young population hungry for knowledge and opportunity. Every student who learns to program, to think algorithmically, to build software, adds another brick to the foundation of a modern digital economy.",

    "Graph theory began with Euler walking across the bridges of Konigsberg and asking a simple question. From that single puzzle grew an entire mathematical field that now underpins the internet, social networks, and logistics.",

    "Cryptography is the art of keeping secrets in plain sight. A well designed cipher transforms meaningful text into apparent noise, and only those who hold the key can reverse the transformation and read what was hidden.",

    "Algorithms are everywhere. When you search for a route, sort a list, compress an image, or recommend a video, an algorithm is making decisions at machine speed. Understanding them is understanding how the modern world actually works.",

    "The beauty of mathematics lies not in computation but in proof. A proof does not merely show that something is true for a million cases. It shows that it must be true for all cases, forever, with absolute certainty.",

    "UBT is not just a university. For many students in Kosovo it is the place where abstract curiosity becomes concrete skill, where someone who grew up playing video games discovers they can actually build one from scratch.",

    "Combinatorics teaches us to count without counting. Instead of listing every possibility, we find the pattern, the formula, the closed form that collapses infinite cases into a single expression. That is the real magic of mathematics.",

    "A good software engineer is not the one who writes the most code but the one who writes the least code necessary. Simplicity, clarity, and correctness are harder to achieve than complexity, and far more valuable in the long run.",

    "The Vigenere cipher was considered unbreakable for centuries. It took the index of coincidence, a statistical insight about letter frequency, to finally crack it. Even strong secrets leave patterns for those who know how to look.",

    "Every time you compile code and it works on the first try, you feel a small miracle has occurred. Every time it does not, you learn something. Either way, programming is an endless dialogue between intention and reality.",
]

BG      = "#f8f8f6"
SURFACE = "#ffffff"
BORDER  = "#d8d8d4"
FG      = "#1a1a1a"
FG_DIM  = "#909088"
ACCENT2 = "#d4d4d0"
RED     = "#b03020"
BLUE    = "#1d6fa4"
MONO    = ("Courier New", 11)


def field(parent, height=4, width=78, readonly=False):
    t = tk.Text(parent, height=height, width=width,
                font=MONO, relief="flat",
                bg=SURFACE if not readonly else "#f4f4f2",
                fg=FG, insertbackground=FG,
                bd=0, highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor="#999",
                wrap="word")
    if readonly:
        t.config(state="disabled")
    return t


def lbl(parent, text, bold=False, dim=False, size=10):
    font = ("Georgia", size, "bold" if bold else "normal")
    fg   = FG_DIM if dim else FG
    return tk.Label(parent, text=text, font=font, bg=BG, fg=fg)


def sep(parent):
    tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", pady=12)


def btn(parent, text, command):
    return tk.Button(parent, text=text,
                     font=("Georgia", 10),
                     relief="groove",
                     bg="#eae9e6", fg=FG,
                     activebackground="#d8d7d4",
                     activeforeground=FG,
                     cursor="hand2",
                     padx=14, pady=3,
                     command=command)
class DecryptTab:
    def __init__(self, frame):
        frame.configure(bg=BG, padx=20, pady=16)

        lbl(frame, "Ciphertext", bold=True).pack(anchor="w")

        self.input_txt = field(frame, height=4)
        self.input_txt.pack(fill="x", pady=(0, 10))

        btn(frame, "Crack", self.run_attack).pack(anchor="w", pady=(0, 16))

        sep(frame)

        res = tk.Frame(frame, bg=BG)
        res.pack(fill="x")

        def row(r, text, color):
            lbl(res, text, bold=True).grid(row=r, column=0, sticky="w", pady=5)
            v = tk.Label(res, text="—", font=("Courier New", 13, "bold"),
                         fg=color, bg=BG)
            v.grid(row=r, column=1, sticky="w", padx=16)
            return v

        self.lbl_period = row(0, "Key length", RED)
        self.lbl_key    = row(1, "Key",        BLUE)

        lbl(res, "Plaintext", bold=True).grid(row=2, column=0, sticky="nw", pady=5)
        self.txt_plain = field(res, height=5, width=60, readonly=True)
        self.txt_plain.grid(row=2, column=1, sticky="w", padx=16, pady=4)

    def run_attack(self):
        raw        = self.input_txt.get("1.0", "end-1c")
        ciphertext = vc.clean(raw)

        if len(ciphertext) < 20:
            messagebox.showerror("Too short",
                                 "Ciphertext must be at least 20 letters.")
            return

        self.txt_plain.config(state="normal")
        self.txt_plain.delete("1.0", "end")

        best_k, _ = vc.estimate_period(ciphertext)
        self.lbl_period.config(text=str(best_k))

        key, plaintext = vc.crack_vigenere(ciphertext, best_k)

        self.lbl_key.config(text=key)
        self.txt_plain.insert("1.0", plaintext)
        self.txt_plain.config(state="disabled")


class EncryptTab:
    def __init__(self, frame):
        frame.configure(bg=BG, padx=20, pady=16)

        top_row = tk.Frame(frame, bg=BG)
        top_row.pack(fill="x")
        lbl(top_row, "Plaintext", bold=True).pack(side="left", anchor="w")
        btn(top_row, "Random example", self.fill_random).pack(side="left", padx=(12, 0), pady=(0,8))

        self.txt_plain = field(frame, height=4)
        self.txt_plain.pack(fill="x", pady=(0, 12))

        lbl(frame, "Key", bold=True).pack(anchor="w")
        lbl(frame, "Letters only, no spaces",
            dim=True, size=9).pack(anchor="w", pady=(2, 6))

        self.txt_key = field(frame, height=1)
        self.txt_key.pack(fill="x", pady=(0, 10))

        btn(frame, "Encrypt", self.run_encrypt).pack(anchor="w", pady=(0, 16))

        sep(frame)

        res = tk.Frame(frame, bg=BG)
        res.pack(fill="x")

        lbl(res, "Key (cleaned)", bold=True).grid(row=0, column=0, sticky="w", pady=5)
        self.lbl_key_clean = tk.Label(res, text="—",
                                      font=("Courier New", 13, "bold"),
                                      fg=BLUE, bg=BG)
        self.lbl_key_clean.grid(row=0, column=1, sticky="w", padx=16)

        lbl(res, "Ciphertext", bold=True).grid(row=1, column=0, sticky="nw", pady=5)
        self.txt_cipher = field(res, height=5, width=60, readonly=True)
        self.txt_cipher.grid(row=1, column=1, sticky="w", padx=16, pady=4)

        btn(res, "Copy", self.copy_cipher).grid(
            row=2, column=1, sticky="w", padx=16, pady=(0, 4))

    def fill_random(self):
        self.txt_plain.delete("1.0", "end")
        self.txt_plain.insert("1.0", random.choice(EXAMPLES))

    def run_encrypt(self):
        plaintext = self.txt_plain.get("1.0", "end-1c")
        key_raw   = self.txt_key.get("1.0", "end-1c")

        key = ve.clean(key_raw)
        if not key:
            messagebox.showerror("No key", "Please enter a key.")
            return

        if not ve.clean(plaintext):
            messagebox.showerror("No text", "Please enter some plaintext.")
            return

        result = ve.encrypt_vigenere(plaintext, key)
        if result is None:
            return

        self.lbl_key_clean.config(text=key)
        self.txt_cipher.config(state="normal")
        self.txt_cipher.delete("1.0", "end")
        self.txt_cipher.insert("1.0", result)
        self.txt_cipher.config(state="disabled")

    def copy_cipher(self):
        self.txt_cipher.config(state="normal")
        text = self.txt_cipher.get("1.0", "end-1c")
        self.txt_cipher.config(state="disabled")
        if text:
            self.txt_cipher.clipboard_clear()
            self.txt_cipher.clipboard_append(text)


class App:
    def __init__(self, root):
        self.root = root
        root.title("Vigenère")
        root.configure(bg=BG)
        root.resizable(False, False)

        header = tk.Frame(root, bg=BG, padx=24, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="Vigenère Cipher",
                 font=("Georgia", 17, "bold"), bg=BG, fg=FG).pack(anchor="w")
        tk.Label(header, text="Encrypt plaintext or crack ciphertext",
                 font=("Georgia", 9), bg=BG, fg=FG_DIM).pack(anchor="w", pady=(2, 0))

        tk.Frame(root, height=1, bg=BORDER).pack(fill="x")

        tab_bar = tk.Frame(root, bg=BG, padx=24)
        tab_bar.pack(fill="x")

        self.tab_content = tk.Frame(root, bg=BG)
        self.tab_content.pack(fill="both", expand=True)

        self.frames   = {}
        self.tab_btns = {}

        for name in ("Encrypt", "Crack"):
            f = tk.Frame(self.tab_content, bg=BG)
            self.frames[name] = f

        EncryptTab(self.frames["Encrypt"])
        DecryptTab(self.frames["Crack"])

        for name in ("Encrypt", "Crack"):
            b = tk.Label(tab_bar, text=name,
                         font=("Georgia", 10),
                         bg=BG, fg=FG_DIM,
                         padx=4, pady=10,
                         cursor="hand2")
            b.pack(side="left", padx=(0, 20))
            b.bind("<Button-1>", lambda e, n=name: self.switch(n))
            self.tab_btns[name] = b

        self.switch("Encrypt")

    def switch(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

        for n, b in self.tab_btns.items():
            if n == name:
                b.config(fg=FG, font=("Georgia", 10, "bold"))
            else:
                b.config(fg=FG_DIM, font=("Georgia", 10))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()