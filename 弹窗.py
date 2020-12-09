'''
Description: 实现在桌面弹小窗。数量、内容可自定义。
Version: 1.0
Autor: Shi_Ao_Han
Date: 2020-09-29 20:35:23
LastEditors: Shi_Ao_Han
LastEditTime: 2020-10-12 18:05:18
'''
import tkinter as tk
import random
import threading
import time
def dow():
    window = tk.Tk()
    width=window.winfo_screenwidth()
    height=window.winfo_screenheight()
    a=random.randrange(0,width)
    b=random.randrange(0,height)
    window.title('我爱你！')
    window.geometry("200x50"+"+"+str(a)+"+"+str(b))
    tk.Label(window,
        text='我爱你！',    # 标签的文字
        bg='Red',     # 背景颜色
        font=('楷体', 17),     # 字体和字体大小
        width=15, height=2  # 标签长宽
        ).pack()    # 固定窗口位置
    window.mainloop()

threads = []
for i in range(100):#需要的弹框数量
    t = threading.Thread(target=dow)
    threads.append(t)
    time.sleep(0.1)
    threads[i].start()