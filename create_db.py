import sqlite3, os


def create_database():
        path = os.path.abspath("Peek")
        path = path[:-4]
        conn = sqlite3.connect(path+"main.db")
        conn.commit()
        conn.close()

        try:
            os.mkdir(path+"screenshot")
            os.mkdir(path+"gallery")
        except:
            pass
