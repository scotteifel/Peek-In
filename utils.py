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


#  Put (sorted) AM times in the list before (sorted) PM .
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


# def delete_database():
#     with open("main.db", "r+b") as file:
#         print(len(file.read()))
#         info = file.read()
#         file.write(info[:20000])
#         file.truncate(20001)
