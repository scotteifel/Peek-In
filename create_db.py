import sqlite3
import os



def create_database():
    path = os.path.abspath("Peek")
    path = path[:-4]
    conn = sqlite3.connect(path+"main.db")
    conn.commit()
    conn.close()
    
    try:
        os.mkdir(path+"screenshot") # Used for SS comparisons
        os.mkdir(path+"gallery") # Gallery pictures temp. stored here when it's open. It's faster.
    except:
        pass