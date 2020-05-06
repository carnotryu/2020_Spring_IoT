import serial
from tkinter import *
import threading
from datetime import datetime

print('Connecting...')
ser = serial.Serial('COM10', 250000, timeout=1)
if ser.isOpen():
    print('Connected!')

on = True
loop_active = True
data_receive = True

data_save = None
save_flag = 0
test_trial = 1

time_prev = 0
time_now = 0

def ser_write():
    global on
    if on:
        ser.write(b'135')
    else:
        ser.write(b'024')
    on = not on

class Upd(threading.Thread):

    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        global loop_active, save_flag, data_save, time_prev, time_now
        while loop_active:
            if data_receive:
                x = ser.readline()
                x = x.split()
                if len(x) > 7:
                    for i in range(0, 8):
                        labels[i].configure(text=x[i])
                    if save_flag == 1:
                        time_now = datetime.now()
                        elapsed = (time_now - time_prev).total_seconds()
                        data_save.writelines(str(elapsed) + "\t")
                        for i in range(0,8):
                            x[i] = float(x[i])
                            if i < 7:
                                data_save.writelines(str(x[i]) + "\t")
                            else:
                                data_save.writelines(str(x[i]) + "\n")
        ser.close()
        self.root.quit()
        self.root.update()

def loop_trigger():
    global data_receive
    if data_receive:
        data_receive = False
        ser.write(b's')
    elif not data_receive:
        data_receive = True
        ser.write(b'r')

def rec_start():
    global data_save, save_flag, test_trial, time_prev
    data_save = open("test" + str(test_trial) + ".txt", "w")
    save_flag = 1
    lb.configure(text = 'recording...')
    time_prev = datetime.now()

def rec_stop():
    global data_save, save_flag, test_trial
    data_save.close()
    test_trial += 1
    save_flag = 0
    lb.configure(text = 'completed')

def exitProgram():
    global loop_active
    loop_active = False

win = Tk()
win.title("serial_test")
win.geometry("300x400")
upd = Upd(win)

bt1 = Button(win, text='LED ON/OFF', command=ser_write)
bt1.pack()
bt2 = Button(win, text='data ON/OFF', command=loop_trigger)
bt2.pack()

labels = [None] * 8

for i in range(8):
    labels[i] = Label(win, text = "0")

for lab in labels:
    lab.pack()

bt3 = Button(win, text = 'rec_start', command = rec_start)
bt4 = Button(win, text = 'rec_stop', command = rec_stop)
bt3.pack()
bt4.pack()

lb = Label(win, text = "waiting")
lb.pack()

bt5 = Button(win, text = 'exit', command = exitProgram)
bt5.pack()

win.mainloop()