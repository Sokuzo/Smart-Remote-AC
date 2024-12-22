
#Import library
import os
import threading

#Import module
import speechRecognition
import faceDetection
import script_gui
import energy


'''
Penjelasan Script:
main.py                     Program utama yang dijalankan
remote.py                   Tempat dimana data remote AC disimpan
script_gui.py               Program yang menjalankan GUI
faceDetection.py            Program yang menjalankan pendeteksi wajah
speechRecognition.py        Program yang menjalankan pendeteksi suara
soundPlay.py                Program yang menjalankan pemutaran suara/audio
energy.py                   Program yang menghitung konsumsi energi
'''

#---------------------------------------PROGRAM UTAMA-----------------------------------------------

if __name__ == "__main__":
    os.system("cls") #Bersihkan terminal

    #Inisialisasi thread
    t1 = threading.Thread(target=faceDetection.startCam)                #Thread untuk menjalankan face detection
    t2 = threading.Thread(target=energy.run)                            #Thread untuk menjalankan perhitungan konsumsi energi
    t3 = threading.Thread(target=speechRecognition.listen_and_respond)  #Thread untuk menjalankan speech recognition

    #Mulai thread
    t1.start() 
    t2.start()
    t3.start()

    #Jalankan UI
    script_gui.runGUI()

#---------------------------------------------------------------------------------------------------