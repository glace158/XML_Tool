import sys
from PySide6.QtWidgets import *
from nodeGraph import *
class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("NodeMaker")
        self.setFixedSize(700,500)
        # Create widgets
        self.layouts = []
        
        self.setting_widgets()
        self.node_display()
        self.setting_layouts()
        
        self.node_create()
        # Add button signal to greetings slot
        #        self.button.clicked.connect(self.greetings)
    
    def setting_widgets(self):
        self.name_edit = QLineEdit()
        self.layouts.append(self.create_label_layout("Name", self.name_edit))
        
        self.pin_button = QPushButton("Pin Setting")
        self.layouts.append(self.create_label_layout("Pin", self.pin_button))

        self.shape_combo = QComboBox()
        self.shape_combo.addItem("rectangle")
        self.shape_combo.addItem("Circle")
        self.shape_combo.addItem("Diamond")
        self.layouts.append(self.create_label_layout("Shape", self.shape_combo))
        
        self.img_edit = FileEdit("Drag&Drop here")
        self.layouts.append(self.create_label_layout("Iamge URL", self.img_edit))
        
        self.content_button = QPushButton("Contents Setting")
        self.layouts.append(self.create_label_layout("Contents", self.content_button))

    def node_display(self):
        self.node_view = QGraphicsView()
        self.node_graph = BackgroundGraph()
        self.node_view.setInteractive(False)
        self.node_view.setScene(self.node_graph)

    def node_create(self):
        self.node_graph.addItem(NodeGraphics("test"))

    def setting_layouts(self):
        # Create layout and add widgets
        h_layout = QHBoxLayout()
        
        v_layout = QVBoxLayout()

        for layout in self.layouts: 
            v_layout.addLayout(layout)
        
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self.node_view)    
        # Set dialog layout
        self.setLayout(h_layout)

    def create_label_layout(self, label_text:str, widget:QWidget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout
    
    # Greets the user
    def greetings(self):
        print(f"Hello {self.edit.text()}")
        
class FileEdit(QLineEdit):
    def __init__( self, parent=None):
        super(FileEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent( self, event ):
        data = event.mimeData()
        urls = data.urls()
        if ( urls and urls[0].scheme() == 'file' ):
            event.acceptProposedAction()

    def dragMoveEvent( self, event ):
        data = event.mimeData()
        urls = data.urls()
        if ( urls and urls[0].scheme() == 'file' ):
            event.acceptProposedAction()

    def dropEvent( self, event ):
        data = event.mimeData()
        urls = data.urls()
        if ( urls and urls[0].scheme() == 'file' ):
            # for some reason, this doubles up the intro slash
            filepath = str(urls[0].path())[1:]
            self.setText(filepath)
            
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())