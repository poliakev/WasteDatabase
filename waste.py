from hashlib import pbkdf2_hmac
from tkinter import *
import tkinter.messagebox as tm

import sqlite3 as sql
w = sql.connect('waste.db')
waste = w.cursor()

# *** dont forget w.commit() and w.close()

password = 'mystup213123d' #default + int after last three letter of lastname in username

hash_name = 'sha256'
salt = 'ssdirf993lksiqb4'
iterations = 100000

#password is super<marker> manage<marker> dispatch<marker> drive<marker>
#test driver login: oza1 password: drive1
#test acc manager login: own23 password: manage23
#test supervisor login: ser43 password super43
#test dispatcher login: ach48 password dispatch48

#login_attempt()


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text= "Username")
        self.label_password = Label(self, text= "Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show = "*")
        self.label_username.grid(row = 0, sticky = E)
        self.label_password.grid(row = 1, sticky = E)
        self.entry_username.grid(row = 0, column = 1)
        self.entry_password.grid(row = 1, column = 1)
        
        self.checkbox = Checkbutton(self, text='Keep me logged in')
        self.checkbox.grid(columnspan = 2)

        self.logbtn = Button(self, text="Login", command =self._login_btn_clicked)
        self.logbtn.grid(columnspan = 2)

        self.pack()

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        userLog = []
        userRole = []
        userPassword = []
        userID = []
        userSupervisor = []
        for row in waste.execute('select login, role, password, user_id, supervisor_pid from users, personnel where user_id = PID'):
            userLog.append(row[0])
            userRole.append(row[1])
            userPassword.append(row[2])
            userID.append(row[3])
            userSupervisor.append(row[4])
        
        if username == '' or password == '':
            tm.showerror("Error","Please Enter Valid Username and Password")

        for i in range(len(userLog)):
            if username == userLog[i]:
                hashed_pwd = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
                if hashed_pwd == userPassword[i]:
                    print ('bruh')
                    self.operation_window(userRole[i], userID[i], userSupervisor[i])
                else:
                    tm.showerror("Incorrect Password")
    
    def operation_window(self, role, ID, supervisor):
        self.myID = ID
        self.myRole = role
        self.mySupervisor = supervisor
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.newWindow.wm_title("#%s menu" % self.myRole)
        #l = lf.Label(t, text="some text")
        #l.pack(side ="top", fill = "both", expand = True, padx = 100, pady = 100)
        

root = Tk()
lf = LoginFrame(root)
root.mainloop()


