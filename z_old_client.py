import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300, bg="#005C4B")
        
        self.pls = Label(self.login,text = "Please login to continue",justify = CENTER,font = "Helvetica 14 bold",bg="#005C4B")
        self.pls.place( relheight = 0.15,relx = 0.2,rely = 0.07)
        self.labelName = Label(self.login,text = "Name: ",font = "Helvetica 12",bg="#005C4B")
        self.labelName.place(relheight = 0.2,relx = 0.1,rely = 0.2)
        self.entryName = Entry(self.login,font = "Helvetica 14",bg="green")
        self.entryName.place(relwidth = 0.4,relheight = 0.12,relx = 0.35,rely = 0.2)
        self.entryName.focus()

        self.bttn=Button(self.login, text="Join Room", font = "Helvetica 14 bold", command=lambda: self.goAhead(self.entryName.get()),bg="green")
        self.bttn.place(relx=0.4,rely=0.5)
        
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rec=Thread(target=self.receive)
        rec.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                print(f"orignal: {message}")
                if message == 'NICKNAME':
                    print(f"if: {message}")
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMsg(message)
                    print(f"else: {message}")
            except:
                print("An error occured!")
                client.close()
                break
    
    def layout(self, name):
        self.name=name

        # self.Window = Tk()
        self.Window.deiconify()

        self.Window.title("Chat-Room")

        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=600,height=500, bg='#013d33')

        self.labelHead=Label(self.Window,bg="white",fg="white",text=self.name, font="Helvetica 14 bold",pady=5)
        self.labelHead.place(relwidth=1)

        self.line=Label(self.Window,bg="#005C4B",width=500)
        self.line.place(relwidth=1,relheight=0.07,rely=0.012)

        self.txtArea=Text(self.Window,width=20,height=2,bg="#002830", fg="white", font="Helvetica 12",padx=5,pady=5)
        self.txtArea.place(relheight=0.745, relwidth=1, rely=0.08)

        self.bottomLabel = Label(self.Window, bg="#005C4B", height=80)
        self.bottomLabel.place(relwidth=1,rely=0.825)

        self.entryMsg=Entry(self.bottomLabel, bg="green", fg="white", font="Helvetica 12")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()

        self.send_Bttn=Button(self.bottomLabel,text="↩",font='Helvetica 21', bg="green", width=20, command=lambda: self.send_Button(self.entryMsg.get()))
        self.send_Bttn.place(relwidth=0.22, relheight=0.06, rely=0.008, relx=0.77)

        self.txtArea.config(cursor='arrow')
        self.scrollBar=Scrollbar(self.txtArea)
        self.scrollBar.place(relheight=1, relx=0.974)
        self.scrollBar.config(command=self.txtArea.yview)
        self.txtArea.config(state=DISABLED)

        self.Window.mainloop()

    def send_Button(self,msg):
        self.txtArea.config(state=DISABLED)
        self.msg=msg
        self.entryMsg.delete(0,END)
        snd=Thread(target=self.write)
        snd.start()

    def showMsg(self, msg):
        self.txtArea.config(state=NORMAL)
        self.txtArea.insert(END, msg+'\n\n')
        self.txtArea.config(state=DISABLED)
        self.txtArea.see(END)

    def write(self):
        self.txtArea.config(state=DISABLED)
        while True:
            message = '{}: {}'.format(self.name, self.msg)
            client.send(message.encode('utf-8'))
            self.showMsg(message)
            break


g = GUI()