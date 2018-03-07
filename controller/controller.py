# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:51:22 2018

@author: Misha
"""

import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog

import threading
import time

import pyspeedtest
import paramiko

## TODO: make ssh keys work

SERVER = "25.3.82.86"
USER = "misha"
KEYFILE = "C:/Users/misha/.ssh/rsa-key-rpi-misha.ppk"


class PingerThread(threading.Thread):
    
    def __init__(self, handler):
        threading.Thread.__init__(self)
        self.handler = handler
        self.last_result = ""
        self.exit = False
        self.ntests = 1
        self.avg = 0
        self.thisping = 0
        
    def run(self):
        print('Beginning pinger thread')
        st = pyspeedtest.SpeedTest()
        while not self.exit:
            print('Pinging')
            try:
                self.thisping = st.ping(SERVER)
            except Exception as e:
                self.thisping = 0  # connection failure
            self.avg += self.avg - (self.thisping / self.ntests)
            self.ntests += 1
            self.last_result = "Last: {}ms / Avg: {}ms".format(str(self.avg),
                                                               str(self.thisping))
            self.handler.label_pingtime.config(text=self.last_result)
            time.sleep(5)
            
    def join(self, timeout=None):
        self.exit = True
        super(PingerThread, self).join(timeout=None)
            

class ServerController(object):
    
    def __init__(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ping = PingerThread(self)
        self.root = tk.Tk()
        self.build_gui()
        self.connect()
        self.root.mainloop()
    
    def connect(self):
        self._ssh.connect(SERVER, username=USER, 
                          password=simpledialog.askstring(
                                  'Password', 
                                  'Enter SSH password for {}'.format(USER),
                                  show='*'))
        self.ping.start()
    
    def cmd(self, command):
        return self._ssh.exec_command(command)
    
    def cmda(self, command):
        r = self.cmd(command)
        # stdin [0], stdout [1], stderr [2]
        self.output_window.delete(1.0, tk.END)
        self.output_window.insert(tk.INSERT, "====== STDOUT ======\n")
        self.output_window.insert(tk.INSERT, r[1].read())
        self.output_window.insert(tk.INSERT, "\n======= STDERR ======\n")
        self.output_window.insert(tk.INSERT, r[2].read())
    
    def dump_lists(self):
        self.cmda("python /mnt/share/misha/inet_speed_test/combine_lists.py")
    
    def load_to_sql(self):
        self.cmda("python /mnt/share/misha/inet_speed_test/mysql_pst.py " 
                  "/mnt/share/misha/inet_speed_test/master.ilog")
        
    def reboot(self):
        ## FIXME: This needs to be more secure!!
        self.cmda("echo 'Febfd3323374973' | sudo -S reboot")
    
    def custom_command(self):
        self.cmda(self.entry_command.get())
    
    def build_gui(self): 
        """
        ####################################################################
        # Server Controller                                       __ [ ] X #
        # Last ping time: 21ms         +---------------------------------+ #
        # [Dump lists] [Load to SQL]   |                                 | #
        # [Reboot]                     |                                 | #
        #                              |                                 | #
        # +--------------------------+ |             Output              | #
        # |          Text            | |                                 | #
        # |         Entry            | |                                 | #
        # +--------------------------+ |                                 | #
        # [Send command]               +---------------------------------+ #
        ####################################################################
        """
        
        self.root.title("Server Controller")
        
        self.label_pingtime = tk.Label(master=self.root, text="")
        self.label_pingtime.grid(row=0, column=0, columnspan=2)
        
        ###
        ### Add custom commands here.
        ###
        
        self.button_listdump = tk.Button(master=self.root, text="Dump lists",
                                         command=self.dump_lists)
        self.button_listdump.grid(row=1, column=0)
        
        self.button_loadsql = tk.Button(master=self.root, text="Load to SQL",
                                        command=self.load_to_sql)
        self.button_loadsql.grid(row=1, column=1)
        
        self.button_reboot = tk.Button(master=self.root, text='Reboot',
                                       command=self.reboot)
        self.button_reboot.grid(row=2, column=0)
        
        ###
        ### End custom command section.
        ###
        
        self.entry_command = tk.Entry(master=self.root, width="35",
                                      font=('Consolas', 10),
                                      justify='left')
        self.entry_command.grid(row=4, column=0, rowspan=2, columnspan=2,
                                sticky=tk.NW+tk.SE)
        
        self.button_sendcmd = tk.Button(master=self.root, text="Send command",
                                        command=self.custom_command)
        self.button_sendcmd.grid(row=6, column=0)
        
        self.output_window = tk.Text(master=self.root, width="80")
        self.output_window.grid(row=0, column=3, rowspan=7)
        
if __name__ == '__main__':
    s = ServerController()