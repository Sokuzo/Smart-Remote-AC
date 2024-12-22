#Import library
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import threading

#Import module
import remote
import soundPlayer
import time
import energy
import faceDetection
import speechRecognition
import timerDialog
import timerDialog2

windowOpen = True
fps = 30
index = 0
lastGraphUpdate = time.time()

#-------------------------------SUBPROGRAM----------------------------------------
def on_button_power(): #Fungsi tombol power
    if remote.myRemote.menyala:
        remote.myRemote.matikanAC()
        print("AC MATI")
    else:
        remote.myRemote.nyalakanAC()
        print("AC NYALA")
    threading.Thread(target=soundPlayer.soundBeep).start()

def on_button_suhuNaik(): #Fungsi suhu naik
    remote.myRemote.naikSuhu()
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()

def on_button_suhuTurun(): #Fungsi suhu turun
    remote.myRemote.turunSuhu()
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()

def on_button_satuan(): #Fungsi ubah satuan
    remote.myRemote.ubahSatuan()
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()

def on_button_mode(): #Fungsi ubah mode
    remote.myRemote.ubahMode()
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()

def on_button_fan(): #Fungsi ubah fan
    remote.myRemote.ubahFan()
    switchFanImage(remote.myRemote.fan)
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()

def on_button_swing(): #Fungsi ubah swing
    remote.myRemote.toggleSwing()
    switchSwingImage()
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()

def on_button_timer(): #Fungsi nyalakan/matikan timer durasi
    if remote.myRemote.timerMenyala: #Matikan timer durasi
        remote.myRemote.timerMenyala = False
        threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()
    else: #Nyalakan timer durasi
        dialog = timerDialog.TimerDialog(app)
        dialog.grab_set()

def on_button_timer2(): #Fungsi nyalakan/matikan timer waktu
    if remote.myRemote.timerMenyala: #Matikan timer waktu
        remote.myRemote.timerMenyala = False
        threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()
    else: #Nyalakan timer waktu
        dialog = timerDialog2.TimerDialog(app)
        dialog.grab_set()

def on_button_face(): #Fungsi nyalakan/matikan face detection
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()
    if faceDetection.faceOn: #Matikan face detection
        faceDetection.faceOn = False
    else: #Nyalakan face detection
        faceDetection.faceOn = True

def on_button_speech(): #Fungsi nyalakan/matikan speech recognition
    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()
    if speechRecognition.speechOn: #Matikan speech recognition
        speechRecognition.speechOn = False
    else: #Nyalakan speech recognition
        speechRecognition.speechOn = True

def on_option_selected(choice): #Meng-update gambar dan fungsi saat mengubah tombol custom
    global index

    threading.Thread(target=soundPlayer.soundBeep, daemon=True).start()

    #Ubah pilihan tombol custom
    selected_index = options.index(choice)
    index = selected_index


    # Update gambar tombol
    images = [image_timer, image_timer, image_face, image_speech]
    canvasTimer.itemconfig(clockImage, image=images[selected_index])
    canvasTimer.update()

def on_button_special(event): #Fungsi untuk tombol custom, menyesuaikan option yang dipilih
    functions = [on_button_timer, on_button_timer2, on_button_face, on_button_speech]
    functions[index]()

def on_enter(event): #Mengubah warna tombol saat mouse meng-hover icon
    canvasTimer.itemconfig(circle, fill="orange")

def on_leave(event): #Mengubah warna tombol saat mouse meng-hover icon
    canvasTimer.itemconfig(circle, fill="white")

def update(): #Fungsi yang mengupdate tampilan GUI setiap frame
    global lastGraphUpdate

    while windowOpen:
        time.sleep(1/fps)

        #---------------------Set satuan AC----------------------
        satuan = ""
        if remote.myRemote.satuan == "Fahrenheit":
            satuan = "F"
        else:
            satuan = "C"

        #----------------------Set status AC-------------------
        status = "OFF"
        if remote.myRemote.menyala:
            status = "ON"

        #-------------------------Update timer--------------------
        sisaTimer = 0

        if remote.myRemote.timerMenyala:
            sisaTimer = remote.myRemote.timerDurasi - (time.time() - remote.myRemote.timerWaktuStart)
            #Update UI ring timer
            angle = (max(0, sisaTimer)/remote.myRemote.timerDurasi) * 360
            canvasTimer.itemconfig(ring, extent=angle)
        else:
            canvasTimer.itemconfig(ring, extent=0)

        #Jika timer habis
        if (remote.myRemote.timerMenyala) and (sisaTimer < 0):
            remote.myRemote.matikanAC()
            remote.myRemote.matikanTimer()
            canvasTimer.itemconfig(ring, extent=0)
            threading.Thread(target=soundPlayer.soundTimer, daemon=True).start()
            sisaTimer = 0

        #----------------Cek apakah ada wajah terdeteksi------------
        if faceDetection.faceOn:
            canvasTimer.itemconfig(ring, extent=359.9)
            if faceDetection.faceDetected:
                remote.myRemote.nyalakanAC()
            else:
                remote.myRemote.matikanAC()

        #----------------Cek apakah speech recognition menyala-------------
        if speechRecognition.speechOn:
            canvasTimer.itemconfig(ring, extent=359.9)

        #----------------Update graph pada menu energy--------------
        if (time.time() - lastGraphUpdate) > energy.delay:
            lastGraphUpdate = time.time()

            #Masukkan data baru
            new_point = energy.total_pemakaian
            data_points.append(new_point)

            #Jika data melebihi data maksimum, hapus data awal
            if len(data_points) > max_points:
                data_points.pop(0)

            #Atur range vertikal data
            min_y = min(data_points)
            max_y = max(data_points)
            y_range = max_y - min_y if max_y != min_y else 5
            canvasGraph.delete("all")

            #Gambar graph baru
            for i in range(1, len(data_points)):
                scaled_y1 = (data_points[i-1] - min_y) / y_range * (canvasGraph.winfo_height() - 20)
                scaled_y2 = (data_points[i] - min_y) / y_range * (canvasGraph.winfo_height() - 20)
                
                canvasGraph.create_line(
                    (i-1) * x_offset, canvasGraph.winfo_height() - scaled_y1, 
                    i * x_offset, canvasGraph.winfo_height() - scaled_y2, 
                    fill="orange", width=6
                )

        #----------------Update variabel-variabel pada display-------------------
        suhuText.set(f"{remote.myRemote.suhu} °{satuan}")
        modeText.set(str(remote.modeList[remote.myRemote.mode]))
        ubahSatuanText.set(f"Ubah satuan (°{satuan})")
        energyText.set(f"{energy.total_pemakaian:.1f}")
        statusText.set(status)

        try:
            faceDetection.delay = int(entryDelayVar.get())
        except:
            pass

def load_png_image(png_path, width, height): #Fungsi untuk load gambar dari file
    image = Image.open(png_path)                                        #Buka file gambar
    image = image.resize((width, height), Image.Resampling.LANCZOS)     #Atur ukuran file gambar
    return ImageTk.PhotoImage(image)

def switchTab(tab):
    for frame in tabs: #Hapus menu saat ini
        frame.grid_forget()

    for frame in tabs:
        if frame == tab: #Pindah ke menu tab
            frame.grid(row=0, column=0, sticky="nsew")
            break

def switchFanImage(speed): #Ubah gambar kecepatan fan
    labelFan.configure(image=images_fan[speed])

def switchSwingImage(): #Ubah gambar swing
    if remote.myRemote.swing == False:
        labelSwing.configure(image=empty_image)
    else:
        labelSwing.configure(image=image_swing)

def runGUI():

    #--------------------------------------------VARIABEL GLOBAL---------------------------------------
    global suhuText
    global modeText
    global ubahSatuanText
    global energyText
    global statusText

    global windowOpen
    global tabs
    global app
    global button_energy
    global button_home
    global button_settings
    global labelFan
    global labelSwing
    global clockImage

    global images_fan
    global empty_image
    global image_swing
    global canvasTimer
    global ring
    global circle
    global options

    global image_timer
    global image_face
    global image_speech
    global image_home
    global selected_option
    global data_points, x_offset, canvasGraph, max_points
    global entryDelayVar

    windowOpen = True
    
    #--------------------------------------------JALANKAN WINDOW------------------------------------

    app = ctk.CTk()
    app.title("Smart AC Remote")
    app.geometry("480x800")

    #Set grid
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=0)
    app.grid_columnconfigure(0, weight=0)

    #Set satuan AC saat ini
    satuan = "C"
    if remote.myRemote.satuan == "Fahrenheit":
        satuan = "F"

    #------------------------------------STRING VAR-----------------------------------------------------

    suhuText = ctk.StringVar(value="20")
    modeText = ctk.StringVar(value=str(remote.modeList[remote.myRemote.mode]))
    ubahSatuanText = ctk.StringVar(value=f"Ubah satuan (°{satuan})")
    energyText = ctk.StringVar(value="0")
    statusText = ctk.StringVar(value="OFF")

    #--------------------------------------------IMAGES-------------------------------------------

    #Load semua gambar yang diperlukan
    image_power = load_png_image("Image/power.png", 50, 50)
    image_energy = load_png_image("Image/energy.png", 50, 50)
    image_settings = load_png_image("Image/settings.png", 50, 50)
    image_home = load_png_image("Image/home.png", 70,70)
    image_fanLogo = load_png_image("Image/fan.png", 50, 50)
    image_swing = load_png_image("Image/swing.png", 50, 50)
    image_timer = load_png_image("Image/timer.png", 40, 40)
    image_face = load_png_image("Image/face.png", 50, 50)
    image_speech = load_png_image("Image/speech.png", 60, 60)
    empty_image = load_png_image("Image/empty.png", 50, 50)

    images_fan = []
    for i in range(remote.fanMax + 1):
        if i == 0:
            images_fan.append(empty_image)
        else:
            images_fan.append(load_png_image(f"Image/fan/fan_{i}.png", 50, 50))
    
    #-----------------------------------------------FONTS----------------------------------------

    #Buat variabel untuk setiap font
    custom_font = ctk.CTkFont(family="Gotham", size=30)
    font_kecil = ctk.CTkFont(family="Gotham", size=15)
    font_suhu = ctk.CTkFont(family="Gotham Black", size=120)
    font_plus_minus = ctk.CTkFont(family="Gotham Black", size=70)

    #------------------------------------------------FRAME----------------------------------------

    #Buat frame untuk setiap menu
    tabs = []

    frame_home = ctk.CTkFrame(app, 480, 600)
    frame_energy = ctk.CTkFrame(app, 480, 600)
    frame_settings = ctk.CTkFrame(app, 480, 600)

    tabs.append(frame_home)
    tabs.append(frame_energy)
    tabs.append(frame_settings)

    #----------------------------------------------FRAME HOME-------------------------------------

    #Tombol power
    button_power = ctk.CTkButton(
        frame_home,
        image=image_power,
        text="",
        command=on_button_power,
        width=100,
        height=100,
        corner_radius=20,
        fg_color="white",
        hover_color="orange"
    )

    # Tombol naikkan suhu
    button_suhuNaik = ctk.CTkButton(
        frame_home,
        text="+",  
        command=on_button_suhuNaik,  
        width=100,  
        height=100,  
        corner_radius=20,  
        fg_color="transparent",  
        hover_color="orange",  
        font = font_plus_minus
    )

    # Tombol turunkan suhu
    button_suhuTurun = ctk.CTkButton(
        frame_home,
        text="-",  
        command=on_button_suhuTurun,  
        width=100,  
        height=100,  
        corner_radius=20,  
        fg_color="transparent",  
        hover_color="orange",  
        font = font_plus_minus
    )

    # Tombol ubah mode
    button_mode = ctk.CTkButton(
        frame_home,
        text="MODE",  
        command=on_button_mode,  
        width=80,  
        height=80,  
        corner_radius=5,  
        fg_color="white",  
        hover_color="orange",  
        font = font_kecil,
        text_color="black"
    )

    # Tombol ubah fan
    button_fan = ctk.CTkButton(
        frame_home,
        text="",
        image=image_fanLogo,  
        command=on_button_fan,  
        width=80,  
        height=80,  
        corner_radius=5,  
        fg_color="white",  
        hover_color="orange",  
        font = font_kecil
    )

    # Tombol ubah swing
    button_swing = ctk.CTkButton(
        frame_home,
        text="SWING",
        image=None,  
        command=on_button_swing,  
        width=80,  
        height=80,  
        corner_radius=5,  
        fg_color="white",  
        hover_color="orange",  # 
        font = font_kecil,
        text_color="black"
    )

    #Tombol custom (Timer, Face, Speech)
    canvasTimer = ctk.CTkCanvas(frame_home, width=100, height=100, bg="#2B2B2B", highlightthickness=0)
    canvasTimer.place(relx=0.8, rely=0.9, anchor="center")
    circle = canvasTimer.create_oval(10, 10, 90, 90, fill="white", outline="")
    clockImage = canvasTimer.create_image(50, 50, image=image_timer)
    canvasTimer.tag_bind(clockImage, "<Button-1>", on_button_special)
    canvasTimer.tag_bind(circle, "<Button-1>", on_button_special)
    canvasTimer.tag_bind(circle, "<Enter>", on_enter)  # Mouse enters
    canvasTimer.tag_bind(circle, "<Leave>", on_leave)  # Mouse leaves
    canvasTimer.tag_bind(clockImage, "<Enter>", on_enter)  # Mouse enters
    canvasTimer.tag_bind(clockImage, "<Leave>", on_leave)  # Mouse leaves
    ring = canvasTimer.create_arc(10, 10, 90, 90, start=90, extent=0, outline="#FFA500", width=5, style=tk.ARC)

    #Letakkan tombol
    button_power.place(relx=0.5, rely=0.85, anchor="center")
    button_suhuNaik.place(relx=0.7, rely=0.55, anchor="center")
    button_suhuTurun.place(relx=0.3, rely=0.55, anchor="center")
    button_mode.place(relx=0.2, rely=0.75, anchor="center")
    button_swing.place(relx=0.2, rely=0.9, anchor="center")
    button_fan.place(relx=0.8, rely=0.75, anchor="center")

    #Buat label
    labelSuhu = ctk.CTkLabel(frame_home, textvariable=suhuText, font=font_suhu)
    labelMode = ctk.CTkLabel(frame_home, textvariable = modeText, font=custom_font)
    labelFan = ctk.CTkLabel(frame_home, text="", font=custom_font)
    labelSwing = ctk.CTkLabel(frame_home, text="", font=custom_font)
    labelTitle = ctk.CTkLabel(frame_home, text="HOME", font=custom_font)
    labelStatus = ctk.CTkLabel(frame_home, textvariable=statusText, font=custom_font)

    #Letakkan label
    labelSuhu.place(relx=0.5, rely=0.25, anchor="center")
    labelStatus.place(relx=0.5, rely=0.1, anchor = "center")
    labelMode.place(relx=0.24, rely=0.37, anchor="center")
    labelSwing.place(relx=0.5, rely=0.37, anchor="center")
    labelFan.place(relx=0.76, rely=0.37, anchor="center")
    labelTitle.place(relx=0.5, rely=0.05, anchor="center")

    #----------------------------------------------------------------------------------------

    #-------------------------------------------FRAME ENERGY---------------------------------

    #Buat label
    label = ctk.CTkLabel(frame_energy, text="ENERGY", font=custom_font)
    labelEnergy = ctk.CTkLabel(frame_energy, textvariable=energyText, font=font_suhu)
    labelKWH = ctk.CTkLabel(frame_energy, text="KWH", font=custom_font)

    #Letakkan label
    label.place(relx=0.5, rely=0.05, anchor="center")
    labelEnergy.place(relx=0.5, rely=0.2, anchor="center")
    labelKWH.place(relx=0.5, rely=0.3, anchor="center")

    #Graph energy
    canvasGraph = ctk.CTkCanvas(frame_energy, width=400, height=400, bg="#2B2B2B")
    canvasGraph.place(relx=0.5, rely=0.675, anchor="center")
    data_points = []
    max_points = 50 
    x_offset = 10 

    #---------------------------------------------------------------------------------------
    
    #-------------------------------------------FRAME SETTINGS---------------------------------

    #Buat label
    label = ctk.CTkLabel(frame_settings, text="SETTINGS", font=custom_font)
    labelDelay = ctk.CTkLabel(frame_settings, text="Durasi delay face detection (dalam detik):", font=font_kecil)
    labelDropdown = ctk.CTkLabel(frame_settings, text="Ubah tombol custom:", font=font_kecil)

    #Letakkan label
    label.place(relx=0.5, rely=0.05, anchor="center")
    labelDelay.place(relx=0.5, rely=0.35, anchor="center")
    labelDropdown.place(relx=0.5, rely=0.55, anchor="center")

    #Buat entry
    entryDelayVar = ctk.StringVar(value="5")
    entryDelay = ctk.CTkEntry(frame_settings, textvariable=entryDelayVar)
    entryDelay.place(relx=0.5, rely=0.4, anchor="center")

    #Tombol untuk mengubah satuan remote AC
    button_satuan = ctk.CTkButton(
        frame_settings,
        textvariable= ubahSatuanText,  # Button text
        command=on_button_satuan,  # Function to call on button click
        width=100,  # Button width 
        height=100,  # Button height
        corner_radius=20,  # Rounded corners
        fg_color="white",  # Button color
        hover_color="orange",  # Hover effect color
        font=font_kecil,
        text_color="black"
    )
    button_satuan.place(relx=0.5, rely=0.2, anchor="center")

    #Dropdown untuk mengubah tombol custom
    options = ["Timer Durasi", "Timer Waktu", "Face Detection", "Speech Recognition"]
    selected_option = ctk.StringVar(value=options[0])  # Default value
    dropdown = ctk.CTkComboBox(frame_settings, values=options, variable=selected_option, command=on_option_selected)
    dropdown.place(relx=0.5, rely=0.6, anchor="center")

    #---------------------------------------------------------------------------------------

    #-----------------------------TAB BUTTONS------------------------------------------------

    #Buat frame untuk tombol menu
    buttons = ctk.CTkFrame(app)

    #Letakkan tombol pada bawah layar
    buttons.grid(row=1,column=0)
    buttons.grid_rowconfigure(0, weight=1)

    #Tomobl menu energy
    button_energy = ctk.CTkButton(
        buttons,
        text="",
        image=image_energy,
        fg_color="white",  
        hover_color="lightblue",  
        command=lambda: switchTab(frame_energy)
        )
    
    #Tombol menu home
    button_home = ctk.CTkButton(
        buttons,
        text="",
        image=image_home,
        fg_color="white",  
        hover_color="lightblue",  
        command=lambda: switchTab(frame_home)
        )
    
    #Tombol menu settings
    button_settings = ctk.CTkButton(
        buttons,
        text="",
        image=image_settings,
        fg_color="white",  
        hover_color="lightblue", 
        command=lambda: switchTab(frame_settings)
        )

    #Atur menu default sebagai menu home
    frame_home.grid(row=0, column=0, sticky="nsew")

    #Atur posisi tombol menu
    button_energy.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    button_home.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    button_settings.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    #Jalankan aplikasi
    switchFanImage(remote.myRemote.fan)
    tUpdate = threading.Thread(target=update,daemon=True)
    tUpdate.start()
    app.mainloop()