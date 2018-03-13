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
                    self.operation_window(userRole[i], userID[i])
                else:
                    tm.showerror("Incorrect Password")
    
    def operation_window(self, role, ID):
        self.myID = ID
        self.myRole = role
        #self.mySupervisor = supervisor
        self.newWindow = Toplevel(self)
        self.newWindow.wm_title("#%s menu" % self.myRole)

        if role == 'account manager':
            self.SelectCustomer = Button(self.newWindow, text = "Select Customer", command = self._select_cust)
            self.SelectCustomer.grid(row = 0, column = 0)
            self.CreateNewAccount = Button(self.newWindow, text = "Create New Account", command = self._create_new_acc)
            self.CreateNewAccount.grid(row = 0, column = 1)
            self.CreateNewAgreement = Button(self.newWindow, text = "Create New Agreement", command = self._create_service_agr)
            self.CreateNewAgreement.grid(row = 1, column = 0)
            self.CreateReport = Button(self.newWindow, text = "Create Report", command = self._create_report)
            self.CreateReport.grid(row = 1, column = 1)

        self.returnbutton = Button(self.newWindow, text = "Log Out", command= self.newWindow.destroy)
        self.returnbutton.grid(columnspan = 6)
        
        
#test number for own23 : 12345698
    def _select_cust(self):
        self.custselect = Toplevel(self.newWindow)
        self.lablecustnum = Label(self.custselect, text = "Customer's Master Account Number")
        self.inputcustnum = Entry(self.custselect)
        self.lablecustnum.grid(row = 0, column = 0)
        self.inputcustnum.grid(row = 0, column = 1)

        self.buttoncustnum = Button(self.custselect, text = "Select", command = self._customer_selected)
        self.buttoncustnum.grid(columnspan = 2)
        self.returnbutton = Button(self.custselect, text = "Return", command= self.custselect.destroy)
        self.returnbutton.grid(columnspan = 3)

    def _customer_selected(self):
        self.mycustomers = []
        statement = ('select * from accounts where account_mgr = ?')
        for row in waste.execute(statement, [self.myID]):
            self.mycustomers.append(row)

        if len(self.mycustomers) == 0:
            tm.showerror("No Customers Under Selected Account Manager!")
        else:
            for i in range(len(self.mycustomers)):
                if self.inputcustnum.get() == self.mycustomers[i][0]:
                    self._customer_found((self.mycustomers[i]))

    def _customer_found(self, custlist):
        self.customerselected = Toplevel(self.custselect)
        print (custlist)

        self.lableaccnum = Label(self.customerselected, text = "Account Number")
        self.lableaccnum.grid(row = 0, column = 0)
        self.lableaccmgr = Label(self.customerselected, text = "Account Manager")
        self.lableaccmgr.grid(row = 0, column = 1)
        self.lableaccname = Label(self.customerselected, text = "Customer Name")
        self.lableaccname.grid(row = 0, column = 2)
        self.lablecustname = Label(self.customerselected, text = "Customer Number")
        self.lablecustname.grid(row = 0, column = 3)
        self.lablecusttype = Label(self.customerselected, text = "Customer Type")
        self.lablecusttype.grid(row = 0, column = 4)
        self.lablestartdate = Label(self.customerselected, text = "Start Date")
        self.lablestartdate.grid(row = 0, column = 5)
        self.lableenddate = Label(self.customerselected, text = "End Date")
        self.lableenddate.grid(row = 0, column = 6)
        self.labletotalamount = Label(self.customerselected, text = "Total Amount")
        self.labletotalamount.grid(row = 0, column = 7)

        self.rlableaccnum = Label(self.customerselected, text = custlist[0])
        self.rlableaccnum.grid(row = 1, column = 0)
        self.rlableaccmgr = Label(self.customerselected, text = custlist[1])
        self.rlableaccmgr.grid(row = 1, column = 1)
        self.rlableaccname = Label(self.customerselected, text = custlist[2])
        self.rlableaccname.grid(row = 1, column = 2)
        self.rlablecustname = Label(self.customerselected, text = custlist[3])
        self.rlablecustname.grid(row = 1, column = 3)
        self.rlablecusttype = Label(self.customerselected, text = custlist[4])
        self.rlablecusttype.grid(row = 1, column = 4)
        self.rlablestartdate = Label(self.customerselected, text = custlist[5])
        self.rlablestartdate.grid(row = 1, column = 5)
        self.rlableenddate = Label(self.customerselected, text = custlist[6])
        self.rlableenddate.grid(row = 1, column = 6)
        self.rlabletotalamount = Label(self.customerselected, text = custlist[7])
        self.rlabletotalamount.grid(row = 1, column = 7)
        
        
        #TODO make scrollable list with all agreements associated with master account

    def _create_new_acc(self):
        self.newacc = Toplevel(self)
        self.newacc.wm_title("Create Account")
        self.lablecreatenum = Label(self.newacc, text = "Master Account Number ######## ")
        self.inputmasternum = Entry(self.newacc)
        self.lablecreatenum.grid(row = 0, column = 0)
        self.inputmasternum.grid(row = 0, column = 1)
        
        self.accman = self.myID

        self.lablecustname = Label(self.newacc, text = "Customer Name")
        self.inputcustname = Entry(self.newacc)
        self.lablecustname.grid(row = 1, column = 0)
        self.inputcustname.grid(row = 1, column = 1)

        self.lablecontactinfo = Label(self.newacc, text = "Phone (###) ###-####")
        self.inputcontactinfo = Entry(self.newacc)
        self.lablecontactinfo.grid(row = 2, column = 0)
        self.inputcontactinfo.grid(row = 2, column = 1)
    
        self.lablecusttype = Label(self.newacc, text = "Customer Type")
        self.inputcusttype = Entry(self.newacc)
        self.lablecusttype.grid(row = 3, column = 0)
        self.inputcusttype.grid(row = 3, column = 1)
        
        #get time module and fix this
        self.lablestartdate = Label(self.newacc, text = "Start Date (yyyy-mm-dd)")
        self.inputstartdate = Entry(self.newacc)
        self.lablestartdate.grid(row = 4, column = 0)
        self.inputstartdate.grid(row = 4, column = 1)

        self.lableenddate = Label(self.newacc, text = "End Date (yyyy-mm-dd)")
        self.inputenddate = Entry(self.newacc)
        self.lableenddate.grid(row = 5, column = 0)
        self.inputenddate.grid(row = 5, column = 1)

        self.custtotal = 0    

        self.selectacc = Button(self.newacc, text = "Create Account", command = self._makeaccount)
        self.selectacc.grid(row = 6, column = 0)

        self.exitcreate = Button(self.newacc, text = "Return", command= self.newacc.destroy)
        self.exitcreate.grid(row = 6, column = 1)
        
    
    def _makeaccount(self):
        account_number = self.inputmasternum.get()
        account_mgr = self.accman
        cust_name = self.inputcustname.get()
        contact_info = self.inputcontactinfo.get()
        customer_type = self.inputcusttype.get()
        start_date = self.inputstartdate.get()
        end_date = self.inputenddate.get()
        total_amount = self.custtotal
        
        statementacc = '''INSERT INTO accounts (account_no, account_mgr, customer_name, contact_info, customer_type, start_date, end_date, total_amount) values(?,?,?,?,?,?,?,?)'''
        waste.execute(statementacc, [account_number, account_mgr, cust_name, contact_info, customer_type, start_date, end_date, total_amount])
        w.commit()

    def _create_service_agr(self):
        #todo
        print ('you tired bro')

    def _create_report(self):
        #todo
        print ('give up')


root = Tk()
lf = LoginFrame(root)
root.mainloop()


