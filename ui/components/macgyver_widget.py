from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtCore import Qt, QRectF, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QLinearGradient

class MacGyverWidget(QWidget):
    closed = Signal(QWidget) # Signal emitted when closed, passing self

    def __init__(self, title="", size_span=(1, 1)):
        super().__init__()
        self.title = title
        self.span_w, self.span_h = size_span
        
        # Responsive margins and spacing based on widget size
        margins, spacing = self._get_responsive_layout_params()
        
        # Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(margins, margins, margins, margins)
        self.main_layout.setSpacing(spacing)
        
        # Close Button (macOS Style with × on hover)
        self.close_btn = QPushButton("", self)
        btn_size = 12 if (self.span_w == 1 and self.span_h == 1) else 14
        self.close_btn.setFixedSize(btn_size, btn_size)
        btn_pos = 8 if (self.span_w == 1 and self.span_h == 1) else 10
        self.close_btn.move(btn_pos, btn_pos)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #ff5f57;
                border-radius: {btn_size//2}px;
                border: 1px solid #e0443e;
                color: #8b0000;
                font-weight: bold;
                font-size: {btn_size-2}px;
                padding-bottom: 2px;
                min-width: 0px;
                min-height: 0px;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: #ff7b75;
            }}
            QPushButton:pressed {{
                background-color: #e0443e;
            }}
        """)
        # Show × on hover
        self.close_btn.enterEvent = lambda e: self.close_btn.setText("×")
        self.close_btn.leaveEvent = lambda e: self.close_btn.setText("")
        self.close_btn.clicked.connect(self._on_close)
        self.close_btn.raise_()
        
        # Drag & Drop support
        self.drag_start_pos = None
        self.setMouseTracking(False)  # Only track when pressed
        
        # Header
        if title:
            title_size = self._get_title_font_size()
            self.title_label = QLabel(title)
            self.title_label.setStyleSheet(f"font-family: 'Segoe UI'; font-weight: bold; font-size: {title_size}px; color: rgba(255, 255, 255, 0.7);")
            self.title_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) # Align right to avoid close button
            self.main_layout.addWidget(self.title_label)
        else:
            self.title_label = None
            
        # Content Area (to be filled by subclasses)
        self.content_area = QVBoxLayout()
        self.main_layout.addLayout(self.content_area)
        self.main_layout.addStretch()

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
        
        # Fixed size based on span - CRITICAL: prevents stretching!
        # Base unit: 160px
        self._update_size()
    
    def _get_responsive_layout_params(self):
        """Calculate responsive margins and spacing based on widget size."""
        # Smaller widgets need tighter spacing
        if self.span_w == 1 and self.span_h == 1:
            return 12, 6  # margins, spacing
        elif self.span_w <= 2 and self.span_h == 1:
            return 16, 8
        elif self.span_w == 2 and self.span_h == 2:
            return 20, 10
        else:  # Large widgets
            return 24, 12
    
    def _get_title_font_size(self):
        """Calculate title font size based on widget dimensions."""
        if self.span_w == 1 and self.span_h == 1:
            return 12
        elif self.span_w <= 2:
            return 14
        else:
            return 16
    
    def _tr(self, key: str, default: str = None) -> str:
        """Helper function for translations. Access i18n service from QApplication."""
        try:
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
            if app and hasattr(app, 'i18n_service'):
                return app.i18n_service.tr(key, default)
        except:
            pass
        return default if default else key
    
    def _update_size(self):
        """Update widget size based on current span."""
        size_w = 160 * self.span_w
        size_h = 160 * self.span_h
        self.setMinimumSize(size_w, size_h)
        self.setMaximumSize(size_w, size_h)
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size. Override in subclasses that need responsive layouts."""
        self.span_w = w
        self.span_h = h
        
        # Update margins and spacing
        margins, spacing = self._get_responsive_layout_params()
        self.main_layout.setContentsMargins(margins, margins, margins, margins)
        self.main_layout.setSpacing(spacing)
        
        # Update close button
        btn_size = 12 if (w == 1 and h == 1) else 14
        self.close_btn.setFixedSize(btn_size, btn_size)
        btn_pos = 8 if (w == 1 and h == 1) else 10
        self.close_btn.move(btn_pos, btn_pos)
        
        # Update title if present
        if self.title_label:
            title_size = self._get_title_font_size()
            self.title_label.setStyleSheet(f"font-family: 'Segoe UI'; font-weight: bold; font-size: {title_size}px; color: rgba(255, 255, 255, 0.7);")
        
        # Update size
        self._update_size()

    def _on_close(self):
        self.closed.emit(self)
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect().adjusted(5, 5, -5, -5) # Margin for shadow
        
        # Squircle Path
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 24, 24)
        
        # Glass Background
        painter.setBrush(QColor(30, 30, 30, 200))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        
        # Gradient Border
        grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        grad.setColorAt(0.0, QColor(255, 255, 255, 40))
        grad.setColorAt(1.0, QColor(255, 255, 255, 10))
        
        pen = QPen(QBrush(grad), 1.5)
        painter.setPen(pen)
        painter.drawPath(path)

    def add_bubble(self, widget):
        """Adds a widget wrapped in a 'Bubble' container."""
        bubble = QWidget()
        bubble.setObjectName("Bubble")
        bubble.setStyleSheet("""
            QWidget#Bubble {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(bubble)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(widget)
        
        self.content_area.addWidget(bubble)
    
    def mousePressEvent(self, event):
        """Start potential drag operation."""
        if event.button() == Qt.LeftButton:
            # Check if click is NOT on close button
            if not self.close_btn.geometry().contains(event.pos()):
                self.drag_start_pos = event.pos()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Initiate drag if mouse moved enough."""
        if not (event.buttons() & Qt.LeftButton):
            return
        if self.drag_start_pos is None:
            return
        
        # Check if moved far enough to start drag
        from PySide6.QtWidgets import QApplication
        if (event.pos() - self.drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return
        
        # Start drag operation
        from PySide6.QtCore import QMimeData, QByteArray
        from PySide6.QtGui import QDrag, QPainter, QPixmap
        
        drag = QDrag(self)
        mime_data = QMimeData()
        
        # Store widget info
        widget_data = f"{self.__class__.__name__}|{self.span_w}|{self.span_h}"
        mime_data.setData("application/x-macgyver-widget", QByteArray(widget_data.encode()))
        drag.setMimeData(mime_data)
        
        # Create drag pixmap (semi-transparent version of widget)
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setOpacity(0.7)
        self.render(painter, QPoint(0, 0))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        # Execute drag
        drag.exec(Qt.MoveAction)
        self.drag_start_pos = None
    
    def mouseReleaseEvent(self, event):
        """Clear drag state."""
        self.drag_start_pos = None
        super().mouseReleaseEvent(event)
