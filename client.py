#-----------Bolierplate Code Start -----
from http import server
from msilib.schema import ListBox
import socket
from sqlite3 import connect
from threading import Thread
from tkinter import *
from tkinter import ttk

PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

name = None
listbox =  None
textarea= None
labelchat = None
text_message = None

def receiveMessage():
    global SERVER
    global BUFFER_SIZE

    while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list = chunk.decode().split(",")
                listbox.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
            else:
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see("end")
                print(chunk.decode('ascii'))
        except:
            pass

def showClientList():
    global listbox
    global SERVER
    listbox.delete(0,END)
    SERVER.send('show list'.encode('ascii'))

def connectToServer():
    global SERVER
    global name
    global sendingfile

    cName=name.get()
    SERVER.send(cName.encode())

def openChatWindow():
    print('\n\t\t\t\t IP Messenger')
    window=Tk()
    window.title('Messenger')
    window.geometry('500x350')
    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    nameLabel=Label(window,text='Enter your name:',font=('Calibri',10))
    nameLabel.place(x=10,y=8)

    name=Entry(window,width=30,font=('Calibri',10))
    name.place(x=120,y=8)

    connectServer=Button(window,text='Connect to chat server',bd=1,font=('Calibri',10),command=connectToServer)
    connectServer.place(x=350,y=6)

    seperator=ttk.Separator(window,orient='horizontal')
    seperator.place(x=0,y=35,relwidth=1,height=0.1)

    labelUsers=Label(window,text='Active Users',font=('Calibri',10))
    labelUsers.place(x=10,y=50)

    listbox=Listbox(window,height=5,width=67,activestyle='dotbox',font=('Calibri',10))
    listbox.place(x=10,y=70)

    scrollBar1=Scrollbar(listbox)
    scrollBar1.place(relheight=1,relx=1)
    scrollBar1.config(command=listbox.yview)

    connectButton=Button(window,text='Connect',font=('Calibri',10),bd=1)
    connectButton.place(x=282,y=160)

    disconnectButton=Button(window,text='Disconnect',font=('Calibri',10),bd=1)
    disconnectButton.place(x=350,y=160)

    refreshButton=Button(window,text='Refresh',bd=1,font=('Calibri',10),command=showClientList)
    refreshButton.place(x=435,y=160)

    labelchat=Label(window,text='Chat window',font=('Calibri',10))
    labelchat.place(x=10,y=180)

    textarea=Text(window,width=67,height=6,font=('Calibri',10))
    textarea.place(x=10,y=200)

    scrollBar2=Scrollbar(textarea)
    scrollBar2.place(relheight=1,relx=1)
    scrollBar2.config(command=textarea.yview)

    attach=Button(window,text='Attach and send',bd=1,font=('Calibri',10))
    attach.place(x=10,y=305)

    text_message=Entry(window,width=43,bd=1,font=('Calibri',12))
    text_message.pack()
    text_message.place(x=450,y=305)

    send=Button(window,text='Send',font=('Calibri',10),bd=1)
    send.place(x=450,y=305)

    filePathLabel=Label(window,text='',fg='blue',font=('Calibri',8))
    filePathLabel.place(x=10,y=330)

    window.mainloop()

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    recv_thread=Thread(target=receiveMessage)
    recv_thread.start()
    openChatWindow()

setup()