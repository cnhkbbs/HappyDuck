# -*- coding: utf-8 -*-
# -*- by:sboxm-*-
# 核心部分
from json import loads
from os import getcwd
from random import seed, randint
from datetime import datetime
from ctypes import windll
from requests import get, exceptions
from win32con import MB_OK, HKEY_CURRENT_USER, REG_SZ
from win32api import RegSetValueEx, RegCloseKey, MessageBox, RegCreateKey
from PIL import Image, ImageDraw, ImageFont

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


# 壁纸json获取，提前获取json，减少请求发送
def get_data(category=0):
    urls = [
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/newestList?pageno=0&count=100',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=36&pageno=0&count=50',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=6&pageno=0&count=50',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=30&pageno=1&count=30',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=9&pageno=0&count=100',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=15&pageno=0&count=50',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=26&pageno=0&count=50',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=11&pageno=0&count=20',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=14&pageno=0&count=50',
        'https://bird.ioliu.cn/v2?url=http://wp.birdpaper.com.cn/intf/GetListByCategory?cids=5&pageno=0&count=50'
    ]
    counts = [100, 50, 50, 30, 100, 50, 50, 20, 50, 50]
    try:
        potho_json = get(urls[category], headers=headers, timeout=5).text
        with open('photojson.json', 'w') as ptojson:
            ptojson.write(potho_json)
    except exceptions.ConnectTimeout:
        print('exceptions.ConnectTimeout')
        MessageBox(0, "数据更新超时，请稍后重试", "啊哦！出错了", MB_OK)
    except exceptions.ConnectionError:
        MessageBox(0, "网络错误，请稍后重试", "啊哦！出错了", MB_OK)
    except FileExistsError:
        MessageBox(0, "数据写入失败，请检查你的写入权限", "啊哦！出错了", MB_OK)
    return counts[category]


# 直接获取必应每日美图
def get_Bing_photo():
    url = 'https://tool.liumingye.cn/bingimg/img.php'
    try:
        photo = get(url, headers).content
        with open('photo.jpg', 'wb') as fp:
            fp.write(photo)
    except RuntimeError:
        MessageBox(0, "错误", "啊哦！出错了", MB_OK)
    except exceptions.ConnectionError:
        MessageBox(0, "网络错误，请稍后重试", "啊哦！出错了", MB_OK)


# 获取非必应壁纸
def get_photo(count=10):
    # 利用当前读秒作为伪随机数种子
    seed(int(datetime.now().strftime('%S')))
    try:
        with open('photojson.json', 'r') as ptojson:
            photo_dict = loads(ptojson.read())
        randomNum = randint(0, count)
        target = photo_dict['data']['list'][randomNum]['url']
        photo = get(target, headers).content
        with open('photo.jpg', 'wb') as fp:
            fp.write(photo)
    except FileNotFoundError:
        get_data()
        get_photo()
    except exceptions.ConnectTimeout:
        MessageBox(0, "数据更新超时，请稍后重试", "啊哦！出错了", MB_OK)
    except exceptions.ConnectionError:
        MessageBox(0, "网络错误，请稍后重试", "啊哦！出错了", MB_OK)


# 获取随机一言，并将一言打印到壁纸中
def print_hitokoto():
    try:
        hitokoto = get('https://v1.hitokoto.cn/', headers=headers, timeout=5)
        hitokoto_text = loads(hitokoto.text)
        font = ImageFont.truetype(r"C:\Windows\Fonts\Microsoft YaHei UI\msyh.ttc", 60, encoding='unic')
        photo = Image.open('photo.jpg')
        I1 = ImageDraw.Draw(photo)
        I1.text((1500, 950), hitokoto_text["hitokoto"], fill=(255, 255, 255), font=font)
        photo.save('photo.jpg')
    except OSError:
        MessageBox(0, "未知错误", "啊哦！出错了", MB_OK)
    except exceptions.ConnectTimeout:
        MessageBox(0, "数据更新超时，请稍后重试", "啊哦！出错了", MB_OK)
    except exceptions.ConnectionError:
        MessageBox(0, "网络错误，请稍后重试", "啊哦！出错了", MB_OK)


# 设置壁纸
def set_wallpaper(mode=0):
    try:
        with open('photo.jpg', 'r'):
            pass
    except FileNotFoundError:
        MessageBox(0, "图片数据丢失！", "啊哦！出错了", MB_OK)
        return
    path = getcwd() + '\\photo.jpg'
    windll.user32.SystemParametersInfoW(20, 0, path, 0)
    if mode == 1:
        Hkey = RegCreateKey(HKEY_CURRENT_USER, r'Control Panel\Desktop')
        RegSetValueEx(Hkey, 'WallPaper', 0, REG_SZ, path)
        RegCloseKey(Hkey)


# 写入参数
def save_config(config):
    try:
        with open('config.json', 'w') as fconfig:
            fconfig.write(config)
    except FileNotFoundError:
        MessageBox(0, "参数写入失败", "啊哦！出错了", MB_OK)


def core_fun(config):
    updatecycle = config['updatecycle']
    onchange = config['onchange']
    if config['biying']:
        get_Bing_photo()
        set_wallpaper(config['mode'])
        onchange = False
    else:
        if config['updatecycle'] <= 0:  # 更新周期结束
            get_photo(get_data(config['category']))
            updatecycle = 10
            set_wallpaper(config['mode'])
        elif config['onchange']:        # 配置发生改变
            get_photo(get_data(config['category']))
            onchange = False
            updatecycle = 10
            set_wallpaper(config['mode'])
        else:                           # 正常执行
            set_wallpaper(config['mode'])
            get_photo(50)
            updatecycle = updatecycle - 1
            if config['hitokoto']:
                print_hitokoto()
    # json预处理
    hitokoto = 'true' if config['hitokoto'] else 'false'
    biying = 'true' if config['biying'] else 'false'
    onchange = 'true' if onchange else 'false'
    config_up = '{\n"hitokoto":' + hitokoto + ',\n"biying":' + biying + ',\n"category":' + str(
        config['category']) + ',\n"mode":' + str(config['mode']) + ',\n"updatecycle":' + str(
        updatecycle) + ',\n"onchange":' + onchange + '\n}'
    save_config(config_up)      # 写入新更新周期信息
    return
