#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   printf.py
@Time    :   2020/08/16
@Author  :   Yaronzz
@Version :   3.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import aigpy
import logging
import prettytable

import tidal_dl.apiKey as apiKey

from tidal_dl.model import *
from tidal_dl.paths import *
from tidal_dl.settings import *
from tidal_dl.lang.language import *


VERSION = '2022.03.04.2'
__LOGO__ = f'''
 /$$$$$$$$ /$$       /$$           /$$               /$$ /$$
|__  $$__/|__/      | $$          | $$              | $$| $$
   | $$    /$$  /$$$$$$$  /$$$$$$ | $$          /$$$$$$$| $$
   | $$   | $$ /$$__  $$ |____  $$| $$ /$$$$$$ /$$__  $$| $$
   | $$   | $$| $$  | $$  /$$$$$$$| $$|______/| $$  | $$| $$
   | $$   | $$| $$  | $$ /$$__  $$| $$        | $$  | $$| $$
   | $$   | $$|  $$$$$$$|  $$$$$$$| $$        |  $$$$$$$| $$
   |__/   |__/ \_______/ \_______/|__/         \_______/|__/
   
       https://github.com/yaronzz/Tidal-Media-Downloader 
       
                        {VERSION}
'''




class Printf(object):

    @staticmethod
    def logo():
        print(__LOGO__)
        logging.info(__LOGO__)

    @staticmethod
    def __gettable__(columns, rows):
        tb = prettytable.PrettyTable()
        tb.field_names = list(aigpy.cmd.green(item) for item in columns)
        tb.align = 'l'
        for item in rows:
            tb.add_row(item)
        return tb
    
    @staticmethod
    def usage():
        print("=============TIDAL-DL HELP==============")
        tb = Printf.__gettable__(["OPTION", "DESC"], [
            ["-h or --help",        "show help-message"],
            ["-v or --version",     "show version"],
            ["-o or --output",      "download path"],
            ["-l or --link",        "url/id/filePath"],
            ["-q or --quality",     "track quality('Normal','High,'HiFi','Master')"],
            ["-r or --resolution",  "video resolution('P1080', 'P720', 'P480', 'P360')"]
        ])
        print(tb)
        
    @staticmethod
    def checkVersion():
        onlineVer = aigpy.pip.getLastVersion('tidal-dl')
        if onlineVer is None:
            icmp = aigpy.system.cmpVersion(onlineVer, VERSION)
            if icmp > 0:
                Printf.info(LANG.PRINT_LATEST_VERSION + ' ' + onlineVer)

    @staticmethod
    def settings():
        data = SETTINGS
        tb = Printf.__gettable__([LANG.SETTING, LANG.VALUE], [
            #settings - path and format
            [LANG.SETTING_PATH, getProfilePath()],
            [LANG.SETTING_DOWNLOAD_PATH, data.downloadPath],
            [LANG.SETTING_ALBUM_FOLDER_FORMAT, data.albumFolderFormat],
            [LANG.SETTING_TRACK_FILE_FORMAT, data.trackFileFormat],
            [LANG.SETTING_VIDEO_FILE_FORMAT, data.videoFileFormat],
            
            #settings - quality
            [LANG.SETTING_AUDIO_QUALITY, data.audioQuality],
            [LANG.SETTING_VIDEO_QUALITY, data.videoQuality],
            
            #settings - else
            [LANG.SETTING_USE_PLAYLIST_FOLDER, data.usePlaylistFolder],
            [LANG.SETTING_ONLY_M4A, data.onlyM4a],
            [LANG.SETTING_CHECK_EXIST, data.checkExist],
            [LANG.SETTING_SHOW_PROGRESS, data.showProgress],
            [LANG.SETTING_SHOW_TRACKINFO, data.showTrackInfo],
            [LANG.SETTING_SAVE_ALBUMINFO, data.saveAlbumInfo],
            [LANG.SETTING_SAVE_COVERS, data.saveCovers],
            [LANG.SETTING_INCLUDE_EP, data.includeEP],
            [LANG.SETTING_LANGUAGE, getLangName(data.language)],
            [LANG.SETTINGS_ADD_LRC_FILE, data.lyricFile],
            [LANG.SETTING_APIKEY, f"[{data.apiKeyIndex}]" + apiKey.getItem(data.apiKeyIndex)['formats']]
        ])
        print(tb)

    @staticmethod
    def choices():
        print("====================================================")
        tb = Printf.__gettable__([LANG.CHOICE, LANG.FUNCTION], [
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '0':"), LANG.CHOICE_EXIT],
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '1':"), LANG.CHOICE_LOGIN],
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '2':"), LANG.CHOICE_LOGOUT],
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '3':"), LANG.CHOICE_SET_ACCESS_TOKEN],
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '4':"), LANG.CHOICE_SETTINGS + '-Path'],
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '5':"), LANG.CHOICE_SETTINGS + '-Quality'],
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '6':"), LANG.CHOICE_SETTINGS + '-Else'],
            [aigpy.cmd.green(LANG.CHOICE_ENTER + " '7':"), LANG.CHOICE_APIKEY],
            [aigpy.cmd.green(LANG.CHOICE_ENTER_URLID), LANG.CHOICE_DOWNLOAD_BY_URL],
        ])
        tb.set_style(prettytable.PLAIN_COLUMNS)
        print(tb)
        print("====================================================")

    @staticmethod
    def enter(string):
        aigpy.cmd.colorPrint(string, aigpy.cmd.TextColor.Yellow, None)
        ret = input("")
        return ret
    
    @staticmethod
    def enterBool(string):
        aigpy.cmd.colorPrint(string, aigpy.cmd.TextColor.Yellow, None)
        ret = input("")
        return ret == '1'

    @staticmethod
    def enterPath(string, errmsg, retWord='0', default=""):
        while True:
            ret = aigpy.cmd.inputPath(aigpy.cmd.yellow(string), retWord)
            if ret == retWord:
                return default
            elif ret == "":
                print(aigpy.cmd.red(LANG.PRINT_ERR + " ") + errmsg)
            else:
                break
        return ret

    @staticmethod
    def enterLimit(string, errmsg, limit=[]):
        while True:
            ret = aigpy.cmd.inputLimit(aigpy.cmd.yellow(string), limit)
            if ret is None:
                print(aigpy.cmd.red(LANG.PRINT_ERR + " ") + errmsg)
            else:
                break
        return ret

    @staticmethod
    def enterFormat(string, current, default):
        ret = Printf.enter(string)
        if ret == '0' or aigpy.string.isNull(ret):
            return current
        if ret.lower() == 'default':
            return default
        return ret

    @staticmethod
    def err(string):
        print(aigpy.cmd.red(LANG.PRINT_ERR + " ") + string)
        # logging.error(string)

    @staticmethod
    def info(string):
        print(aigpy.cmd.blue(LANG.PRINT_INFO + " ") + string)

    @staticmethod
    def success(string):
        print(aigpy.cmd.green(LANG.PRINT_SUCCESS + " ") + string)

    @staticmethod
    def album(data: Album):
        tb = Printf.__gettable__([LANG.MODEL_ALBUM_PROPERTY, LANG.VALUE], [
            [LANG.MODEL_TITLE, data.title],
            ["ID", data.id],
            [LANG.MODEL_TRACK_NUMBER, data.numberOfTracks],
            [LANG.MODEL_VIDEO_NUMBER, data.numberOfVideos],
            [LANG.MODEL_RELEASE_DATE, data.releaseDate],
            [LANG.MODEL_VERSION, data.version],
            [LANG.MODEL_EXPLICIT, data.explicit],
        ])
        print(tb)
        logging.info("====album " + str(data.id) + "====\n" +
                     "title:" + data.title + "\n" +
                     "track num:" + str(data.numberOfTracks) + "\n" +
                     "video num:" + str(data.numberOfVideos) + "\n" +
                     "==================================")

    @staticmethod
    def track(data: Track, stream: StreamUrl = None):
        tb = Printf.__gettable__([LANG.MODEL_TRACK_PROPERTY, LANG.VALUE], [
            [LANG.MODEL_TITLE, data.title],
            ["ID", data.id],
            [LANG.MODEL_ALBUM, data.album.title],
            [LANG.MODEL_VERSION, data.version],
            [LANG.MODEL_EXPLICIT, data.explicit],
            ["Max-Q", data.audioQuality],
        ])
        if stream is not None:
            tb.add_row(["Get-Q", str(stream.soundQuality)])
            tb.add_row(["Get-Codec", str(stream.codec)])
        print(tb)
        logging.info("====track " + str(data.id) + "====\n" + \
                     "title:" + data.title + "\n" + \
                     "version:" + str(data.version) + "\n" + \
                     "==================================")

    @staticmethod
    def video(data: Video, stream: VideoStreamUrl = None):
        tb = Printf.__gettable__([LANG.MODEL_VIDEO_PROPERTY, LANG.VALUE], [
            [LANG.MODEL_TITLE, data.title],
            [LANG.MODEL_ALBUM, data.album.title if data.album != None else None],
            [LANG.MODEL_VERSION, data.version],
            [LANG.MODEL_EXPLICIT, data.explicit],
            ["Max-Q", data.quality],
        ])
        if stream is not None:
            tb.add_row(["Get-Q", str(stream.resolution)])
            tb.add_row(["Get-Codec", str(stream.codec)])
        print(tb)
        logging.info("====video " + str(data.id) + "====\n" +
                     "title:" + data.title + "\n" +
                     "version:" + str(data.version) + "\n" +
                     "==================================")

    @staticmethod
    def artist(data: Artist, num):
        tb = Printf.__gettable__([LANG.MODEL_ARTIST_PROPERTY, LANG.VALUE], [
            [LANG.MODEL_ID, data.id],
            [LANG.MODEL_NAME, data.name],
            ["Number of albums", num],
            [LANG.MODEL_TYPE, str(data.type)],
        ])
        print(tb)
        logging.info("====artist " + str(data.id) + "====\n" +
                     "name:" + data.name + "\n" +
                     "album num:" + str(num) + "\n" +
                     "==================================")

    @staticmethod
    def playlist(data):
        tb = Printf.__gettable__([LANG.MODEL_PLAYLIST_PROPERTY, LANG.VALUE], [
            [LANG.MODEL_TITLE, data.title],
            [LANG.MODEL_TRACK_NUMBER, data.numberOfTracks],
            [LANG.MODEL_VIDEO_NUMBER, data.numberOfVideos],
        ])
        print(tb)
        logging.info("====playlist " + str(data.uuid) + "====\n" +
                     "title:" + data.title + "\n" +
                     "track num:" + str(data.numberOfTracks) + "\n" +
                     "video num:" + str(data.numberOfVideos) + "\n" +
                     "==================================")

    @staticmethod
    def mix(data):
        tb = Printf.__gettable__([LANG.MODEL_PLAYLIST_PROPERTY, LANG.VALUE], [
            [LANG.MODEL_ID, data.id],
            [LANG.MODEL_TRACK_NUMBER, len(data.tracks)],
            [LANG.MODEL_VIDEO_NUMBER, len(data.videos)],
        ])
        print(tb)
        logging.info("====Mix " + str(data.id) + "====\n" +
                     "track num:" + str(len(data.tracks)) + "\n" +
                     "video num:" + str(len(data.videos)) + "\n" +
                     "==================================")

    @staticmethod
    def apikeys(items):
        print("-------------API-KEYS---------------")
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green('Index'), 
                          aigpy.cmd.green('Valid'),
                          aigpy.cmd.green('Platform'), 
                          aigpy.cmd.green('Formats'), ]
        tb.align = 'l'
        
        for index, item in enumerate(items):
            tb.add_row([str(index), 
                        aigpy.cmd.green('True') if item["valid"] == "True" else aigpy.cmd.red('False'),
                        item["platform"], 
                        item["formats"]])
        print(tb)
