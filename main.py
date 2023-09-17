import sys
from PySide6.QtWidgets import *
from nodeGraph import BackgroundGraph

from widgetDisplay import *
from node import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("NodeMaker")
        self.setFixedSize(1000,700)
        # Create widgets
        self.layouts = []
        
        self.node_display()# 노드 화면 구성
        self.set_display()# 전체 화면 구성

        self.node_create()

    def node_display(self):
        self.node_view = QGraphicsView()
        self.node_graph = BackgroundGraph()
        self.node_view.setInteractive(False)
        self.node_view.setScene(self.node_graph)

    def set_display(self):
        h_layout = QHBoxLayout()
        
        widget_layout = WidgetDisplay().get_layout()

        h_layout.addLayout(widget_layout)
        h_layout.addWidget(self.node_view)    
        # Set dialog layout
        self.setLayout(h_layout)

    def node_create(self):
        node = NodeFactory().get_node("rectangle")
        con_list = [{"type": "label"}, {"type": "line"}]
        content = ContentFactory(con_list)

        node.add_content(content)

        self.node_graph.addItem(node)


    def create_label_layout(self, label_text:str, widget:QWidget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout
     

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())