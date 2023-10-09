import os, time
import datetime
from pathlib import Path
from PIL import ImageTk, Image
import threading

from concurrent.futures import Future

from tkinter import messagebox, PhotoImage
import tkinter as tk

# Styling Layer
from tkinter import ttk
from ttkthemes import ThemedTk

from app import commence_script
from utils import sort_gallery, sort_times
from create_db import create_database
from db_functions import *
from settings import *


class Application(ttk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.password_limiter = 0
        self.clear_gallery()
        self.has_account()

    ####   Login Window   ####
    ##########################

    def login_window(self, name):
        WIDTH_HEIGHT = 380, 180
        c = self.place_window_center(WIDTH_HEIGHT[0], WIDTH_HEIGHT[1])
        self.master.geometry("%dx%d+%d+%d" % (c[0], c[1], c[2], c[3]))
        self.master.resizable(False, False)

        self.new_account = ttk.Button(self.master, takefocus=False, text="Create Account",
                                      command=self.create_account_page)
        self.quit = ttk.Button(self.master, takefocus=False, text="Exit",
                               command=self.master.destroy)
        
        self.enter = ttk.Button(self.master, takefocus=False, text="Submit",
                                command=self.check_credentials)
        self.master.bind('<Return>', lambda event: self.check_credentials())

        self.greet = ttk.Label(
            self.master, text="Welcome", font=("Helvetica", 15))
        self.ask_name = ttk.Label(self.master, text="Enter Username")
        self.ask_pass = ttk.Label(self.master, text="Enter Password")

        self.enter_name = ttk.Entry(self.master)
        self.enter_name.insert(0, name)
        self.enter_name.focus()
        self.enter_pass = ttk.Entry(self.master, show="*")

        self.radio_var = tk.IntVar(self.master)
        self.check_btn = ttk.Checkbutton(
            self.master, takefocus=False, text="Auto-login", variable=self.radio_var)

        self.greet.place(x=160, y=10)
        self.ask_name.place(x=60, y=52)
        self.enter_name.place(x=150, y=50)
        self.ask_pass.place(x=62, y=82)
        self.enter_pass.place(x=149, y=80)
        self.check_btn.place(x=148, y=105)

        self.new_account.place(x=33, y=130)
        self.enter.place(x=160, y=130)
        self.quit.place(x=260, y=130)


    ####   Create Account   ####
    ############################

    def create_account_page(self):
        self.master.withdraw()

        self.new_user_win = tk.Toplevel(self.master)
        # self.new_user_win.protocol('WM_DELETE_WINDOW', end_process)
        self.new_user_win.protocol('WM_DELETE_WINDOW', self.destroy)
        self.new_user_win.resizable(False, False)

        WIDTH_HEIGHT = 350, 200
        c = self.place_window_center(WIDTH_HEIGHT[0], WIDTH_HEIGHT[1])
        self.new_user_win.geometry("%dx%d+%d+%d" % (c[0], c[1], c[2], c[3]))

        self.submit = ttk.Button(self.new_user_win, takefocus=False, text="Submit",
                                 command=self.create_user)
        self.back_to_login = ttk.Button(self.new_user_win, takefocus=False, text="Sign In",
                                        command=self.to_login_window)
        self.quit = ttk.Button(self.new_user_win, takefocus=False, text="Exit",
                               command=self.master.destroy)

        self.name_entry = ttk.Entry(self.new_user_win)
        self.name_entry.focus()
        self.pass_entry = ttk.Entry(self.new_user_win, show="*")
        self.confirm_entry = ttk.Entry(self.new_user_win, show="*")

        self.name_label = ttk.Label(self.new_user_win, text="Enter Username")
        self.pass_label = ttk.Label(self.new_user_win, text="Enter Password")
        self.confirm_label = ttk.Label(self.new_user_win,
                                       text="Confirm Password")
        self.info = ttk.Label(self.new_user_win, text="Create A New Account",
                              font=("Helvetica", 15))

        self.info.place(x=85, y=8)
        self.name_label.place(x=59, y=50)
        self.name_entry.place(x=145, y=48)

        self.pass_label.place(x=61, y=80)
        self.pass_entry.place(x=145, y=77)

        self.confirm_label.place(x=45, y=110)
        self.confirm_entry.place(x=145, y=106)

        self.back_to_login.place(x=30, y=145)
        self.submit.place(x=128, y=145)
        self.quit.place(x=228, y=145)

    ####  Home Window   ####
    ########################

    def home_window(self):
        self.master.withdraw()

        self.home_win = tk.Toplevel(self.master)
        self.home_win.title("Peek In")
        self.home_win.protocol('WM_DELETE_WINDOW', self.hide)
        self.home_win.resizable(False, False)
        WIDTH_HEIGHT = 367, 300
        c = self.place_window_center(WIDTH_HEIGHT[0], WIDTH_HEIGHT[1])
        self.home_win.geometry("%dx%d+%d+%d" % (c[0], c[1], c[2], c[3]))

        self.variable = tk.StringVar(self.home_win)
        dates = fetch_dates()
        if dates:
            self.select_dates = ttk.OptionMenu(self.home_win, self.variable,
                                               dates[0], *dates)
        else:
            dates = ["---"]
            self.select_dates = ttk.OptionMenu(self.home_win, self.variable,
                                               *dates)

        self.image_viewer = ttk.Button(self.home_win, takefocus=False, text="View Images",
                                       command=self.gallery_window)


        # self.start_script = ttk.Button(self.home_win, takefocus=False, text="Start",
        #                                command=self.started_script)
        self.start_script = ttk.Button(self.home_win, takefocus=False, text="Start",
                                       command=self.started_script)

        self.stop_script_btn = ttk.Button(self.home_win, takefocus=False, text="Stop",
                                          command=self.stop_script)
        self.hide_wins = ttk.Button(self.home_win, takefocus=False, text="Hide Window",
                                    command=self.hide)
        self.settings = ttk.Button(self.home_win, takefocus=False, text="Settings",
                                   command=self.settings_window)
        self.logout_btn = ttk.Button(self.home_win, takefocus=False, text="  Logout  ",
                                     command=self.logout)
        self.quit_program = ttk.Button(self.home_win, takefocus=False, text="Exit Program",
                                       command=self.exit_program)

        self.welcome = ttk.Label(self.home_win, text="Peek In",
                                 font=(TITLE_FONT))
        self.timer = ttk.Label(self.home_win, font='Helvetica 11 bold')

        amt = set_delay
        self.timer["text"] = 'Timer set to {amount} second{s}'.format(
            amount=amt, s="s" if amt != 1 else "")

        self.welcome.place(x=150, y=7)
        self.image_viewer.place(x=135, y=35)
        self.select_dates.place(x=140, y=70)

        self.timer.place(x=107, y=110)

        self.start_script.place(x=95, y=140)
        self.stop_script_btn.place(x=190, y=140)

        self.hide_wins.place(x=89, y=185)
        self.settings.place(x=195, y=185)

        self.logout_btn.place(x=96, y=230)
        self.quit_program.place(x=190, y=230)

    ####   Settings Window   ####
    #############################

    def settings_window(self):
        # Make sure window doesn't open twice
        try:
            self.settings_win.state()
            return
        except:
            pass

        self.settings_win = tk.Toplevel(self.master)
        self.settings_win.resizable(False, False)

        WIDTH_HEIGHT = 300, 270
        c = self.place_window_center(WIDTH_HEIGHT[0], WIDTH_HEIGHT[1],
                                     height_offset=15)
        self.settings_win.geometry("%dx%d+%d+%d" % (c[0], c[1], c[2], c[3]))

        self.set_delay = ttk.Button(self.settings_win, takefocus=False,
                                    text="Set Timer Delay", command=self.set_timer)
        self.delete_user = ttk.Button(self.settings_win, takefocus=False,
                                      text="Delete account", command=self.delete_account)
        self.delete_settings_win = ttk.Button(self.settings_win, takefocus=False,
                                              text="  Close  ", command=self.settings_win.destroy)

        self.check_var = tk.IntVar(self.settings_win)
        self.auto_login_toggle = ttk.Checkbutton(self.settings_win, takefocus=False, text="Auto-login", variable=self.check_var,
                                                 command=self.switch_auto_login)

        self.enter_timer_delay = ttk.Entry(self.settings_win, width=5)
        self.enter_timer_delay.delete(0, tk.END)
        self.enter_timer_delay.insert(0, set_delay)
        # Start the cursor on the time delay box
        self.enter_timer_delay.focus()

        self.setting_label = ttk.Label(self.settings_win, text="Settings", font=("Helvetica", 14))

        self.delay_label = ttk.Label(self.settings_win, text="Screenshot's delay in minutes.", font=("Helvetica", 11))

        self.auto_login_label = ttk.Label(self.settings_win, text="Set auto-login state", font=("Helvetica", 11))


        if check_auto_login() == 1:
            self.auto_login_toggle.invoke()

        self.setting_label.place(x=120, y=12)
        
        self.delay_label.place(x=50, y=50)
        self.set_delay.place(x=76, y=75)
        self.enter_timer_delay.place(x=184, y=78)

        self.auto_login_label.place(x=90, y=125)
        self.auto_login_toggle.place(x=115, y=149)

        self.delete_user.place(x=60, y=200)
        self.delete_settings_win.place(x=170, y=200)

    ####   Gallery Window   ####
    ############################

    def gallery_window(self):
        global total
        global PIC_NUM
        global pic_timestamps
        global pictures
        global anchor_offset
        # Check db to see if selected date exists
        total = retrieve_image(self.variable.get())

        if total:
            # Make sure Gallery opens only once with button click.
            try:
                self.win.state()
                return
            except:
                pass

            self.win = tk.Toplevel(self.master)
            self.win.protocol("WM_DELETE_WINDOW", self.close_gallery)

            # pictures & pic_stamps referenced for gallery
            # and saving pic to comp.
            pictures = ['gallery/' + x for x in os.listdir("gallery/")
                        if x.endswith(PIC_EXT)]
            pictures = sort_gallery(pictures)
            with open("crnt.txt") as file:
                pic_timestamps = [line.strip() for line in file]
                pic_timestamps = sort_times(pic_timestamps)

            self.next = ttk.Button(self.win, takefocus=False, text="Next",
                                   command=self.next_pic)
            self.previous = ttk.Button(self.win, takefocus=False, text="Previous",
                                       command=self.previous_pic)
            self.save_im = ttk.Button(self.win, takefocus=False, text="Save To Desktop",
                                      command=self.save_img)
            self.delete_btn = ttk.Button(self.win, takefocus=False, text="Delete Image",
                                         command=self.delete_im)
            self.delete_day = ttk.Button(self.win, takefocus=False, text="Delete All",
                                         command=self.delete_day_all)
            self.back_button = ttk.Button(self.win, takefocus=False, text="Close",
                                          command=self.close_gallery)

            self.timestamp = ttk.Label(self.win)
            self.timestamp["text"] = pic_timestamps[0]
            self.pic_number = ttk.Label(self.win)
            self.pic_number["text"] = "1 of " + str(total)

            img = Image.open('gallery/1'+PIC_EXT)
            self.img = ImageTk.PhotoImage(img)

            m_wd = self.master.winfo_screenwidth()
            pic_w, pic_h = self.img.width(), self.img.height()
            padding = (m_wd-pic_w)/2

            mon_width = self.master.winfo_screenwidth()
            mon_height = self.master.winfo_screenheight()
            centr = pic_w/2
            self.pic_window = tk.Canvas(self.win, width=pic_w, height=pic_h)

            # For 1080p resolution
            if mon_width == 1920 and mon_height == 1080:
                anchor_offset = 0
                self.win.geometry("%dx%d+%d+%d" %
                                  (pic_w+25, pic_h+110, padding, 1))
                self.pic_window.create_image(anchor_offset, 0, anchor='nw',
                                             image=self.img)

                self.pic_window.place(x=10, y=10)
                self.pic_number.place(x=centr+3, y=pic_h+10)
                self.timestamp.place(x=centr-17, y=pic_h+29)

                self.previous.place(x=centr-130, y=pic_h+15)
                self.next.place(x=centr+80, y=pic_h+15)

                self.save_im.place(x=centr-143, y=pic_h+47)
                self.delete_btn.place(x=centr-25, y=pic_h+47)
                self.delete_day.place(x=centr+75, y=pic_h+47)

                self.back_button.place(x=centr-20, y=pic_h+78)
            else:
                # For 3440x1440 resolution
                anchor_offset = 10
                self.win.geometry("%dx%d+%d+%d" %
                                  (pic_w+40, pic_h+160, padding, 10))
                self.pic_window.create_image(anchor_offset, 0, anchor='nw',
                                             image=self.img)

                self.pic_window.place(x=10, y=10)
                self.pic_number.place(x=centr+3, y=pic_h+13)
                self.timestamp.place(x=centr-10, y=pic_h+30)

                self.previous.place(x=centr-66, y=pic_h+53)
                self.next.place(x=centr+22, y=pic_h+53)

                self.save_im.place(x=centr-143, y=pic_h+85)
                self.delete_btn.place(x=centr-27, y=pic_h+85)
                self.delete_day.place(x=centr+71, y=pic_h+85)

                self.back_button.place(x=centr-23, y=pic_h+122)

            PIC_NUM = 1

##########################################
#        ^^^^^^^^^^^^^^^^^^^^^^^         #
#    End of Different GUI Window Code    #
#                                        #
##########################################

    def has_account(self):
        global CRNT_USER

        info = find_last_user()
        if info:
            CRNT_USER = info[0]

            if info[1] == 0:
                self.login_window(info[0])
            else:
                self.auto_login(info[0], info[1])
        else:
            self.create_account_page()

    def to_login_window(self):
        self.new_user_win.destroy()
        self.master.deiconify()
        self.login_window("")

    def switch_auto_login(self):
        if self.check_var == 1:
            manage_auto_login(1)
            self.check_var = 0
        else:
            manage_auto_login(0)
            self.check_var = 1

    def auto_login(self, name, key):
        global set_delay
        global CRNT_USER

        CRNT_USER = name

        db_auto_login(name, key)
        set_delay = check_time_delay()
        self.home_window()

    def check_credentials(self, event=None):

        global set_delay
        global CRNT_USER

        CRNT_USER = self.enter_name.get()
        pasw = self.enter_pass.get()

        answer = validate_login(CRNT_USER, pasw)

        if self.password_limiter == MAX_TRIES:
            messagebox.askokcancel(
                message="Too many guesses.  Please wait 15 seconds before trying again.")
            self.too_many_guesses()
            return

        if answer == "Not found":
            messagebox.askokcancel(
                message="Please enter a valid username\n or create a new one")
            return

        if answer == "Pass incorrect":
            messagebox.askokcancel(message="Invalid password.")
            self.password_limiter += 1
            return

        set_delay = check_time_delay()

        self.home_window()

        if self.radio_var.get() == True:
            manage_auto_login(0)

        elif check_auto_login() == 1:
            manage_auto_login(1)

    def too_many_guesses(self):

        if self.password_limiter == 6:
            self.enter['state'] = 'disabled'
            self.new_account['state'] = 'disabled'
            routine = self.after(15000, self.too_many_guesses)
            self.password_limiter = 0
            return routine
        else:
            self.enter['state'] = 'normal'
            self.new_account['state'] = 'normal'
            return

    def create_user(self):
        global set_delay
        global CRNT_USER

        if self.pass_entry.get() != self.confirm_entry.get():
            messagebox.askokcancel(message="Passwords do not match.")
            return

        if not self.name_entry.get()[0].isalpha():
            messagebox.askokcancel(
                message="Username must start with a letter.")
            return

        name = self.name_entry.get().lower()
        passw = self.pass_entry.get()
        CRNT_USER = name

        if 3 < len(passw) < 30:
            response = add_username(name, passw)

            if response == True:
                set_delay_time(5)
                set_delay = 5
                self.home_window()
                self.new_user_win.destroy()
            else:
                messagebox.askokcancel(message="Username already exists.")
        else:
            messagebox.askokcancel(
                message="Password must be longer than 4 characters.")

    def next_pic(self):

        global PIC_NUM

        if total == 1:
            return

        if PIC_NUM < total:
            img = Image.open(pictures[PIC_NUM])
            PIC_NUM += 1

        else:
            img = Image.open(pictures[0])
            PIC_NUM = 1
        self.img = ImageTk.PhotoImage(img)
        self.pic_window.create_image(anchor_offset, 0, anchor='nw',
                                     image=self.img)
        self.pic_number["text"] = str(PIC_NUM) + " of " + str(total)
        self.timestamp["text"] = pic_timestamps[PIC_NUM-1]

    def previous_pic(self):

        global PIC_NUM

        if total == 1:
            return

        if PIC_NUM > 1:
            PIC_NUM -= 1
            img = Image.open(pictures[PIC_NUM-1])
        else:
            PIC_NUM = total
            img = Image.open(pictures[-1])
        self.img = ImageTk.PhotoImage(img)
        self.pic_window.create_image(anchor_offset, 0, anchor='nw',
                                     image=self.img)
        self.pic_number["text"] = str(PIC_NUM) + " of " + str(total)
        self.timestamp["text"] = pic_timestamps[PIC_NUM-1]

    def save_img(self):

        pic_path = self.timestamp.cget("text")
        save_to_comp(pic_path)

    def delete_im(self):

        global total
        global PIC_NUM
        global pictures
        global pic_timestamps

        delete_image(self.timestamp.cget("text"))

        if total == 1:
            self.update_dates_menu()
            self.close_gallery()
            return

        pic_timestamps.remove(self.timestamp.cget("text"))
        if PIC_NUM == 1:
            pictures.remove(pictures[0])
            self.timestamp["text"] = pic_timestamps[0]
            if total == 2:
                img = Image.open(pictures[0])
            else:
                img = Image.open(pictures[PIC_NUM-1])
        else:
            pictures.remove(pictures[PIC_NUM-1])
            if PIC_NUM == total:
                PIC_NUM -= 1
            path = pictures[PIC_NUM-1]
            img = Image.open(path)
            self.timestamp["text"] = pic_timestamps[PIC_NUM-1]

        self.img = ImageTk.PhotoImage(img)

        mon_width = self.master.winfo_screenwidth()
        mon_height = self.master.winfo_screenheight()

        if mon_width == 1920 and mon_height == 1080:
            anchor_offset = 0
        else:
            anchor_offset = 10
        self.pic_window.create_image(
            anchor_offset, 0, anchor='nw', image=self.img)

        total -= 1
        self.pic_number["text"] = str(PIC_NUM) + ' of ' + str(total)

    def delete_day_all(self):
        # Deletes entire days photos
        # Option is only accessible in the gallery window

        self.delete_day["state"] = "disabled"
        ok = messagebox.askokcancel(
            message="This will delete all pictures for this day, continue?")
        self.delete_day["state"] = "normal"

        if not ok:
            return

        delete_day(self.variable.get())
        self.close_gallery()
        self.update_dates_menu()

    def delete_account(self):
        self.delete_user["state"] = "disabled"
        ok = messagebox.askokcancel(
            message="This will delete user and exit program.\n{x}Continue?"
            .format(x=" "*22))
        self.delete_user["state"] = "normal"

        if not ok:
            return

        delete_user(CRNT_USER)

        messagebox.askokcancel(message="{s} successfully removed from database.\n{x}Program will now close"
                               .format(s=CRNT_USER, x=" "*15))
        self.destroy()


    def started_script(self):
        global routine

        # start= time.time()
        # print(start)
        # print(start - time.time())
        
        # Try/except so when script is already running and started again
        # current script stops to prevent multiple instances.
        try:
            routine
        except:
            pass
        else:
            self.after_cancel(routine)

        today = threading.Thread(target=commence_script).start()
        
        self.update_dates_menu()

        if self.variable.get() == "---":
            self.variable.set(today)

        self.home_win.title("Peek In - Running ")

        routine = self.after(set_delay * 1000, self.started_script)
        return routine

    def set_timer(self):
        global set_delay
        try:
            int(self.enter_timer_delay.get())
            set_delay = int(self.enter_timer_delay.get())
            if len(str(set_delay)) > 4:
                messagebox.askokcancel(
                message="The timer's interval must be less than 5 digits long.")
                self.enter_timer_delay.delete(0, tk.END)
            elif len(str(set_delay)) < 1:
                messagebox.askokcancel(
                message="The timer's interval must be over 1 second.")
            set_delay_time(set_delay)
            self.timer["text"] = 'Timer set to {amount} second{s}'.format(
                amount=set_delay, s="s" if set_delay != 1 else "")
        except:
            self.enter_timer_delay.delete(0, tk.END)


    def stop_script(self):
        self.home_win.title("Peek In")
        try:
            self.after_cancel(routine)
        except:
            pass
        script_off()


    def update_dates_menu(self):
        menu = self.select_dates["menu"]
        menu.delete(0, tk.END)
        dates = fetch_dates()

        if dates:
            for item in dates:
                menu.add_command(label=item, command=lambda value=item:
                                 self.variable.set(value))
            return
        self.variable.set("---")

    def hide(self):

        self.home_win.withdraw()

        try:
            self.win.withdraw()
        except:
            pass
        try:
            self.settings_win.withdraw()
        except:
            pass

    # Generates coordinates for a windows "geometry" method.
    def place_window_center(self, width, height, height_offset=0):
        monitor_width = self.master.winfo_screenwidth()
        monitor_height = self.master.winfo_screenheight()

        x_coord = (monitor_width/2) - (width/2)
        y_coord = (monitor_height/2) - (height/2)
        if height_offset != 0:
            y_coord += height_offset
        return width, height, x_coord, y_coord

    def logout(self):

        self.stop_script()
        self.home_win.destroy()
        self.master.deiconify()
        self.login_window(CRNT_USER)

        # auto-login to off
        if check_auto_login() == 1:
            manage_auto_login(1)

        try:
            self.settings_win.destroy()
        except:
            pass
        try:
            self.win.destroy()
        except:
            pass

    def close_gallery(self):
        self.clear_gallery()
        self.win.destroy()
        threading.Thread(target=vacuum_db).start()


    # Clears temporary gallery folder of pictures.
    def clear_gallery(self):
        gallery_grp = 'gallery/'
        t = [gallery_grp+x.name for x in Path(gallery_grp).iterdir()]
        for item in t:
            os.remove(item)
            try:
                os.remove("crnt.txt")
            except:
                pass

    def exit_program(self):

        script_off()
        self.clear_gallery()
        self.master.destroy()

##########                  ###########
#####  End of Application Class  ######
##########                  ###########


def main():
    create_database()
    root = ThemedTk(theme="arc")
    root.title("Peek In")
    # icon = PhotoImage(file='')
    # root.iconphoto(True, icon)

    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':

    main()