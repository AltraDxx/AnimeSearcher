from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent,QMediaPlaylist
# from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui, QtCore
import sys
import requests
import json
import base64
from Ui_MainWindow import Ui_MainWindow
import time
import aiohttp
import os
from PyQt5.QtCore import Qt
from urllib.parse import urlparse, unquote

class RequestFailedError(Exception):...

class MediaDownloader(QThread):
    media_downloaded = pyqtSignal(str)

    def __init__(self, url, row):
        super().__init__()
        self.url = url
        self.row = row

    def run(self):
        parsed_url = urlparse(self.url)
        file_name = parsed_url.path.split("/")[-1]
        temp_path = f'temp/{unquote(file_name)}'
        response = None
        for i in range(5):
            try:
                response = requests.get(url=self.url)
                break
            except Exception as e:
                time.sleep(3)
                print(e)
        if response is None:
            return
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        self.media_downloaded.emit(temp_path)

def safe_run_with_log(f):
    def wrapper(*args, **kwargs):
        ret = None
        for i in range(5):
            try:
                ret = f(*args, **kwargs)
                break
            except Exception as e:
                print(e)
                time.sleep(1)
        return ret
    return wrapper

def json_to_file(json_obj:dict, file:str) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, indent=4, ensure_ascii=False)

def image_to_base64(image_path:str) -> str:
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data)
        base64_string = base64_data.decode("utf-8")
        return base64_string

def read_file(file:str) -> bytes:
    with open(file, 'rb') as file:
        data = file.read()
    return data

async def download_file_async(url:str, status:QStatusBar = None, label:QLabel = None):
        # self.lbFile:QLabel
        # self.lbSize:QLabel
        # self.lbSpeed:QLabel
        # self.progressBar:QProgressBar

        start_time = time.time()

        parsed_url = urlparse(url)
        file_name = parsed_url.path.split("/")[-1]
        temp_path = f'temp/{unquote(file_name)}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_size = int(response.headers['Content-Length'])
                downloaded_size = 0
                block_size = 10

                with open(temp_path, 'wb') as file:
                    while True:
                        buffer = await response.content.read(block_size)
                        if not buffer:
                            break

                        downloaded_size += len(buffer)
                        file.write(buffer)
                        elapsed_time = time.time() - start_time
                        download_speed = downloaded_size / elapsed_time / 1024

                        progress = min(downloaded_size * 100 / file_size, 100)
                        p1 = int(progress // 10)
                        p2 = 10 - p1
                        if status:
                            status.showMessage(f'{os.path.basename(temp_path)} [{p1*"*"}{p2*"-"}] {progress:.2f} {download_speed:.2f}KB/s')
                if label:
                    pixmap = QtGui.QPixmap(temp_path)
                    label.setPixmap(pixmap)

def search_watch_link(title):
    from lxml import etree
    url = f'https://hanime1.me/search?query={title}&type=&genre=&sort=&year=&month='
    response = requests.get(url)
    html = etree.HTML(response.text)
    r = {}
    for v in html.xpath('//*[@id="home-rows-wrapper"]/div[3]/div/div'):
        title = v.xpath('div/div[2]/div/div[1]')[0].text
        link = v.xpath('a')[0].get('href')
        r[title] = link
    return r

@safe_run_with_log
def request_anilistInfo(file_path:str) -> list[dict]:
    file_data = read_file(file_path)
    response = requests.post(
        url = f'https://api.oioweb.cn/api/search/anilistInfo',
        files= {'file':file_data }
    )
    if response.status_code != 200:
        raise RequestFailedError(f'status code ({response.status_code}) is not 200.') 
    data:dict = response.json()
    msg = data.get('msg', None)
    code = data.get('code', None)
    if msg != 'success' or code != 200:
        raise RequestFailedError(f'response data invalid. (code={code}, msg={msg})')
    return data['result']

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.data = None
        self.image_downloader_pool = []
        self.video_downloader_pool = []
        self.video_map:dict = {}
        self.setupUi(self)
        self.init_media_player()
        self.statusbar:QStatusBar
        # self.statusbar.showMessage("hello")
        # self.tbResult.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tbResult.setColumnWidth(0, 320)
        self.tbResult.setColumnWidth(1, 290)
        self.tbResult.setColumnWidth(2, 90)

    def btnFile_clicked(self):
        file = self.select_file("Images (*.jpg *.png *.jpeg *.gif)")
        if file is None:
            self.tbResult:QTableWidget
            self.tbResult.setRowCount(0)
            self.image_downloader_pool = []
            self.video_downloader_pool = []
            self.video_map = {}
            return
        self.txtFile.setText(file)
        self.data = request_anilistInfo(file)
        if self.data is None:
            self.tbResult:QTableWidget
            self.tbResult.setRowCount(0)
            self.image_downloader_pool = []
            self.video_downloader_pool = []
            self.video_map = {}
            return
        self.update_table()

    def tbResult_itemSelectionChanged(self):
        if self.tbResult.selectedIndexes() is None or len(self.tbResult.selectedIndexes()) == 0:
            pass
        else:
            index = self.tbResult.selectedItems()[0].row()
            self.update_info(index)
            video = self.video_map.get(str(index), None)
            if video is not None:
                self.play_video(video)
            else:
                print(self.video_map)


    def select_file(self, filter):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter(filter)
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            return filenames[0]
        else:
            return None
        
    def update_info(self, index):
        result = self.data[index]

        native:str = result['anilist']['title']['native']
        english:str = result['anilist']['title']['english']
        synonyms:list = result['anilist']['synonyms']

        filename = result['filename']
        episode = result['episode']
        start = result['from']
        end = result['to']
        from_to = f"{int(start//60)}m{start%60:.2f}s -- {int(end//60)}m{end%60:.2f}s"
        # similarity = result['similarity']
        # video = result['video']
        # image = result['image']

        self.textBrowser:QTextBrowser       
        self.textBrowser.setHtml(QtCore.QCoreApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">{native}</span></p>\n"
f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">{english}</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">别名：</span><span style=\" font-size:11pt;\">    {', '.join(synonyms)}</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">文件：</span><span style=\" font-size:11pt;\">    {filename}</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">章节：</span><span style=\" font-size:11pt;\">    {episode}</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#5500ff;\">时间：</span><span style=\" font-size:11pt;\">    {from_to}</span></p></body></html>"))
        
    def update_table(self):
        self.tbResult:QTableWidget
        self.tbResult.setRowCount(0)
        self.image_downloader_pool = []
        self.video_downloader_pool = []
        self.video_map = {}
        for result in self.data:

            native:str = result['anilist']['title']['native']
            english:str = result['anilist']['title']['english']

            similarity = result['similarity']
            video = result['video']
            image = result['image']

            # insert row
            row = self.tbResult.rowCount()
            self.tbResult.insertRow(row)

            # pre download video
            self.download_video(video, row)

            # col 0
            self.tbResult.setCellWidget(row,0,QLabel())
            self.download_image(image, row)

            # col 1
            col1 = QTableWidgetItem(f'{native}\n{english}')
            col1.setTextAlignment(Qt.AlignCenter)
            fo1 = QtGui.QFont(col1.font().family(), 12)
            col1.setFont(fo1)
            self.tbResult.setItem(row, 1, col1)

            # col 2
            col2 = QTableWidgetItem(f'{similarity*100:.2f}%')
            col2.setTextAlignment(Qt.AlignCenter)
            fo2 = QtGui.QFont(col2.font().family(), 12)
            fo2.setBold(True)
            col2.setForeground(QtGui.QColor(34, 139, 34))
            col2.setFont(fo2)
            self.tbResult.setItem(row, 2, col2)

        self.tbResult.resizeRowsToContents()
        

    def init_media_player(self):
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.widget)

        self.playlist = QMediaPlaylist(self.media_player)
        self.playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
        self.media_player.setPlaylist(self.playlist)
        
    def play_video(self, file):
        self.playlist.clear()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
        self.media_player.play()

    def download_image(self, url, row):
        self.image_downloader_pool.append(MediaDownloader(url, row))
        self.image_downloader_pool[-1].media_downloaded.connect(self.update_image)
        self.image_downloader_pool[-1].start()

    def update_image(self, image_path):
        md_down:MediaDownloader = self.sender()
        label:QLabel = self.tbResult.cellWidget(md_down.row, 0)
        pixmap = QtGui.QPixmap(image_path)
        label.setPixmap(pixmap)
        self.tbResult.resizeRowsToContents()

    def download_video(self, url, row):
        self.video_downloader_pool.append(MediaDownloader(url, row))
        self.video_downloader_pool[-1].media_downloaded.connect(self.map_video)
        self.video_downloader_pool[-1].start()

    def map_video(self, video_path):
        md_down:MediaDownloader = self.sender()
        self.video_map[str(md_down.row)] = video_path
        print(f'map:{md_down.row} {video_path}')

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    if not os.path.exists('temp'):
        os.mkdir('temp')

    app = QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())