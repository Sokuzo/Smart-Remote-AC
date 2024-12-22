#Import library
import customtkinter as ctk
import tkinter as tk
from datetime import datetime

#Import module
import threading
import soundPlayer
import remote

def time_difference_in_seconds(target_time_str):
    #Waktu sekarang
    now = datetime.now()
    
    #Ubah target_time_srt menjadi waktu
    target_time = datetime.strptime(target_time_str, "%H:%M:%S").time()
    
    #Hitung detik awal dan akhir timer
    current_seconds = now.hour * 3600 + now.minute * 60 + now.second
    target_seconds = target_time.hour * 3600 + target_time.minute * 60 + target_time.second
    
    #Hitung selisih waktu
    difference = target_seconds - current_seconds
    
    #Jika waktunya sudah terlewat, tambahkan 24 jam
    if difference < 0:
        difference += 86400

    return difference

class TimerDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        #Buat dialog timer
        super().__init__(parent)
        self.geometry("300x150")
        self.title("Pilih Waktu agar AC Mati")

        self.label = ctk.CTkLabel(self, text="Masukkan jam dalam format HH:MM:DD")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="Start Timer", command=self.on_start)
        self.start_button.pack(pady=10)

    def on_start(self):
        waktu = self.entry.get()

        if waktu: #Pastikan terdapat input
            try:
                #Pisahkan string menjadi jam, menit, dan detik, lalu pastikan valid
                hours, minutes, seconds = map(int, waktu.split(":"))
                
                #Cek apakah valid
                if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60: #Jika valid, jalankan timer
                    selisih_waktu = time_difference_in_seconds(waktu)
                    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()
                    remote.myRemote.nyalakanTimer(selisih_waktu)
                    self.destroy()
                else: #Jika tidak, beri peringatan
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, "Input tidak valid!!!")
            except ValueError:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "Input tidak valid!!!")
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Input tidak valid!!!")
