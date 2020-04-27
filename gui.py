import os, subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import ImageTk, Image

from app import commence_script, sort_gallery, sort_times
from create_db import create_database
from db_functions import (add_username, validate_login, retrieve_image,
set_delay_time, check_time_delay, fetch_dates, delete_image, delete_day,
script_off, check_script, save_to_comp, check_user, delete_user)
## Styling
from tkinter import ttk
from ttkthemes import ThemedTk

global set_delay
global pic_num
global script_title
global win_title_prefix

win_title_prefix = " "
pic_num = 1
#pic_ext var in db_functions file and app file also. Used .jpg
#to reduce pic size, other ext should work. Eg ".png". Need to
#change im.save(initial pic) "quality" kwarg in app.py also if modified
pic_ext=".jpg"


class Application(ttk.Frame):


    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.has_account()


    def login_window(self,name):
        self.master.title("Peek In")

        self.greet = ttk.Label(self.master)
        self.greet["text"]="Welcome"

        self.enter_name = ttk.Entry(self.master)
        self.enter_name.insert(0,name)
        self.ask_name = ttk.Label(self.master)
        self.ask_name["text"]="Enter Username"
        self.ask_pass = ttk.Label(self.master)
        self.ask_pass["text"]="Enter Password"
        self.enter_pass = ttk.Entry(self.master,show="*")
        self.enter_pass.insert(0,"Scott1")

        self.new_account = ttk.Button(self.master,text="Create Account",
                                      command=self.create_account_page)

        self.quit = ttk.Button(self.master,text="Exit",
                               command=self.master.destroy)

        self.enter = ttk.Button(self.master,text="Submit",command=self.check_credentials)

                                    # w_of_wind = 370    185
                                    # h_of_wind = 210    105
        print("Start")
        self.greet.place(x=160,y=5)
        self.ask_name.place(x=60,y=32)
        self.enter_name.place(x=150,y=30)
        self.ask_pass.place(x=62,y=62)
        self.enter_pass.place(x=149,y=60)
        self.new_account.place(x=33,y=100)
        self.quit.place(x=260,y=100)
        self.enter.place(x=160,y=100)
        self.clear_gallery()
        print("done")

    def create_account_page(self):

        self.master.withdraw()
        self.new_user_win = tk.Toplevel(self.master)

        self.new_user_win.protocol('WM_DELETE_WINDOW',end_process)
        self.new_user_win.resizable(False,False)
        w_of_wind = 350
        h_of_wind = 200
        monitor_width = self.master.winfo_screenwidth()
        monitor_height = self.master.winfo_screenheight()
        x_coord = (monitor_width/2) - (w_of_wind/2)
        y_coord = (monitor_height/2) - (h_of_wind/2)
        self.new_user_win.geometry("%dx%d+%d+%d" % (w_of_wind, h_of_wind, x_coord, y_coord))

        self.greet2 = ttk.Label(self.new_user_win,text="Create A New Account",font=("Helvetica",15))

        self.ask_name2 = ttk.Label(self.new_user_win)
        self.ask_name2["text"]="Enter Username"
        self.enter_name2 = ttk.Entry(self.new_user_win)

        self.ask_pass2 = ttk.Label(self.new_user_win)
        self.ask_pass2["text"]="Enter Password"
        self.enter_pass2 = ttk.Entry(self.new_user_win,show="*")

        self.enter2 = ttk.Button(self.new_user_win,text="Submit",command=self.create_user)


        self.back_to_login = ttk.Button(self.new_user_win,text="Sign In",
        command=self.to_login)
        self.quit = ttk.Button(self.new_user_win,text="Exit",
                               command=self.master.destroy)

        self.greet2.place(x=100,y=8)
        self.ask_name2.place(x=59,y=45)
        self.enter_name2.place(x=145,y=45)
        self.ask_pass2.place(x=62,y=75)
        self.enter_pass2.place(x=145,y=75)
        self.back_to_login.place(x=30,y=115)
        self.enter2.place(x=125,y=115)
        self.quit.place(x=225,y=115)


    def logged_in(self):
        print("Logged in func")

        self.home_win = tk.Toplevel(self.master)

        self.home_win.title("Peek In logged in")
        self.home_win.protocol('WM_DELETE_WINDOW',self.hide)
        self.home_win.resizable(False,False)

        w_of_wind = 380
        h_of_wind = 250
        monitor_width = self.master.winfo_screenwidth()
        monitor_height = self.master.winfo_screenheight()
        x_coord = (monitor_width/2) - (w_of_wind/2)
        y_coord = (monitor_height/2) - (h_of_wind/2)
        self.home_win.geometry("%dx%d+%d+%d" % (w_of_wind, h_of_wind, x_coord, y_coord))

        self.welcome = ttk.Label(self.home_win, text="Welcome to Peek In",
        font=("Helvetica",12))

        self.image_viewer = ttk.Button(self.home_win,text="View Images",
        command=self.gallery_window)

        self.variable = tk.StringVar(self.home_win)
        dates=fetch_dates()

        try:
            self.variable.set(dates[-1])
        except:
            dates=["None"]

        self.select_dates = ttk.OptionMenu(self.home_win, self.variable, *dates)

        self.timer = ttk.Label(self.home_win)

        self.start_script = ttk.Button(self.home_win,text="Start Script",
        command=self.started_script)

        self.stop_script = ttk.Button(self.home_win,text="Stop Script",
        command=self.stop_script)
        # self.select_dates = ttk.Combobox(self.home_win, width=10, textvariable=self.variable)
        # try:
        #     self.variable.set(dates[-1])
        # except:
        #     self.select_dates['values']=("-|-")
        # self.select_dates.grid()
        self.timer["text"]='Timer set to {amt} seconds.'.format(amt=set_delay)

        self.hide_wins = ttk.Button(self.home_win,text="Close Window",command=self.hide)

        self.settings = ttk.Button(self.home_win,text="Settings",
        command=self.settings_window)

        self.quit_program = ttk.Button(self.home_win,text="Exit Progam",
        command=self.exit_program)

        self.master.withdraw()
        try:
            self.new_user_win.state()
        except:
            pass

        self.welcome.place(x=120,y=7)
        self.image_viewer.place(x=150,y=35)
        self.select_dates.place(x=155,y=70)
        self.timer.place(x=130,y=110)
        self.start_script.place(x=102,y=140)
        self.stop_script.place(x=202,y=140)
        self.hide_wins.place(x=45,y=190)
        self.settings.place(x=158,y=190)
        self.quit_program.place(x=258,y=190)

    def gallery_window(self):
        global total
        global pic_num
        global pic_timestamps
        global pictures
        ##  Check db to see if selected date exists
        total = retrieve_image(self.variable.get())

        if total:
            #Gallery opens only once on button click.
            try:
                self.win.state()
                return
            except:
                pass

            self.win=tk.Toplevel(self.master)
            self.win.protocol("WM_DELETE_WINDOW",self.close_gallery)

            ## pictures & pic_stamps referenced for gallery and saving pic to comp.
            pictures = ['gallery/' + x for x in os.listdir("gallery/") if x.endswith(pic_ext)]
            pictures=sort_gallery(pictures)
            with open("crnt.txt") as file:
                pic_timestamps = [line.strip() for line in file]
                pic_timestamps = sort_times(pic_timestamps)

            self.timestamp = ttk.Label(self.win)
            self.timestamp["text"]=pic_timestamps[0]

            self.pic_number = ttk.Label(self.win)
            self.pic_number["text"]="1 of " + str(total)

            self.next = ttk.Button(self.win,text="Next",command=self.next_pic)
            self.previous=ttk.Button(self.win,text="Previous",command=self.previous_pic)

            self.save_im=ttk.Button(self.win,text="Save To Desktop",command=self.save_img)

            self.delete_btn=ttk.Button(self.win,text="Delete Image",command=self.delete_im)

            self.delete_day=ttk.Button(self.win,text="Delete All",
                                    command=self.delete_day_all)

            self.back_button = ttk.Button(self.win,text="Close",
                                          command=self.close_gallery)

            img = Image.open('gallery/1'+pic_ext)
            self.img = ImageTk.PhotoImage(img)

            m_wd = self.master.winfo_screenwidth()
            pic_w, pic_h = self.img.width(), self.img.height()
            padding = (m_wd-pic_w)/2

            # win_size = str(cnv_w+20)+"x"+str(int(cnv_h+150))
            self.win.geometry("%dx%d+%d+%d" % (pic_w+40,pic_h+160,padding,10))

            self.pic_window = tk.Canvas(self.win,width=pic_w,height=pic_h)
            self.pic_window.create_image(10,0,anchor='nw',image=self.img)

            centr = pic_w/2
            self.pic_window.place(x=10,y=10)
            self.pic_number.place(x=centr+3,y=pic_h+10)
            self.timestamp.place(x=centr-15,y=pic_h+30)

            self.previous.place(x=centr-70,y=pic_h+50)
            self.next.place(x=centr+20,y=pic_h+50)

            self.save_im.place(x=centr-143,y=pic_h+85)
            self.delete_btn.place(x=centr-25,y=pic_h+85)
            self.delete_day.place(x=centr+75,y=pic_h+85)

            self.back_button.place(x=centr-20,y=pic_h+120)

            pic_num=1


    def settings_window(self):
        ##Make sure window doesn't open twice
        try:
            self.settings_win.state()
            return
        except:
            pass

        self.settings_win = tk.Toplevel(self.master)
        self.settings_win.resizable(False,False)

        w_of_wind = 350
        h_of_wind = 190
        monitor_width = self.master.winfo_screenwidth()
        monitor_height = self.master.winfo_screenheight()
        x_coord = (monitor_width/2) - (w_of_wind/2)
        y_coord = (monitor_height/2) - (h_of_wind/2)+15

        self.settings_win.geometry("%dx%d+%d+%d" % (w_of_wind,h_of_wind,x_coord,y_coord))

        self.set_delay = ttk.Button(self.settings_win,text="Set Timer Delay",
                        command=self.set_timer)

        self.enter_timer_delay = ttk.Entry(self.settings_win,text=set_delay,width=5)
        self.enter_timer_delay.delete(0,tk.END)
        self.enter_timer_delay.insert(0, set_delay)

        self.delete_account = ttk.Button(self.settings_win,text="Delete account",
                                        command=self.delete_account)
        # self.delete_database = ttk.Button(self.settings_win,text="Restart Database",
        #                                 command=self.delete_db)
        # self.delete_database.grid()
        self.delete_settings_win = ttk.Button(self.settings_win,text="  Close  ",
                                    command=self.settings_win.destroy)

        self.set_delay.place(x=120,y=15)
        self.enter_timer_delay.place(x=155,y=50)
        self.delete_account.place(x=75,y=90)
        self.delete_settings_win.place(x=190,y=90)

##  End of different windows^^

    def has_account(self):
        name = check_user()
        if name:
            self.login_window(name)
        else:
            self.create_account_page()


    def to_login(self):
        self.new_user_win.destroy()
        self.master.deiconify()
        self.login_window("")


    def check_credentials(self,event=None):
        global set_delay
        global win_title_prefix

        ##Setting wintitle for user-specific script recognition for end_script()
        name = win_title_prefix = self.enter_name.get()
        pasw = self.enter_pass.get()

        answer = validate_login(name,pasw)
        if answer:
            set_delay = check_time_delay()

            self.logged_in()
            if answer[1]==1:
                ## Var for ending crnt background process before restarting fresh.
                end_script()
                self.started_script()
                print("Started Script")
            elif answer == "Not answer":
                self.greet["text"]='Incorrect Password.'
            else:
                self.greet["text"]='Please enter a valid username\n or create a new one'


    def create_user(self):
        global set_delay
        global win_title_prefix

        name = self.enter_name2.get()
        passw = self.enter_pass2.get()
        win_title_prefix = name

        if 3<len(passw)<16:
            response = add_username(name,passw)

            if response == True:
                set_delay_time(5)
                set_delay = 5
                self.logged_in()
                self.new_user_win.destroy()
            else:
                self.greet['text']="Username exists"
        else:
            self.greet["text"]="Password must be longer than 4-15 characters."


    def next_pic(self):
        global pic_num
        if pic_num < total:
            img = Image.open(pictures[pic_num])
            pic_num+=1

        else:
            img = Image.open(pictures[0])
            pic_num=1
        self.img = ImageTk.PhotoImage(img)
        self.pic_window.create_image(40,40,anchor='nw',image=self.img)
        self.pic_number["text"]=str(pic_num) +" of " +str(total)
        self.timestamp["text"]=pic_timestamps[pic_num-1]


    def previous_pic(self):
        global pic_num
        if pic_num > 1:
            pic_num-=1
            img = Image.open(pictures[pic_num-1])
        else:
            pic_num=total
            img = Image.open(pictures[-1])
        self.img = ImageTk.PhotoImage(img)
        self.pic_window.create_image(40,40,anchor='nw',image=self.img)
        self.pic_number["text"]=str(pic_num) +" of " +str(total)
        self.timestamp["text"]=pic_timestamps[pic_num-1]


    def save_img(self):
        pic_path=self.timestamp.cget("text")
        save_to_comp(pic_path)


    def delete_im(self):
        global total
        global pic_num
        global pictures
        global pic_timestamps

        delete_image(self.timestamp.cget("text"))

        if total == 1:
            self.close_gallery()
            try:
                self.variable.set(dates[-1])
            except:
                self.variable.set("---")
            return

        pic_timestamps.remove(self.timestamp.cget("text"))
        if pic_num == 1:
            pictures.remove(pictures[0])
            self.timestamp["text"]=pic_timestamps[0]
            if total == 2:
                img = Image.open(pictures[0])
            else:
                img = Image.open(pictures[pic_num-1])
        else:
            pictures.remove(pictures[pic_num-1])
            if pic_num == total:
                pic_num -= 1
            path = pictures[pic_num-1]
            img = Image.open(path)
            self.timestamp["text"]=pic_timestamps[pic_num-1]


        self.img = ImageTk.PhotoImage(img)

        self.pic_window.create_image(40,40,anchor='nw',image=self.img)

        total -= 1
        self.pic_number["text"]=str(pic_num)+' of '+str(total)


    def delete_day_all(self):
        ok = messagebox.askokcancel(
            message="This will delete all pictures for this day, continue?")
        if not ok:
            return

        delete_day(self.variable.get())
        self.close_gallery()
        dates=fetch_dates()

        try:
            self.variable.set(dates[-1])
        except:
            self.variable.set("---")


    def delete_account(self):

        ok = messagebox.askokcancel(
          message="This will delete user and exit program.\n         Continue?")

        if not ok:
            return
        ## got var from hidden self.master entry box
        delete_user(self.enter_name.get())
        messagebox.showinfo(message=
        "Successfully removed from database\n          Program will now close")
        self.exit_program()


    # def delete_db(self):
    #
    #     ok = messagebox.askokcancel(
    #      message="All database information will be lost.\n         Continue?")
    #
    #     if not ok:
    #         return
    #     delete_database()
    #     print("Self done in delete db")


    def set_timer(self):
        global set_delay
        set_delay=int(self.enter_timer_delay.get())
        set_delay_time(set_delay)
        self.timer["text"]='Timer set to {amt} seconds.'.format(amt=set_delay)
        self.started_script()


    def started_script(self):
        global routine

        #Used try/except so when script is already running and started again
        #current script stops and is restarted to prevent multiple instances.
        try:
            routine
        except:
            pass
        else:
            self.after_cancel(routine)

        today = commence_script()
        # set date selector to today if currently none.
        if len(self.variable.get()) == 0:
            self.variable.set(today)
        routine = self.after(set_delay * 1000, self.started_script)

        ##  Renames title to enable subprocess to identify it.
        self.home_win.title(win_title_prefix+" Peek In (running)")

        dates=fetch_dates()
        self.variable.set(dates[-1])

        return routine


    def stop_script(self):
        self.home_win.title("Peek In")
        try:
            self.after_cancel(routine)
            self.script_on.pack_forget()
        except:
            pass
        script_off()


    def clear_gallery(self):
        gallery_grp = 'gallery/'
        t = [gallery_grp+x.name for x in Path(gallery_grp).iterdir()]
        for item in t:
            os.remove(item)
        try:
            os.remove("crnt.txt")
        except:
            pass

    def hide(self):

        try:
            self.home_win.withdraw()
        except:
            pass
        try:
            self.win.withdraw()
        except:
            pass
        print("Withdrew")

    def center_gallery(self):
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()

    ## Clears temporary gallery folder of pictures.
    def close_gallery(self):
        self.clear_gallery()
        self.win.destroy()


    def exit_program(self):
        script_off()
        self.clear_gallery()
        end_app()

###  END OF CLASS ###

##  Run before program loads to prevent multiple instances appearing
##  If run from inside program (tk button) it will close program.
def end_process():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call('cmd /c "taskkill /f /FI "WINDOWTITLE eq Peek In*"" /T'
                    ,shell=True,startupinfo=si)

## Ends user-specific script running bc window title was changed to "<user> Running Peek In"
def end_script():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.call('cmd /c "taskkill /f /FI "WINDOWTITLE eq {win_title}*"" /T'
        .format(win_title=win_title_prefix+" Peek In (running)"),shell=True,startupinfo=si)

##  Closes app in task manager to both end script if running and program gui
def end_app():
    end_process()
    end_script()

def main():
    create_database()
    # root = tk.Tk()
    root = ThemedTk(theme="arc")

    w_of_wind = 380
    h_of_wind = 180
    monitor_width = root.winfo_screenwidth()
    monitor_height = root.winfo_screenheight()
    x_coord = (monitor_width/2) - (w_of_wind/2)
    y_coord = (monitor_height/2) - (h_of_wind/2)
    root.geometry("%dx%d+%d+%d" % (w_of_wind, h_of_wind, x_coord, y_coord))
    root.resizable(False,False)

    root.title("Peek In")
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    end_process()
    main()


###  CHANGING Window titles is used in program for task manager call identification
###  Different states will either be left or ended depending on function.
###  IE "Peek In"-(Users script not running)  to "Running Peek in"-(Users script is running)
