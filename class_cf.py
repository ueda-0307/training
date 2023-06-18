# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 10:35:18 2023

@author: ueda1
"""
import class_melcor as MERCOR
#import MAIN as MAIN
import class_logicerror as LOGICERROR
import sys

from graphviz import Graph
from graphviz import Digraph

#子クラス(MelcorObject継承　CF)    
class ControlFunction(MERCOR.MelcorObject):
    
    def __init__(self):
        self.connect = None
    
    #printでオブジェクトが指定された場合の処理
    def __str__(self):
        line = "Control Function\n"
        for s in self.text:         #結合で何してる？
            line += s
        return line
    
    def convert(self):
        #ID,NO,LOGIC取得
        #print(self.text)
        self.name  = self.text[0].split()[1]    #ID
        self.no    = self.text[0].split()[2]    #NO
        self.logic = self.text[0].split()[3]    #LOGIC
        self.connect_name = []
        
        #CF_ARGの個数取得
        begin = 0
        for i, line in enumerate(self.text):
            if "CF_ARG" in line:
                begin = i
                self.argline = int(line.split()[1])     #CF_ARG "X" Xを取得
                break
        
        #CF_ARGにあるIDを取得
        for i in range(begin,len(self.text)):
            #CF_ARGをnameに整合する処理：CF_VALU（）の名称取得
            temp = ""
            if "CF-VALU" in self.text[i]:
                temp = self.text[i].split()[1]
                start = temp.find("(") + 1
                end = temp.rfind(")")
                temp = temp[start:end]
                
            else:
                temp = self.text[i].split()[1]
            
            self.connect_name.append(temp)  #CF_ARG 記載のIDを取得
            #self.connect_name.append(self.text[i].split()[1])  #CF_ARG 記載のIDを取得
            
        #必要ないけど残す
        if self.logic == 'T-O-F':
            pass
        elif self.logic == 'L-A-IFTE':
            pass
        elif self.logic == 'TAB-FUN':
            pass
        elif self.logic == 'EQUALS':
            pass
        elif self.logic == 'L-GE':
            pass
        elif self.logic == 'MAX':
            pass
        elif self.logic == 'L-EQ':
            pass
        elif self.logic == 'DIVIDE':
            pass
        elif self.logic == 'ADD':
            pass
        elif self.logic == 'L-GT':
            pass
        elif self.logic == 'T-F-O':
            pass
        elif self.logic == 'MULTIPLY':
            pass
        
        #elif ....
        else:
            #print('not found parameter {}'.format(self.logic))
            raise LOGICERROR.LogicNotFoundError('not found parameter {}'.format(self.logic))

#接続箇所を設定する
    def make_link(self, CF_list):
        self.connect = []
        #オブジェクトループ
        #print(self.connect_name)
        #sys.exit()
        for CF in CF_list:
            #CF_ARGのループ
            for name in self.connect_name:
                #name(CF_ARG)とCF.name(CF_ID)が一致するならself.connectに格納
                if name == CF.name:
                    #self.connect.append(CF)
                    self.connect.append(name)
            
            #ここでエラー処理が必要だと思う(connect_nameが該当しない場合のwarning処理)
        #print(self.connect)
                    
                

#CF = ControlFunction()