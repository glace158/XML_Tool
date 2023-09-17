from PySide6.QtWidgets import *
from fileImporter import FileImporter

class WidgetDisplay():#widget 화면 구성
    def get_layout(self):
        layouts = self._setting_widgets()
        v_layout = QVBoxLayout()

        for layout in layouts: 
            v_layout.addLayout(layout)
        
        return v_layout

    def _setting_widgets(self):
        layouts = []
        name_edit = QLineEdit()
        layouts.append(self._create_label_widget("Name", name_edit))
        
        pin_button = QPushButton("Pin Setting")
        layouts.append(self._create_label_widget("Pin", pin_button))

        shape_combo = QComboBox()
        shape_combo.addItem("rectangle")
        shape_combo.addItem("Circle")
        shape_combo.addItem("Diamond")
        layouts.append(self._create_label_widget("Shape", shape_combo))
        
        img_edit = FileImporter("Drag&Drop here")
        layouts.append(self._create_label_widget("Iamge URL", img_edit))
        
        content_button = QPushButton("Contents Setting")
        layouts.append(self._create_label_widget("Contents", content_button))
        return layouts
    
    def _create_label_widget(self, label_text:str, widget:QWidget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout
    
