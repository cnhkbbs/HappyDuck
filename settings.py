# -*- coding: utf-8 -*-
# -*- by:sboxm-*-
# 设置部分
from tkinter import Label, Button, Tk, StringVar, OptionMenu
from json import load


class GUI:
    # 渲染主窗体
    def __init__(self, configs):
        # 配置读取部分
        self.hitokoto_cfg = configs['hitokoto']
        self.biying_cfg = configs['biying']
        self.category_cfg = configs['category']
        self.mode_cfg = configs['mode']
        self.onchange_cfg = configs['onchange']
        # 窗体部分
        self.window = Tk()
        self.window.title("设置")
        self.window.geometry("190x230")
        self.window.attributes("-toolwindow", True)
        self.window.minsize(190, 250)
        self.window.maxsize(190, 250)
        self.title = Label(self.window, text="壁纸鸭设置\n——————————————", anchor='center')
        self.title.grid(row=0, column=0, columnspan=4)
        # 一言
        self.hitokoto_text = Label(self.window, text='一言')
        self.hitokoto_button = Button(self.window, text='开' if self.hitokoto_cfg else '关',
                                      command=self.toggle_hitokoto)
        self.hitokoto_text.grid(row=1, column=0)
        self.hitokoto_button.grid(row=1, column=1)
        # 必应
        self.biying_text = Label(self.window, text='必应')
        self.biying_button = Button(self.window, text='开' if self.biying_cfg else '关',
                                    command=self.toggle_biying)
        self.biying_text.grid(row=2, column=0)
        self.biying_button.grid(row=2, column=1)
        # 类型
        self.category_text = Label(self.window, text='类型')
        self.options = ['随机', '4K', '美女', '美图', '风景', '小清新', '动漫卡通', '明星', '动物', '游戏']
        self.selected = StringVar(value=self.options[self.category_cfg])
        self.selection = OptionMenu(self.window, self.selected, *self.options, command=self.toggle_category)
        self.category_text.grid(row=3, column=0)
        self.selection.grid(row=3, column=1, columnspan=3)
        # 模式
        self.mode_text = Label(self.window, text='模式')
        self.mode_button = Button(self.window, text='临时' if self.mode_cfg == 0 else '永久',
                                  command=self.toggle_mode)
        self.mode_text.grid(row=4, column=0)
        self.mode_button.grid(row=4, column=1)
        # 保存按钮
        self.save_button = Button(self.window, text='保存并应用', command=self.save_settings)
        self.save_button.grid(row=5, column=0, columnspan=4)
        # 底部信息
        self.title = Label(self.window, text="——————————————\n版本 V1.0.0  主打就是一个简陋", anchor='center')
        self.title.grid(row=6, column=0, columnspan=4)
        self.window.mainloop()

    # 保存设置
    def save_settings(self):
        with open('config.json', 'w') as fp:
            hitokoto = 'true' if self.hitokoto_cfg else 'false'
            biying = 'true' if self.biying_cfg else 'false'
            update_config = '{\n"hitokoto":' + hitokoto + ',\n"biying":' + biying + ',\n"category":' + str(
                self.category_cfg) + ',\n"mode":' + str(self.mode_cfg) + ',\n"updatecycle":10,\n"onchange":true\n}'
            fp.write(update_config)

    def toggle_mode(self):
        if self.mode_button["text"] == "临时":
            self.mode_cfg = 1
            self.mode_button["text"] = "永久"
        else:
            self.mode_cfg = 0
            self.mode_button["text"] = "临时"

    def toggle_category(self, event=None):
        option_dict = {'随机': 0, '4K': 1, '美女': 2, '美图': 3, '风景': 4, '小清新': 5, '动漫卡通': 6, '明星': 7,
                       '动物': 8, '游戏': 9}
        self.category_cfg = option_dict[self.selected.get()]

    def toggle_biying(self):
        if self.biying_button["text"] == "开":
            self.biying_cfg = False
            self.biying_button["text"] = "关"
        else:
            self.biying_cfg = True
            self.biying_button["text"] = "开"

    def toggle_hitokoto(self):
        if self.hitokoto_button["text"] == "开":
            self.hitokoto_cfg = False
            self.hitokoto_button["text"] = "关"
        else:
            self.hitokoto_cfg = True
            self.hitokoto_button["text"] = "开"


if __name__ == '__main__':
    # 读取config配置
    try:
        config = open('config.json', 'r')
        config_dit = load(config)
        window1 = GUI(config_dit)
    except FileNotFoundError:
        pass
