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
        self.newWindow = Toplevel(self)
        self.newWindow.wm_title("#%s menu" % self.myRole)

        if role == 'Account Manager':
            self.userMode = 'account manager'
            self.SelectCustomer = Button(self.newWindow, text = "Select Customer", command = self._select_cust)
            self.SelectCustomer.grid(row = 0, column = 0)
            self.CreateNewAccount = Button(self.newWindow, text = "Create New Account", command = self._create_new_acc)
            self.CreateNewAccount.grid(row = 0, column = 1)
            self.CreateNewAgreement = Button(self.newWindow, text = "Create New Agreement", command = self._create_new_agreement)
            self.CreateNewAgreement.grid(row = 1, column = 0)
            self.CreateReport = Button(self.newWindow, text = "Create Report", command = self._create_report)
            self.CreateReport.grid(row = 1, column = 1)
        elif role == 'Supervisor':
            self.userMode = 'supervisor'
            self.Createnewacc = Button(self.newWindow, text = "Create New Account", command = self._create_new_acc)
            self.Createnewacc.grid(row = 0, column = 0)
            self.Createrep = Button(self.newWindow, text = "Create Report", command = self._create_report)
            self.Createrep.grid(row = 0, column = 1)
            self.Createmanrep = Button(self.newWindow, text = "Create Manager Report", command = self._create_mgr_report)
            self.Createmanrep.grid(row = 1, column = 0)
        elif role == 'Driver':
            self.userMode = 'driver'
            self.SelectCustomer = Button(self.newWindow, text = "Task List", command = self._task_list)
            self.SelectCustomer.grid(row = 0, column = 0)

        elif role == 'Dispatcher':
            self.userMode = 'dispatcher'
            self.Selectserv = Button(self.newWindow, text = "Select Service Agreement", command = self._select_service)
            self.Selectserv.grid(row = 0, column = 0)

        self.returnbutton = Button(self.newWindow, text = "Log Out", command= self.newWindow.destroy)
        self.returnbutton.grid(columnspan = 6)

    def _select_service(self):
        print ('service')
        #TODO
        #The dispatcher must be able to first select a service agreement. Then, he or she should be given options to select driver, truck, and a container to be dropped off and picked up with the following constraints:
        #1 if a driver is selected who owns a truck, that truck should be automatically selected; otherwise the dispatcher also must select a truck.

        #2 The information about the container to be picked up must be filled in automatically; the dispatcher should not have to select this container. If there is already a container at the location for the selected service agreement, that is the container to be picked up (the last record where a container was dropped off at that location will have the information about the container). If there is no container yet at the location of the service agreement, the "Dummy Container” (container ID = '0000') should be picked up.

        #3 The dispatcher should select the container to be dropped off from a list of available containers; this list should only show available containers that can hold the appropriate waste type, given in the service agreement. A container is available, if it is not currently located at a customer's service agreement location and not already scheduled to be dropped off at a future date.

        #4 For the date_time entry it is sufficient to just enter a date string in the form ' YYYY-MM-DD' (i.e., not including time information).
            

    def _task_list(self):
        print ('task list')
        #TODO
        #For a given date range, list all the tours that they have been assigned to. The information about a tour consists of the the following:

            #1The location where to exchange containers.
            #2The local contact information for the service agreement.
            #3The waste_type involved in the service agreement.
            #4The container ID of the container to be dropped off.
            #5The container ID of the container to be picked up.

    def _create_mgr_report(self):
        print ('create mgr report')
        #TODO
        #Create a summary report that contains the following summary information for each of the account managers that the supervisor supervises: the total number of master agreements for an account manager, the total number of service agreements, the sum of the prices and the sum of the internal cost of all service agreements for the account manager. The report should be sorted by the difference between the sum of prices and the sum of internal costs.
        
    def _create_report(self):
        print ('create report')
        #check userMode if 'account manager':
        #TODO
        #Create a summary report for a single customer, listing the total number of service agreements, the sum of the prices and the sum of the internal cost of the service agreements, as well as the number of different waste types that occur in the service agreements.
        #call self._customer_selected and set self.mode to report
        #check userMode if 'supervisor'
        #Same as account managers, but with the following differences: 1) the supervisor should be able to select a customer from the customers of all account managers that the supervisor supervises; 2) the report should also include the name of the account manager who manages the account.

    def _create_new_agreement(self):
        self.newagr = Toplevel(self.newWindow)
        self.newagr.wm_title("Create New Agreement")
        self.lablecustnum = Label(self.newagr, text = "Customer's Master Account Number ########")
        self.inputmasternum = Entry(self.newagr)
        self.lablecustnum.grid(row = 0, column = 0)
        self.inputmasternum.grid(row = 0, column = 1)
        
        self.mode = 'newagr'
        self.buttoncustnum = Button(self.newagr, text = "Select", command = self._customer_selected)
        self.buttoncustnum.grid(columnspan = 2)


    def _select_cust(self):
        self.custselect = Toplevel(self.newWindow)
        self.lablecustnum = Label(self.custselect, text = "Customer's Master Account Number")
        self.inputcustnum = Entry(self.custselect)
        self.lablecustnum.grid(row = 0, column = 0)
        self.inputcustnum.grid(row = 0, column = 1)

        self.mode = 'info'
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
        if self.mode == 'info':
            for i in range(len(self.mycustomers)):
                if self.inputcustnum.get() == self.mycustomers[i][0]:
                    self._customer_found((self.mycustomers[i]))
        elif self.mode == 'newagr':
            for i in range(len(self.mycustomers)):
                if self.inputmasternum.get() == self.mycustomers[i][0]:
                    self._new_agreement((self.mycustomers[i]))

    def _new_agreement(self, custlist):
        #test number for own23 : 12345698
        #For a given customer, add a new service agreement with all the required information -except for the master account number, and the service_no, which should be automatically filled in by the system; master_account is the number of the selected customer, and the service_no is a running numbers, so the next available number should be filled in.
        #TODO
        #find highest service num then add to it and pull master_account number from custlist
        #ie something like select service_no from service_agreements; (select highest service no)
        print ('new agr')
        

    def _customer_found(self, custlist):
        self.customerselected = Toplevel(self.custselect)

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
        
        self.returnbutton = Button(self.customerselected, text = "Return", command= self.customerselected.destroy)
        self.returnbutton.grid(columnspan = 3)
        
        #TODO make scrollable list with all agreements associated with master account

    def _create_new_acc(self):
        self.newacc = Toplevel(self)
        self.newacc.wm_title("Create Account")
        self.lablecreatenum = Label(self.newacc, text = "Master Account Number ######## ")
        self.inputmasternum = Entry(self.newacc)
        self.lablecreatenum.grid(row = 0, column = 0)
        self.inputmasternum.grid(row = 0, column = 1)
        
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
        
        if self.userMode == 'account manager':
            self.accman = self.myID
        elif self.userMode == 'supervisor':
            #TODO check to see if supervisor can assign selected mgr (if in personnel the account manager's supervisor is = to self.myID
            #possible drop down menu (in my wildest dreams)
            self.lableaccmgr = Label(self.newacc, text = "Account Manager")
            self.inputaccmgr = Entry(self.newacc)
            self.lableaccmgr.grid(row = 7, column = 0)
            self.inputaccmgr.grid(row = 7, column = 1)
    
    def _makeaccount(self):
        account_number = self.inputmasternum.get()
        if self.userMode == 'account manager':
            account_mgr = self.accman
        elif self.userMode == 'supervisor':
            account_mgr = self.self.inputaccmgr.get()
        cust_name = self.inputcustname.get()
        contact_info = self.inputcontactinfo.get()
        customer_type = self.inputcusttype.get()
        start_date = self.inputstartdate.get()
        end_date = self.inputenddate.get()
        total_amount = self.custtotal
        
        statementacc = '''INSERT INTO accounts (account_no, account_mgr, customer_name, contact_info, customer_type, start_date, end_date, total_amount) values(?,?,?,?,?,?,?,?)'''
        waste.execute(statementacc, [account_number, account_mgr, cust_name, contact_info, customer_type, start_date, end_date, total_amount])
        w.commit()


root = Tk()
lf = LoginFrame(root)
root.mainloop()


