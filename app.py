import pyautogui
import datetime

# Potentially removable

# import os
# import sys
# import io
from db_functions import img_to_db

pic_ext = ".jpg"
prev_pic = b" "


def commence_script():
    global prev_pic

    now = datetime.datetime.now()
    current = now.strftime("%I:%M.%S %p")
    today = now.strftime("%m.%d.%y")
    today = now.strftime("%m.%d.%y")

    initial_pic = "screenshot/current1"+pic_ext
    img = pyautogui.screenshot(initial_pic)
    print("Screenshot taken")

    # Resize fullscreen screenshot
    y_ratio = img.size[1]/img.size[0]
    dimension_x = float(img.size[0])*.82
    dimension_y = dimension_x*y_ratio
    img.thumbnail((dimension_x, dimension_y))
    img.save(initial_pic, quality=90)
    with open(initial_pic, "rb") as file:
        # If length of bytes same as previous picture,
        # picture not saved bc it must be same pic, to save space.
        crnt = len(file.read())
        if prev_pic == crnt:
            print("Same Screenshot")
            return
        prev_pic = crnt

    img_to_db(current, today, initial_pic)
    return today


# def delete_database():
#     with open("main.db", "r+b") as file:
#         print(len(file.read()))
#         info = file.read()
#         file.write(info[:20000])
#         file.truncate(20001)


# Gallery sorting func so pictures are viewed in order
def sort_gallery(x):

    list1, list2, list3, list4 = [], [], [], []
    for a in x:
        if len(a) == 13:
            list1.append(a)
        if len(a) == 14:
            list2.append(a)
        if len(a) == 15:
            list3.append(a)
        if len(a) == 16:
            list4.append(a)
    zipped = list(zip(list1, list2, list3, list4))
    zipped.sort()
    if list2:
        list1 += list2
    if list3:
        list1 += list3
    if list4:
        list1 += list4
    return list1


#  Puts AM sorted times in list before PM sorted.
def sort_times(y):

    list1, list2 = [], []
    for a in y:
        if a[-2:] == "AM":
            list1.append(a)
        else:
            list2.append(a)
    list1.sort()
    list2.sort()
    if list2:
        list1 += list2
    return list1
