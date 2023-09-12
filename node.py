from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from PySide6.QtWidgets import QGraphicsItem

class INode(QGraphicsItem):#원본 객체와 장식된 객체 모두를 묶는 인터페이스
    def __init__(self, parent: QGraphicsItem = None) -> None:
        super().__init__(parent)
    
    def content(self):
        raise NotImplementedError
    
    
class Node(INode):#장식될 원본 객체
    def __init__(self, parent: QGraphicsItem = None) -> None:
        super().__init__(parent)
        self.width = 150
        self.height = 300
        self.node_shape = "RECTANGLE"
        color = "RED"
        self.title = "test"
        self.edge_size = 10#라운딩 엣지
        self.title_height = 24
        self._padding = 4
        
        self.set_color(color)
        self.content()

    def boundingRect(self):
        return QRectF(
            0,
            0,
            2 * self.edge_size + self.width,
            2 * self.edge_size + self.height
        ).normalized()
    
    def set_color(self, color:str, tilte_color:str=None):
        color_list = {
            "BLACK": "#000000",
            "WHITE": "#FFFFFF",
            "RED": "#FF0000",
            "GREEN": "#008000",
            "BLUE": "#0000FF",
            "YELLOW": "#FFFF00",
            "CYAN": "#00FFFF",
            "MAGENTA": "#FF00FF",
            "GRAY": "#808080",
            "LIGHT GRAY": "#D3D3D3",
            "DARK GRAY": "#A9A9A9",
            "BROWN": "#A52A2A",
            "ORANGE": "#FFA500",
            "PINK": "#FFC0CB",
            "PURPLE": "#800080",
            "LIME": "#00FF00",
            "OLIVE": "#808000",
            "SIENNA": "#A0522D",
            "GOLD": "#FFD700",
            "SILVER": "#C0C0C0",
            "NAVY BLUE": "#000080",
            "AQUA": "#00FFFF",
            "TEAL": "#008080",
            "FUCHSIA": "#800080",
            "ARDUINO" : "#008CBA"
        }

        color_code = "#000000"#black
        if color.upper() in color_list:
            color_code = color_list.get(color.upper())
        elif '#' in color:
            color_code = color

        if (tilte_color != None) and (tilte_color in color_list):
            tilte_color_code = color_list.get(tilte_color)
        else:
            tilte_color_code = color_code

        self._pen_default = QPen(QColor("#000000"))#외각 테두리
        self._pen_selected = QPen(QColor("#FFFFA637"))#선택 시 테두리

        self._brush_title = QBrush(QColor(tilte_color_code))#타이틀 배경 색상
        self._brush_background = QBrush(QColor(color_code))#배경 색상

        

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)#라운딩 박스 그리기
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)#라운딩 된 부분 매꾸기
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)#라운딩 된 부분 매꾸기
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

    def content(self):
        pass
    
class NodeDecorator(INode): # 장식자 추상 클래스
    def __init__(self, component : INode, parent: QGraphicsItem = None) -> None:
        super().__init__(parent)
        self.wrappee = component #원본 객체를 composition

    def content(self):
        self.wrappee.content()#위임
    
    def boundingRect(self):
        self.wrappee.boundingRect()
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        self.wrappee.paint(painter, option, widget)


class LineEditDecorator(NodeDecorator):#장식자 클래스
    def __init__(self, component: INode, parent: QGraphicsItem = None) -> None:
        super().__init__(component, parent)
        self.content()
    def content(self):
        super().content()#원본 객체를 상위 클래스의 위임을 통해 실행하고
        '''
        print("test")
        #장식 클래스만의 메소드를 실행한다.
        title_font = QFont("Ubuntu", 12)
        self.title_item = QLabel("test")
        self.title_item.setFont(title_font)

        self.title_item.move(10, 10)
        
        self.title_item.setStyleSheet(
            """
            color: white;
            background: #00000000;
            """
            )
        '''
        line_edit = QLineEdit()
        line_edit.setText("1")

        line_edit.setStyleSheet("background: #e0e0e0;")
        line_edit.move(10, 10)
        line_edit.setFixedWidth(20)  # 위젯 폭
        line_edit.setFixedHeight(20)  # 위젯 높이
        self.grContent = QGraphicsProxyWidget(self)
        self.grContent.setWidget(line_edit)  
