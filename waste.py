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
        
        self.newUser = Button(self, text = "Create New User", command = self._createUser)
        self.newUser.grid(row = 2 , column = 0)

        self.logbtn = Button(self, text = "Login", command = self._menu)
        self.logbtn.grid(row = 2, column = 1)
        self.quit = Button(self, text = "QUIT", fg = "red", command = root.destroy)
        self.quit.grid(row = 2, column = 2)


        self.mycustomers = [] #maybe shouldn't be here o well

        self.pack()

    def _createUser(self):
        self.userWindow = Toplevel(self)
        self.userWindow.wm_title("Create New User")
        self.newlabel_username = Label(self.userWindow, text= "New User")
        self.newlabel_role = Label(self.userWindow, text= "Role")
        self.newlabel_password = Label(self.userWindow, text= "Password")
        self.newlabel_confirmpassword = Label(self.userWindow, text= "Confirm Password")


        self.newentry_username = Entry(self.userWindow)
        self.newrole_username = Entry(self.userWindow)
        self.newentry_password = Entry(self.userWindow, show = "*")
        self.confirmnewentry_password = Entry(self.userWindow, show = "*")
        self.newlabel_username.grid(row = 0, sticky = E)
        self.newlabel_role.grid(row = 1, sticky = E)
        self.newlabel_password.grid(row = 2, sticky = E)        
        self.newlabel_confirmpassword.grid(row = 3, sticky = E)
        self.newentry_username.grid(row = 0, column = 1)
        self.newrole_username.grid(row = 1, column = 1)
        self.newentry_password.grid(row = 2, column = 1)
        self.confirmnewentry_password.grid(row = 3, column = 1)
        
        
        self.createbtn = Button(self.userWindow, text = "Create", command = self._create_btn_clicked)
        self.createbtn.grid(row = 4, column = 0)

        self.quit = Button(self.userWindow, text = "QUIT", fg = "red", command = self._withdraw)
        self.quit.grid(row = 4, column = 1)
        
    def _create_btn_clicked(self):
        self.nuser = self.newentry_username.get()
        self.nrole = self.newrole_username.get()
        self.npassword = self.newentry_password.get()
        self.nconpassword = self.confirmnewentry_password.get()
        self.nid = 25252
        
        if self.npassword == self.nconpassword and self.nuser != '' and self.nrole != '':
            nhashed_password = pbkdf2_hmac(hash_name, bytearray(self.npassword, 'ascii'), bytearray(salt, 'ascii'), iterations)
            statement = '''INSERT INTO users (user_id, role, login, password) values(?,?,?,?);''' #not sure if semicolon is necessary
            #self.generateID()
            waste.execute(statement, [self.nid, self.nrole, self.nuser, sql.Binary(nhashed_password)])
            #don't forget peronnel........
        

            w.commit()


    def _withdraw(self):
        self.userWindow.withdraw()
        

    def _menu(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        userLog = []
        userRole = []
        userPassword = []
        userID = []
        #userSupervisor = []
        for row in waste.execute('select login, role, password, user_id from users'):
            userLog.append(row[0])
            userRole.append(row[1])
            userPassword.append(row[2])
            userID.append(row[3])
            #userSupervisor.append(row[4])
        
        if username == '' or password == '':
            tm.showerror("Error","Please Enter Valid Username and Password")

        for i in range(len(userLog)):
            if username == userLog[i]:
                hashed_pwd = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
                if hashed_pwd == userPassword[i]:
                    self.menuWindow = Toplevel(self)

                    self.myID = userRole[i]
                    self.myRole = userID[i]

                    self.menuWindow.wm_title("#%s menu" % self.myRole)

                    #example button
                    #self.createbtn = Button(self.userWindow, text = "Create", command = self._create_btn_clicked)

                    self.SelectCustomer = Button(self.menuWindow, text = "Select Customer", command = self._select_cust_clicked)
                    self.SelectCustomer.grid(row = 0, column = 0)
                    self.CreateNewAccount = Button(self.menuWindow, text = "Create New Account", command = self._create_new_acc)
                    self.CreateNewAccount.grid(row = 0, column = 1)
                    self.CreateNewAgreement = Button(self.menuWindow, text = "Create New Agreement", command = self._create_service_agr)
                    self.CreateNewAgreement.grid(row = 1, column = 0)
                    self.CreateReport = Button(self.menuWindow, text = "Create Report", command = self._create_report)
                    self.CreateReport.grid(row = 1, column = 1)

                    self.returnbutton = Button(self.menuWindow, text = "Return", command= self.menuWindow.destroy)
                    self.returnbutton.grid(columnspan = 6)
                else:
                    tm.showerror("Incorrect Password")   
        
        #self.scrollbar = ScrollBar(self)
        #self.scrollbar.pack(side=RIGHT, fill = 'y')
       
        #self.listbox = Listbox(self)
        #self.listbox.pack() 
        # test master acc # 87625036 for own23
    def _create_new_acc(self):
        print ('ok')
        #self.lableselectcust = Label(self.newWindow, text = "Enter master account number")
        #self.inputmasternum = Entry(self.newWindow)
        #self.lableselectcust.grid(row = 0, column = 0)
        #self.inputmasternum.grid(row = 0, column = 1)
        #print ('hi')

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


