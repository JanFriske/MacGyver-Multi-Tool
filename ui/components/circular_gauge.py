from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QConicalGradient, QFont, QBrush

class CircularGauge(QWidget):
    def __init__(self, title="", min_val=0, max_val=100, unit="", size=120):
        super().__init__()
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val
        self.unit = unit
        self.size = size  # Store size for font scaling
        
        # Use setFixedSize for precise control
        self.setFixedSize(size, size)

    def set_value(self, val):
        self.value = max(self.min_val, min(self.max_val, val))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Use actual widget size for rendering
        rect = self.rect().adjusted(10, 10, -10, -10)
        size = min(rect.width(), rect.height())
        rect.setSize(QSize(size, size))
        rect.moveCenter(self.rect().center())
        
        # Semi-Circle Configuration (270 degrees, starting from bottom-left)
        start_angle = 225 * 16
        span_angle = -270 * 16
        
        # Responsive arc thickness based on gauge size
        if self.size < 60:
            arc_width = 4
        elif self.size < 90:
            arc_width = 6
        else:
            arc_width = 8
        
        # Background Arc
        pen_bg = QPen(QColor(255, 255, 255, 30), arc_width, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(rect, start_angle, span_angle)
        
        # Value Arc
        range_val = self.max_val - self.min_val
        if range_val == 0: range_val = 1
        pct = (self.value - self.min_val) / range_val
        value_span = span_angle * pct
        
        # Gradient (Visible Spectrum: Red -> Violet)
        grad = QConicalGradient(rect.center(), -45)
        
        grad.setColorAt(0.000, QColor("#AF52DE")) # Violet
        grad.setColorAt(0.125, QColor("#007AFF")) # Blue
        grad.setColorAt(0.250, QColor("#34C759")) # Green
        grad.setColorAt(0.375, QColor("#FFCC00")) # Yellow
        grad.setColorAt(0.500, QColor("#FF9500")) # Orange
        grad.setColorAt(0.625, QColor("#FF3B30")) # Red
        
        pen_val = QPen(Qt.NoBrush, arc_width, Qt.SolidLine, Qt.RoundCap)
        pen_val.setBrush(QBrush(grad))
        painter.setPen(pen_val)
        
        if pct > 0.01:
            painter.drawArc(rect, start_angle, value_span)

        # Text - Responsive font sizes based on gauge size
        painter.setPen(QColor(255, 255, 255))
        
        # Scale fonts: 40px gauge=0.4x, 60px=0.6x, 100px=1.0x, 120px=1.2x
        scale_factor = self.size / 100.0
        
        # Enhanced scaling for very small gauges
        if self.size < 60:
            title_size = max(6, int(8 * scale_factor))
            value_size = max(10, int(16 * scale_factor))
            unit_size = max(6, int(9 * scale_factor))
        else:
            title_size = max(7, int(9 * scale_factor))
            value_size = max(12, int(18 * scale_factor))
            unit_size = max(7, int(10 * scale_factor))
        
        # Title (Top)
        painter.setFont(QFont("Segoe UI", title_size, QFont.Bold))
        painter.drawText(rect.adjusted(0, 15, 0, 0), Qt.AlignTop | Qt.AlignHCenter, self.title)
        
        # Value (Center)
        painter.setFont(QFont("Segoe UI", value_size, QFont.Bold))
        val_str = f"{int(self.value)}"
        painter.drawText(rect, Qt.AlignCenter, val_str)
        
        # Unit (Bottom)
        painter.setFont(QFont("Segoe UI", unit_size))
        painter.drawText(rect.adjusted(0, 0, 0, -15), Qt.AlignBottom | Qt.AlignHCenter, self.unit)

