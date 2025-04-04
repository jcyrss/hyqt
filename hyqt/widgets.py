from PySide6.QtWidgets import *
from PySide6 import QtGui,QtCore

from .utils import clearLayout, isodate2str, NAM

from .richedit import RichTextBrowser, RichTextEdit 

import re

class VerticalLine(QFrame):
    def __init__(self, color='#E5E5E5', lineWidth=1):
        super().__init__()
        self.setFixedWidth(lineWidth)
        self.setStyleSheet(f'background-color:{color}')
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

class HorizontalLine(QFrame):
    def __init__(self, color='#E5E5E5', lineWidth=1):
        super().__init__()
        self.setFixedHeight(lineWidth)
        self.setStyleSheet(f'background-color:{color}')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


class VaryWidthLineEdit(QLineEdit):
    def __init__(self,text, clickCallBack=None):
        super().__init__(text)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.textChanged.connect(self.adjustWidth)

        self.clickCallBack = clickCallBack
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustWidth()

    def adjustWidth(self):
        
        fm = self.fontMetrics()
        text_width = fm.boundingRect(self.text()).width()  + 15
        if text_width < 50:
            text_width = 50

        self.setFixedWidth(text_width)

    def mouseReleaseEvent(self, event):
        if self.clickCallBack:
            self.clickCallBack()

    def setBackgroundColor(self, color):
        if color == 'none':
            color = '#e8f0fe'

        style = f'''
QLineEdit{{    
    background: {color};
    height: 24px;  
    border: none;
    color: #32779f;
    padding:3px;
}}
'''
        self.setStyleSheet(style)

class EditableButton(QFrame):
    def __init__(self, text , clickCallBack, showEdit=False, renameCallBack=None, **attrs):
        super().__init__()

        # 设置动态添加的属性
        for k,v in attrs.items():
            setattr(self, k, v)

        self.btn  = Button2(text, clickCallBack=lambda:clickCallBack(self))

        self.edit   = VaryWidthLineEdit(text, clickCallBack=lambda:clickCallBack(self))
        # 参考 https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.Qt.FocusPolicy
        self.edit.setFocusPolicy(QtCore.Qt.StrongFocus)

        if showEdit:
            self.btn.hide()
            self.edit.setFocus()
        else:
            self.edit.hide()

        layout = QHBoxLayout(self)
        layout.addWidget(self.btn)
        layout.addWidget(self.edit)

        def rename():
            oldName = self.btn.text().strip()
            newName = self.edit.text().strip()
            
            if not newName :
                QMessageBox.critical(self, '', '不能为空')
                return

            # 名字确实改变了
            if newName != oldName:

                if renameCallBack:
                    ret = renameCallBack(self, oldName, newName )
                    # 改名失败， 直接返回，继续处于编辑状态
                    if not ret:  
                        return
                    
                self.btn.setText(self.edit.text())

            self.btn.show() 
            self.edit.hide()


        self.edit.editingFinished.connect(rename)
        self.btn.mouseDoubleClickEvent = self.mouseDoubleClickEvent

        # self.setBackgroundColor = self.btn.setBackgroundColor

        # text方法 传递为属性对象的方法
        self.text = self.btn.text

    def mouseDoubleClickEvent(self, event):
        self.edit.setText(self.btn.text())
        self.edit.show()
        self.btn.hide()

    def setBackgroundColor(self, color):
        self.btn.setBackgroundColor(color)
        self.edit.setBackgroundColor(color)

class EditableLabel(QFrame):
    def __init__(self, text , style='color:#2268a2', clickCallBack=None):
        super().__init__()
        self.label  = StyledLabel(text, style=style, clickCallBack=clickCallBack)

        self.edit   = QLineEdit()
        self.edit.hide()

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)

        self.edit.returnPressed.connect(
            lambda: self.label.setText(self.edit.text()) \
                or self.label.show() \
                or self.edit.hide())

    def mouseDoubleClickEvent(self, event):
        self.edit.setText(self.label.text())
        self.edit.show()
        self.label.hide()


class ClickableLabel(QLabel):
    def __init__(self,text='', clickCallBack=None):
        super().__init__(text)
        
        self.clickCallBack = clickCallBack


    def mouseReleaseEvent(self, event):
        if self.clickCallBack:
            self.clickCallBack()


class StyledLabel(ClickableLabel):
    def __init__(self,text='', style='color:#2268a2', objName=None, clickCallBack=None):
        super().__init__(text,clickCallBack=clickCallBack)
        
        self.setStyleSheet(style)

        if objName:
            self.setObjectName(objName)




class Button2(QPushButton):
    base_style = '''
QPushButton {    
    color: SteelBlue;    
    padding: 2px 5px;           
    border:  <border>;
    font-size: <font-size>;      
    background-color: <backGroundColor>;
}
QPushButton:hover {      
    color:white;
    background-color: <hoverBackGroundColor>;  
}
QPushButton:disabled {
    color:darkgray;
}
'''

      
    _myStyle = {
        'border' : '.5px solid #2268a2',
        'font-size' : '13px'
    }

    
    def __init__(self, text='', iconImg=None, backGroundColor='none',
                 hoverBackGroundColor='#2268a2', clickCallBack=None):
        super().__init__(text)

        if iconImg:
            # 设置图标
            self.setIcon(QtGui.QIcon(iconImg))

        style = self.base_style
    
        for k,v in self._myStyle.items():
            style = style.replace(f'<{k}>', v)

        style = style.replace('<backGroundColor>', backGroundColor)
        style = style.replace('<hoverBackGroundColor>', hoverBackGroundColor)
        
        self.style = style
        self.setStyleSheet(style)
        
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        if clickCallBack:
            self.clicked.connect(clickCallBack)


    def setBackgroundColor(self, color):
        pattern = r"(background-color:).+?;"
        self.style = re.sub(pattern, rf"\1 {color} ;", self.style, count=1)
        self.setStyleSheet(self.style)

class Button_NoBorder(Button2): 

    _myStyle = {
        'border' : 'none',
        'font-size' : '13px'
    }
    
    
class Button_NoBorder_Little(Button2): 

    _myStyle = {
        'border' : 'none',
        'font-size' : '12.5px'
    }

class ButtonWithValue(QFrame):
    def __init__(self, text):
        super().__init__()
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        btn = Button_NoBorder_Little(text)

        self.valueInput = valueInput = QLineEdit()
        valueInput.setFixedSize(70, 24)     
        valueInput.setAlignment(QtGui.Qt.AlignCenter)
        valueInput.setStyleSheet('font-size:13px')
        valueInput.setValidator(QtGui.QIntValidator()) # 只允许输入数字

        layout.addWidget(btn)
        layout.addWidget(valueInput)

        layout.addStretch()

        self.clicked = btn.clicked

    def value(self):
        return self.valueInput.text()

class Selector(QFrame) :
    def __init__(self, title, multiSelection=True, \
            itemWithValue=False, searchCallBack=None):
        super().__init__()  
        self.multiSelection = multiSelection
        self.itemWithValue = itemWithValue

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(3)

        
        # 标题 / 搜索框 / 选中 选项
        layout_1_titleValue = QHBoxLayout()
        layout.addLayout(layout_1_titleValue)
        
        # 标题
        layout_1_titleValue.addWidget(QLabel(title))
        layout_1_titleValue.addSpacing(10)

        # 搜索框
        edit_keywords = QLineEdit()
        edit_keywords.setPlaceholderText('输入关键词查找')
        edit_keywords.setFixedSize(180, 24)
        edit_keywords.setAlignment(QtGui.Qt.AlignCenter)
        edit_keywords.setStyleSheet('font-size:13px')
        layout_1_titleValue.addWidget(edit_keywords)
        edit_keywords.returnPressed.connect(
            lambda: searchCallBack(edit_keywords.text())
        )

        layout_1_titleValue.addSpacing(10)

        # 选中选项 layout
        self.lo_1_1_chosen = QHBoxLayout()
        layout_1_titleValue.addLayout(self.lo_1_1_chosen)

        layout_1_titleValue.addStretch()

        # 选项列表
        self.listBox = listBox = QListWidget()
        listBox.setFixedHeight(80)
        layout.addWidget(listBox)

        listBox.itemDoubleClicked.connect(lambda item:self.addSelection(item.text(),item.itemData))

        self.chosenNames = []

        layout.addStretch()


    def setListItems(self, itemList):
        
        self.listBox.clear()
        
        for itemData in itemList:
            listItem = QListWidgetItem(itemData['name'])
            listItem.itemData = itemData  
            self.listBox.addItem(listItem)

    
    def addSelection(self, itemText, itemData):
        
        # 已经有相同的选中，直接返回
        if itemText in self.chosenNames:
            return
        
        # 如果是单选，且已经有其它选中选项，先去掉该选项
        if not self.multiSelection and self.chosenNames :
            clearLayout(self.lo_1_1_chosen)
            self.chosenNames = []
      

        valueItem =  ButtonWithValue(itemText) if self.itemWithValue \
            else  Button_NoBorder_Little(itemText)  
        
        valueItem.itemData = itemData

        self.lo_1_1_chosen.addWidget(valueItem)
        self.chosenNames.append(itemText)

        valueItem.clicked.connect(
            lambda: self.lo_1_1_chosen.removeWidget(valueItem) or \
                valueItem.deleteLater() or \
                self.chosenNames.remove(itemText)
        )


    def getChosenDataList(self):
        vlayout = self.lo_1_1_chosen
        if not self.itemWithValue:
            return [vlayout.itemAt(i).widget().itemData \
                for i in range(vlayout.count())] 
        else:
            retList = []
            for i in range(vlayout.count()):
                chosenBtn = vlayout.itemAt(i).widget()
                chosenBtn.itemData['amount'] = chosenBtn.value()
                retList.append(chosenBtn.itemData)

            return retList


class TimeLine(QFrame): 
    def __init__(self, steps, currentstate, getStepDataApiUrlTemplate):
        super().__init__()

        self.setMinimumWidth(700)

        lo = QVBoxLayout(self)
        lo.setContentsMargins(0,0,0,0)
        lo.setSpacing(0)

        # ** 显示操作步骤
        for itemData in steps:
            lo.addWidget(TimeLineStep(itemData, getStepDataApiUrlTemplate))

        # ** 显示时间线当前状态
        lo_1_curState = QHBoxLayout()
        lo.addLayout(lo_1_curState)

        lo_1_curState.addSpacing(10)

        label = QLabel()
        label.setPixmap(QtGui.QPixmap('icons/dot2.png')\
            .scaledToWidth(20, QtCore.Qt.SmoothTransformation))
        lo_1_curState.addWidget(label)

        
        lo_1_curState.addSpacing(20)

        label = StyledLabel('当前状态：' + currentstate, 'color:#32779f')
        lo_1_curState.addWidget(label)

        lo_1_curState.addStretch()

        lo.addStretch()

class TimeLineStep(QFrame):
    style = '''
#TimeLineStep:hover{
    background: aliceblue;
}
'''
    def __init__(self, itemData, getStepDataApiUrlTemplate):
        super().__init__()
        self.itemData = itemData
        self.getStepDataApiUrlTemplate = getStepDataApiUrlTemplate

        self.setObjectName('TimeLineStep')
        self.setStyleSheet(self.style)        
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        lo = QHBoxLayout(self)
        lo.setSpacing(20)
        lo.setContentsMargins(16,0,0,0)

        # ** 显示左边竖线
        lo.addWidget(DotLine())


        # ** 显示头像

        avatar = itemData['operator__avatar']
        avatar = avatar if avatar else 'default'

        avatarLabel = QLabel()
        avatarLabel.setPixmap(QtGui.QPixmap(f'icons/avatars/{avatar}.png')\
            .scaledToWidth(36, QtCore.Qt.SmoothTransformation))
        lo.addWidget(avatarLabel, alignment=QtGui.Qt.AlignTop)

        
        # ** 显示中间主体信息
        lo_1_body = QVBoxLayout()
        lo.addLayout(lo_1_body)
        lo_1_body.setSpacing(8)

        lo_1_1_body_top = QHBoxLayout()
        lo_1_body.addLayout(lo_1_1_body_top)
        lo_1_1_body_top.setSpacing(8)

        
        lo_1_1_body_top.addWidget(
            StyledLabel(itemData['operator__realname'], 'color:#32779f')
        )
        
        lo_1_1_body_top.addWidget(
            QLabel(itemData['actionname'])
        )

        lo_1_1_body_top.addStretch()

        lo_1_body.addWidget(
            QLabel(isodate2str(itemData['actiondate']))
        )


        # 详细信息Frame
        self.detailGot = False 
        self.detailFrame = QFrame()        
        lo_1_body.addWidget(self.detailFrame)
        self.detailFrameLayout = QVBoxLayout(self.detailFrame)
        self.detailFrame.setStyleSheet('.QFrame{border:1px solid LightSteelBlue;}')
        self.detailFrame.setMinimumWidth(600)
        self.detailFrame.hide()



        # 添加 QSpacerItem 为了让每个Step隔开一些距离，但是同时竖线 直接是连着的
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Fixed)
        lo_1_body.addItem(spacer)

        lo_1_body.addStretch()

        lo.addStretch()

        self.nam = NAM.getInstance()


    def mouseDoubleClickEvent(self, event):
        if self.detailFrame.isVisible():
            self.detailFrame.hide()
            return
        
        self.detailFrame.show()
        if self.detailGot:
            return

        stepId = self.itemData['id']
        
        def replyGot(retObj):
            self.detailGot = True
            
            stepData = retObj['data']
            for field in stepData:
                self.detailFrameLayout.addWidget(StyledLabel(field['name'],'color:#32779f'))

                if field['type'] == 'RichTextEdit':
                    valueWidget = RichTextBrowser(html=field['value'])
                else:   
                    if field['type'] == 'DateTimePicker':
                        value = isodate2str(field["value"])
                    else:
                        value = field["value"]

                    valueWidget = QLabel(value)
                    valueWidget.setWordWrap(True)

                self.detailFrameLayout.addWidget(valueWidget)

                self.detailFrameLayout.addSpacing(10)
          

        self.nam.get(self.getStepDataApiUrlTemplate.format(stepId), 
                 okHandler=replyGot)


class DotLine(QFrame):
    def __init__(self,):
        super().__init__()

        self.setFixedWidth(8)

        lo = QVBoxLayout(self)
        lo.setSpacing(0)
        lo.setContentsMargins(0,0,0,0)
        
        dot1Label = QLabel()
        dot1Label.setPixmap(QtGui.QPixmap(f'icons/dot1.png')\
            .scaledToWidth(8, QtCore.Qt.SmoothTransformation))
        lo.addWidget(dot1Label, alignment=QtCore.Qt.AlignHCenter)


        # vline = QFrame()
        # vline.setFixedWidth(5)
        # vline.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)        
        # # 这里不加 background-color 会导致显示不出来竖线，应该是qt 的 bug
        # vline.setStyleSheet(
        #     'border-right:.5px solid LightSteelBlue;background-color:transparent;')

        vline = VerticalLine()
        lo.addWidget(vline, alignment=QtCore.Qt.AlignHCenter)



if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    testData = {
  "ret": 0,
  "rec": {
    "id": 4,
    "creatorname": "车间工1",
    "title": "2024-11-30 03:00 - 普瑞巴林（Lyrica）提纯 第6期 - 室温稳定观察",
    "currentstate": "空白/对照样工作已开始",
    "createdate": "2024-11-30T01:38:28.056Z",
    "steps": [
      {
        "id": 10,
        "operator_id": 2,
        "operator__realname": "车间工1",
        "operator__avatar": "m2",
        "actiondate": "2024-11-30T01:38:28.056Z",
        "actionname": "创建送样申请",
        "nextstate": "送样申请已创建"
      },
      {
        "id": 11,
        "operator_id": 2,
        "operator__realname": "车间工1",
        "operator__avatar": "m2",
        "actiondate": "2024-11-30T01:43:56.899Z",
        "actionname": "修改送样时间",
        "nextstate": "送样申请已创建"
      },
      {
        "id": 12,
        "operator_id": 3,
        "operator__realname": "质检工1",
        "operator__avatar": "f2",
        "actiondate": "2024-11-30T01:45:00.262Z",
        "actionname": "开始空白/对照样工作",
        "nextstate": "空白/对照样工作已开始"
      },
      {
        "id": 13,
        "operator_id": 2,
        "operator__realname": "车间工1",
        "operator__avatar": "m2",
        "actiondate": "2024-11-30T01:46:17.693Z",
        "actionname": "修改送样时间",
        "nextstate": "空白/对照样工作已开始"
      },
      {
        "id": 14,
        "operator_id": 3,
        "operator__realname": "质检工1",
        "operator__avatar": "f2",
        "actiondate": "2024-11-30T01:50:16.278Z",
        "actionname": "确知修改送样时间",
        "nextstate": "空白/对照样工作已开始"
      }
    ]
  },
  "whaticando": [
    {
      "name": "确认收到样品",
      "submitdata": [
        {
          "name": "备注",
          "type": "PlainTextEdit",
          "check_string_len": [
            0,
            50000
          ]
        }
      ]
    },
    {
      "name": "确知修改送样时间",
      "submitdata": [
        {
          "name": "备注",
          "type": "PlainTextEdit",
          "check_string_len": [
            0,
            50000
          ]
        }
      ]
    }
  ],
}

    rec = testData["rec"]
    app = QApplication()
    f = TimeLine(rec['steps'], rec['currentstate'])
    f.resize(600,500)
    f.show()
    app.exec()
