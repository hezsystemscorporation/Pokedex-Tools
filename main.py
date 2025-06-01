import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QLabel
from PySide6.QtGui import QPixmap, QPainter, QFontDatabase, QIcon
from PySide6.QtCore import Qt
from bsc_data import BscDataWindow
from pokedex import PokedexWindow
from damage_calculator import CalculatorWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokémon Tools ver. 4.0 (Copyright 2025 Michael Hertz & DPW Group 6. All rights reserved. )")
        self.setFixedSize(1000, 600)
        base_dir = os.path.dirname(__file__)

        icon_path = os.path.join(base_dir, 'ptlogo.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.bg_pixmap = QPixmap(os.path.join(base_dir, 'background.png'))

        # Load custom fonts
        font_id1 = QFontDatabase.addApplicationFont(os.path.join(base_dir, 'font', '汉仪文黑-65W.ttf'))
        font_families1 = QFontDatabase.applicationFontFamilies(font_id1)
        self.main_font = font_families1[0] if font_families1 else ''
        font_id2 = QFontDatabase.addApplicationFont(os.path.join(base_dir, 'font', 'segoepr.ttf'))
        font_families2 = QFontDatabase.applicationFontFamilies(font_id2)
        self.pokedex_font = font_families2[0] if font_families2 else ''

        main_layout = QVBoxLayout(self)
        # Reduced top margin and layout spacing
        main_layout.setContentsMargins(50, 175, 50, 180)
        main_layout.setSpacing(5)

        # Title logo
        title_label = QLabel(self)
        title_pixmap = QPixmap(os.path.join(base_dir, 'logo.svg')).scaled(525, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        title_label.setPixmap(title_pixmap)
        title_label.setAlignment(Qt.AlignHCenter)
        main_layout.addWidget(title_label)

        # Buttons container with its own layout for tight spacing
        buttons_container = QWidget(self)
        button_layout = QVBoxLayout(buttons_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(3)

        btn1 = QPushButton("Basic Data Reports")
        btn2 = QPushButton("Pokédex Search")
        btn3 = QPushButton("Damage Calculator")

        for btn in (btn1, btn2, btn3):
            btn.setFixedSize(400, 40)
            btn.setStyleSheet(
                f"QPushButton {{ background-color: #FEE6A3; color: #7E5249; font-family: '{self.main_font}'; font-size: 18px; font-weight: bold; border: none; border-radius: 20px; }}"
            )
            effect = QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(12)
            effect.setOffset(0, 3)
            btn.setGraphicsEffect(effect)
            button_layout.addWidget(btn, alignment=Qt.AlignHCenter)

        # Override Pokédex button font only
        btn2.setStyleSheet(
            f"QPushButton {{ background-color: #FEE6A3; color: #7E5249; font-family: '{self.pokedex_font}'; font-size: 18px; font-weight: bold; border: none; border-radius: 20px; }}"
        )

        main_layout.addWidget(buttons_container, alignment=Qt.AlignHCenter)

        btn1.clicked.connect(self.open_bsc)
        btn2.clicked.connect(self.open_pokedex)
        btn3.clicked.connect(self.open_calculator)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg_pixmap)

    def open_bsc(self):
        self.bsc_window = BscDataWindow()
        self.bsc_window.show()

    def open_pokedex(self):
        self.pokedex_window = PokedexWindow()
        self.pokedex_window.show()

    def open_calculator(self):
        self.calculator_window = CalculatorWindow()
        self.calculator_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
