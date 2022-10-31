from tkinter import *
import tkinter as tk
import threading
master = Tk(className=' Automata Auto-Run')
master.geometry("1024x600")
master.resizable(0,0)
photo = PhotoImage(file = "assets/logo_automata_bulat.png")
master.iconphoto(False, photo)
bg = PhotoImage(file = "assets/bg.png")
  
# Create Canvas
canvas = Canvas(master, width = 1024,
                 height = 600)
canvas.pack(fill = "both", expand = True)
canvas.create_image( 0, 0, image = bg, 
                     anchor = "nw")
widget = Label(canvas, text='Checking folder hasil deteksi ...', fg='white', bg='black', font=("Cursive", 12))
widget.place(x=333, y=389)
#widget.pack()
def on_closing():
    pass
def btn1():
    exec(open("testcam.py").read())
def btn2():
    exec(open("program-demo-python.py").read())
def btn3():
    exec(open("a.py").read())
def btn4():
    exec(open("a.py").read())
def exitWindow():
    master.quit()

class CanvasButton:
    def __init__(self, canvas, x, y, image_path, image_path2, command):
        x, y = canvas.canvasx(x), canvas.canvasy(y) # Convert window to canvas coords.
        self.btn_image = PhotoImage(file=image_path)
        self.btn_clicked_image = PhotoImage(file=image_path2)
        canvas_btn_img_obj = canvas.create_image(x, y, anchor='nw', image=self.btn_image, activeimage=self.btn_clicked_image)
        canvas.tag_bind(canvas_btn_img_obj, "<Button-1>", lambda event: command())

canvas_btn1 = CanvasButton(canvas, 333, 278, 
    'assets/Button_1.png', 
    'assets/Button_1ef.png', btn1)
canvas_btn2 = CanvasButton(canvas, 333, 334,   
    'assets/Button_2.png', 
    'assets/Button_2ef.png', btn2)
#canvas_btn3 = CanvasButton(canvas, 333, 389, 'assets/Button_3.png', 'assets/Button_3ef.png', btn3)
#canvas_btn4 = CanvasButton(canvas, 333, 444, 'assets/Button_4.png', 'assets/Button_4ef.png', btn4)
canvas_btnExit = CanvasButton(canvas, 582, 499, 
    'assets/Button_keluar.png', 
    'assets/Button_keluaref.png', exitWindow)

windowWidth = 1024
windowHeight = 600
# Gets both half the screen width/height and window width/height
positionRight = int(master.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(master.winfo_screenheight()/2 - windowHeight/2)
# Positions the window in the center of the page.
master.geometry("+{}+{}".format(positionRight, positionDown))
stop_threads = False
class autoUpload (threading.Thread):
    def run(self):
        from ftplib import FTP
        import mysql.connector
        import os
        import time
        import shutil
        from datetime import datetime
        from urllib.request import urlopen
        def internet_on():
            try:
                urlopen('https://google.com', timeout=1)
                return True
            except:
                return False
        global widget
        def while1():
            while (internet_on()):
                global widget
                global stop_threads
                widget.config(text="Alat terhubung dengan Internet.")
                timerCount = 0
                lenFiles = 0
                #HOSTNAME = "xxxxxxxxxxx.id"
                #USERNAME = "aaaa@xxxxxxxxxx.id"
                #PASSWORD = "xxxxxx"
                #ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD) # setelah edit konfigurasi di atas silahkan uncomment baris 84 - 88
                #ftp_server.encoding = "utf-8"
                print("silahkan edit konfigurasi ftp terlebih dahulu")
                #conn = mysql.connector.connect(
                #    host="IP ADDRESS host", 
                #    user="adminblabla", 
                #    passwd="passwordadmin",
                #    db="namadatabase bukan nama table")
                #mycursor = conn.cursor() #setelah edit konfigurasi di atas silahkan uncomment baris 90 - 95 dan 135 - 138
                print("silahkan edit konfigurasi sql terlebih dahulu")
                frameList = []
                now = datetime.now()
                dt_string = now.strftime("%d%m%Y%H%M%S")
                folder_pindah = dt_string
                os.mkdir("" + folder_pindah)
                while True:
                    files = os.listdir("hasil_deteksi")
                    files2 = os.listdir("" + folder_pindah)
                    if len(files) == 0:
                        timerCount += 1
                        print (timerCount)
                        if timerCount == 5 and len(files2) == 0:
                            print("dihapus foldernya")
                            widget.config(text='Tidak terdapat hasil deteksi. Alat siap digunakan.')
                            #widget = Label(canvas, text='Tidak terdapat hasil deteksi. Alat siap digunakan.', fg='white', bg='black', font=("Cursive", 14)).place(x=353, y=389)
                            os.rmdir("" + folder_pindah)
                            stop_threads = True
                            break
                        if timerCount == 10:
                            print("Semua file deteksi telah berhasil diupload")
                            widget.config(text='Semua file deteksi telah berhasil diupload.')
                            stop_threads = True
                            break
                        time.sleep(1)
                    for f in files:
                        localpath = os.path.join("hasil_deteksi/", f)
                        if os.path.isfile(localpath):
                            x = f.split("_", )
                            y = x[2].split(".jpg", )
                            frameTimeNow = x[0]
                            ket = x[1]
                            koor = y[0]
                            val = (f, koor, ket)
                            #for list in frameList:
                            if frameTimeNow not in frameList:
                                timerCount = 0
                                with open(localpath, "rb") as file:
                                    print("Kerusakan terdeteksi, mengupload foto " + f)
                                    #ftp_server.storbinary(f"STOR {f}", file)
                                    #query = "INSERT INTO gambar_data (nama_gambar,lokasi,keterangan) VALUES (%s, %s, %s)"
                                #mycursor.execute(query, val)
                                #conn.commit()
                                shutil.move(localpath, "" + folder_pindah)
                                frameList.append(frameTimeNow)
                                #widget = Label(canvas, text=str(len(frameList))+' foto kerusakan berhasil diupload.', fg='white', bg='black', font=("Cursive", 14)).place(x=333, y=389)
                                widget.config(text=str(len(frameList))+' foto kerusakan berhasil diupload.')
                            if len(frameList) == len(frameList):
                                timerCount += 1
                                #print (timerCount)
                                if timerCount == 7:
                                    print("Upload selesai.")
                                    stop_threads = True
                                time.sleep(1)
                    if stop_threads == True:
                        break
                break
        while1()
        if internet_on()==False:
            widget.config(text='Alat tidak terhubung Internet.')

        while (internet_on()==False):
            internet_on()
            #print(internet_on())
            if internet_on():
                widget.config(text='Alat terhubung Internet.')
                while1()
                break
autoUpload().start()
master.mainloop()