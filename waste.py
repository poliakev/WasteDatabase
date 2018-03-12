from hashlib import pbkdf2_hmac
import tkinter as tk
import sqlite3 as sql
w = sql.connect('waste.db')
waste = w.cursor()

password = 'mystup213123d' #default + int after last three letter of lastname in username

hash_name = 'sha256'
salt = 'ssdirf993lksiqb4'
iterations = 100000

#password = ('mystupidpassword12') #marker is int following the last three chars of lastname ie mystupidpassword12 for ard12
hashed_pwd = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
#print (str_hashed_pwd[2:])

# c.execute('''create table t1 (att1, att2)''')
# conn.commit() <saves changes
# conn.close() <close connection *make sure to commit changes

# to get data from queries
#for row in waste.execute('select att1 from t1'):
#   print row
# they will show as a list ('entry', 'entry2')
users = []
for row in c.execute('select login from users'):
    users.append(row[0])
#print (users)
def login_attempt():
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users:
        print ('user varified')

#login_attempt()


print (hashed_pwd)
class Waste_App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.login = tk.Button(self, text = "LOG IN", fg = "green", bg = "black", command = self.log_in)
        self.login.pack(side = "right", fill = 'y')
        #self.logout = tk.Button(self, text = "LOG OUT", fg = "red", command = self.log_out)



        self.quit = tk.Button(self, text = "QUIT", fg = "red", command = root.destroy)
        self.quit.pack(side = "bottom")

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello\n(click me)",
        self.hi_there["command"] = self.say_hi        
        self.hi_there.pack(side = "top")

    def say_hi(self):
        print ("hello waste!")
    def log_in(self):
        print ("Log in attempted")
    def log_out(self):
        print ("Log out attempted")


root = tk.Tk()
app = Waste_App(master=root)
app.mainloop()


