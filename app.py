import pyscreeze
import time
from db_functions import img_to_db
from settings import PIC_EXT, PREV_PIC

def take_screenshot(the_date,the_time):
    global PREV_PIC
    start= time.time()
    # now = datetime.datetime.now()

    # # Remove any 0 before an hour from 1-9
    # formatted_hour = now.strftime("%I")
    # if formatted_hour[0] == '0':
    #     formatted_hour = formatted_hour[1]

    # current = now.strftime(formatted_hour + ":%M:%S %p")
    # today = now.strftime(r"%m.%d.%y")

    initial_pic = "screenshot/current1"+PIC_EXT
    img = pyscreeze.screenshot(initial_pic)
    print("Screenshot taken")

    # Resize the fullscreen screenshot
    y_ratio = img.size[1]/img.size[0]
    dimension_x = float(img.size[0])*.82
    dimension_y = dimension_x*y_ratio
    img.thumbnail((dimension_x, dimension_y))
    img.save(initial_pic, quality=90)

    with open(initial_pic, "rb") as file:
        # If the length of bytes is the same as previous picture,
        # picture will not be saved bc guess is it's the same pic, saves db space.
        crnt = len(file.read())
        if PREV_PIC == crnt:
            print("Same Screenshot")
            return
        PREV_PIC = crnt

    img_to_db(the_time, the_date, initial_pic)