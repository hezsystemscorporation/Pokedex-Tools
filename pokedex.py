import os
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QSizePolicy, QFrame
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPixmap, QPainter, QFont, QFontDatabase, QIcon
from PySide6.QtCore import Qt

class PokedexWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokédex (ver. 4.0)")
        self.setFixedSize(1000, 600)
        base_dir = os.path.dirname(__file__)

        # Load icon & background
        icon_path = os.path.join(base_dir, 'ptlogo.svg')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.bg_pix = QPixmap(os.path.join(base_dir, 'background3.png'))

        # Load fonts
        seg_id = QFontDatabase.addApplicationFont(os.path.join(base_dir, 'font', 'segoeprb.ttf'))
        seg_family = QFontDatabase.applicationFontFamilies(seg_id)[0] if seg_id != -1 else 'Arial'
        hy_id = QFontDatabase.addApplicationFont(os.path.join(base_dir, 'font', 'HYWenHei-35J.ttf'))
        hy_family = QFontDatabase.applicationFontFamilies(hy_id)[0] if hy_id != -1 else seg_family

        # Title
        title = QLabel('Pokédex')
        title.setFont(QFont(seg_family, 24))
        title.setStyleSheet('color: white;')
        title.setAlignment(Qt.AlignCenter)

        # Search & Nav
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search name/type1/type2/abilities...')
        self.search_input.returnPressed.connect(self.run_search)
        self.search_input.setStyleSheet(
            'QLineEdit { border:1px solid black; padding:6px; background:white; border-radius:4px; font-size:14px; }'
        )
        self.btn_search = QPushButton('Search')
        self.btn_prev = QPushButton('Previous')
        self.btn_next = QPushButton('Next')
        for btn in (self.btn_search, self.btn_prev, self.btn_next):
            btn.setFont(QFont(seg_family, 10))
            btn.setStyleSheet(
                'QPushButton { background:#FEE6A3; color:black; border:1px solid black; border-radius:8px; padding:6px 12px; }'
                'QPushButton:hover { background:#FDD871; }'
                'QPushButton:pressed { background:#FDD157; }'
            )
        self.btn_search.clicked.connect(self.run_search)
        self.btn_prev.clicked.connect(self.show_previous)
        self.btn_next.clicked.connect(self.show_next)

        # Load data
        df_path = os.path.join(base_dir, 'pokemon.xlsx')
        self.df = pd.read_excel(df_path, engine='openpyxl')
        for col in ['name', 'type1', 'type2', 'abilities', 'japanese_name']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('').astype(str)
        self.filtered = self.df
        self.current_index = 0

        # Grid layout (12 rows x 5 cols)
        grid = QGridLayout()
        grid.setSpacing(0)

        # Fonts
        name_font = QFont(seg_family, 20)
        num_font = QFont(hy_family, 20)
        bold_font = QFont('Arial', 12, QFont.Bold)
        normal_font = QFont('Arial', 12)

        # 1) Name and number merged
        self.lbl_name = QLabel()
        self.lbl_name.setFont(name_font)
        self.lbl_name.setStyleSheet('color: brown;')
        self.lbl_name.setAlignment(Qt.AlignCenter)
        self.lbl_num = QLabel()
        self.lbl_num.setFont(num_font)
        self.lbl_num.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.lbl_name, 0, 0, 2, 4)

        # 2) Japanese name row
        self.lbl_jp = QLabel()
        self.lbl_jp.setFont(normal_font)
        self.lbl_jp.setStyleSheet('color: brown;')
        self.lbl_jp.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.lbl_jp, 2, 0, 1, 4)

        # 3) Type icons row
        lbl = QLabel('Type')
        lbl.setFont(bold_font)
        lbl.setAlignment(Qt.AlignCenter)
        grid.addWidget(lbl, 3, 0)
        self.type_box = QHBoxLayout()
        self.type_box.setAlignment(Qt.AlignLeft)
        type_widget = QWidget()
        type_widget.setLayout(self.type_box)
        grid.addWidget(type_widget, 3, 1, 1, 3)

        # 4) Abilities row
        lbl = QLabel('Abilities')
        lbl.setFont(bold_font)
        lbl.setAlignment(Qt.AlignCenter)
        grid.addWidget(lbl, 4, 0)
        self.lbl_abilities = QLabel()
        self.lbl_abilities.setFont(normal_font)
        self.lbl_abilities.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.lbl_abilities, 4, 1, 1, 3)

        # 5) Stats split into two columns (rows 5-7)
        left_stats = [('HP', 'hp'), ('Defense', 'defense'), ('SpA', 'sp_attack')]
        right_stats = [('Attack', 'attack'), ('Speed', 'speed'), ('SpD', 'sp_defense')]
        for i, (label_text, field) in enumerate(left_stats, start=5):
            lbl = QLabel(label_text)
            lbl.setFont(bold_font)
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, i, 0)
            val = QLabel()
            val.setFont(normal_font)
            val.setAlignment(Qt.AlignCenter)
            grid.addWidget(val, i, 1)
            setattr(self, f'{field}_lbl', val)
        for i, (label_text, field) in enumerate(right_stats, start=5):
            lbl = QLabel(label_text)
            lbl.setFont(bold_font)
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, i, 2)
            val = QLabel()
            val.setFont(normal_font)
            val.setAlignment(Qt.AlignCenter)
            grid.addWidget(val, i, 3)
            setattr(self, f'{field}_lbl', val)

        # 6) Extras split two columns (rows 8-10)
        extras = [
            ('Base Egg Steps', 'base_egg_steps', 'Base Happiness', 'base_happiness'),
            ('Capture Rate', 'capture_rate', 'Generation', 'generation'),
            ('Height (m)', 'height_m', 'Weight (kg)', 'weight_kg')
        ]
        for row_idx, (l_text, l_field, r_text, r_field) in enumerate(extras, start=8):
            l_lbl = QLabel(l_text)
            l_lbl.setFont(bold_font)
            l_lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(l_lbl, row_idx, 0)
            l_val = QLabel()
            l_val.setFont(normal_font)
            l_val.setAlignment(Qt.AlignCenter)
            grid.addWidget(l_val, row_idx, 1)
            setattr(self, f'{l_field}_lbl', l_val)

            r_lbl = QLabel(r_text)
            r_lbl.setFont(bold_font)
            r_lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(r_lbl, row_idx, 2)
            r_val = QLabel()
            r_val.setFont(normal_font)
            r_val.setAlignment(Qt.AlignCenter)
            grid.addWidget(r_val, row_idx, 3)
            setattr(self, f'{r_field}_lbl', r_val)

        # 7) Legendary footer (row 11)
        self.lbl_legend = QLabel()
        self.lbl_legend.setFont(normal_font)
        self.lbl_legend.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.lbl_legend, 11, 0, 1, 4)

        # 8) Rightmost column: Pokémon image (rows 0-5)
        self.img_label = QLabel(alignment=Qt.AlignCenter)
        grid.addWidget(self.img_label, 0, 4, 6, 1)

        # 9) Radar chart (rows 6-11)
        self.radar = QSvgWidget()
        self.radar.setFixedSize(300, 300)
        radar_frame = QFrame()
        radar_frame.setFrameShape(QFrame.NoFrame)
        radar_frame.setStyleSheet('background: white;')
        radar_layout = QVBoxLayout(radar_frame)
        radar_layout.setContentsMargins(0, 0, 0, 0)
        radar_layout.addWidget(self.radar)
        grid.addWidget(radar_frame, 6, 4, 6, 1)

        # Wrap with main frame and apply borders
        container = QFrame()
        container.setLayout(grid)
        container.setFrameShape(QFrame.NoFrame)
        container.setStyleSheet(
            'QWidget#container { border:2px solid black; }'
            'QLabel { border:1px solid black; }'
        )

        # Assemble all
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_next)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.btn_search)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(container)
        main_layout.addLayout(nav_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Init display
        self.run_search()
        self.show_entry()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg_pix)

    def run_search(self):
        keyword = self.search_input.text().lower().strip()
        mask = self.df['name'].str.lower().str.contains(keyword) if keyword else pd.Series(True, index=self.df.index)
        for col in ('type1', 'type2', 'abilities'):
            if keyword:
                mask |= self.df[col].str.lower().str.contains(keyword)
        self.filtered = self.df[mask] if not self.df[mask].empty else self.df
        self.current_index = 0

    def show_entry(self):
        if self.filtered.empty:
            return
        row = self.filtered.iloc[self.current_index]
        base_dir = os.path.dirname(__file__)

        # Name & #
        self.lbl_name.setText(row['name'] + f" (#{row.get('pokedex_number','')})")
        # Japanese
        self.lbl_jp.setText(row.get('japanese_name',''))

        '''
        # Types as strip icons
        # clear
        for i in reversed(range(self.type_box.count())):
            widget = self.type_box.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # add
        for t in ['type1', 'type2']:
            typ = row.get(t, '')
            if typ:
                icon_path = os.path.join(base_dir, 'icons', f'{typ}.svg')
                lbl = QLabel()
                lbl.setPixmap(QPixmap(icon_path).scaledToHeight(24, Qt.SmoothTransformation))
                lbl.setAlignment(Qt.AlignLeft)
                self.type_box.addWidget(lbl)
        '''

        # Types as strip icons
        # clear
        for i in reversed(range(self.type_box.count())):
            widget = self.type_box.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # add
        for t in ['type1', 'type2']:
            typ = row.get(t, '')
            if typ:
                icon_path = os.path.join(base_dir, 'icons', f'{typ}.svg')
                lbl = QLabel()
                lbl.setStyleSheet('border: none; background: transparent;')
                pix = QPixmap(icon_path).scaledToHeight(24, Qt.SmoothTransformation)
                lbl.setPixmap(pix)
                lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.type_box.addWidget(lbl)


        # Abilities
        abil_text = row['abilities'].strip("[]'").replace("', ", ", ")
        self.lbl_abilities.setText(abil_text)

        # Stats
        for stat in ['hp','defense','sp_attack','attack','speed','sp_defense']:
            getattr(self, f'{stat}_lbl').setText(str(row.get(stat,'')))

        # Extras
        for field in ['base_egg_steps','base_happiness','capture_rate','generation','height_m','weight_kg']:
            val = row.get(field)
            text = str(val) if val not in (None, '') else 'N/A'
            getattr(self, f'{field}_lbl').setText(text)

        # Legendary footer
        leg = 'is legendary.' if row.get('is_legendary') == 1 else 'is not legendary.'
        self.lbl_legend.setText(f'This Pokémon {leg}')

        # Image
        name_lower = row['name'].lower().replace(' ', '_')
        img_path = os.path.join(base_dir, 'pokemon_image', name_lower, str(row.get('image_content','')))
        if not os.path.exists(img_path):
            img_path = os.path.join(base_dir, 'nodata.svg')
        pix = QPixmap(img_path).scaled(195, 195, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_label.setPixmap(pix)

        # Radar
        radar_path = os.path.join(base_dir, 'pokemon_radar_chart_trans', f'radar_{name_lower}.svg')
        if not os.path.exists(radar_path):
            radar_path = os.path.join(base_dir, 'nodata.svg')
        self.radar.setFixedSize(225, 195)
        self.radar.load(radar_path)

        # Nav enable/disable
        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled(self.current_index < len(self.filtered) - 1)

    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_entry()

    def show_next(self):
        if self.current_index < len(self.filtered) - 1:
            self.current_index += 1
            self.show_entry()
