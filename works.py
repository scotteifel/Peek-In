# "If needed" code.

# code to check tasks in task manager.  Finds peek in program
# def script_state():
#     # count=0
#     # r = os.popen('tasklist /v').read().strip().split('\n')
#     # print('# of tasks is {num}'.format(num=len(r)))
#     # if 'Peek In' in r:
#     #     print("True")
#     # for x in range(len(r)):
#     #     if 'Peek In main()' in r[x]:
#             # count+=1
#     end_process()
#             # os.system('cmd /k "taskkill /F /FI "WINDOWTITLE eq Peek In" /T"')
#             # print(r[x])
#         # if "Login to Peek In" in r[x]:
#         #     count+=1
#         #     end_login()
#         #     # os.system('cmd /k "taskkill /F /FI "WINDOWTITLE eq Peek In" /T"')
#         #     print(r[x])
#     # print("Total count is : "+str(count) )
#
#
# # def stop_background_script():
# #     count=0
# #     r = os.popen('tasklist /v').read().strip().split('\n')
# #     print('# of tasks is {num}'.format(num=len(r)))
# #     for x in range(len(r)):
# #         if 'Running Peek In' in r[x]:
# #             count+=1
# #             # end_app()
# #             os.system('cmd /k "taskkill /F /FI "WINDOWTITLE eq Running Peek In" /T"')
# #             print(r[x])
# #     print("Total count is : "+str(count))


# Code to test different theme wrappers
# self.change = ttk.Button(self,text='change',command=self.changer)
# self.change.grid()

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
