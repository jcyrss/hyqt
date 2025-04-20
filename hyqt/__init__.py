version = '0.0.6'

from PySide6.QtWidgets import *
from PySide6 import QtCore

import random, string
from .utils import *
from .widgets import *

from dataclasses import dataclass
from collections.abc import Callable

from typing import TypedDict, Unpack, Required, NotRequired

# generate random unique 12-char string
def _randomString():
    return ''.join(random.choices(string.ascii_lowercase, k=20))



# set style to widget 
def ss(widget:QWidget,     
    size:tuple[int,int]|None=None,        
    width:int|None=None,   
    height:int|None=None,
    minWidth:int|None=None,
    minHeight:int|None=None,
    maxWidth:int|None=None,
    maxHeight:int|None=None,

    stretchFactor:int=0,
    align:str|None=None,
    
    color:str|None=None,
    bgColor:str|None=None, 
    fontSize:int|None=None,
    fontWeight:str|None=None,
    fontFamily:str|None=None,

    border:str|None=None,
    padding:str|None=None,  
    hExpanding=True,       
    vExpanding=False,    

    name:str|None=None,    
    styleSheet:str='',
) -> QWidget:   
    """
    Parameters
    ----------
    widget : QWidget
        需要设置样式的控件

    size : tuple[int,int] | None, optional
        设置控件的尺寸
    width : int | None, optional
        设置控件的固定宽度
    height : int | None, optional
        设置控件的固定高度

    minWidth : int | None, optional
        最小宽度
    minHeight : int | None, optional
        最小高度
    maxWidth : int | None, optional
        最大宽度
    maxHeight : int | None, optional
        最大高度

    stretchFactor : int, optional
        设置控件 在上级容器中的扩展权重

    align : str | None, optional
        设置控件 在上级容器中的对齐

    color : str | None, optional
        字体颜色
    bgColor : str | None, optional
        背景颜色
    fontSize : int | None, optional
        字体大小 
    fontFamily : str | None, optional
        字体，比如 "微软雅黑"
        
    border : str | None, optional
        边框，比如 "1px solid #367fa9"

    padding :  string, optional
        设置控件的 QSS padding，比如 "13px"，
        "15px 16px 17px 18px" 是上右下左的顺序设置

        注意和Row，Column 容器控件 的 paddings 设置不一样，
        那个是数字或者是数字列表，而且是左上右下次序

    hExpanding : bool, optional
        是否横向扩展，缺省为 False
    vExpanding : bool, optional
        是否纵向扩展，缺省为 False

    name : str | None, optional
        setObjectName 设置的名称

    styleSheet : str, optional
        该控件的styleSheet，用来设置其它参数没有设置的样式
    """
    
    if size is not None:
        widget.resize(*size)
    
    if width is not None:
        widget.setFixedWidth(width)

    if height is not None:
        widget.setFixedHeight(height)

    if minWidth is not None:
        widget.setMinimumWidth(minWidth)

    if minHeight is not None:
        widget.setMinimumHeight(minHeight)

    if maxWidth is not None:
        widget.setMaximumWidth(maxWidth)

    if maxHeight is not None:
        widget.setMaximumHeight(maxHeight)

    widget._hy_stretchFactor = stretchFactor

    if align is not None:
        widget._hy_align = align

    style = ''

    if border is not None:
        style += f'  border: {border};\n'
        
    if color is not None:
        style += f'  color: {color};\n'
    
    if bgColor is not None:
        style += f'  background-color: {bgColor};\n'

    if fontSize is not None:
        style += f'  font-size: {fontSize}px;\n'

    if fontWeight is not None:
        style += f'  font-weight: {fontWeight};\n'

    if fontFamily is not None:
        style += f'  font-family: {fontFamily};\n'
    
    if padding is not None:
        style += f'  padding: {padding};\n'
    
    if name:
        widget.setObjectName(name)

    if style or styleSheet:    
        if not name:
            name = _randomString()   
            widget.setObjectName(name)
        widget.setStyleSheet(f'#{name} {{\n{style}\n}}\n\n{styleSheet}')        
    
    hp = QSizePolicy.Expanding if hExpanding else QSizePolicy.Maximum
    vp = QSizePolicy.Expanding if vExpanding else QSizePolicy.Maximum
    widget.setSizePolicy(hp, vp)

    return widget



class _WidgetArgs(TypedDict):
    """
    Parameters
    ----------
    size : tuple[int,int] | None, optional
        设置控件的尺寸
    width : int | None, optional
        设置控件的固定宽度
    height : int | None, optional
        设置控件的固定高度

    minWidth : int | None, optional
        最小宽度
    minHeight : int | None, optional
        最小高度
    maxWidth : int | None, optional
        最大宽度
    maxHeight : int | None, optional
        最大高度

    stretchFactor : int, optional
        设置控件 在上级容器中的扩展权重

    align : str | None, optional
        设置控件 在上级容器中的对齐

    color : str | None, optional
        字体颜色
    bgColor : str | None, optional
        背景颜色
    fontSize : int | None, optional
        字体大小 
    fontFamily : str | None, optional
        字体，比如 "微软雅黑"
        
    border : str | None, optional
        边框，比如 "1px solid #367fa9"

    padding :  string, optional
        设置控件的 QSS padding，比如 "13px"，
        "15px 16px 17px 18px" 是上右下左的顺序设置

        注意和Row，Column 容器控件 的 paddings 设置不一样，
        那个是数字或者是数字列表，而且是左上右下次序

    hExpanding : bool, optional
        是否横向扩展，缺省为 False
    vExpanding : bool, optional
        是否纵向扩展，缺省为 False

    name : str | None, optional
        setObjectName 设置的名称

    styleSheet : str, optional
        该控件的styleSheet，用来设置其它参数没有设置的样式
    """

    size         :NotRequired[tuple[int,int]]
    width        :NotRequired[int]
    height       :NotRequired[int]
    minWidth     :NotRequired[int]
    minHeight    :NotRequired[int]
    maxWidth     :NotRequired[int]
    maxHeight    :NotRequired[int]

    stretchFactor:NotRequired[int]
    align        :NotRequired[str]

    color        :NotRequired[str]
    bgColor      :NotRequired[str]
    fontSize     :NotRequired[int]
    fontWeight   :NotRequired[str]
    fontFamily   :NotRequired[str]

    border       :NotRequired[str]
    padding      :NotRequired[str]
    hExpanding   :NotRequired[bool]
    vExpanding   :NotRequired[bool]

    name         :NotRequired[str]
    styleSheet   :NotRequired[str]



def _custom_widget_init(self, parentType, args, kwargs):
    def _popStyleArgs(kwargs:dict):
        retDict = {}
        for name in _WidgetArgs.__annotations__.keys():
            val = kwargs.pop(name,None)
            if val is not None:
                retDict[name] = val
        return retDict

    styleArgs = _popStyleArgs(kwargs)
    parentType.__init__(self, *args, **kwargs)
    ss(self, **styleArgs)

class Label(QLabel):

    
    def __init__(self, *args, 
        labelImg:str|None=None,
        labelImgSize:int|None=None,        
        **kwargs: Unpack[_WidgetArgs]):

        _custom_widget_init(self, QLabel, args, kwargs)

        if labelImg is not None:
            if labelImgSize is not None:
                self.setPixmap(QtGui.QPixmap(labelImg).scaledToWidth(labelImgSize, QtCore.Qt.SmoothTransformation))
            else:
                self.setPixmap(QtGui.QPixmap(labelImg))


class Button(QPushButton):
    def __init__(self, *args, 
        onClick:Callable|None=None,     
        **kwargs: Unpack[_WidgetArgs]):
        
        _custom_widget_init(self, QPushButton, args, kwargs)

        self.clicked.connect(onClick)


class Input(QLineEdit):
    
    AlignTable = {
        'center': QtCore.Qt.AlignHCenter,
        'left':   QtCore.Qt.AlignLeft,
        'right':  QtCore.Qt.AlignRight,
    }

    EchoModeTable = {
        'normal':   QLineEdit.Normal,
        'no-echo':   QLineEdit.NoEcho,
        'password': QLineEdit.Password,
        'password-echo-on-edit':   QLineEdit.PasswordEchoOnEdit,
        # Normal                    = ...  # 0x0
        # NoEcho                    = ...  # 0x1
        # Password                  = ...  # 0x2
        # PasswordEchoOnEdit        = ...  # 0x3
    }

    def __init__(self, *args, 
        placeholder:str|None=None,
        textAlign:str|None=None,
        echoMode:str|None=None,
        leadingActionIcon:str|None=None,
        trailingActionIcon:str|None=None,
        intOnly:bool|None=None, 
        onChange:Callable|None=None,     
        **kwargs: Unpack[_WidgetArgs]):
        """

        Parameters
        ----------
        placeholder : str | None, optional
            输入提示占位符
        textAlign : str | None, optional
            内部文本的对齐方式，取值为 center, left, right
        echoMode : str | None, optional
            文字回显模式，取值为 normal, no-echo, password， password-echo-on-edit
        leadingActionIcon : str | None, optional
            内部前置图标
        trailingActionIcon : str | None, optional
            内部后置图标
        intOnly : bool | None, optional
            只允许输入整数
        onChange : Callable | None, optional
            内部文本改变时的回调函数
        """
        
        _custom_widget_init(self, QLineEdit, args, kwargs)

        if placeholder is not None:
            self.setPlaceholderText(placeholder)

        if textAlign is not None:
            align = self.AlignTable.get(textAlign)
            if align is None:
                print(f'textAlign `{textAlign}` not in {self.AlignTable.keys()}')
            self.setAlignment(align)
        
        if echoMode is not None:
            mode = self.EchoModeTable.get(echoMode)
            if mode is None:
                print(f'echoMode `{echoMode}` not in {self.EchoModeTable.keys()}')
            self.setEchoMode(mode)

        if leadingActionIcon is not None:
            self.addAction(QtGui.QIcon(leadingActionIcon), QLineEdit.LeadingPosition)

        if trailingActionIcon is not None:
            self.addAction(QtGui.QIcon(trailingActionIcon), QLineEdit.TrailingPosition)

        if intOnly is not None:
            self.setValidator(QtGui.QIntValidator())

        if onChange is not None:
            self.textChanged.connect(onChange)

class TextArea(QTextEdit):
    def __init__(self, *args, 
        placeholder:str|None=None,
        onChange:Callable|None=None,     
        **kwargs: Unpack[_WidgetArgs]):
        """

        Parameters
        ----------
        placeholder : str | None, optional
            输入提示占位符
        onChange : Callable | None, optional
            内部文本改变时的回调函数
        """
        
        _custom_widget_init(self, QTextEdit, args, kwargs)

        if placeholder is not None:
            self.setPlaceholderText(placeholder)

        if onChange is not None:
            self.textChanged.connect(onChange)


class TextBrowser(QTextBrowser):
    def __init__(self, *args,   
        **kwargs: Unpack[_WidgetArgs]):
        
        _custom_widget_init(self, QTextBrowser, args, kwargs)



@dataclass
class s__:    
    
    """
    Parameters
    ----------
    windowTitle : str | None, optional
        窗口标题

    itemsJustify : str | None, optional
        设置子控件的主轴对齐
        取值为 start, center, end， even, None
        
        如果为 even， 表示平均间隔，类似 css flex justify space-between 的效果            
        | ele | ↔ | ele | ↔ | ele |  ↔ | ele |   
        为 even 时， spacing 的值强制为0。


    itemsAlign : str | None, optional
        设置子控件的从轴对齐

        Column 取值为 top, center, bottom, None
        Row 取值为 left, center, right, None

        注意， 如果设置了 itemsAlign ，会阻止子控件的 sizepolicy Expanding。
        参考 https://stackoverflow.com/q/25512664/2602410


    spacing : int, optional
        子子控件之间的间隔，单位 px, 缺省为 10px。 

        如果为-1， 表示平均间隔，类似 css flex justify space-between 的效果            
        | ele | ↔ | ele | ↔ | ele |  ↔ | ele |   
        为-1时， justify的值无效。

    size: list | tuple | None, optional
        设置自身的尺寸，比如 (300, 200) 就是宽度300px，高度200px

    width : int | None, optional
        设置自身的固定宽度
    height : int | None, optional
        设置自身的固定高度

    minWidth : int | None, optional
        设置最小宽度
    minHeight : int | None, optional
        设置最小高度
    maxWidth : int | None, optional
        设置最大宽度
    maxHeight : int | None, optional
        设置最大高度

    stretchFactor : int, optional
        设置容器控件自身 在上级容器中的扩展权重

    align : str | None, optional
        设置容器控件自身 在上级容器中的对齐

    color : str | None, optional
        字体颜色
    bgColor : str | None, optional
        背景颜色
    fontSize : int | None, optional
        字体大小 
    fontFamily : str | None, optional
        字体，比如 "微软雅黑"
        
    border : str | None, optional
        边框，比如 "1px solid #367fa9"

    paddings : int | list, optional
        内边距，单位 px，可以是整数，或者是列表
        比如 paddings=10 表示四边距都是 10px
        paddings=[10, 20, 30, 40] 表示 左10px，上20px，右30px，下40px

    hExpanding : bool, optional
        是否横向扩展，缺省为 True
    vExpanding : bool, optional
        是否纵向扩展，缺省为 True

    name : str | None, optional
        setObjectName 设置的名称

    styleSheet : str, optional
        该控件的styleSheet，用来设置其它参数没有设置的样式
    """    
    windowTitle:str|None=None
    itemsJustify:str|None=None
    itemsAlign:str|None=None  
    spacing:int=10

    size:tuple[int,int]|None=None
    width:int|None=None
    height:int|None=None
    minWidth:int|None=None
    minHeight:int|None=None 
    maxWidth:int|None=None
    maxHeight:int|None=None

    stretchFactor:int=0
    align:str|None=None

    color: str|None=None
    bgColor:str|None=None
    fontSize:int|None=None
    fontFamily:str|None=None
    border:str|None=None
    paddings:int|list=0  
    hExpanding:bool=True   
    vExpanding:bool=True
    name:str|None=None
    styleSheet:str=''

    
def spacing(value:int):
    return  f'spacing:{value}'  # ['spacing', value] 

stretch = 'stretch'

class _Container(QFrame):    
    def __init__(self, *children ):   

        if len(children) == 0:
            s = s__()
        elif isinstance(children[0], s__):
            s = children[0]
            children = children[1:]
        else:
            s = s__()
        
        
        # pass list of widgets as children
        if len(children)==1 and isinstance(children[0], list):
            children = children[0]
            
        self.itemsJustify = s.itemsJustify
        self._hy_stretchFactor = s.stretchFactor
        
        if s.align is not None:
            self._hy_align = s.align
        
        if s.itemsJustify not in ['start', 'center', 'end', 'even', None]:
            raise ValueError("justify must be 'start', 'center', 'end', 'even', None")


        if s.itemsJustify and 'stretch' in children:
            raise ValueError('stretch as child must with justify set as None')
        
        if s.itemsAlign is not None:
            self.alignValue =  self.AlignTable.get(s.itemsAlign)
            if self.alignValue is None:
                raise ValueError(f'align `{s.itemsAlign}` not in {self.AlignTable.keys()}')
        else:
            self.alignValue =  None

        super().__init__()

        if s.windowTitle is not None:
            self.setWindowTitle(s.windowTitle)

        self.lo :QBoxLayout = self.LayoutBox(self)

        if s.size:
            self.resize(*s.size)
                
        if s.width is not None:
            self.setFixedWidth(s.width)

        if s.height is not None:
            self.setFixedHeight(s.height)

        if s.minWidth is not None:
            self.setMinimumWidth(s.minWidth)

        if s.minHeight is not None:
            self.setMinimumHeight(s.minHeight)

        if s.maxWidth is not None:
            self.setMaximumWidth(s.maxWidth)

        if s.maxHeight is not None:
            self.setMaximumHeight(s.maxHeight)

        if isinstance(s.paddings, int):
            self.lo.setContentsMargins(s.paddings, s.paddings, s.paddings, s.paddings)
        else:
            self.lo.setContentsMargins(*s.paddings)


        if s.spacing < 0 :
            s.spacing = 0
            
        self.lo.setSpacing(s.spacing)    



        style = ''

        if s.border is not None:
            style += f'  border: {s.border};\n'
        
        if s.color is not None:
            style += f'  color: {s.color};\n'
        
        if s.bgColor is not None:
            style += f'  background-color: {s.bgColor};\n'

        if s.fontSize is not None:
            style += f'  font-size: {s.fontSize}px;\n'

        if s.fontFamily is not None:
            style += f'  font-family: {s.fontFamily};\n'
        
        
        if s.name:
            self.setObjectName(s.name)

        if style or s.styleSheet:    
            oid = s.name
            if not s.name:
                oid = _randomString()   
                self.setObjectName(oid)
            self.setStyleSheet(f'#{oid} {{\n{style}\n}}\n\n{s.styleSheet}')    
               

        hp = QSizePolicy.Expanding if s.hExpanding else QSizePolicy.Fixed
        vp = QSizePolicy.Expanding if s.vExpanding else QSizePolicy.Fixed
        self.setSizePolicy(hp, vp)

        
        # 添加一个children属性，方便遍历子控件
        self.children = list(children)  # 因为 children 一般是 tuple 类型，所以需要转换

        lastIdx = len(children) - 1    

        if s.itemsJustify in ['end','center']:
            self.lo.addStretch()
        
        for idx, child in enumerate(children):
            if child == 'stretch':
                self.lo.addStretch()
                continue

            if isinstance(child, str) and  child.startswith('spacing:'):
                value = int(child.split(':')[1])
                self.lo.addSpacing(value)
                continue
            
            stretchFactor = 0
            if hasattr(child, '_hy_stretchFactor'):
                stretchFactor = child._hy_stretchFactor

            # if stretchFactor > 0:
            #     print('===', child, 'stretchFactor:', stretchFactor)

            if isinstance(child, QLayout):
                self.lo.addLayout(child, stretchFactor)
            else:
                self.lo.addWidget(child, stretchFactor)

            # 设置子控件的对齐, 注意会阻止子控件的 sizepolicy Expanding，如果不需要，不要设置
            # 参考 https://stackoverflow.com/q/25512664/2602410
            if self.alignValue is not None:
                # 对于分割线，不设置，否则分割线扩展策略不生效，会看不见
                if isinstance(child, VerticalLine) or isinstance(child, HorizontalLine):
                    continue
                self.lo.setAlignment(child, self.alignValue)
            if hasattr(child, '_hy_align'):
                alignValue =  self.AlignTable.get(child._hy_align)
                if alignValue is None:
                    raise ValueError(f'align `{child._hy_align}` not in {self.AlignTable.keys()}')
                self.lo.setAlignment(child, alignValue)

            # 类似 css flex justify space-between 的效果
            if self.itemsJustify == 'even' and idx != lastIdx:
                self.lo.addStretch()

        if s.itemsJustify in ['start','center']:
            self.lo.addStretch()



    def append(self, child, *args, **kwargs):
        
        def _add(child):  
            if isinstance(child, QLayout, *args, **kwargs):
                self.lo.addLayout(child, *args, **kwargs)
            else:
                self.lo.addWidget(child, *args, **kwargs)

            if self.alignValue is not None:
                self.lo.setAlignment(child, self.alignValue)

        def _insert(child, index):  
            if isinstance(child, QLayout):
                self.lo.insertLayout(index, child, *args, **kwargs)
            else:
                self.lo.insertWidget(index, child, *args, **kwargs)

            if self.alignValue is not None:
                self.lo.setAlignment(child, self.alignValue)

            
        # 类似 css flex justify space-between 的效果
        if self.itemsJustify == 'even':     
            #   ele   
            #   ele   ↔   ele   ↔    ele
            
            # ***** 如果原来里面为空 ， 不需要插入 SpacerItem
            if len(self.children)==0:
                _add(child)  

            # ***** 如果原来里面非空，需要先加 SpacerItem，后面再加 child
            else:
                self.lo.addStretch()
                _add(child)   

        elif self.itemsJustify == 'start'  :
            #   ele    ele    ele   ↔
            _insert(child, len(self.children))

        elif self.itemsJustify == 'center' :
            #    ↔    ele    ele    ↔
            _insert(child, len(self.children)+1)

        elif self.itemsJustify == 'end' or self.itemsJustify == None:
            #    ↔    ele    ele   
            #    ele    ele     
            _add(child)

        # children属性里面不包含 spacerItem
        self.children.append(child)

    def insert(self, index, child, *args, **kwargs):
        """
        Inserts a child widget or layout at the specified index within the layout.

        :param index: The position at which the child should be inserted.
        :type index: int
        :param child: The widget or layout to be inserted.
        :type child: QWidget or QLayout
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.

        The method handles different justification cases such as 'start', 'center',
        and 'end', and inserts spacer items to achieve CSS-like flex justify 
        space-between effects when justify is 'even'. 
        """

        def _insert(child, index):  
            if isinstance(child, QLayout):
                self.lo.insertLayout(index, child, *args, **kwargs)
            else:
                self.lo.insertWidget(index, child, *args, **kwargs)

            if self.alignValue is not None:
                self.lo.setAlignment(child, self.alignValue)

        # index 为 负数/最后一个/超过范围   都视为添加在最后， 走 append 方法
        if index < 0 or index >= len(self.children):
            return self.append(child, *args, **kwargs)
        
        # 剩下情况的只可能是 ： index >=0  并且  原来里面有元素


        # 类似 css flex justify space-between 的效果
        if self.itemsJustify == 'even' :
            #   ele   ↔   ele   ↔   ele    ↔   ele          
            #    0         1          2          3
            #    0    1    2     3    4    5     6        
       
            # ** 如果是插入位置是第一个，还要插入后面的 SpacerItem
            if index == 0:
                _insert(child, 0) 
                self.lo.insertStretch(1)
                return    

            # ** 插入位置不是第一个， 也不是最后一个（因为最后一个走 append 方法）
            #   ele   ↔   ele
            else:
                real_index = 2*index
                self.lo.insertStretch(real_index)  
                _insert(child, real_index)   

        elif self.itemsJustify == 'start' or self.itemsJustify == None:
            #   ele    ele     ↔
            #   ele    ele    
            _insert(child, index)

        elif self.itemsJustify == 'center' or self.itemsJustify == 'end':
            #    ↔    ele    ele    ↔
            #    ↔    ele    ele    
            _insert(child, index+1)

        # children属性里面不包含 spacerItem
        self.children.insert(index, child)


    def remove(self,  child, deleteAlso=False):
        """
        去掉内部指定子控件

        :param child: 子控件
        :param deleteAlso: 是否删除该子控件
        """
        def _deleteStretch(index):
            itemToRemove = self.lo.takeAt(index)
            if itemToRemove:
                self.lo.removeItem(itemToRemove);
                del itemToRemove

        # if child not in self.children:
        #     return
        
        index = self.children.index(child)

        # 不存在，直接返回
        if index == -1:
            return
        

        # **  如果是 justify == 'even' ， 并且 不止一个元素,  先删除 spacerItem **
        if self.itemsJustify == 'even' and len(self.children)>1:
            #   ele   ↔   ele   ↔   ele    ↔   ele          
            #    0         1          2          3
            #    0    1    2     3    4    5     6        


            # 是第一个元素， 删除后面的 SpacerItem
            if index == 0: 
                _deleteStretch(1)
            # 不是第一个元素， 删除前面的 SpacerItem
            else:
                _deleteStretch(2*index-1)


        # 其它的 justfy 情况 不需要特别处理
            #   ele   ele                  #  justify == None
            #   ele                        #  justify == 'even' and 只有一个元素   
            #    ↔    ele    ele    ↔      #  justify == 'center'
            #    ↔    ele    ele           #  justify == 'start'
            #   ele   ele     ↔            #  justify == 'end'


        # ** 再删除元素 **
        if isinstance(child, QLayout):
            clearLayout(child)
            # child.setParent(None)
        else:
            self.lo.removeWidget(child)

        if deleteAlso:    
            child.deleteLater()
                
        self.children.remove(child)


    def delete(self, child):
        """
        去掉内部指定子控件，并删除该子控件对象

        :param child: 子控件
        """
        self.remove(child, deleteAlso=True)

    def clear(self):
        """
        清空所有内部子控件
        """
        clearLayout(self.lo, )
        # self.lo.deleteLater()
        
        self.children = []

        # 再 补充 SpacerItem

        # if self.itemsJustify == 'even' :
        #     #   ele   ↔   ele   ↔   ele    ↔   ele          
        #    return
        
        
        if self.itemsJustify == 'start' or self.itemsJustify == 'end':
            #    ↔
            #    ↔
            self.lo.addStretch()
            return

        if self.itemsJustify == 'center':
            #    ↔    ↔
            self.lo.addStretch()



    def preSibling(self, child):        
        """
        Return the previous sibling widget of the given widget.

        Args:
            child (QWidget): the given widget

        Returns:
            QWidget or None: the previous sibling widget, or None if the given widget is the first one
        """
        idx = self.children.index(child)
        if idx == -1 or idx == 0:    
            return None
        return self.children[idx-1]

    def nextSibling(self, child):        
        """
        Return the next sibling widget of the given widget.

        Args:
            child (QWidget): the given widget

        Returns:
            QWidget or None: the next sibling widget, or None if the given widget is the last one
        """
        idx = self.children.index(child)
        if idx == -1 or idx == len(self.children)-1:
            return None
        return self.children[idx+1]
    
    def replaceWidget(self, oldWidget, newWidget, deleteOldWidget=False):
        """
        Replace oldWidget with newWidget in the layout of this container.

        Args:
            oldWidget (QWidget): the widget to be replaced
            newWidget (QWidget): the widget to replace with
            deleteOldWidget (bool): whether to delete the old widget after replacement

        Returns:
            None
        """
        oldItem = self.lo.replaceWidget(oldWidget, newWidget) 
        if not oldItem: 
            return 
        
        if deleteOldWidget:
            oldWidget.deleteLater()


# Row is a QFrame container with horizental layout 
class Row(_Container):
    AlignTable = {
        'center': QtCore.Qt.AlignVCenter,
        'top':    QtCore.Qt.AlignTop,
        'bottom': QtCore.Qt.AlignBottom,
    }

    LayoutBox = QHBoxLayout

    def subClassSetup(self):...
        # if self.itemsJustify == 'left':
        #     self.itemsJustify = 'start'
        # elif self.itemsJustify == 'right':
        #     self.itemsJustify = 'end'
            
# Column is a QFrame container with vertical layout
class Column(_Container):
    AlignTable = {
        'center': QtCore.Qt.AlignHCenter,
        'left':   QtCore.Qt.AlignLeft,
        'right':  QtCore.Qt.AlignRight,
    }

    LayoutBox = QVBoxLayout

    
    def subClassSetup(self):...
        # if self.itemsJustify == 'top':
        #     self.itemsJustify = 'start'
        # elif self.itemsJustify == 'bottom':
        #     self.itemsJustify = 'end'




def createForm( fields:list|dict, okBtnText='确定', 
               okCallback=None, cancelCallback=None):
    
    fieldsFrame = QFrame()
    fieldsLayout = QVBoxLayout(fieldsFrame)
    fieldsLayout.setSpacing(0)

    # （name, widget）   的控件 列表或者字典
    if isinstance(fields, dict) or isinstance(fields, list):
        if isinstance(fields, dict):
            fields = fields.items()
            
        for name, widget in fields:        
            fieldsLayout.addWidget(QLabel(name))
            fieldsLayout.addWidget(widget)
            
            fieldsLayout.addSpacing(20)
    else:
        # 单独的一个控件，直接显示
        fieldsLayout.addWidget(fields)


    actionLayout = QHBoxLayout()
    fieldsLayout.addSpacing(8)
    fieldsLayout.addLayout(actionLayout)
    
    btnOk = Button_NoBorder_Little('确定')
    btnCancel = Button_NoBorder_Little('取消')

    
    btnOk.clicked.connect(
        lambda: okCallback(fieldsFrame)
    )
    btnCancel.clicked.connect(
        lambda: cancelCallback(fieldsFrame)
    )
            
    actionLayout.addWidget(btnOk)
    actionLayout.addWidget(btnCancel)

    return fieldsFrame


# 达到类似HTML中 flexbox 的效果
class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super().__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()




# testing code below

