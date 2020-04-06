import os, subprocess
import tkinter as tk
from pathlib import Path
from PIL import ImageTk, Image


from app import commence_script, sort_gallery, sort_times
from create_db import create_database
from db_functions import (add_username, validate_login, retrieve_image,
            set_delay_time, check_time_delay, fetch_dates, delete_image,
            delete_day, script_off, check_script, save_to_comp)

global set_delay
global pic_num
pic_num = 1
#pic_ext var in db_functions file and app file also. Used .jpg
#to reduce pic size, other ext should work. Eg ".png". Need to
#change im.save(initial pic) "quality" kwarg in app.py also to modify
pic_ext=".jpg"


class Application(tk.Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.pack()
        self.login()



    def login(self):
        self.enter = tk.Button(self,text="Submit",command=self.check_credentials)
        self.new_account = tk.Button(self,text="Create Account",
                                      command=self.create_account_page)
        self.quit = tk.Button(self,text="Exit",fg="red",
                               command=self.master.destroy)

        self.greet = tk.Label(self,bg='lightblue')
        self.greet["text"]="Welcome!\n Please sign in."
        self.greet.pack()

        self.ask_name = tk.Label(self)
        self.ask_name["text"]="Enter Username"

        self.ask_pass = tk.Label(self)
        self.ask_pass["text"]="Enter Password"

        self.enter_name = tk.Entry(self)
        self.enter_name.insert(0,"Scott")
        self.enter_name.pack()

        self.enter_pass = tk.Entry(self,show="*")
        self.enter_pass.insert(0,"Scott1")
        self.enter_pass.pack()

        self.ask_name.pack()
        self.ask_pass.pack()
        self.enter.pack()
        self.new_account.pack()
        self.quit.pack()
        self.clear_gallery()


    def check_credentials(self,event=None):
        global set_delay

        name = self.enter_name.get()
        pasw = self.enter_pass.get()
        answer = validate_login(name,pasw)

        if answer:
            set_delay = check_time_delay()
            self.logged_in()
            if answer[1]==1:
                end_script()
                self.started_script()
                print("Started Script")
        elif answer == "Not answer":
            self.greet["text"]='Incorrect Password.'
        else:
            self.greet["text"]='Please enter a valid username\n or create a new one'


    def create_account_page(self, event=None):
        self.new_account.pack_forget()
        self.enter.pack_forget()
        self.quit.pack_forget()
        # self.enter_name.delete(0,tk.END)
        # self.enter_pass.delete(0,tk.END)
        self.create_new_account = tk.Button(self,text="Submit",
                                             command=self.create_user)
        self.create_new_account.pack()
        self.quit.pack()
        self.greet['text']="Enter name and password."


    def create_user(self):
        global set_delay

        name = self.enter_name.get()
        passw = self.enter_pass.get()

        if 3<len(passw)<16:
            response = add_username(name,passw)

            if response == True:
                self.create_new_account.pack_forget()
                set_delay_time(5)
                set_delay = 5
                self.logged_in()
            else:
                self.greet['text']="Username exists"
        else:
            self.greet["text"]="Password must be longer than 4-15 characters."


    def logged_in(self):
        self.home_win = tk.Toplevel(self.master)

        self.home_win.title("Peek In main()")
        self.home_win.protocol('WM_DELETE_WINDOW',self.hide)

        self.home_win.geometry("380x290")


        self.instruct = tk.Label(self.home_win)
        self.instruct["text"]="\nSelect your preferences to begin program."
        self.instruct.pack()

        self.enter_timer_delay = tk.Entry(self.home_win,text=set_delay,width=5)
        self.enter_timer_delay.pack()

        self.set_delay = tk.Button(self.home_win,text="Set Timer Delay",
                        command=self.set_timer)
        self.set_delay.pack()


        self.timer = tk.Label(self.home_win)
        self.timer.pack()

        self.script_on = tk.Label(self.home_win)
        self.script_on["text"]="Running"

        self.start_script = tk.Button(self.home_win,text="Start Script",
                            command=self.started_script)
        self.start_script.pack()

        dates=fetch_dates()

        self.variable = tk.StringVar(self.home_win)

        try:
            self.variable.set(dates[-1])
        except:
            dates=["None"]

        self.select_dates = tk.OptionMenu(self.home_win, self.variable, *dates)
        self.select_dates.pack()


        self.image_viewer = tk.Button(self.home_win,text="View Images",
                            command=self.gallery)
        self.image_viewer.pack()

        self.stop_script = tk.Button(self.home_win,text="Stop",
                           command=self.stop_script)
        self.stop_script.pack()

        self.timer["text"]='Timer set to {amt} seconds.'.format(amt=set_delay)
        self.enter_timer_delay.insert(0, set_delay)

        self.hide_wins = tk.Button(self.home_win,text="Close Window",command=self.hide)
        self.hide_wins.pack()
        self.quit_program = tk.Button(self.home_win,text="Exit Progam",fg="red",
                               command=self.exit_program)
        self.quit_program.pack()
        self.master.withdraw()


    def gallery(self):
        global total
        global pic_num
        global pic_timestamps
        global pictures
        ## pictures var used to organize current selectable gallery pictures.
        ## It is read from by next and previous pic btns and adjusted with delete_im

        ##  Checking db to see if selected date has data
        total = retrieve_image(self.variable.get())
        if total:

            self.win=tk.Toplevel(self.master)
            self.win.protocol("WM_DELETE_WINDOW",self.close_gallery)
            ## pictures & pic_stamps referenced for gallery and saving pic to comp.
            pictures = ['gallery/' + x for x in os.listdir("gallery/") if x.endswith(pic_ext)]
            pictures=sort_gallery(pictures)
            with open("crnt.txt") as file:
                pic_timestamps = [line.strip() for line in file]
            pic_timestamps = sort_times(pic_timestamps)


            self.pic_number = tk.Label(self.win)
            self.pic_number["text"]="1 of " + str(total)
            self.pic_number.pack()

            self.next = tk.Button(self.win,text="Next",command=self.next_pic)
            self.next.pack()
            self.previous=tk.Button(self.win,text="Previous",command=self.previous_pic)
            self.previous.pack()
            # self.fullscreen=tk.Button(self.win,text="Fullsize",command=self.view_fullscreen)
            # self.fullscreen.pack()
            self.delete_btn=tk.Button(self.win,text="Delete Image",command=self.delete_im)
            self.delete_btn.pack()


            self.delete_day=tk.Button(self.win,text="Delete All",
                                    command=self.delete_day_all)
            self.delete_day.pack()

            self.save_im=tk.Button(self.win,text="Save To Desktop",command=self.save_img)
            self.save_im.pack()

            self.timestamp = tk.Label(self.win)
            self.timestamp["text"]=pic_timestamps[0]
            self.timestamp.pack()

            img = Image.open('gallery/1'+pic_ext)
            self.img = ImageTk.PhotoImage(img)

            cnv_w = self.img.width()
            cnv_h = cnv_w*.42
            win_width = str(cnv_w+90)+"x"+str(int(cnv_h+150))
            self.win.geometry(win_width)

            self.pic_window = tk.Canvas(self.win,width=cnv_w,height=cnv_h)
            self.pic_window.create_image(40,40,anchor='nw',image=self.img)
            self.pic_window.pack()

            self.back_button = tk.Button(self.win,text="Close",
                                          command=self.close_gallery)
            self.back_button.pack()

            pic_num=1


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
        pic = save_to_comp(pic_path)


    def delete_im(self):
        global total
        global pic_num
        global pictures

        delete_image(self.variable.get(),pic_num)

        if total==1:
            self.close_gallery()
            return

        if pic_num == 1:
            pictures.remove(pictures[0])
            if total == 2:
                img=Image.open(pictures[0])
            else:
                img = Image.open(pictures[pic_num-1])
        else:
            pictures.remove(pictures[pic_num-1])
            if pic_num == total:
                pic_num-=1
            path=pictures[pic_num-1]
            img = Image.open(path)

        self.img = ImageTk.PhotoImage(img)

        self.pic_window.create_image(40,40,anchor='nw',image=self.img)

        total-=1
        self.pic_number["text"]=str(pic_num)+' of '+str(total)


    def delete_day_all(self):
        delete_day(self.variable.get())
        self.close_gallery()
        dates=fetch_dates()

        try:
            self.variable.set(dates[-1])
        except:
            self.variable.set("---")


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
        routine = self.after(set_delay*1000, self.started_script)

        self.script_on.pack()
        ##  Renames title to enable subprocess to identify it.
        self.home_win.title("Running Peek In")
        return routine


    def stop_script(self):
        self.home_win.title("Peek In main()")
        try:
            self.after_cancel(routine)
            self.script_on.pack_forget()
        except:
            pass
        script_off()
        print("Script stopped.")


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


    def exit_program(self):
        script_off()
        self.clear_gallery()
        end_app()


    ## Clears temporary gallery.
    def close_gallery(self):
        self.clear_gallery()
        self.win.destroy()


###  END OF GUI CLASS ###

##  Run when program starts to prevent multiple instances appearing
##  Also will end program if title is "Peek In" and exit button pressed
def end_process():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call('cmd /c "taskkill /f /FI "WINDOWTITLE eq Peek In*"" /T',
                shell=True,startupinfo=si)

## Ends program if script running bc title is changed to "Running Peek In"
def end_script():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call('cmd /c "taskkill /f /FI "WINDOWTITLE eq Running Peek In*"" /T',
                shell=True,startupinfo=si)

##  Closes app in task manager to both end script if running and program gui
def end_app():
    end_process()
    end_script()

def main():
    create_database()
    root = tk.Tk()
    root.geometry("380x210")
    root.title("Peek In main()")
    app = Application(master=root)
    app.mainloop()




if __name__ == '__main__':
    end_process()
    main()

###  CHANGING Window titles is used in program for task manager call identification
###  Different states will either be left or ended depending on the need.
###  IE "Peek In"  to "Running Peek in"
