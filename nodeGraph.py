from typing import Optional
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from abc import *
import math

import PySide6.QtWidgets
from PySide6.QtWidgets import QGraphicsItem

class BackgroundGraph(QGraphicsScene):
    def __init__(self):
        super().__init__()

        # settings
        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

        #self.scene_width = 64000
        #self.scene_height = 64000
        #self.setSceneRect(-self.scene_width / 2, -self.scene_height / 2, self.scene_width, self.scene_height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(x, top, x, bottom))
            else: lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % (self.gridSize*self.gridSquares) != 0): lines_light.append(QLine(left, y, right, y))
            else: lines_dark.append(QLine(left, y, right, y))


        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)

#원본 객체와 장식된 객체 모두를 묶는 인터페이스
class INode(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem | None = ...) -> None:
        super().__init__(parent)

        self.width = 150
        self.height = 300
        self.node_shape = "RECTANGLE"
        color = "GRAY"

        self.edge_size = 10#라운딩 엣지
        self.title_height = 24
        self._padding = 4

        self.set_color(color)
        self.content()
        
    def set_color(self, color:str, title_color:str = None):
        pass

    def content(self):
        pass

# 장식될 원본 객체
class Node(INode):
    def __init__(self, parent: QGraphicsItem | None = ...) -> None:
        super().__init__(parent)

    def set_color(self, color: str, title_color: str = None):
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

        if (title_color != None) and (title_color in color_list):
            title_color_code = color_list.get(title_color)
        else:
            title_color_code = color_code

        self._pen_default = QPen(QColor("#000000"))#외각 테두리
        self._pen_selected = QPen(QColor("#FFFFA637"))#선택 시 테두리

        self._brush_title = QBrush(QColor(title_color_code))#타이틀 배경 색상
        self._brush_background = QBrush(QColor(color_code))#배경 색상

    def content(self):
        pass

class NodeDecorator(INode):
    def __init__(self, component:INode):
        super().__init__()
        self.component = component
    
    def set_color(self, color: str, title_color: str = None):
        self.component.set_color(color, title_color)
    
    def content(self):
        self.component.content()

class LabelDecorator(NodeDecorator):
    def __init__(self, text:str, component: INode):
        super().__init__(component)
        self.text = text
    
    def set_color(self, color: str, title_color: str = None):
        super().set_color(color, title_color)
    
    def content(self):
        super().content()
        font = QFont("Ubuntu", 12)
        self.item = QLabel(self.text)
        self.item.setFont(font)
        
        self.item.move(10, 10)
        self.grContent = QGraphicsProxyWidget(self)

        self.item.setStyleSheet(
            """
            color: white;
            background: #00000000;
            """
            )
        
        self.grContent.setWidget(self.item)

class LineEditDecorator(NodeDecorator):
    def __init__(self, component: INode):
        super().__init__(component)
        
    def set_color(self, color: str, title_color: str = None):
        super().set_color(color, title_color)
    
    def content(self):
        super().content()
        self.grContent = QGraphicsProxyWidget(self)
        line_edit = QLineEdit(self)
        line_edit.setText("1")

        line_edit.setStyleSheet("background: #e0e0e0;")
        line_edit.move(100, 65)
        line_edit.setFixedWidth(20)  # 위젯 폭
        line_edit.setFixedHeight(20)  # 위젯 높이

        self.grContent.setWidget(line_edit)

class NodeGraphics(QGraphicsItem):
    def __init__(self, title:str):
        super().__init__()

        self.width = 150
        self.height = 300
        self.node_shape = "RECTANGLE"
        color = "GRAY"

        self.edge_size = 10#라운딩 엣지
        self.title_height = 24
        self._padding = 4

        self.set_color(color)
        self.initcontent(title)
        
        self.initTitle(title)

    
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

    def initTitle(self, title):

        title_font_color = Qt.white
        title_font = QFont("Ubuntu", 12)
        self.title_item = QLabel(title)
        #title_item.setPlainText(title)
        self.title_item.setStyleSheet("color: white;")
        #self.title_item.setDefaultTextColor(title_font_color)
        self.title_item.setFont(title_font)
        self.title_item.move(self._padding, 0)
        #self.title_item.setTextWidth(
        #    self.width
        #    - 2 * self._padding
        #)

    def initcontent(self, title:str):
        
        #self.content = QLabel("add")
        title_font = QFont("Ubuntu", 12)
        self.title_item = QLabel(title)
        self.title_item.setFont(title_font)
        
        self.title_item.move(10, 10)
        self.grContent = QGraphicsProxyWidget(self)

        #self.content.setGeometry(self.edge_size,
        #                            self.title_height * 2 // 3 + self.edge_size,
        #                            self.width - 2 * self.edge_size,
        #                            self.height - 2 * self.edge_size - self.title_height * 2 // 3)

        self.title_item.setStyleSheet(
            """
            color: white;
            background: #00000000;
            """
            )
        self.grContent.setWidget(self.title_item)
        
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        
        if self.node_shape == "RECTANGLE":
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

        elif self.node_shape == "CIRCLE":
            # title
            path_title = QPainterPath()
            path_title.setFillRule(Qt.WindingFill)
            title_coords = [QPointF(self.width / 2, 0), QPointF(0, self.height / 2),
                            QPointF(self.width / 2, self.height), QPointF(self.width, self.height / 2)]
            self.bluepolygon = QPolygonF(title_coords)
            path_title.addPolygon(self.bluepolygon)
            painter.setPen(Qt.NoPen)
            # painter.setBrush(self._brush_background)
            painter.drawPath(path_title.simplified())

            # content
            path_content = QPainterPath()
            path_content.setFillRule(Qt.WindingFill)
            path_content.addEllipse(0, 0, self.width, self.height)
            # path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
            # path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._brush_background)
            painter.drawPath(path_content.simplified())

            # outline
            path_outline = QPainterPath()
            path_outline.addEllipse(0, 0, self.width, self.height)
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path_outline.simplified())

        elif self.node_shape == "RHOMBUS":
            path_title = QPainterPath()
            path_title.setFillRule(Qt.WindingFill)
            title_coords = [QPointF(self.width / 2, 0), QPointF(0, self.height / 2), QPointF(self.width / 2, self.height), QPointF(self.width, self.height / 2)]
            self.bluepolygon = QPolygonF(title_coords)
            path_title.addPolygon(self.bluepolygon)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._brush_background)
            painter.drawPath(path_title.simplified())

            # content
            path_content = QPainterPath()
            path_content.setFillRule(Qt.WindingFill)
            contet_coords = [QPointF(self.width / 2, 0), QPointF(0, self.height / 2), QPointF(self.width / 2, self.height),
                      QPointF(self.width, self.height / 2)]
            self.bluepolygon = QPolygonF(contet_coords)
            path_content.addPolygon(self.bluepolygon)

            painter.setPen(Qt.NoPen)
            painter.setBrush(self._brush_background)
            painter.drawPath(path_content.simplified())

            # outline
            outline_coords = [QPointF(self.width/2, 0), QPointF(0, self.height/2), QPointF(self.width/2, self.height), QPointF(self.width, self.height/2)]
            self.bluepolygon = QPolygonF(outline_coords)
            path_outline = QPainterPath()
            path_outline.addPolygon(self.bluepolygon)
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path_outline.simplified())

