# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:38:34 2023

@author: ueda1
"""

import os
import sys
import pprint
from graphviz import Graph
from graphviz import Digraph

#別ファイル読み込み
import class_melcor as MERCOR
import class_cf as CF
import class_tf as TF
import class_logicerror as LOGICERROR
#import class_gui as GUI

#GUI関連
import PySide6
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtCore, QtGui
from PySide6.QtGui import (QPixmap) # Qtで画像を扱うのに必要
from PySide6.QtWidgets import (QApplication, QMainWindow, QListWidget, QListWidgetItem,
                               QHBoxLayout, QPushButton,QVBoxLayout)
from PySide6.QtWidgets import QLabel,QWidget
###外部入力にした方が実用的
#読み込みファイル名
filepath = "HPI_sample_input.txt"

class InputGenerator(object):
    def __init__(self):        

        #初期化
        self.ALL_LIST = []
        self.CF_list  = [] # Control Function list
        self.TF_list  = [] # Table Function list
    
    def read(self, filepath):
        
        #ファイル読み込み
        with open(filepath, 'r') as f:
            line = f.readline()    #ファイル1行読み込み
            cf_flag = False        #CFフラグ、初期値：FALSE
            tf_flag = False        #TFフラグ、初期値：FALSE
            lines = None           #
            
            ####[_INPUT]を対象にした方が処理少なくなる？→現状はCFIDグループの最後にTF_INPUTが入るバグあり
            
            #入力をグループ化(####最後のグループが入力されていないバグあり)
            while line:
                #lineの改行コード削除
                line = line.strip()
                
                #lineに「!」がある場合の処理(コメント削除処理)
                if "!" in line:                #lineに!が含まれるなら実行
                    index = line.index('!')    #lineの左から最初の!がある位置を取得   
                    line = line[:index]        #lineを!までの文字列に変更
                
                #lineが何もない場合の処理(例：改行のみ)
                if line.strip() == "":         #lineが””なら実行
                    line = f.readline()        #入力の次の行を取得
                    continue                   #whileへ戻る
                
                #CF_IDのグループ作成
                if 'CF_ID' in line:  
                    
                    #CFのリスト作成(ID,NO,LOGIC)
                    if lines is not None:
                        cf = CF.ControlFunction()  #cfオブジェクトの生成(ControlFunctionの呼び出し)
                        cf.text = lines          #cfオブジェクトのself.textにlineを格納
                        #print(cf.text)
                        #sys.exit()
                        self.CF_list.append(cf)      #オブジェクトをリストに格納
                        
                    #CFグループ1行目を取得
                    lines = [line]
        
                    #グループ作成フラグ
                    cf_flag = True   #CFフラグON
                    tf_flag = False  #TFフラグOFF
                    
                ###TFの1行目を作成(cf_flagをFALSEにして、TF_FLAGをTRUEにする)
                elif 'TF_ID' in line:  
                    
                    #TFのリスト作成(ID,SCALE)
                    if lines is not None:
                        tf = TF.TableFunction()
                        tf.text = lines
                        self.TF_list.append(tf)
                    
                    #TFグループ1行目を取得
                    lines = [line]
                    
                    #グループ作成フラグ
                    cf_flag = True   #CFフラグON
                    tf_flag = False  #TFフラグOFF
                    
                #CFの2行目以降のパラメータ格納
                elif cf_flag == True:
                    
                    lines.append(line)
                
                #TFの2行目以降のパラメータ格納    
                elif tf_flag == True:
                    
                    lines.append(line)    
                
                #CF,TF以外の処理
                else:
                    pass
                
                line = f.readline()              #1行格納終わったので、次の行を読み込み(whileの繰り返し作業)
        
        self.ALL_LIST.extend(self.CF_list)
        self.ALL_LIST.extend(self.TF_list)
        
        #inputの必要な情報をクラスに格納(name探索するので
        for cf in self.CF_list:
            try:
               cf.convert()
        #        #デバッグ確認
        #        #print(cf.name)
        #        #print(cf.no)
        #        #print(cf.logic)
        #        #print(cf.connect_name)
        #    
        #    #エラーチェック(logic)
            except LOGICERROR.LogicNotFoundError as e:
                print(e)
                pass
        
        #関係図の描画
        #g = Graph()        #矢印なし描画   default:PDF  例：Graph(format='png')
        #g = Digraph()       #矢印あり描画   default:PDF  例：Digraph(format='png')
        #g = Digraph(format='png')
        #g.attr('graph', rankdir='LR')    #TYPE 描画方向のタイプを定義 default：縦方向　LRで横方向
        #g.attr('node' , shape='square')  #TYPE node描画のタイプを定義
        
        #cfid = []
        #for cf in self.CF_list:
        #    #cf.connect取得
        #    cf.make_link(self.CF_list)
        #    #デバッグ確認
        #    #print(cf.name)
        #    #print(cf.connect)
        #    
        #    #cfのIDをリスト化(後で描画するため)
        #    cfid.append(cf.name)
        #    
        #    #接続先のループ
        #    for connect in cf.connect:
        #        # edgeを追加
        #        g.edge(cf.name, connect)   #接続を格納  引数3はラベル。条件分岐の真偽など記載した方がわかりやすくなる
        #表示＆保存
        #filename = "./draw"
        #pngfile = filename + ".png"
        #g.render(filename, view=False)
              
class MainWindow(QMainWindow,QWidget):
    
    def __init__(self, parent=None):
        # 親クラスの初期化
        super().__init__(parent)
                
        self.CF_list = None
            
        # ウィンドウタイトル
        self.setWindowTitle("練習中")
        
        # ウィンドウの位置とサイズの変更
        xPos = 400  # x座標（px単位）
        yPos = 500  # y座標（px単位）
        windowWidth = 600   # ウィンドウの横幅（px単位）
        windowHeight = 400  # ウィンドウの高さ（px単位）
        self.setGeometry(xPos, yPos, windowWidth, windowHeight)
        
        central_widget = QWidget()   #central_widgetにQWidgetの機能追加
        hbox = QVBoxLayout()         #hboxにQVBoxLayoutの機能追加

        #白枠の設定
        self.listWidget = QListWidget() #listWidgetにQListWidgetの機能追加
        hbox.addWidget(self.listWidget) #hboxにlistWidgetを追加？listWidgetとは？
        
        #ボタンの設定
        button = QPushButton('Load')  #押下ボタンを作成(文字列:Load)
        button.clicked.connect(self.on_load) #ボタンの押下処理
        hbox.addWidget(button)         #hboxにボタン情報登録
        
        central_widget.setLayout(hbox) #ウィジェットのレイアウトにself.listWidgetとbuttonをセット
                
        self.setCentralWidget(central_widget) #中央のウィジェットにcentral_widgetを描画

        """
        # Listにアイテムを追加する
        for cf in CF_list:
            item = QListWidgetItem(cf.name, self.listWidget)
            # 背景色を指定したい場合
            #item.setBackground(QBrush(QColor(255, 0, 0)))
            self.listWidget.itemClicked.connect(self.clicked)
        """
    
    #ボタン押下処理
    def on_load(self):
        #CF読み込み
        print('Load data')
        input_generator = InputGenerator()
        input_generator.read(filepath)
        self.CF_list = input_generator.CF_list  #input_generator.CF_list変数をこっちのクラスで読み込む
        
        #関係図の描画
        #g = Graph()        #矢印なし描画   default:PDF  例：Graph(format='png')
        #g = Digraph()       #矢印あり描画   default:PDF  例：Digraph(format='png')
        g = Digraph(format='png')
        g.attr('graph', rankdir='LR')    #TYPE 描画方向のタイプを定義 default：縦方向　LRで横方向
        g.attr('node' , shape='square')  #TYPE node描画のタイプを定義
        
        for cf in self.CF_list:
            #cf.connect取得
            cf.make_link(self.CF_list)
            
            #接続先のループ
            for connect in cf.connect:
                # edgeを追加
                g.edge(cf.name, connect)   #接続を格納  引数3はラベル。条件分岐の真偽など記載した方がわかりやすくなる
        #表示＆保存
        filename = "./draw"
        pngfile = filename + ".png"
        g.render(filename, view=False)
        
        
        
    
    #def clicked(self, item):
        # Signalで受け取る場合
    #    print(item.text())
        # listWidgetから選択されている値を取得したい場合
    #    print(self.listWidget.currentItem().text()) 


if __name__ == '__main__':
    #PySide6を環境変数に登録処理。(今はシステムから設定している)
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    #print(pngfile)
    
    #ウィンドウ作成    
    app = QApplication(sys.argv)
    #window = GUI.MainWindow(cfid,pngfile)   # ユーザがコーディングしたクラス
    window = MainWindow()   # ユーザがコーディングしたクラス
    window.show()                   # PySide6のウィンドウを表示
    sys.exit(app.exec())            # PySide6の終了
