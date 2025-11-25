"""
Translation Statistics Dialog
Displays detailed translation coverage statistics for all languages.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush

from core.services.i18n_service import I18nService

class TranslationStatsDialog(QDialog):
    def __init__(self, i18n_service: I18nService, parent=None):
        super().__init__(parent)
        self.i18n_service = i18n_service
        self.setWindowTitle(self.i18n_service.tr("stats.title", "Translation Statistics"))
        self.setMinimumSize(1000, 700)  # Increased from 800x600 for better column visibility
        
        self._init_ui()
        self._load_data()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel(f"<h2>{self.i18n_service.tr('stats.header', 'Translation Coverage Report')}</h2>")
        header.setTextFormat(Qt.RichText)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Summary
        self.summary_label = QLabel("Loading...")
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.summary_label.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 10px;")
        layout.addWidget(self.summary_label)
        
        # Table with extended columns
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            self.i18n_service.tr("stats.column_language", "Language"),
            self.i18n_service.tr("stats.column_code", "Code"),
            self.i18n_service.tr("stats.column_native", "Native"),
            self.i18n_service.tr("stats.column_fallback_de", "FB: DE"),
            self.i18n_service.tr("stats.column_fallback_en", "FB: EN"),
            self.i18n_service.tr("stats.column_missing", "Missing"),
            self.i18n_service.tr("stats.column_coverage", "Coverage")
        ])
        
        # Table Styling - Optimized column widths for readability
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)       # Language Name (user can adjust)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Code
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Native
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Fallback DE
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Fallback EN
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Missing
        header.setSectionResizeMode(6, QHeaderView.Stretch)       # Progress Bar
        
        # Set minimum width for Language column to ensure readability
        self.table.setColumnWidth(0, 250)  # Language Name gets more space
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)
        
        layout.addWidget(self.table)
        
        # Close Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton(self.i18n_service.tr("dialog.close", "Close"))
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
    def _load_data(self):
        stats = self.i18n_service.get_translation_stats()
        
        if not stats:
            self.summary_label.setText("No statistics available.")
            return
            
        # Update Summary with new categories
        total_langs = len(stats)
        fully_native = sum(1 for s in stats.values() if s['percent_native'] >= 100)
        using_fallbacks = sum(1 for s in stats.values() if s['fallback_de'] > 0 or s['fallback_en'] > 0)
        with_missing = sum(1 for s in stats.values() if s['missing'] > 0)
        
        self.summary_label.setText(
            f"{self.i18n_service.tr('stats.total_languages', 'Total Languages')}: <b>{total_langs}</b> | "
            f"{self.i18n_service.tr('stats.fully_native', 'Fully Native')}: <b>{fully_native}</b> | "
            f"{self.i18n_service.tr('stats.using_fallbacks', 'Using Fallbacks')}: <b>{using_fallbacks}</b> | "
            f"{self.i18n_service.tr('stats.with_missing', 'With Missing')}: <b>{with_missing}</b>"
        )
        
        # Populate Table
        self.table.setRowCount(len(stats))
        self.table.setSortingEnabled(False) # Disable sorting while populating
        
        for row, (lang_code, data) in enumerate(stats.items()):
            lang_name = self.i18n_service.get_language_name(lang_code)
            
            # 0: Language Name
            name_item = QTableWidgetItem(lang_name)
            
            # Add Flag Icon
            from PySide6.QtGui import QIcon
            flag_path = self.i18n_service.get_flag_path(lang_code)
            if flag_path:
                name_item.setIcon(QIcon(str(flag_path)))
                
            self.table.setItem(row, 0, name_item)
            
            # 1: Code
            code_item = QTableWidgetItem(lang_code)
            code_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, code_item)
            
            # 2: Native (Green)
            native_item = QTableWidgetItem()
            native_item.setData(Qt.DisplayRole, data['native'])
            native_item.setTextAlignment(Qt.AlignCenter)
            native_item.setToolTip(self.i18n_service.tr('stats.tooltip_native', 'Direct translations in this language'))
            if data['native'] > 0:
                native_item.setForeground(QBrush(QColor("#27ae60")))  # Green
            self.table.setItem(row, 2, native_item)
            
            # 3: Fallback DE (Orange)
            fb_de_item = QTableWidgetItem()
            fb_de_item.setData(Qt.DisplayRole, data['fallback_de'])
            fb_de_item.setTextAlignment(Qt.AlignCenter)
            fb_de_item.setToolTip(self.i18n_service.tr('stats.tooltip_fallback_de', 'Uses German fallback'))
            if data['fallback_de'] > 0:
                fb_de_item.setForeground(QBrush(QColor("#e67e22")))  # Orange
            self.table.setItem(row, 3, fb_de_item)
            
            # 4: Fallback EN (Yellow)
            fb_en_item = QTableWidgetItem()
            fb_en_item.setData(Qt.DisplayRole, data['fallback_en'])
            fb_en_item.setTextAlignment(Qt.AlignCenter)
            fb_en_item.setToolTip(self.i18n_service.tr('stats.tooltip_fallback_en', 'Uses English fallback'))
            if data['fallback_en'] > 0:
                fb_en_item.setForeground(QBrush(QColor("#f39c12")))  # Yellow
            self.table.setItem(row, 4, fb_en_item)
            
            # 5: Missing (Red with background)
            missing_item = QTableWidgetItem()
            missing_item.setData(Qt.DisplayRole, data['missing'])
            missing_item.setTextAlignment(Qt.AlignCenter)
            missing_item.setToolTip(self.i18n_service.tr('stats.tooltip_missing', '⚠️ No translation available (shows key name)'))
            if data['missing'] > 0:
                missing_item.setForeground(QBrush(QColor("#e74c3c")))  # Red
                missing_item.setBackground(QBrush(QColor("#ffe5e5")))  # Light red bg
            self.table.setItem(row, 5, missing_item)
            
            # 6: Coverage (Progress Bar)
            percent = data['percent_coverage']
            prog_item = QTableWidgetItem()
            prog_item.setData(Qt.DisplayRole, percent)
            self.table.setItem(row, 6, prog_item)
            
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(int(percent))
            progress.setTextVisible(True)
            progress.setFormat(f"{percent}%")
            progress.setAlignment(Qt.AlignCenter)
            
            # Color coding based on coverage
            if percent >= 100:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #2ecc71; }") # Green
            elif percent >= 80:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #f1c40f; }") # Yellow
            else:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #e74c3c; }") # Red
                
            self.table.setCellWidget(row, 6, progress)
            
        self.table.setSortingEnabled(True)
