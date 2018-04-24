# -*- coding: utf-8 -*-

import win32api
import win32gui
import win32con
from urllib import request
import re
import contextlib
import os

bingUrl = "https://cn.bing.com"


def getImgInfo(context):
    # r: 原生字符串
    matchObj = re.search(r'g_img=\{url.+\.jpg"', context)
    matchUrl = matchObj.group()
    imgUrl = matchUrl.split("\"")[1]
    imgName = imgUrl.split("/")[-1]
    return imgUrl, imgName


def getContext(url):
    with contextlib.closing(request.urlopen(url)) as r:
        return r.read()


def writeImg(imgPath, img):
    with open(imgPath, "wb") as f:
        f.write(img)


def setWallPaper(dir):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 0：居中显示，1：左右拉伸，2：适应桌面
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,
                                  dir, win32con.SPIF_SENDWININICHANGE)


html = getContext(bingUrl).decode("UTF-8")
imgInfo = getImgInfo(html)
imgUrl = bingUrl + imgInfo[0]
print("obtain image path: %s" % imgUrl)
imgPath = "./" + imgInfo[1]
print("image name: %s" % imgInfo[1])

img = getContext(imgUrl)
print("writing image into file...")

writeImg(imgPath, img)

setWallPaper(os.path.abspath(imgPath))
print("done.")
#os.remove(imgName)