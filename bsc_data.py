import os
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtCore import Qt

class BscDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(__file__)

        icon_path = os.path.join(base_dir, 'ptlogo.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle("Basic Data Reports (ver. 2.0)")
        self.setFixedSize(800, 600)
        self.bg_pixmap = QPixmap(os.path.join(base_dir, 'bgpoke.png'))

        # Read available report images
        data_dir = os.path.join(base_dir, 'pokemon_total_data')
        svg_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.svg')]
        self.report_names = [os.path.splitext(f)[0] for f in svg_files]
        self.svg_paths = {name: os.path.join(data_dir, name + '.svg') for name in self.report_names}

        # Combo box
        self.combo = QComboBox()
        self.combo.addItems(self.report_names)
        self.combo.currentTextChanged.connect(self.update_chart)
        # Style combo: taller, internal padding, border, rounded, shadow
        self.combo.setFixedHeight(50)
        self.combo.setStyleSheet(
            "QComboBox {"
            "  padding: 5px"
            "  border: 1px solid #707070;"
            "  border-radius: 8px;"
            "  background: white;"
            "}"
        )
        combo_shadow = QGraphicsDropShadowEffect(self)
        combo_shadow.setBlurRadius(10)
        combo_shadow.setOffset(0, 2)
        self.combo.setGraphicsEffect(combo_shadow)

        # Chart container
        container = QWidget()
        container.setFixedSize(700, 450)
        container.setStyleSheet(
            "QWidget {"
            "  border: 3px dashed #b0b0b0;"
            "  border-radius: 12px;"
            "  background-color: rgba(255,255,255,153);"
            "}"
        )
        container_shadow = QGraphicsDropShadowEffect(self)
        container_shadow.setBlurRadius(12)
        container_shadow.setOffset(0, 3)
        container.setGraphicsEffect(container_shadow)

        # SVG display
        self.svg_widget = QSvgWidget()
        self.svg_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.svg_widget.setStyleSheet("background: transparent;")

        # Layouts
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.combo)
        top_layout.addStretch()

        chart_layout = QVBoxLayout(container)
        chart_layout.setContentsMargins(10, 10, 10, 10)
        chart_layout.addWidget(self.svg_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(container)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Initial chart
        self.update_chart(self.report_names[0])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg_pixmap)

    def update_chart(self, name):
        path = self.svg_paths.get(name)
        if path and os.path.exists(path):
            self.svg_widget.load(path)
