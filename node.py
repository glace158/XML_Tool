from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QGraphicsItem



class INode(QGraphicsItem):#원본 객체와 장식된 객체 모두를 묶는 인터페이스
    def __init__(self, parent: QGraphicsItem = None) -> None:
        super().__init__(parent)
        
        self.width = 200
        self.height = 300
        self.node_shape = "RECTANGLE"
        color = "GRAY"
        self.title = "test"
        self.edge_size = 10#라운딩 엣지
        self.title_height = 24
        self.padding = 4

        self.set_color(color)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)


    def boundingRect(self):
        return QRectF(
            0,
            0,
            2 * self.edge_size + self.width,
            2 * self.edge_size + self.height
        ).normalized()
    
    def add_content(self, content:QWidget):
        print("add_content")
        self.content = content
        self.gr_content = QGraphicsProxyWidget(self)
        
        self.content.setGeometry(self.edge_size,
                                    self.title_height * 2 // 3 + self.edge_size,
                                    self.width - 2 * self.edge_size,
                                    self.height - 2 * self.edge_size - self.title_height * 2 // 3)
        

        self.content.setStyleSheet("background: #00000000;")
        
        self.gr_content.setWidget(self.content)

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

        self.pen_default = QPen(QColor("#000000"))#외각 테두리
        self.pen_selected = QPen(QColor("#FFFFA637"))#선택 시 테두리

        self.brush_title = QBrush(QColor(tilte_color_code))#타이틀 배경 색상
        self.brush_background = QBrush(QColor(color_code))#배경 색상
    
class RectangleNode(INode):#제품 구현체
    def __init__(self, parent: QGraphicsItem = None) -> None:
        super().__init__(parent)
    
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)#라운딩 박스 그리기
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)#라운딩 된 부분 매꾸기
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)#라운딩 된 부분 매꾸기
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

    def content(self):
        pass

class CircleNode(INode):#제품 구현체
    def __init__(self, parent: QGraphicsItem = None) -> None:
        super().__init__(parent)
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        title_coords = [QPointF(self.width / 2, 0), QPointF(0, self.height / 2),
                        QPointF(self.width / 2, self.height), QPointF(self.width, self.height / 2)]
        self.bluepolygon = QPolygonF(title_coords)
        path_title.addPolygon(self.bluepolygon)
        painter.setPen(Qt.NoPen)
        # painter.setBrush(self.brush_background)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addEllipse(0, 0, self.width, self.height)
        # path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        # path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addEllipse(0, 0, self.width, self.height)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

class DiamondNode(INode):
    def __init__(self, parent: QGraphicsItem = None) -> None:
        super().__init__(parent)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        title_coords = [QPointF(self.width / 2, 0), QPointF(0, self.height / 2), QPointF(self.width / 2, self.height), QPointF(self.width, self.height / 2)]
        self.bluepolygon = QPolygonF(title_coords)
        path_title.addPolygon(self.bluepolygon)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        contet_coords = [QPointF(self.width / 2, 0), QPointF(0, self.height / 2), QPointF(self.width / 2, self.height),
                    QPointF(self.width, self.height / 2)]
        self.bluepolygon = QPolygonF(contet_coords)
        path_content.addPolygon(self.bluepolygon)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        outline_coords = [QPointF(self.width/2, 0), QPointF(0, self.height/2), QPointF(self.width/2, self.height), QPointF(self.width, self.height/2)]
        self.bluepolygon = QPolygonF(outline_coords)
        path_outline = QPainterPath()
        path_outline.addPolygon(self.bluepolygon)
        painter.setPen(self.pen_default if not self.isSelected() else self.pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

class NodeFactory():
    def get_node(self, node_type):
        if node_type == "circle":
            node = CircleNode()
        if node_type == "diamond":
            node = DiamondNode()
        else:
            node = RectangleNode()
        
        return node
    


class IContent(QWidget):#원본 객체와 장식된 객체 모두를 묶는 인터페이스
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.contents = []

    def set_content(self, content:QWidget):
        raise NotImplementedError
    
    
class NodeContent(IContent):#장식될 원본 객체
    def __init__(self, parent: QWidget = None):
        super().__init__(parent) 

    def set_content(self, content:QWidget):
        print("base")
        print(self.contents)
        self.contents.append(content)
        return self

class NodeDecorator(IContent): # 장식자 추상 클래스

    _component : IContent = None

    def __init__(self, component : IContent, parent: QWidget = None):
        super().__init__(parent)
        self._component = component #원본 객체를 composition

    @property
    def component(self) -> IContent:
        return self._component

    def set_content(self, content:QWidget):
        return self._component.set_content(content)#위임

class LineEditDecorator(NodeDecorator):#장식자 클래스
    #def __init__(self, component: IContent, parent: QWidget = None):
    #    super().__init__(component, parent)
        #self.content()

    def set_content(self, content:QWidget):
        self.component.set_content()#원본 객체를 상위 클래스의 위임을 통해 실행하고
        #장식 클래스만의 메소드를 실행한다.

        print("lineedit")
        print(self.contents)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText("1")

        self.line_edit.setStyleSheet("background: #e0e0e0;")
        self.line_edit.move(20, 20)
        self.line_edit.setFixedWidth(20)  # 위젯 폭
        self.line_edit.setFixedHeight(20)  # 위젯 높이
        

        self.contents.append(self.line_edit)

        return self

class TextDecorator(NodeDecorator):#장식자 클래스
    #def __init__(self, component: IContent, parent: QWidget = None):
    #    super().__init__(component, parent)
        #self.content()

    def set_content(self):
        self.component.set_content()#원본 객체를 상위 클래스의 위임을 통해 실행하고
        
        print("text")
        print(self.contents)
        #장식 클래스만의 메소드를 실행한다.
        #title_font = QFont("Ubuntu", 12)
        #title_item.setFont(title_font)

        self.title_item = QLabel("test",self)
        self.title_item.move(10, 10)
        
        self.title_item.setStyleSheet(
            """
            color: white;
            background: #00000000;
            """
            )
        
        self.contents.append(self.title_item)
        return self

class ContentFactory(QWidget):
    def __init__(self, contents, parent: QWidget = None):
        super().__init__(parent)    
        for content in contents:
            if content["type"] == "label":
                self.set_label()
            elif content["type"] == "line":
                self.set_line_edit()
    def set_label(self):
        self.title_item = QLabel("test",self)
        self.title_item.move(10, 10)
        
        self.title_item.setStyleSheet(
            """
            color: white;
            background: #00000000;
            """
            )
        
    def set_line_edit(self):
        self.line_edit = QLineEdit(self)
        self.line_edit.setText("1")

        self.line_edit.setStyleSheet("background: #e0e0e0;")
        self.line_edit.move(20, 20)
        self.line_edit.setFixedWidth(20)  # 위젯 폭
        self.line_edit.setFixedHeight(20)  # 위젯 높이
