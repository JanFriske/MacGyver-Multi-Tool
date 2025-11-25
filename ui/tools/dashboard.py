from PySide6.QtWidgets import QWidget, QGridLayout, QScrollArea, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, QMimeData, QPoint, QRect
from PySide6.QtGui import QDrag, QPixmap

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        
        # Main Layout (Scrollable)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")
        
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        # We use a grid layout for the content, but we manage positions manually for D&D
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)
        
        # Grid State
        self.widgets = [] # List of (widget, row, col, span_w, span_h)
        self.max_cols = 4 # Increased to 4 for better flexibility
        self.cell_size = 160 # Base unit size

    def add_widget(self, widget, span_w=1, span_h=1):
        """Adds a widget to the first available spot."""
        row, col = self._find_free_spot(span_w, span_h)
        self._place_widget(widget, row, col, span_w, span_h)

    def _find_free_spot(self, span_w, span_h):
        """Find first available spot, searching from top to bottom, left to right."""
        max_search_rows = 50
        
        # Search rows from top to bottom
        for row in range(max_search_rows):
            # Search columns from LEFT to RIGHT
            # Ensure widget fits: max column is max_cols - span_w
            for col in range(0, self.max_cols - span_w + 1):
                if self._is_spot_free(row, col, span_w, span_h):
                    return row, col
        
        # Fallback: add to bottom left
        return max_search_rows, 0

    def _is_spot_free(self, row, col, span_w, span_h, exclude_widget=None):
        for w, r, c, sw, sh in self.widgets:
            if w == exclude_widget:
                continue
            # Check intersection
            if not (col + span_w <= c or col >= c + sw or row + span_h <= r or row >= r + sh):
                return False
        return True

    def _place_widget(self, widget, row, col, span_w, span_h):
        self.grid_layout.addWidget(widget, row, col, span_h, span_w)
        self.widgets.append((widget, row, col, span_w, span_h))
        
        # Connect close signal
        if hasattr(widget, 'closed'):
            try:
                widget.closed.disconnect()
            except: pass
            widget.closed.connect(self.remove_widget)
            
        # Enable dropping on widgets (for reordering)
        widget.setAcceptDrops(True)

    def remove_widget(self, widget):
        self.grid_layout.removeWidget(widget)
        widget.setParent(None)
        self.widgets = [w for w in self.widgets if w[0] != widget]
        widget.deleteLater()

    # --- Drag & Drop Logic ---
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-macgyver-widget"):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """Show visual feedback during drag."""
        if event.mimeData().hasFormat("application/x-macgyver-widget"):
            # Calculate target grid cell
            # Event position is relative to this widget (DashboardWidget)
            # Map through scroll area viewport to content widget
            pos = event.position().toPoint()
            viewport_pos = self.scroll_area.viewport().mapFrom(self, pos)
            content_pos = self.scroll_area.viewport().mapTo(self.content_widget, viewport_pos)
            row, col = self._pos_to_grid(content_pos)
            
            # Parse widget size from mime data
            data = event.mimeData().data("application/x-macgyver-widget").data().decode()
            parts = data.split('|')
            if len(parts) >= 3:
                span_w = int(parts[1])
                span_h = int(parts[2])
                
                # Ensure widget fits in grid
                if col + span_w > self.max_cols:
                    col = max(0, self.max_cols - span_w)
                
                # Identify the widget being dragged to exclude it from collision checks
                drag_source = event.source()
                exclude_widget = None
                if drag_source and drag_source.parent() == self.content_widget:
                    exclude_widget = drag_source

                # Check if placement is valid
                if self._is_spot_free(row, col, span_w, span_h, exclude_widget=exclude_widget):
                    event.acceptProposedAction()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle widget drop - move to new grid position."""
        if not event.mimeData().hasFormat("application/x-macgyver-widget"):
            event.ignore()
            return
        
        # Get drop position
        # Event position is relative to this widget (DashboardWidget)
        # Map through scroll area viewport to content widget
        pos = event.position().toPoint()
        viewport_pos = self.scroll_area.viewport().mapFrom(self, pos)
        content_pos = self.scroll_area.viewport().mapTo(self.content_widget, viewport_pos)
        target_row, target_col = self._pos_to_grid(content_pos)
        
        # Parse widget data
        data = event.mimeData().data("application/x-macgyver-widget").data().decode()
        parts = data.split('|')
        if len(parts) < 3:
            event.ignore()
            return
        
        span_w = int(parts[1])
        span_h = int(parts[2])
        
        # Ensure widget fits in grid
        if target_col + span_w > self.max_cols:
            target_col = max(0, self.max_cols - span_w)
        
        # Find the dragged widget
        drag_source = event.source()
        if drag_source and drag_source.parent() == self.content_widget:
            # Widget being reordered
            # Find it in our widgets list
            widget_entry = None
            for entry in self.widgets:
                if entry[0] == drag_source:
                    widget_entry = entry
                    break
            
            if widget_entry:
                old_widget, old_row, old_col, old_sw, old_sh = widget_entry
                
                # Don't move if dropped at same position
                if target_row == old_row and target_col == old_col:
                    event.acceptProposedAction()
                    return
                
                # Check if target is free (excluding the widget itself)
                if self._is_spot_free(target_row, target_col, span_w, span_h, exclude_widget=old_widget):
                    # Remove from old position
                    self.grid_layout.removeWidget(old_widget)
                    self.widgets.remove(widget_entry)
                    
                    # Place at new position
                    self._place_widget(old_widget, target_row, target_col, span_w, span_h)
                    
                    event.acceptProposedAction()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def _pos_to_grid(self, pos):
        """Convert pixel position to grid coordinates."""
        # Account for margins and spacing
        margin = 20
        spacing = 20
        
        x = pos.x() - margin
        y = pos.y() - margin
        
        # Calculate grid cell
        cell_total_size = self.cell_size + spacing
        
        # Calculate row and column
        col = max(0, int(x / cell_total_size))
        row = max(0, int(y / cell_total_size))
        
        # Ensure column doesn't exceed max_cols
        col = min(col, self.max_cols - 1)
        
        return row, col
