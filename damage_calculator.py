import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout,
    QCheckBox, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QIcon, QFontDatabase, QPixmap, QPainter, QFont
from PySide6.QtCore import Qt

# Type effectiveness data
type_chart = {
    "Normal": {"Ghost": 0, "Rock": 0.5, "Steel": 0.5},
    "Fire": {"Grass": 2, "Ice": 2, "Bug": 2, "Steel": 2, "Fire": 0.5, "Water": 0.5, "Rock": 0.5, "Dragon": 0.5},
    "Water": {"Fire": 2, "Rock": 2, "Ground": 2, "Water": 0.5, "Grass": 0.5, "Dragon": 0.5},
    "Electric": {"Water": 2, "Flying": 2, "Electric": 0.5, "Grass": 0.5, "Dragon": 0.5, "Ground": 0},
    "Grass": {"Water": 2, "Ground": 2, "Rock": 2, "Fire": 0.5, "Grass": 0.5, "Poison": 0.5, "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Grass": 2, "Ground": 2, "Flying": 2, "Dragon": 2, "Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Rock": 2, "Dark": 2, "Steel": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Ghost": 0, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Fairy": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0},
    "Ground": {"Fire": 2, "Electric": 2, "Poison": 2, "Rock": 2, "Steel": 2, "Grass": 0.5, "Bug": 0.5, "Flying": 0},
    "Flying": {"Grass": 2, "Fighting": 2, "Bug": 2, "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Steel": 0.5, "Dark": 0},
    "Bug": {"Grass": 2, "Psychic": 2, "Dark": 2, "Fire": 0.5, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Flying": 2, "Bug": 2, "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5},
    "Ghost": {"Ghost": 2, "Psychic": 2, "Dark": 0.5, "Normal": 0},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Psychic": 2, "Ghost": 2, "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Ice": 2, "Rock": 2, "Fairy": 2, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
    "Fairy": {"Fighting": 2, "Dragon": 2, "Dark": 2, "Fire": 0.5, "Poison": 0.5, "Steel": 0.5},
}

all_types = sorted(type_chart.keys())

class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(__file__)
        # Window icon
        icon_path = os.path.join(base_dir, 'ptlogo.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle("Final Damage Calculator (ver. 2.0)")
        self.setFixedSize(750, 450)
        # Background image
        self.bg_pixmap = QPixmap(os.path.join(base_dir, 'bgpoke.png'))

        # Load main font
        font_id = QFontDatabase.addApplicationFont(os.path.join(base_dir, 'font', '汉仪文黑-65W.ttf'))
        families = QFontDatabase.applicationFontFamilies(font_id)
        main_font = families[0] if families else ''

        # Title label
        title_label = QLabel("Final Damage Calculator", self)
        title_font = QFont(main_font, 20)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignHCenter)

        # Container
        container = QWidget(self)
        container.setFixedSize(500, 330)
        container.setStyleSheet(
            "QWidget {"
            "  border: 3px dashed #b0b0b0;"
            "  border-radius: 12px;"
            "  background-color: rgba(255,255,255,0.6);"
            "}"
        )
        container_shadow = QGraphicsDropShadowEffect(self)
        container_shadow.setBlurRadius(12)
        container_shadow.setOffset(0, 3)
        container.setGraphicsEffect(container_shadow)

        form_layout = QVBoxLayout(container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

        # Base damage input
        self.damage_entry = QLineEdit()
        self.damage_entry.setFixedHeight(40)
        self.damage_entry.setStyleSheet(
            "QLineEdit { padding: 5px 10px; border: 1px solid #707070; border-radius: 8px; background: white; }"
        )
        entry_shadow = QGraphicsDropShadowEffect(self)
        entry_shadow.setBlurRadius(10)
        entry_shadow.setOffset(0, 2)
        self.damage_entry.setGraphicsEffect(entry_shadow)
        form_layout.addLayout(self._row("Base Damage:", self.damage_entry, main_font))

        # ComboBox style: border retained, remove popup border
        combo_style = (
            "QComboBox { padding: 5px 10px; border: 1px solid #707070; border-radius: 8px; background: white; }"
            "QComboBox QAbstractItemView { border: none; }"
        )
        combo_shadow = QGraphicsDropShadowEffect(self)
        combo_shadow.setBlurRadius(10)
        combo_shadow.setOffset(0, 2)

        # Attacker type
        self.attacker_type = QComboBox()
        self.attacker_type.addItems(all_types)
        self.attacker_type.setFixedHeight(40)
        self.attacker_type.setStyleSheet(combo_style)
        self.attacker_type.setGraphicsEffect(combo_shadow)
        # Narrow popup width to avoid overlapping border
        self.attacker_type.view().setFixedWidth(240)
        form_layout.addLayout(self._row("Attack Type:", self.attacker_type, main_font))

        # Defender type 1
        self.defender_type_1 = QComboBox()
        self.defender_type_1.addItems(all_types)
        self.defender_type_1.setFixedHeight(40)
        self.defender_type_1.setStyleSheet(combo_style)
        self.defender_type_1.setGraphicsEffect(combo_shadow)
        self.defender_type_1.view().setFixedWidth(240)
        form_layout.addLayout(self._row("Defender Type 1:", self.defender_type_1, main_font))

        # Defender type 2
        self.defender_type_2 = QComboBox()
        self.defender_type_2.addItem("")
        self.defender_type_2.addItems(all_types)
        self.defender_type_2.setFixedHeight(40)
        self.defender_type_2.setStyleSheet(combo_style)
        self.defender_type_2.setGraphicsEffect(combo_shadow)
        self.defender_type_2.view().setFixedWidth(240)
        form_layout.addLayout(self._row("Defender Type 2:", self.defender_type_2, main_font))

        # STAB checkbox
        self.stab_check = QCheckBox("Same-Type Attack Bonus (STAB)")
        self.stab_check.setStyleSheet("QCheckBox { background: transparent; border: none; }")
        form_layout.addWidget(self.stab_check)

        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self._style_button(self.calc_button, main_font)
        self.calc_button.clicked.connect(self.calculate_damage)
        form_layout.addWidget(self.calc_button)

        # Result label
        self.result_label = QLabel("Final Damage: ")
        self.result_label.setStyleSheet("QLabel { background: transparent; border: none; }")
        form_layout.addWidget(self.result_label)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 30, 0, 50)
        main_layout.setSpacing(10)
        main_layout.addWidget(title_label, alignment=Qt.AlignHCenter)
        main_layout.addWidget(container, alignment=Qt.AlignHCenter|Qt.AlignTop)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg_pixmap)

    def _row(self, label_text, widget, font_family):
        row = QHBoxLayout()
        label = QLabel(label_text)
        label.setFont(QFontDatabase.font(font_family, '', 12))
        label.setStyleSheet("QLabel { background: transparent; border: none; }")
        row.addWidget(label)
        row.addWidget(widget)
        return row

    def _style_button(self, button, font_family):
        button.setFixedHeight(40)
        button.setStyleSheet(
            f"QPushButton {{ background-color: #FEE6A3; color: #7E5249; font-family: '{font_family}'; font-size: 14px; font-weight: bold; border: none; border-radius: 20px; }}"
        )
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 3)
        button.setGraphicsEffect(shadow)

    def calculate_damage(self):
        try:
            base_damage = float(self.damage_entry.text())
            attack_type = self.attacker_type.currentText()
            defender_type1 = self.defender_type_1.currentText()
            defender_type2 = self.defender_type_2.currentText()

            mult1 = type_chart.get(attack_type, {}).get(defender_type1, 1)
            mult2 = 1
            if defender_type2 and defender_type2 != defender_type1:
                mult2 = type_chart.get(attack_type, {}).get(defender_type2, 1)

            stab_mult = 1.5 if self.stab_check.isChecked() else 1
            final_mult = mult1 * mult2 * stab_mult
            final_dmg = base_damage * final_mult

            # Display result with enlarged red font for the number
            self.result_label.setText(
                f"Final Damage: <span style='color:#E74C3C; font-size:18px; font-weight:bold;'>{final_dmg:.2f}</span> (x{final_mult:.2f})"
            )
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for base damage.")
