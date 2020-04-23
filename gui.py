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
        self.pack()
        self.has_account()


    def has_account(self):
        name = check_user()
        if name:
            self.login_page(name)
        else:
            self.login_page("None")
            self.create_account_page()


    def login_page(self,name):
        self.enter = ttk.Button(self,text="Submit",command=self.check_credentials)
        self.new_account = ttk.Button(self,text="Create Account",
                                      command=self.create_account_page)
        self.quit = ttk.Button(self,text="Exit",
                               command=self.master.destroy)

        self.greet = ttk.Label(self,)
        self.greet["text"]="Welcome"
        self.greet.pack()
        # self.change = ttk.Button(self,text='change',command=self.changer)
        # self.change.pack()

        self.ask_pass = ttk.Label(self)
        self.ask_pass["text"]="Enter Password"

        self.enter_name = ttk.Entry(self)
        self.enter_name.insert(0,name)
        self.enter_name.pack()

        self.enter_pass = ttk.Entry(self,show="*")
        self.enter_pass.insert(0,"Scott1")
        self.enter_pass.pack()

        self.ask_pass.pack()
        self.enter.pack()
        self.new_account.pack()
        self.quit.pack()
        self.clear_gallery()


    # global i
    # i=0
    #
    # def changer(self):
    #     global i
    #     pixmap_themes = [
    #     "breeze",
    #     "Equilux",
    #     "ITFT1",
    #     "arc",
    #     "blue",
    #     "clearlooks",
    #     "elegance",
    #     "kroc",
    #     "plastik",
    #     "radiance",
    #     "winxpblue"
    #     ]
    #     s =  ttk.Style()
    #     print(i)
    #     s.theme_use(pixmap_themes[i])
    #     i+=1




    def create_account_page(self, event=None):
        self.new_account.pack_forget()
        self.enter_name.pack_forget()
        self.enter_pass.pack_forget()
        self.ask_pass.pack_forget()
        self.enter.pack_forget()
        self.quit.pack_forget()
        self.enter_name.delete(0,ttk.END)
        self.enter_pass.delete(0,tk.END)
        self.greet['text']="Create Account"
        self.enter.configure(command=self.create_user)

        self.ask_name = ttk.Label(self)
        self.ask_name["text"]="Enter Username"
        self.ask_name.pack()
        self.enter_name.pack()
        self.ask_pass.pack()
        self.enter_name.pack()
        self.enter_pass.pack()
        self.enter.pack()

        self.back_to_login = ttk.Button(self,text="Sign In",
        command=self.to_login)
        self.back_to_login.pack()
        self.quit.pack()

    def to_login(self):
        self.ask_pass.pack_forget()
        self.back_to_login.pack_forget()
        self.ask_name.pack_forget()
        self.quit.pack_forget()
        self.enter_name.pack_forget()
        self.enter_pass.pack_forget()
        self.greet.pack_forget()
        self.enter.pack_forget()
        self.login_page("")


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

        name = self.enter_name.get()
        passw = self.enter_pass.get()
        win_title_prefix = name

        if 3<len(passw)<16:
            response = add_username(name,passw)

            if response == True:
                set_delay_time(5)
                set_delay = 5
                self.logged_in()
            else:
                self.greet['text']="Username exists"
        else:
            self.greet["text"]="Password must be longer than 4-15 characters."


    def logged_in(self):

        self.home_win = tk.Toplevel(self.master)

        self.home_win.title("Peek In")
        self.home_win.protocol('WM_DELETE_WINDOW',self.hide)
        self.home_win.resizable(False,False)

        w_of_wind = 380
        h_of_wind = 290
        monitor_width = self.master.winfo_screenwidth()
        monitor_height = self.master.winfo_screenheight()
        x_coord = (monitor_width/2) - (w_of_wind/2)
        y_coord = (monitor_height/2) - (h_of_wind/2)
        self.home_win.geometry("%dx%d+%d+%d" % (w_of_wind, h_of_wind, x_coord, y_coord))


        self.timer = ttk.Label(self.home_win)
        self.timer.pack()

        self.start_script = ttk.Button(self.home_win,text="Start Script",
                            command=self.started_script)

        dates=fetch_dates()

        self.variable = tk.StringVar(self.home_win)

        # try:
        #     self.variable.set(dates[-1])
        # except:
        #     dates=["None"]
        # #
        self.variable.set(dates[-1])

        # self.select_dates = tk.OptionMenu(self.home_win, self.variable, *dates)
        # self.select_dates.pack()

        self.select_dates = ttk.Combobox(self.home_win, width=10, textvariable=self.variable)
        try:
            self.variable.set(dates[-1])
        except:
            self.select_dates['values']=("-|-")
        self.select_dates.pack()


        self.image_viewer = ttk.Button(self.home_win,text="View Images",
                            command=self.gallery_window)
        self.image_viewer.pack()
        self.start_script.pack()

        self.stop_script = ttk.Button(self.home_win,text="Stop Script",
                           command=self.stop_script)
        self.stop_script.pack()

        self.timer["text"]='Timer set to {amt} seconds.'.format(amt=set_delay)


        self.hide_wins = ttk.Button(self.home_win,text="Close Window",command=self.hide)
        self.hide_wins.pack()

        self.settings = ttk.Button(self.home_win,text="Settings",
                                 command=self.settings_window)
        self.settings.pack()

        self.quit_program = ttk.Button(self.home_win,text="Exit Progam",
                               command=self.exit_program)
        self.quit_program.pack()
        self.master.withdraw()


    def gallery_window(self):
        global total
        global pic_num
        global pic_timestamps
        ## These 3 vars used for image viewer gallery and db calls.

        global pictures
        ## pictures var used to organize current selectable gallery pictures.
        ## It is read from by next and previous pic btns and adjusted with delete_im

        ##  Checking db to see if selected date has data
        total = retrieve_image(self.variable.get())

        if total:
            ##Makes sure gallery doesn't reopen when button's pressed and it's open.
            try:
                self.win.state()
                return
            except:
                pass

            self.win=tk.Toplevel(self.master)
            self.win.protocol("WM_DELETE_WINDOW",self.close_gallery)
            # self.win.resizable(False,False)
            ## pictures & pic_stamps referenced for gallery and saving pic to comp.
            pictures = ['gallery/' + x for x in os.listdir("gallery/") if x.endswith(pic_ext)]
            pictures=sort_gallery(pictures)
            with open("crnt.txt") as file:
                pic_timestamps = [line.strip() for line in file]
            pic_timestamps = sort_times(pic_timestamps)


            self.pic_number = ttk.Label(self.win)
            self.pic_number["text"]="1 of " + str(total)
            self.pic_number.pack()

            self.next = ttk.Button(self.win,text="Next",command=self.next_pic)
            self.next.pack()
            self.previous=ttk.Button(self.win,text="Previous",command=self.previous_pic)
            self.previous.pack()

            self.delete_btn=ttk.Button(self.win,text="Delete Image",command=self.delete_im)
            self.delete_btn.pack()

            self.delete_day=ttk.Button(self.win,text="Delete All",
                                    command=self.delete_day_all)
            self.delete_day.pack()

            self.save_im=ttk.Button(self.win,text="Save To Desktop",command=self.save_img)
            self.save_im.pack()

            self.timestamp = ttk.Label(self.win)
            self.timestamp["text"]=pic_timestamps[0]
            self.timestamp.pack()

            img = Image.open('gallery/1'+pic_ext)
            self.img = ImageTk.PhotoImage(img)

            cnv_w = self.img.width()
            cnv_h = cnv_w*.42
            win_width = str(cnv_w+90)+"x"+str(int(cnv_h+150))

            # monitor_width = self.master.winfo_screenwidth()
            # monitor_height = self.master.winfo_screenheight()

            self.win.geometry(win_width+str(50))

            self.pic_window = tk.Canvas(self.win,width=cnv_w,height=cnv_h)
            self.pic_window.create_image(40,40,anchor='nw',image=self.img)
            self.pic_window.pack()

            self.back_button = ttk.Button(self.win,text="Close",
                                          command=self.close_gallery)
            self.back_button.pack()

            pic_num=1


    def settings_window(self):
        self.settings_win = tk.Toplevel(self.master)
        self.settings_win.resizable(False,False)

        w_of_wind = 380
        h_of_wind = 210
        monitor_width = self.master.winfo_screenwidth()
        monitor_height = self.master.winfo_screenheight()
        x_coord = (monitor_width/2) - (w_of_wind/2)
        y_coord = (monitor_height/2) - (h_of_wind/2)+15

        self.settings_win.geometry("%dx%d+%d+%d" % (w_of_wind,h_of_wind,x_coord,y_coord))

        self.set_delay = ttk.Button(self.settings_win,text="Set Timer Delay",
                        command=self.set_timer)
        self.set_delay.pack()

        self.enter_timer_delay = ttk.Entry(self.settings_win,text=set_delay,width=5)
        self.enter_timer_delay.insert(0, set_delay)
        self.enter_timer_delay.pack()

        self.delete_account = ttk.Button(self.settings_win,text="Delete account",
                                        command=self.delete_account)
        self.delete_account.pack()
        # self.delete_database = ttk.Button(self.settings_win,text="Restart Database",
        #                                 command=self.delete_db)
        # self.delete_database.pack()
        self.delete_settings_win = ttk.Button(self.settings_win,text="Close",
                                    command=self.settings_win.destroy)
        self.delete_settings_win.pack()


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

        # self.script_on.pack()

        ##  Renames title to enable subprocess to identify it.
        # self.home_win.title(win_title_prefix+" Running Peek In")
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


    def exit_program(self):
        script_off()
        self.clear_gallery()
        end_app()


    ## Clears temporary gallery folder of pictures.
    def close_gallery(self):
        self.clear_gallery()
        self.win.destroy()


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
    h_of_wind = 210
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
