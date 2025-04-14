import os,re,time

from PySide6.QtWidgets import QApplication, QMainWindow,  \
 QTextEdit, QWidget,QVBoxLayout,QSizePolicy, \
    QToolBar,QFrame,QMessageBox,QTextBrowser

from PySide6 import QtCore,QtGui
from PySide6.QtNetwork import QNetworkAccessManager, \
    QNetworkRequest,QNetworkReply

import re

from .utils import NAM

from functools import partial

class BaseTextEdit(QTextEdit):
    IMAGE_EXTENSIONS = ['.jpg','.png','.bmp']
    DPR = None

    def __init__(self, rte=None, html=None):
        super().__init__()
        self.rte = rte

        self.setObjectName('RichTextEdit')

        if BaseTextEdit.DPR is None:
            BaseTextEdit.DPR = QApplication.primaryScreen().devicePixelRatio()
            print("Device Pixel Ratio:", BaseTextEdit.DPR)

        if html:
            self.setHtml2(html)

        self.document().contentsChanged.connect(self.adjustHeight)

        self.nam = NAM.getInstance()
    
    def onSelect(self):
        self.rte.bold_action.setChecked(self.fontWeight() == QtGui.QFont.Bold) 


    def setHtml2(self, html): 
        """
        重新实现了 QTextEdit 的 setHtml 函数，使得 html 中的远程图片可以正确地显示出来
        
        :param html: HTML 文本
        """
        
        self.setHtml(html)

        self.imagesHandled = {}

        def oneImgDownloaded(imgUrl, reply) :
            if reply.error() != QNetworkReply.NoError:
                print("Error loading image:", reply.errorString())
                return   
                      
            # print(imgUrl,' downloaded.')

            image = QtGui.QImage()
            image.loadFromData(reply.readAll())
            image.setDevicePixelRatio(self.DPR)  # 否则 scale的屏幕，图片会放大模糊 blurry
            
            self.document().addResource(QtGui.QTextDocument.ImageResource, imgUrl, image)
            self.setHtml(html) # 会触发contentsChanged，显示已经加载的图片


        for imgUrl in re.findall(r'<img src="(.+?)"', html):
            
            # 已经处理过的相同图片，不再重复下载
            if imgUrl in self.imagesHandled:
                continue

            self.imagesHandled[imgUrl] = 1


            reply = self.nam.get(QNetworkRequest(QtCore.QUrl(imgUrl)))
            reply.finished.connect(
                lambda imgUrl=imgUrl,reply=reply: oneImgDownloaded(imgUrl,reply)) 


    def adjustHeight(self):
        docHeight = self.document().size().height()
        margins = self.contentsMargins()
        finalHeight = docHeight + margins.top() + margins.bottom()+5
        if finalHeight < 150:
            finalHeight = 150
        self.setFixedHeight(finalHeight)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustHeight()


    def setSelectionColor(self, color):       
        self.setTextColor(QtGui.QColor(color))
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)


    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super().canInsertFromMimeData(source)


    def insertFromMimeData(self, source):

        def splitext(p):
            return os.path.splitext(p)[1].lower()
        
        def addImage(image:QtGui.QImage):
            # 否则 scale的屏幕，图片会放大模糊 blurry
            image.setDevicePixelRatio(self.DPR) 
            
            # 这些新添加的图片，还没有上传到服务端，采用独特的命名方式tmp_，方便后面上传时查找
            url = f'tmp_{time.time()}'
            self.document().addResource(QtGui.QTextDocument.ImageResource, url, image)
            self.textCursor().insertImage(url)

            # 后面可以这样获取图片数据
            # self.document().resource(QtGui.QTextDocument.ImageResource, url)

        if source.hasUrls():
            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                # 本地文件拖拽
                if u.isLocalFile() and file_ext in self.IMAGE_EXTENSIONS:
                    localPath = u.toLocalFile()
                    image = QtGui.QImage(localPath)          
                    addImage(image)
                    
                # 网络图片拖拽，比如从浏览器拖拽图片
                else:
                    print('not local file, maybe network file:', u)
                    break

            else:
                # If all were valid images, finish here.
                return

        # 剪贴板复制图片
        elif source.hasImage():
            image = source.imageData()
            addImage(image)
            return

        super().insertFromMimeData(source)

    def saveTmpResourcesToServer(self):        
        
        """
        保存当前文档里的临时图片资源到服务端，并更新html里的img标签
        
        1. 找到文档里的临时图片资源，都是 tmp_ 开头的
        2. 上传到服务端，得到url
        3. 更新html里的img标签
        4. 如果所有图片都上传成功，后续调用者可以上传更新后的HTML
        """

        self.html = self.toCleanHtml()
        
        self.saveTmpResourcesStatus = 'ongoing'
        
        # 需要上传的图片，都是 tmp命名的
        self.toUploadImgs = set(re.findall(r'<img src="(tmp_.+?)"', self.html))  

        if len(self.toUploadImgs) == 0:     
            self.saveTmpResourcesStatus = 'finished'      
            return

        self.uploadedImgs = set()
        self.uploadFailedImgs = []

        def oneImgUploaded(imageName, image, retObj) :
            if retObj['ret'] != 0:
                print(retObj['msg'])
                self.saveTmpResourcesStatus = 'failed'
                self.uploadFailedImgs.append(imageName)
                QMessageBox.critical(
                    self, '错误',
                    f'上传图片错误: {retObj["msg"]}'
                )
                return
            
            self.uploadedImgs.add(imageName)          
            print(imageName,' uploaded.')


            # 修改 html里面 的img标签src 为 服务端返回的 图片 url
            newUrl = retObj['url']
            oldName = imageName[:-4] # 原来的文档里面图片资源的src名字是 没有后缀 .png 的
            self.html = self.html.replace(f'src="{oldName}"', f'src="{newUrl}"')

            # 更新文档资源， 以新url为key, 这样后面 setHtml2 / setHtml 时，就不用重新下载服务端的图片
            self.document().addResource(QtGui.QTextDocument.ImageResource, newUrl, image)
            self.setHtml(self.html)
            
            # 图片全部上传成功
            if len(self.toUploadImgs) == len(self.uploadedImgs):   
                print('**** all uploaded')      
                self.saveTmpResourcesStatus = 'finished'       
        


        self.imagesHandled = {}

        # 把未上传的图片，上传到服务端
        for imgUrl in self.toUploadImgs:
            
            if self.uploadFailedImgs:               
                break

            # 如果这个图片复制了多份， 只需要上传一份
            if imgUrl in self.imagesHandled:
                continue


            self.imagesHandled[imgUrl] = 1

            image = self.document().resource(QtGui.QTextDocument.ImageResource, imgUrl)
           
            # 所有拖拽，剪贴板 复制的图片，都会变成 bmp 格式

            imageName = imgUrl + '.png'

            print(imageName,' uploading...')
 

            uploadData = qimage_to_png_bytearray(image)

          
            # self.nam.post('http://localhost/api/upload?file_name='+imageName, 
            #     uploadData, contentType="image/image", okHandler=
            #     lambda retObj, reply=reply,imageName=imageName, image=image: \
            #         oneImgUploaded(imageName,image,reply)) 


            self.nam.post('http://localhost/api/upload?file_name='+imageName, 
                uploadData, contentType="image/image", 
                okHandler=partial(oneImgUploaded,imageName,image),
                errHandler=partial(oneImgUploaded,imageName,image),
                ) 


    def toCleanHtml(self):
        def subFunc(match):
            if '-qt-block-indent' in match.group(1):
                return ''
            else: 
                return match.group(0)

        oriHtml = self.toHtml()
        contentPortion = oriHtml[
            re.search("<body .*?>", oriHtml).end() : oriHtml.find('</body>')]

        ret = re.sub(r' style="(.+?)"', subFunc , contentPortion).strip()
        return ret
    
    
def qimage_to_png_bytearray(qimage):
    """Converts a QImage to a PNG bytearray."""

    byte_array = QtCore.QByteArray()
    buffer = QtCore.QBuffer(byte_array)
    buffer.open(QtCore.QIODevice.WriteOnly)
    qimage.save(buffer, "PNG", )
    buffer.close()

    # Return the bytearray
    return byte_array


class RichTextEdit(QFrame):
     
    my_css = '''
QTextEdit {
    font-family: consolas, 微软雅黑 ;
    font-size: 14px;    
    color: rgb(83, 83, 83);
}
'''


    def __init__(self, html=None):
        super().__init__()

        self.setStyleSheet(self.my_css)
        
        self.lo = lo  = QVBoxLayout(self) 
        lo.setContentsMargins(0, 0, 0, 0) 

        # 工具栏
        self.setupToolsBar()

        # 编辑框
        self._te = BaseTextEdit(self, html=html)
        lo.addWidget(self._te)

        # 结尾 addStretch， 可以让该layout后面尽量空白占据，
        lo.addStretch()

        

    def setupToolsBar(self):
        
        # 添加 工具栏
        toolbar = QToolBar(self)
        self.lo.addWidget(toolbar)

        action  = toolbar.addAction(QtGui.QIcon("icons/red.png"),"红色")
        action.triggered.connect(lambda : self._te.setSelectionColor('Crimson'))
        
        action  = toolbar.addAction(QtGui.QIcon("icons/blue.png"),"蓝色")
        action.triggered.connect(lambda : self._te.setSelectionColor('DodgerBlue'))
        
        action  = toolbar.addAction(QtGui.QIcon("icons/green.png"),"绿色")
        action.triggered.connect(lambda : self._te.setSelectionColor('DarkGreen'))
        
        action  = toolbar.addAction(QtGui.QIcon("icons/gray.png"),"缺省")
        action.triggered.connect(lambda : self._te.setSelectionColor('#535353'))

        self.bold_action  = toolbar.addAction("B")
        self.bold_action.setToolTip("粗体")
        self.bold_action.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: 
            self._te.setFontWeight(QtGui.QFont.Weight.Bold if x else QtGui.QFont.Normal))

        # action  = toolbar.addAction("存图")
        # action.triggered.connect(
        #     lambda: self._te.saveTmpResourcesToServer()
        # )

        # action  = toolbar.addAction("clean-html")
        # action.triggered.connect(
        #    lambda: print('------',self._te.toCleanHtml(),'------',sep='\n'))

    def saveTmpResourcesToServer(self):
        self._te.saveTmpResourcesToServer()
        
    def saveTmpResourcesStatus(self):
        return self._te.saveTmpResourcesStatus

    def toHtml(self):    
        return self._te.toCleanHtml()

class RichTextBrowser(QTextBrowser):
    DPR = None

    def __init__(self, html=None, nam=None):
        
        super().__init__()

        self.setStyleSheet(
            """
            QTextBrowser{
                border: none;
            }
            """
        )
        self.verticalScrollBar().setVisible(False)


        if RichTextBrowser.DPR is None:
            RichTextBrowser.DPR = QApplication.primaryScreen().devicePixelRatio()
        
        # 已经放到处理队列的图片
        self.imagesHandled = {}


        if html is not None:
            self.setHtml2(html)

        # self.timer = QtCore.QTimer()
        # self.timer.setSingleShot(True)  # Set as a single-shot timer
        # self.timer.timeout.connect(self.adjustHeight)
        # self.timer.start(0)  

        self.document().contentsChanged.connect(self.adjustHeight)

        # 设置 行距
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)

        block_format = QtGui.QTextBlockFormat()
        # Set line spacing to 1.5 (150%)
        block_format.setLineHeight(40.0, 1)
        cursor.setBlockFormat(block_format)

        if nam is None:
            nam = NAM.getInstance()
        self.nam = nam  
        

    def setHtml2(self,html): 
        """
        重新实现了 QTextEdit 的 setHtml 函数，使得 html 中的远程图片可以正确地显示出来
        
        :param html: HTML 文本
        """
        def oneImgDownloaded(imgUrl, reply) :
            if reply.error() != QNetworkReply.NoError:
                print("Error loading image:", reply.errorString())
                return   
                      
            # print(imgUrl,' downloaded.')

            image = QtGui.QImage()
            image.loadFromData(reply.readAll())
            image.setDevicePixelRatio(self.DPR)  # 否则 scale的屏幕，图片会放大模糊 blurry

            self.document().addResource(QtGui.QTextDocument.ImageResource, imgUrl, image)
            self.setHtml(html) # 会触发contentsChanged，显示已经加载的图片
        
        self.setHtml(html)

        self.imagesHandled = {}
              
        for imgUrl in re.findall(r'<img src=\"(.+?)\"', html):

            # 已经处理过的相同图片，不再重复下载
            if imgUrl in self.imagesHandled:
                # print('handled')
                continue
            
            self.imagesHandled[imgUrl] = 1

            # 已经存在的图片资源，不再重复下载
            image = self.document().resource(QtGui.QTextDocument.ImageResource, imgUrl)
            if image is not None:                
                continue

            print('img downloading:', imgUrl)

            # 外站图片， 使用绝对路径  
            if imgUrl.startswith('http'):
                realUrl = imgUrl

            # 本站图片， 使用相对路径  /upload 开头， 比如  <img src="/upload/4_20241203172704_495915.png" /> 
            elif imgUrl.startswith('/upload/'):
                realUrl = 'http://localhost' + imgUrl

            else:
                print('img Url error:', imgUrl)
                continue


            reply = self.nam.get(QNetworkRequest(QtCore.QUrl(realUrl)))
            reply.finished.connect(
                lambda imgUrl=imgUrl,reply=reply: oneImgDownloaded(imgUrl,reply)) 
        
        
    def adjustHeight(self):
        docHeight = self.document().size().height()
        margins = self.contentsMargins()
        finalHeight = docHeight + margins.top() + margins.bottom()
        # print('adjustHeight', finalHeight)
        self.setFixedHeight(finalHeight+5)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustHeight()



if __name__ == '__main__':

    test_text = '''
<p>from PySideQtGui import abc.py.ppp.ccc.ddd.fff </p>
<p><span style=" color:#ff0000;">import # 这个试试看</span> </p>        
<img src="https://doc.qt.io/qtforpython/_images/windows-pushbutton.png" /> 
<br />
<img src="https://doc.qt.io/qtforpython/_images/windows-pushbutton.png" /> 
<p><br /></p>
<p>其它文本 </p> 
'''


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            # central Widget
            self.resize(800,800)
            centralWidget = QWidget(self)
            self.setCentralWidget(centralWidget)
            mainLayout = QVBoxLayout(centralWidget)

            
            rte = RichTextEdit(html=test_text)
            mainLayout.addWidget(rte)

            gNAM.post(
            'http://localhost/api/mgr/signin', 
            'username=byhy&password=88888888', 
            contentType='application/x-www-form-urlencoded')

    app = QApplication()

    mw = MainWindow()
    mw.show()


    app.exec()
