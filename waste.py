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

        self.logbtn = Button(self, text = "Login", command = self._login_btn_clicked)
        self.logbtn.grid(columnspan = 2)
        self.quit = Button(self, text = "QUIT", fg = "red", command = root.destroy)
        self.quit.grid(columnspan = 2)


        self.mycustomers = [] #maybe shouldn't be here o well

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
                    self.operation_window(userRole[i], userID[i], userSupervisor[i])
                else:
                    tm.showerror("Incorrect Password")
    
    def operation_window(self, role, ID, supervisor):
        self.myID = ID
        self.myRole = role
        self.mySupervisor = supervisor
        self.newWindow = Toplevel(self.master)
        self.newWindow.wm_title("#%s menu" % self.myRole)

        if role == 'account manager':
            self.SelectCustomer = Button(self.newWindow, text = "Select Customer", command = self._select_cust_clicked())
            self.SelectCustomer.grid(row = 0, column = 0)
            #self.CreateNewAccount = Button(self.newWindow, text = "Create New Account", command = self._create_new_acc())
            #self.CreateNewAccount.grid(row = 0, column = 1)
            #self.CreateNewAccount.pack()
            #self.CreateNewAgreement = Button(self.newWindow, text = "Create New Agreement", command = self._create_service_agr())
            #self.CreateNewAgreement.grid(row = 1, column = 0)
            #self.CreateNewAgreement.pack()
            #self.CreateReport = Button(self.newWindow, text = "Create Report", command = self._create_report())
            #self.CreateReport.grid(row = 1, column = 1)
            #self.CreateNewReport.pack()

            #move the following into select customer window with a withdraw()
            #self.lableselectcust = Label(self.newWindow, text = "Enter master account number")
            #self.inputmasternum = Entry(self.newWindow)
            #self.lableselectcust.grid(row = 0, column = 1)
            #self.inputmasternum.grid(row = 1, column = 1)
            #self.selectcust = Button(self.newWindow, text = "Select", command = self._select_cust_clicked(self.myID))
            #self.selectcust.grid(columnspan = 2)
            self.returnbutton = Button(self.newWindow, text = "Return", command= self.newWindow.destroy)
            self.returnbutton.grid(columnspan = 2)
        
        #self.scrollbar = ScrollBar(self)
        #self.scrollbar.pack(side=RIGHT, fill = 'y')
       
        #self.listbox = Listbox(self)
        #self.listbox.pack() 
        # test master acc # 87625036 for own23
    def _create_new_acc(self):
        #todo
        print ('hi')

    def _create_service_agr(self):
        #todo
        print ('you tired bro')

    def _create_report(self):
        #todo
        print ('give up')

    def _select_cust_clicked(self):
        #self.custselect = Toplevel(self.newWindow)
        #self.customer = Entry(self.custselect)
        #self.customer.grid(columnspan = 2)

        statement = ('select account_no from accounts where account_mgr = ?')
        for row in waste.execute(statement, [self.myID]):
            self.mycustomers.append(row[0])
        
        #self.customerselected = Button(self.custselect, text = "select", command = self._select_customer_account())
        #self.customerselected.grid(columnspan = 2)

    
    def _select_customer_account(self):
        self.custWindow = Toplevel(self.newWindow)
        self.custWindow.wm_title("Account number #%s" % self.inputmasternum.get())
        

        

       # for i in range(len(self.mycustomers)):
            #if self.inputmasternum.get() == self.mycustomers[i]:
                #custstatement = ('select * from accounts where account_no = ?')
                #cust = waste.execute(statement, [self.inputmasternum.get()])
                #self.custl1 = Label(self.newWindow, text = "account number")
                #self.custl1.grid(row = 0, column = 0)
               #self.custl2 = Label(self.newWindow, text = "account manager")
               #self.custl2.grid(row = 0, column = 1)
               #self.custl3 = Label(self.newWindow, text = "customer name")
               #self.custl3.grid(row = 0, column = 2)
               #self.custl4 = Label(self.newWindow, text = "contact info")
               #self.custl4.grid(row = 0, column = 3)
               #self.custl5 = Label(self.newWindow, text = "customer type")
               #self.custl5.grid(row = 0, column = 4)
               #self.custl6 = Label(self.newWindow, text = "start date")
               #self.custl6.grid(row = 0, column = 5)
               #self.custl7 = Label(self.newWindow, text = "end date")
               #self.custl7.grid(row = 0, column = 6)
               #self.custl8 = Label(self.newWindow, text = "total amount")
               #self.custl8.grid(row = 0, column = 7)
        




root = Tk()
lf = LoginFrame(root)
root.mainloop()


