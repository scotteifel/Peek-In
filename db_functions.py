import sqlite3,zlib,base64,os,PIL
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from argon2 import PasswordHasher

global CRNT_USR
global KEY
global usr_info

pic_ext=".jpg"
salt=b'!}\xf2\xfe\xfe \xea\xed\xbe\xdaWF\xa39\xadL'

ph =PasswordHasher()


def find_last_user():

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        try:
            cur.execute('''SELECT l_user FROM last_user''')
            name = cur.fetchall()[0]
        except:
            return
        cur.close()
        conn.close()
        return name


def add_username(x,y):
        global CRNT_USR
        global CRNT_USR_INF
        global KEY

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()

        cur.execute('''SELECT name FROM sqlite_master WHERE type="table" AND name="{tab}"'''.format(tab=x))
        name_info = (cur.fetchone())

        if name_info:
            cur.close()
            conn.close()
            return

        hash = ph.hash(y)
        password = y.encode()

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                            salt=salt, iterations=100000, backend=default_backend())
        KEY=base64.urlsafe_b64encode(kdf.derive(password))
        CRNT_USR = x
        CRNT_USR_INF = x + "_info"
        cur.execute('''CREATE TABLE IF NOT EXISTS {tab} (username TEXT,
        password TEXT, day INTEGER, picture TEXT, data BLOB)'''.format(tab=x))
        conn.commit()

        cur.execute('''CREATE TABLE IF NOT EXISTS {info} (script_state INTEGER,
        delay INTEGER)'''.format(info=CRNT_USR_INF))
        conn.commit()

        cur.execute('''CREATE TABLE IF NOT EXISTS last_user(l_user TEXT DEFAULT Hey)''')
        conn.commit()

        cur.execute('''INSERT INTO {tab} (username, password) VALUES (?,?)'''.format(tab=x),
        (x,hash))
        conn.commit()

        cur.execute('''INSERT INTO {info} (script_state, delay) VALUES (?,?)'''.format(info=CRNT_USR_INF),(0,5))
        conn.commit()

        ##Checking for autocomplete in login screen.  Func is has_account() in gui file
        cur.execute('''SELECT * FROM last_user''')
        try:
            results = cur.fetchall()[0]
            cur.execute('''UPDATE last_user SET l_user = (?) WHERE l_user = (?)''',(CRNT_USR,results[0]))
        except:
            cur.execute('''INSERT INTO last_user (l_user) VALUES (?)''',(CRNT_USR,))

        conn.commit()

        cur.close()
        conn.close()

        return True


def validate_login(name,pasw):
        global CRNT_USR
        global KEY
        global CRNT_USR_INF

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()

        cur.execute('''SELECT name FROM sqlite_master WHERE type="table" AND name="{tab}"'''
                    .format(tab=name))
        name_info = (cur.fetchone())

        if not name_info:
            cur.close()
            conn.close()
            return "Not found", 0

        CRNT_USR = name_info[0]
        CRNT_USR_INF = CRNT_USR + "_info"

        cur.execute('''SELECT password FROM {tab} WHERE username = (?)'''.format(tab=name),
            (name,))
        passw_info = cur.fetchone()[0]

        try:
            ph.verify(passw_info, pasw)
        except:
            return "Pass incorrect", 0

        password = pasw.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
        salt=salt, iterations=100000, backend=default_backend())
        KEY = base64.urlsafe_b64encode(kdf.derive(password))


        cur.execute('''SELECT script_state FROM {info}'''.format(info=CRNT_USR_INF))
        script_state= cur.fetchone()[0]
        conn.commit()

        #Updating to autofill last user in login screen
        cur.execute('''UPDATE last_user SET l_user = (?)''',(name,))
        conn.commit()

        cur.close()
        conn.close()

        return True, script_state



def img_to_db(current,date,initial_pic):

        fernet = Fernet(KEY)

        ##  Encryption before compression yields smaller file than vise versa
        with open(initial_pic, "rb") as f:
            data_encrypt1=fernet.encrypt(f.read())
            data=zlib.compress(data_encrypt1,4)

        os.remove(initial_pic)
        try:
            os.remove("screenshot/Thumbs.db")
        except:
            pass

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        cur.execute('''INSERT INTO {tab} (picture,day,data) VALUES (?,?,?)'''
                    .format(tab=CRNT_USR),(current,date,data))
        conn.commit()
        cur.execute('''UPDATE {info} SET script_state = 1'''.format(info=CRNT_USR_INF))

        conn.commit()
        cur.close()
        conn.close()


def retrieve_image(day):

        fernet = Fernet(KEY)

        conn = sqlite3.connect("main.db")
        cur=conn.cursor()

        temp_path = 'gallery/'
        qry = cur.execute('''SELECT data,picture FROM {tab} WHERE day=?'''.format(tab=CRNT_USR),(day,))
        info=qry.fetchall()

        x=1
        times=[]
        for item in info:
            decompressed = zlib.decompress(item[0])
            with open (temp_path + str(x)+ pic_ext, 'wb') as file:
                file.write(fernet.decrypt(decompressed))
                times.append(item[1])
                x+=1
                with open("crnt.txt", "w") as file:
                    for item in times:
                        file.write(item+"\n")

        cur.close()
        conn.close()
        return x-1


def fetch_dates():

        conn = sqlite3.connect('main.db')
        cur = conn.cursor()

        qry = cur.execute('''SELECT day FROM {tab}'''.format(tab=CRNT_USR))

        list = [x for x, in cur.fetchall()]
        del list[0]

        dates=[]
        for item in list:
            if item not in dates:
                dates.append(item)

        cur.close()
        conn.close()
        return dates


def check_script():

        try:
            conn = sqlite3.connect("main.db")
            cur = conn.cursor()
            cur.execute('''SELECT script_state FROM {info}'''.format(info=CRNT_USR_INF))
            script_info = cur.fetchone()[0]
            cur.close()
            conn.close()
            return script_info
        except:
            return

def script_off():

        conn = sqlite3.connect("main.db")
        cur=conn.cursor()
        cur.execute('''UPDATE {info} SET script_state = 0'''.format(info=CRNT_USR_INF))
        conn.commit()
        cur.close()
        conn.close()


def check_time_delay():

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        cur.execute('''SELECT delay FROM {info}'''.format(info=CRNT_USR_INF))
        timer = cur.fetchone()[0]
        cur.close()
        conn.close()
        if timer:
            return int(timer)
        return 0


def set_delay_time(delay):

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        cur.execute('''UPDATE {info} SET delay = (?)'''.format(info=CRNT_USR_INF), (delay,))
        conn.commit()
        cur.close()
        conn.close()

def save_to_comp(picture):

        fernet=Fernet(KEY)

        conn = sqlite3.connect('main.db')
        cur = conn.cursor()
        cur.execute('''SELECT data,day FROM {tab} WHERE picture=?'''.format(tab=CRNT_USR),(picture,))
        qry = cur.fetchall()[0]

        desktop_path=os.path.expanduser("~/Desktop")
        ##Symbols reformatted to prep for saving to desktop.
        desktop_path=desktop_path.replace("\\","/")
        picture=picture.replace(":","h-").replace(".","min-").replace(" ","s-")+pic_ext

        desktop_path+="/pics"
        #Specific folder within "pics" folder for each day with qry 1 result
        day_folder=desktop_path+"/"+qry[1]
        pic_filepath = day_folder+"/"+picture
        try:
            os.mkdir(desktop_path)
        except:
            pass
        try:
            os.mkdir(day_folder)
        except:
            pass
        decompressed = zlib.decompress(qry[0])
        with open (pic_filepath, 'wb') as file:
            file.write(fernet.decrypt(decompressed))

        cur.close()
        conn.close()


def delete_image(time):

        conn = sqlite3.connect('main.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM {tab} WHERE picture=?'''.format(tab=CRNT_USR),(time,))
        conn.commit()
        cur.close()
        conn.close()


def delete_day(day):

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        cur.execute('''DELETE FROM {tab} WHERE day=?'''.format(tab=CRNT_USR), (day,))
        conn.commit()
        cur.close()
        conn.close()

def delete_user(name):

        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS {tab}'''.format(tab=CRNT_USR))
        cur.execute('''DELETE FROM last_user WHERE l_user = (?)''',(name,))
        conn.commit()
        cur.close()
        conn.close()
