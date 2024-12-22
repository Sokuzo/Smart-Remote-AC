#Import library
import time

#Import module
import script_gui
import remote

base_wattage = 0.1      #Dalam KWh
total_pemakaian = 0
delay = 0.1

def run():
    global total_pemakaian
    while script_gui.windowOpen:
        time.sleep(delay)

        #Lakukan perhitungan energi yang digunakan
        wattage = base_wattage

        #Sesuaikan penggunaan energi berdasarkan swing
        if remote.myRemote.swing:
            wattage += 0.05

        #Sesuaikan penggunaan energi berdasarkan suhu
        if remote.myRemote.satuan == "Celcius":
            wattage += (30 - remote.myRemote.suhu) * 0.005
        else:
            wattage += (30 - ((remote.myRemote.suhu - 32) / 1.8)) * 0.005

        #sesuaikan penggunaan energi berdasarkan fan
        wattage += 0.01 * remote.myRemote.fan

        #Tambahkan energi yang digunakan pada total energi
        if remote.myRemote.menyala:
            total_pemakaian += (wattage/10)