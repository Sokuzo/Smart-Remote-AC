#Import library
import customtkinter as ctk
import tkinter as tk

#Import module
import remote
import soundPlayer
import threading

class TimerDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        #Buat menu dialog
        super().__init__(parent)
        self.geometry("300x150")
        self.title("Set Durasi Timer")

        self.label = ctk.CTkLabel(self, text="Masukkan durasi timer (dalam detik):")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start Timer", command=self.on_start)
        self.start_button.pack(pady=10)

    def on_start(self):
        duration = self.entry.get()
        if duration.isdigit():
            threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()
            remote.myRemote.nyalakanTimer(int(duration))
            self.destroy()
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Input tidak valid!!!")