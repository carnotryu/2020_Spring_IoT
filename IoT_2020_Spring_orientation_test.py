import serial
from tkinter import *
import threading
from datetime import datetime

print('Connecting...')
ser = serial.Serial('COM5', 250000, timeout=1)
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

time_start = 0
time_end = 0

state = 0
cnt1 = 0
cnt2 = 0

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
        global loop_active, save_flag, data_save, time_prev, time_now, state, cnt1, cnt2, time_start, time_end
        while loop_active:
            if data_receive:
                x = ser.readline()
                x = x.split()
                if len(x) > 7:
                    lb1.configure(text = x[2])
                    if state == 0:
                        if float(x[2]) > 0.6:
                            state = 1
                            time_start = datetime.now()
                    elif state == 1:
                        if float(x[2]) < 0.6:
                            state = 0
                            time_end = datetime.now()
                            elapsed = (time_end - time_start).total_seconds()
                            if elapsed > 0.5:
                                cnt1 += 1
                            else:
                                cnt2 += 1
                            lb2.configure(text = cnt1)
                            lb3.configure(text = cnt2)

        ser.close()
        self.root.quit()
        self.root.update()

def exitProgram():
    global loop_active
    loop_active = False

win = Tk()
win.title("serial_test")
win.geometry("300x400")
upd = Upd(win)

lb1 = Label(win, text="0.0")
lb1.pack()

lb2 = Label(win, text="0")
lb3 = Label(win, text="0")
lb2.pack()
lb3.pack()

bt5 = Button(win, text = 'exit', command = exitProgram)
bt5.pack()

win.mainloop()