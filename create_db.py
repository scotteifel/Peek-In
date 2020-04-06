import sqlite3, os


def create_database():
        conn = sqlite3.connect("main.db")
        conn.commit()
        conn.close()

        try:
            os.mkdir("screenshot")
            os.mkdir("gallery")
        except:
            pass
