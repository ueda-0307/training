# -*- coding: utf-8 -*-
"""
Created on Tue May 23 00:05:18 2023

@author: ueda1
"""
import os
import sys
import PySide6

from PySide6 import QtGui
from PySide6.QtGui import (QPixmap) # Qtで画像を扱うのに必要
from PySide6.QtGui import (QBrush, QColor)
from PySide6.QtWidgets import (QApplication, QMainWindow, QListWidget, QListWidgetItem)
from PySide6.QtWidgets import QLabel,QWidget

#class MainWindow(QMainWindow):
class MainWindow(QMainWindow,QWidget):
    
    def __init__(self,cfid,pngfile, parent=None):
        # 親クラスの初期化
        super().__init__(parent)
        
        #debug
        #print(cfid)
        
        # ウィンドウタイトル
        self.setWindowTitle("練習中")
        
        # ウィンドウサイズの設定
        #windowWidth = 1000  # ウィンドウの横幅（px単位）
        #windowHeight = 800  # ウィンドウの高さ（px単位）
        
        #self.resize(windowWidth, windowHeight)

        # ウィンドウの位置とサイズの変更
        xPos = 400  # x座標（px単位）
        yPos = 500  # y座標（px単位）
        windowWidth = 600   # ウィンドウの横幅（px単位）
        windowHeight = 400  # ウィンドウの高さ（px単位）
        
        self.setGeometry(xPos, yPos, windowWidth, windowHeight)
        
        # ウィンドウサイズの固定
        #windowWidth = 500   # ウィンドウの横幅（px単位）
        #windowHeight = 200  # ウィンドウの高さ（px単位）
        #
        #self.setFixedSize(windowWidth, windowHeight)
        
        # ラベルを表示するメソッド
        self.SetLabel(pngfile)
        #print(pngfile)
        
        #リストの配置
        #self.listWidget = QListWidget()
        #self.setCentralWidget(self.listWidget)
        
        # Listにアイテムを追加する
        #for i in cfid:
        #    item = QListWidgetItem(i, self.listWidget)
        #    # 背景色を指定したい場合
        #    #item.setBackground(QBrush(QColor(255, 0, 0)))
        #    self.listWidget.itemClicked.connect(self.clicked)
    
    
    def clicked(self, item):
        # Signalで受け取る場合
        print(item.text())
        # listWidgetから選択されている値を取得したい場合
        print(self.listWidget.currentItem().text())        
        
        
    # ラベルは別のメソッドに分けました
    def SetLabel(self,pngfile):
        # ラベルを使うことを宣言（引数のselfはウィンドウのことで、ウィンドウにラベルが表示されます）
        #label = QLabel(self)
        #print(pngfile)
        # ラベルに文字を指定
        #label.setText("CFにおけるIDリスト。")
        
        # ラベルの見た目をQt Style Sheetで設定
        #labelStyle = """QLabel {
        #    color:            #FF00AA;  /* 文字色 */
        #    font-size:        64px;     /* 文字サイズ */
        #    background-color: #FFAA00;  /* 背景色 */
        #}"""
        
        # 見た目の設定をラベルに反映させる
        #label.setStyleSheet(labelStyle)
        
        # ラベルを使うことを宣言
        label = QLabel(self)
        
        # 画像の読み込み
        image = QPixmap(pngfile)
        
        # 画像サイズの変更
        width = image.size().width() / 2    # 横幅を半分に
        height = image.size().height() / 2  # 高さを半分に
        image = image.scaled(width, height) # 読み込んだ画像のサイズを変更
        
        # ラベルに画像を指定
        label.setPixmap(image)
        
        
        
        
          
        
    