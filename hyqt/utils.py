from PySide6.QtNetwork import QNetworkAccessManager,  QNetworkProxy, \
    QNetworkRequest,QNetworkReply

from PySide6 import QtCore
from PySide6.QtWidgets import QLayoutItem, QMessageBox

import json


from datetime import datetime

def isodate2str(isodateStr):
    return datetime.fromisoformat(isodateStr)\
          .astimezone().strftime('%Y-%m-%d %H:%M:%S') 


def clearLayout(layout):
    while layout.count():
        # takeAt will take the item out of the layout
        child:QLayoutItem = layout.takeAt(0)

        # if the child is a widget, delete it
        if child.widget():
            child.widget().deleteLater()

        # if the child is a spacer item, delete it
        elif child.spacerItem():
            si = child.spacerItem()
            del si

        # if the child is a layout, delete it recursively
        elif child.layout():
            clearLayout(child.layout())
            child.layout().deleteLater()

        del child

class NAM:

    single_instance = None

    @classmethod
    def getInstance(cls):
        if cls.single_instance is None:
            cls.single_instance = NAM()
        return cls.single_instance

    def __init__(self, proxy=None):
        
        self.nam  = QNetworkAccessManager(None)
        
        if proxy:
            proxy = QNetworkProxy(QNetworkProxy.HttpProxy, "127.0.0.1", 8888)
            self.nam.setProxy(proxy)

    def post(self, url, data, contentType='application/json', 
             okHandler=None, errHandler=None):
        self.postOrPut(url, data, contentType, okHandler, errHandler, self.nam.post)

    def put(self, url, data, contentType='application/json', 
             okHandler=None, errHandler=None):
        self.postOrPut(url, data, contentType, okHandler, errHandler, self.nam.put)


    def postOrPut(self, url, data, contentType='application/json', 
             okHandler=None, errHandler=None, method=None):
        request = QNetworkRequest(QtCore.QUrl(url))

        request.setHeader(QNetworkRequest.ContentTypeHeader, contentType)
      
      
        # if body is str, convert it to bytes
        if isinstance(data, str):
            data = data.encode()
    
        # send request
        reply = method(request, data)

    
        # set response callback
        reply.finished.connect(lambda: self.replyFinished(reply, okHandler, errHandler) )

    def get(self, url, okHandler=None, errHandler=None):
        request = QNetworkRequest(QtCore.QUrl(url))
      
        # send request
        reply = self.nam.get(request)

        # set response callback
        reply.finished.connect(lambda: self.replyFinished(reply, okHandler, errHandler) )


    # define response callback
    def replyFinished(self, reply, okHandler, errHandler):
        if reply.error() != QNetworkReply.NoError:
            print(reply.errorString())
            QMessageBox.warning(None, 'error', reply.errorString())
            return

        dataBytes = reply.readAll() # return object type is QByteArray
        data = str(dataBytes, 'utf-8')  # convert QByteArray to str   
        # print('--------------') 
        # print(data)

        retObj = json.loads(data)
        if retObj['ret'] != 0:
            print('error',retObj['msg'])
            # QMessageBox.warning(None, 'error', retObj['msg'])
            if errHandler:
                errHandler(retObj)
                
        elif okHandler:
            okHandler(retObj)




