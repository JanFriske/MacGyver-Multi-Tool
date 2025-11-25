from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush

class PremiumTableWidget(QTableWidget):
    """
    Premium macOS-style table widget with frosted glass aesthetics.
    Features:
    - Sortable columns
    - Alternating row colors
    - Hover effects
    - Frosted glass header
    """
    
    row_clicked = Signal(int)
    row_double_clicked = Signal(int)
    
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.columns = columns
        self._init_ui()
        
    def _init_ui(self):
        # Set column count
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        
        # Table behavior
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Header configuration
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Interactive)
        
        # Vertical header (row numbers) - hide
        self.verticalHeader().setVisible(False)
        
        # Premium styling
        self.setStyleSheet("""
            QTableWidget {
                background-color: rgba(30, 30, 30, 0.5);
                border: none;
                border-radius: 8px;
                gridline-color: rgba(255, 255, 255, 0.1);
                color: #e0e0e0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            
            QTableWidget::item {
                padding: 6px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background-color: rgba(0, 122, 255, 0.3);
                color: white;
            }
            
            QTableWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.05);
            }
            
            QHeaderView::section {
                background-color: rgba(50, 50, 50, 0.8);
                color: #aaa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                font-weight: bold;
                font-size: 12px;
            }
            
            QHeaderView::section:hover {
                background-color: rgba(70, 70, 70, 0.8);
            }
            
            QScrollBar:vertical {
                background: rgba(30, 30, 30, 0.3);
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Connect signals
        self.itemClicked.connect(lambda item: self.row_clicked.emit(item.row()))
        self.itemDoubleClicked.connect(lambda item: self.row_double_clicked.emit(item.row()))
    
    def add_row(self, row_data):
        """Add a row with data (list of strings/values)."""
        row = self.rowCount()
        self.insertRow(row)
        
        for col, data in enumerate(row_data):
            item = QTableWidgetItem(str(data))
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.setItem(row, col, item)
        
        return row
    
    def clear_rows(self):
        """Clear all rows but keep headers."""
        self.setRowCount(0)
    
    def set_row_color(self, row, color):
        """Set background color for entire row."""
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setBackground(QBrush(QColor(color)))
    
    def get_row_data(self, row):
        """Get all data from a specific row."""
        data = []
        for col in range(self.columnCount()):
            item = self.item(row, col)
            data.append(item.text() if item else "")
        return data
