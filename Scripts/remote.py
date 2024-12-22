import time

#Set beberapa nilai untuk AC
jumlahMode = 5
modeList = ["Auto", "Cool", "Dry ", "Fan ", "Heat"]
fanMax = 5

class remoteAC: #Buat class remoteAC

    def __init__(self): #Nilai default saat AC dinyalakan
        self.menyala = True
        self.suhu = 20
        self.satuan = "Celcius"
        self.mode = 0
        self.fan = 3
        self.swing = False
        self.timerMenyala = False
        self.timerDurasi = 0
        self.timerWaktuStart = 0

    def matikanAC(self): #Matikan AC
        self.menyala = False

    def nyalakanAC(self): #Nyalakan AC
        self.menyala = True

    def naikSuhu(self): #Naikkan suhu AC sebesar 1 satuan
        if self.satuan == "Celcius":
            self.suhu = min(self.suhu + 1, 30)
        else:
            self.suhu = min(self.suhu + 1, 86)

    def turunSuhu(self): #Turunkan suhu AC sebesar 1 satuan
        if self.satuan == "Celcius":
            self.suhu = max(self.suhu - 1, 16)
        else:
            self.suhu = max(self.suhu - 1, 61)

    def ubahSatuan(self): #Ubah satuan AC
        if self.satuan == "Celcius":
            self.satuan = "Fahrenheit"
            self.suhu = round((self.suhu * 1.8) + 32)
        else:
            self.satuan = "Celcius"
            self.suhu = round((self.suhu - 32) / 1.8)

    def ubahMode(self): #Ubah mode AC
        self.mode = (self.mode + 1) % jumlahMode

    def ubahFan(self): #Ubah fan speed AC
        self.fan = (self.fan + 1) % (fanMax + 1)

    def toggleSwing(self): #Toggle swing AC
        if self.swing:
            self.swing = False
        else:
            self.swing = True

    def nyalakanTimer(self, durasi): #Nyalakan timer AC
        self.timerMenyala = True
        self.timerDurasi = durasi
        self.timerWaktuStart = time.time()

    def matikanTimer(self): #Matikan timer AC
        self.timerMenyala = False
        self.timerDurasi = 0
        self.timerWaktuStart = 0

    def returnData(self):
        result = ""
        # Iterate over each attribute and print it
        for attr, value in vars(self).items():
            print(f"{attr}: {value}")
            result += f"{attr}: {value}\n"
        return result
    
myRemote = remoteAC() #Inisialisasi objek remoteAC