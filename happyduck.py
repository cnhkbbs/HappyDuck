# -*- coding: utf-8 -*-
# -*- 作者:sboxm-*-
import json
import random
import requests
import win32api
import win32con
import ctypes
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


def get_hitokoto():
    hitokoto = requests.get('https://v1.hitokoto.cn/', headers)
    hitokoto_text = json.loads(hitokoto.text)
    win32api.MessageBox(0, hitokoto_text["hitokoto"] + "\nfrom: " + str(hitokoto_text["from_who"]), "一言",
                        win32con.MB_OK)


def set_wallpaper():
    path = os.getcwd() + '\\photo.jpg'
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


def get_data(url, count):
    photo_json = requests.get(url, headers)  # 获取json数据
    photo_dict = json.loads(photo_json.text)  # 转换为字典
    randomnum = random.randint(0, count)
    target = photo_dict['data']['list'][randomnum]['url']
    photo = requests.get(target, headers).content
    with open('photo.jpg', 'wb') as fp:
        fp.write(photo)
    set_wallpaper()


def get_photo(biying, category):
    if biying:
        url = 'https://tool.liumingye.cn/bingimg/img.php'
        photo = requests.get(url, headers).content
        with open('photo.jpg', 'wb') as fp:
            fp.write(photo)
        set_wallpaper()

    else:
        if category == 0:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/newestList?pageno=0&count=100'
            count = 100
        elif category == 1:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=36&pageno=0&count=50'
            count = 50
        elif category == 2:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=6&pageno=0&count=50'
            count = 50
        elif category == 3:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=30&pageno=1&count=30'
            count = 30
        elif category == 4:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=30&pageno=1&count=50'
            count = 50
        elif category == 5:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=15&pageno=0&count=50'
            count = 50
        elif category == 6:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=26&pageno=0&count=50'
            count = 50
        elif category == 7:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=11&pageno=0&count=20'
            count = 20
        elif category == 8:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=14&pageno=0&count=50'
            count = 50
        else:
            url = 'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=5&pageno=0&count=50'
            count = 50
        get_data(url, count)


# 0 随机
# 1 4K
# 2 美女
# 3 美图
# 4 风景
# 5 小清新
# 6 动漫卡通
# 7 明星
# 8 动物
# 9 游戏
if __name__ == '__main__':
    try:
        with open('config.json', 'rb') as jsoninfo:
            json_data = json.load(jsoninfo)
    except:
        win32api.MessageBox(0, "您似乎是第一次启动或是丢失了config.json文件，重新打开本软件即可", "哇哦", win32con.MB_OK)
        json_config = '{"hitokoto":true,"biying":false,"category":0}'
        with open('config.json', 'w') as jsonwrite:
            jsonwrite.write(json_config)

    get_photo(json_data["biying"], json_data["category"])
    if json_data["hitokoto"]:
        get_hitokoto()
