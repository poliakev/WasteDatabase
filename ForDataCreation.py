from hashlib import pbkdf2_hmac
import sqlite3 as sql
conn = sql.connect('/home/user/Documents/C291/GitWaste/WasteDatabase/waste.db')
c = conn.cursor()

# the user's password will be different for different users, e.g.:
password = 'mypass'

# the following three identifiers are arguments to pbkdf2_hmac that must not be changed! 
hash_name = 'sha256'
salt = 'ssdirf993lksiqb4'
iterations = 100000

marker = 0
manlist = []
drivelist = []
suplist = []
dislist = []

# login = (row[1][-3:] + str(marker))

for row in c.execute('select * from personnel p, account_managers d where p.pid = d.pid'):
    manlist.append(row)
for row2 in c.execute('select * from personnel p, drivers d where p.pid = d.pid'):
    drivelist.append(row2)
for row3 in c.execute("select * from personnel p where p.supervisor_pid = '00000'"):
    suplist.append(row3)
for row4 in c.execute("select * from personnel p where p.supervisor_pid = '11111'"):
    dislist.append(row4)

for driver in drivelist:
    marker = marker + 1
    password = 'drive' + str(marker) #ie driver1's pass is drive1
    
    hashed_password = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
    statement = '''INSERT INTO users (user_id, role, login, password) values(?,?,?,?)''' #not sure if semicolon is necessary
    conn.execute(statement, [driver[0], 'driver', (driver[1][-3:] + str(marker)), sql.Binary(hashed_password)])

for man in manlist:
    marker = marker + 1
    password = 'manage' + str(marker) #ie driver1's pass is drive1
    
    hashed_password = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
    statement = '''INSERT INTO users (user_id, role, login, password) values(?,?,?,?);''' #not sure if semicolon is necessary
    conn.execute(statement, [man[0], 'account manager', (man[1][-3:] + str(marker)), sql.Binary(hashed_password)])

for sup in suplist:
    marker = marker + 1
    password = 'super' + str(marker) #ie driver1's pass is drive1
    
    hashed_password = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
    statement = '''INSERT INTO users (user_id, role, login, password) values(?,?,?,?);''' #not sure if semicolon is necessary
    conn.execute(statement, [sup[0], 'supervisor', (sup[1][-3:] + str(marker)), sql.Binary(hashed_password)])

for dis in dislist:
    marker = marker + 1
    password = 'dispatch' + str(marker) #ie driver1's pass is drive1
    
    hashed_password = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
    statement = '''INSERT INTO users (user_id, role, login, password) values(?,?,?,?);''' #not sure if semicolon is necessary
    conn.execute(statement, [dis[0], 'dispatcher', (dis[1][-3:] + str(marker)), sql.Binary(hashed_password)])

password = 'bruh'
hashed_password = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)

statement2 = '''INSERT INTO users (user_id, role, login, password) values(?,?,?,?);''' #not sure if semicolon is necessary
conn.execute(statement2, ['007', 'alden', 'bruh1' , sql.Binary(hashed_password)])
statement3 = '''INSERT INTO users (user_id, role, login, password) values(?,?,?,?);''' #not sure if semicolon is necessary
c.execute(statement3, ['006', 'jan', 'bruh2' , sql.Binary(hashed_password)])
conn.commit()

#for row4 in c.execute("select * from users"):
#    print (row4)



