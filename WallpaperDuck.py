# -*- coding: utf-8 -*-
# -*- by:sboxm-*-
# 20230420重构
import json
import win32api
import win32con
import core

if __name__ == '__main__':
    try:
        with open('config.json', 'rb') as cfjs:
            config = json.load(cfjs)
            core.core_fun(config)
    except FileNotFoundError:
        win32api.MessageBox(0, "您似乎是第一次启动或是丢失了config.json文件，已经重新写入", "哇哦", win32con.MB_OK)
        with open('config.json', 'w') as cfjs:
            config_json = '{\n"hitokoto":false,\n"biying":false,\n"category":0,\n"mode":0,\n"updatecycle":10,\n"onchange":true\n}'  # 写入默认配置
            cfjs.write(config_json)
