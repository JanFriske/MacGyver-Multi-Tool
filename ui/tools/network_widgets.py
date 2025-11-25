from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                                QLineEdit, QTextEdit, QCheckBox, QComboBox)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QColor
import subprocess
import socket
import psutil
import platform

from ui.components.macgyver_widget import MacGyverWidget
from ui.components.premium_table import PremiumTableWidget
from ui.components.circular_gauge import CircularGauge


class PingWidget(MacGyverWidget):
    """2x1 Ping utility with color-coded results."""
    
    def __init__(self):
        super().__init__("Ping", size_span=(2, 1))
        self.ping_process = None
        self._init_ui()
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()
    
    def _init_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Input row
        input_layout = QHBoxLayout()
        self.host_input = QLineEdit("google.com")
        self.host_input.setPlaceholderText("Hostname or IP")
        self.host_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(50, 50, 50, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 6px;
                color: #e0e0e0;
                font-size: 13px;
            }
        """)
        input_layout.addWidget(self.host_input)
        
        self.ping_btn = QPushButton("🌐 Ping")
        self.ping_btn.setFixedWidth(100)
        self.ping_btn.clicked.connect(self._start_ping)
        self.ping_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 122, 255, 0.8);
                border: none;
                border-radius: 6px;
                padding: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 122, 255, 1.0);
            }
        """)
        input_layout.addWidget(self.ping_btn)
        
        layout.addLayout(input_layout)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(80)
        
        # Responsive font size
        font_size = 11 if self.span_w < 3 else 13
        
        self.results_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(20, 20, 20, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                color: #34c759;
                font-family: 'Consolas', monospace;
                font-size: {font_size}px;
                padding: 6px;
            }}
        """)
        layout.addWidget(self.results_text)
        
        self.add_bubble(container)
    
    def _start_ping(self):
        """Execute ping command."""
        host = self.host_input.text()
        if not host:
            return
        
        self.results_text.clear()
        self.results_text.append(f"Pinging {host}...")
        
        # Platform-specific ping command
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', host]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            output = result.stdout
            
            # Color-code based on response time
            if "time=" in output or "Zeit=" in output:
                # Extract time (simplified)
                lines = output.split('\n')
                for line in lines:
                    if 'time=' in line.lower() or 'zeit=' in line.lower():
                        self.results_text.append(line)
                        # Try to extract ms value for color coding
                        try:
                            if 'ms' in line:
                                ms_str = line.split('ms')[0].split()[-1].replace('<', '')
                                ms = float(ms_str)
                                if ms < 50:
                                    self.results_text.setStyleSheet(self.results_text.styleSheet().replace("#34c759", "#34c759"))  # Green
                                elif ms < 200:
                                    self.results_text.setStyleSheet(self.results_text.styleSheet().replace("#34c759", "#ffcc00"))  # Yellow
                                else:
                                    self.results_text.setStyleSheet(self.results_text.styleSheet().replace("#34c759", "#ff3b30"))  # Red
                        except:
                            pass
                
                # Add summary
                summary_lines = [l for l in lines if 'packet' in l.lower() or 'paket' in l.lower()]
                if summary_lines:
                    self.results_text.append("\n" + summary_lines[0])
            else:
                self.results_text.append("❌ Ping failed or host unreachable")
                self.results_text.setStyleSheet(self.results_text.styleSheet().replace("#34c759", "#ff3b30"))
        
        except subprocess.TimeoutExpired:
            self.results_text.append("❌ Ping timeout")
        except Exception as e:
            self.results_text.append(f"❌ Error: {str(e)}")


class ConnectionStatusWidget(MacGyverWidget):
    """1x1 Quick network status indicator."""
    
    def __init__(self):
        super().__init__("Verbindung", size_span=(1, 1))
        self._init_ui()
        
        # Auto-update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_status)
        self.timer.start(5000)
        self._update_status()
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()
    
    def _init_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        
        # Responsive sizes
        icon_size = 48 if self.span_w > 1 else 36
        status_size = 14 if self.span_w > 1 else 12
        ip_size = 12 if self.span_w > 1 else 10
        
        # Status icon
        self.status_icon = QLabel("🌐")
        self.status_icon.setAlignment(Qt.AlignCenter)
        self.status_icon.setStyleSheet(f"font-size: {icon_size}px;")
        layout.addWidget(self.status_icon)
        
        # Status text
        self.status_label = QLabel("Checking...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"font-size: {status_size}px; font-weight: bold; color: #aaa;")
        layout.addWidget(self.status_label)
        
        # IP address
        self.ip_label = QLabel("")
        self.ip_label.setAlignment(Qt.AlignCenter)
        self.ip_label.setStyleSheet(f"font-size: {ip_size}px; color: #777;")
        layout.addWidget(self.ip_label)
        
        self.add_bubble(container)
    
    def _update_status(self):
        """Update network connection status."""
        try:
            # Get local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Check internet connection
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            
            # Connected
            self.status_icon.setText("✅")
            self.status_label.setText("Verbunden")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34c759;")
            self.ip_label.setText(f"IP: {local_ip}")
        
        except:
            # Disconnected
            self.status_icon.setText("❌")
            self.status_label.setText("Getrennt")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ff3b30;")
            self.ip_label.setText("Keine Verbindung")


class SpeedTestWidget(MacGyverWidget):
    """2x1 Network speed test with gauges."""
    
    def __init__(self):
        super().__init__("Speed Test", size_span=(2, 1))
        self._init_ui()
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()
    
    def _init_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Gauges
        # Responsive gauge size
        gauge_size = 100 if self.span_h >= 2 else 70
        
        gauges_layout = QHBoxLayout()
        self.download_gauge = CircularGauge("Download", max_val=100, unit=" Mbps", size=gauge_size)
        self.upload_gauge = CircularGauge("Upload", max_val=100, unit=" Mbps", size=gauge_size)
        gauges_layout.addWidget(self.download_gauge)
        gauges_layout.addWidget(self.upload_gauge)
        layout.addLayout(gauges_layout)
        
        # Test button
        self.test_btn = QPushButton("🚀 Test Speed")
        self.test_btn.clicked.connect(self._run_speed_test)
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 122, 255, 0.8);
                border: none;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(0, 122, 255, 1.0);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 0.5);
            }
        """)
        layout.addWidget(self.test_btn)
        
        self.add_bubble(container)
    
    def _run_speed_test(self):
        """Run speed test (simulated for now)."""
        self.test_btn.setEnabled(False)
        self.test_btn.setText("Testing...")
        
        # In production, use speedtest-cli library
        # For now, simulate
        import random
        download_speed = random.uniform(20, 95)
        upload_speed = random.uniform(5, 30)
        
        self.download_gauge.set_value(download_speed)
        self.upload_gauge.set_value(upload_speed)
        
        # Re-enable button
        QTimer.singleShot(2000, lambda: self.test_btn.setEnabled(True))
        QTimer.singleShot(2000, lambda: self.test_btn.setText("🚀 Test Speed"))


class ActiveConnectionsWidget(MacGyverWidget):
    """2x2 Table of active network connections."""
    
    def __init__(self):
        super().__init__("Aktive Verbindungen", size_span=(2, 2))
        self._init_ui()
        
        # Auto-refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._load_connections)
        self.timer.start(5000)
        self._load_connections()
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()
    
    def _init_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Filter row
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Protokoll:"))
        
        self.protocol_filter = QComboBox()
        self.protocol_filter.addItems(["All", "TCP", "UDP"])
        self.protocol_filter.currentTextChanged.connect(self._load_connections)
        self.protocol_filter.setStyleSheet("""
            QComboBox {
                background-color: rgba(50, 50, 50, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 4px;
                color: #e0e0e0;
            }
        """)
        filter_layout.addWidget(self.protocol_filter)
        filter_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._load_connections)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        # Connections table
        self.table = PremiumTableWidget(["Prozess", "Protokoll", "Local", "Remote", "Status"])
        layout.addWidget(self.table)
        
        self.add_bubble(container)
    
    def _load_connections(self):
        """Load active network connections."""
        self.table.clear_rows()
        
        try:
            protocol_filter = self.protocol_filter.currentText()
            
            connections = psutil.net_connections(kind='inet')
            for conn in connections[:50]:  # Limit to 50
                # Filter by protocol
                if protocol_filter != "All":
                    if protocol_filter == "TCP" and conn.type != socket.SOCK_STREAM:
                        continue
                    if protocol_filter == "UDP" and conn.type != socket.SOCK_DGRAM:
                        continue
                
                # Get process name
                try:
                    process = psutil.Process(conn.pid) if conn.pid else None
                    process_name = process.name() if process else "—"
                except:
                    process_name = "—"
                
                # Protocol
                protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                
                # Addresses
                local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "—"
                remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "—"
                
                # Status
                status = conn.status if hasattr(conn, 'status') else "—"
                
                self.table.add_row([process_name, protocol, local, remote, status])
        
        except Exception as e:
            print(f"Error loading connections: {e}")


class NetworkPathWidget(MacGyverWidget):
    """2x2 Network path visualizer - traces route from user to destination."""
    
    def __init__(self):
        super().__init__("Netzwerkpfad", size_span=(2, 2))
        self._init_ui()
    
    def rebuild_for_span(self, w, h):
        """Rebuild widget for new span size."""
        self.span_w = w
        self.span_h = h
        super().rebuild_for_span(w, h)
        # Clear content_area
        while self.content_area.count():
            item = self.content_area.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._init_ui()
    
    def _init_ui(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Input row
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Ziel:"))
        
        self.target_input = QLineEdit("google.com")
        self.target_input.setPlaceholderText("Hostname oder IP")
        self.target_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(50, 50, 50, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 6px;
                color: #e0e0e0;
                font-size: 13px;
            }
        """)
        input_layout.addWidget(self.target_input)
        
        self.trace_btn = QPushButton("🗺️ Route tracen")
        self.trace_btn.setFixedWidth(130)
        self.trace_btn.clicked.connect(self._start_trace)
        self.trace_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 122, 255, 0.8);
                border: none;
                border-radius: 6px;
                padding: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 122, 255, 1.0);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 0.5);
            }
        """)
        input_layout.addWidget(self.trace_btn)
        layout.addLayout(input_layout)
        
        # Path visualization area
        self.path_container = QWidget()
        self.path_layout = QVBoxLayout(self.path_container)
        self.path_layout.setSpacing(4)
        self.path_layout.setAlignment(Qt.AlignTop)
        
        # Scrollable area for hops
        from PySide6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidget(self.path_container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: rgba(20, 20, 20, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        """)
        layout.addWidget(scroll)
        
        self.add_bubble(container)
        
        # Initial placeholder
        self._show_placeholder()
    
    def _show_placeholder(self):
        """Show placeholder when no trace is active."""
        self._clear_path()
        placeholder = QLabel("🗺️ Route zum Ziel wird hier angezeigt.\nGib ein Ziel ein und klicke auf 'Route tracen'.")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("""
            color: #777;
            font-size: 13px;
            padding: 40px;
        """)
        self.path_layout.addWidget(placeholder)
    
    def _clear_path(self):
        """Clear all hops from display."""
        while self.path_layout.count():
            child = self.path_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _start_trace(self):
        """Start traceroute to target."""
        target = self.target_input.text()
        if not target:
            return
        
        self.trace_btn.setEnabled(False)
        self.trace_btn.setText("Tracing...")
        self._clear_path()
        
        # Add loading indicator
        loading = QLabel("⏳ Route wird ermittelt...")
        loading.setAlignment(Qt.AlignCenter)
        loading.setStyleSheet("color: #007aff; font-size: 14px; padding: 20px;")
        self.path_layout.addWidget(loading)
        
        # Run traceroute in background
        QTimer.singleShot(100, lambda: self._execute_traceroute(target))
    
    def _execute_traceroute(self, target):
        """Execute traceroute command."""
        try:
            # Platform-specific traceroute command
            if platform.system().lower() == 'windows':
                command = ['tracert', '-d', '-h', '15', target]
            else:
                command = ['traceroute', '-m', '15', '-n', target]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            hops = self._parse_traceroute(result.stdout)
            
            self._clear_path()
            if hops:
                self._display_hops(hops, target)
            else:
                self._show_error("Keine Route gefunden oder Fehler beim Tracen.")
        
        except subprocess.TimeoutExpired:
            self._show_error("Timeout: Route konnte nicht vollständig ermittelt werden.")
        except Exception as e:
            self._show_error(f"Fehler: {str(e)}")
        finally:
            self.trace_btn.setEnabled(True)
            self.trace_btn.setText("🗺️ Route tracen")
    
    def _parse_traceroute(self, output):
        """Parse traceroute output into structured hops."""
        hops = []
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Windows format: "  1    <10 ms    <1 ms    <1 ms  192.168.1.1"
            # Linux format: " 1  192.168.1.1  1.234 ms  1.234 ms  1.234 ms"
            
            # Try to extract hop number and IP/time
            parts = line.split()
            if len(parts) < 2:
                continue
            
            # Check if first part is a number (hop number)
            try:
                hop_num = int(parts[0])
            except:
                continue
            
            # Find IP address (looks like x.x.x.x)
            ip = None
            for part in parts:
                if '.' in part and part.replace('.', '').replace('*', '').isdigit():
                    ip = part
                    break
            
            # Find time value (ends with 'ms')
            time_ms = None
            for i, part in enumerate(parts):
                if 'ms' in part.lower():
                    try:
                        # Extract number before 'ms'
                        time_str = part.lower().replace('ms', '').replace('<', '').strip()
                        time_ms = float(time_str)
                        break
                    except:
                        # Try previous part
                        if i > 0:
                            try:
                                time_ms = float(parts[i-1])
                                break
                            except:
                                pass
            
            # If timeout (*   *   *) or no response
            if '*' in line and not ip:
                ip = "* * *"
                time_ms = None
            
            if ip or time_ms is not None:
                hops.append({
                    'hop': hop_num,
                    'ip': ip or "—",
                    'time': time_ms
                })
        
        return hops
    
    def _display_hops(self, hops, target):
        """Display hops visually with spectrum gradient."""
        # Add source (user)
        self._add_hop_widget(0, "🖥️ Sie", "Local", 0, is_source=True)
        
        # Add each hop
        for hop_data in hops:
            self._add_hop_widget(
                hop_data['hop'],
                hop_data['ip'],
                f"{hop_data['time']:.1f} ms" if hop_data['time'] is not None else "Timeout",
                hop_data['time']
            )
        
        # Add destination
        self._add_hop_widget(len(hops) + 1, f"🎯 {target}", "Ziel", 0, is_destination=True)
    
    def _add_hop_widget(self, hop_num, address, time_str, time_ms, is_source=False, is_destination=False):
        """Create a visual hop widget."""
        hop_widget = QWidget()
        hop_layout = QHBoxLayout(hop_widget)
        hop_layout.setContentsMargins(8, 4, 8, 4)
        hop_layout.setSpacing(12)
        
        # Hop number
        if not is_source and not is_destination:
            num_label = QLabel(f"#{hop_num}")
            num_label.setFixedWidth(30)
            num_label.setStyleSheet("color: #777; font-size: 11px; font-weight: bold;")
            hop_layout.addWidget(num_label)
        else:
            hop_layout.addSpacing(30)
        
        # Connection arrow/icon
        if is_source:
            icon = QLabel("🔵")
        elif is_destination:
            icon = QLabel("🔴")
        else:
            icon = QLabel("➜")
        icon.setFixedWidth(20)
        hop_layout.addWidget(icon)
        
        # Address (with elision)
        addr_label = QLabel(address)
        addr_label.setStyleSheet("color: #e0e0e0; font-size: 12px; font-family: 'Consolas', monospace;")
        # addr_label.setWordWrap(True) # Don't wrap, let it clip or elide if we could
        # For simple QLabel, elision is tricky without custom paint or fixed width.
        # We'll rely on layout stretch, but maybe set a max width?
        # Actually, let's just ensure it doesn't push others out.
        # But we can't easily set elide mode on standard QLabel without subclassing or setting text manually with metrics.
        # Let's just keep it as is but maybe reduce font size if it's very long?
        # Or better: use a shorter format for display if possible.
        hop_layout.addWidget(addr_label)
        
        hop_layout.addStretch()
        
        # Time with color coding (spectrum gradient)
        time_label = QLabel(time_str)
        if time_ms is not None and time_ms > 0:
            # Map time to spectrum color (0-200ms range)
            color = self._get_spectrum_color(time_ms, 0, 200)
            time_label.setStyleSheet(f"""
                color: {color};
                font-size: 12px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.05);
                padding: 4px 8px;
                border-radius: 4px;
            """)
        else:
            time_label.setStyleSheet("color: #555; font-size: 12px;")
        
        time_label.setFixedWidth(80)
        time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hop_layout.addWidget(time_label)
        
        # Style the hop widget
        hop_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 50, 50, 0.3);
                border-left: 3px solid rgba(0, 122, 255, 0.5);
                border-radius: 4px;
            }
            QWidget:hover {
                background-color: rgba(70, 70, 70, 0.5);
            }
        """)
        
        hop_widget.setFixedHeight(32)
        self.path_layout.addWidget(hop_widget)
    
    def _get_spectrum_color(self, value, min_val, max_val):
        """Map value to spectrum color (Red->Violet)."""
        # Normalize value to 0-1 range
        normalized = max(0, min(1, (value - min_val) / (max_val - min_val)))
        
        # Spectrum colors (matching CircularGauge)
        colors = [
            "#FF3B30",  # Red (0.0)
            "#FF9500",  # Orange (0.2)
            "#FFCC00",  # Yellow (0.4)
            "#34C759",  # Green (0.6)
            "#007AFF",  # Blue (0.8)
            "#AF52DE",  # Violet (1.0)
        ]
        
        # Find position in color array
        index = normalized * (len(colors) - 1)
        lower_idx = int(index)
        upper_idx = min(lower_idx + 1, len(colors) - 1)
        
        # For simplicity, return the nearest color (no interpolation)
        if index - lower_idx < 0.5:
            return colors[lower_idx]
        else:
            return colors[upper_idx]
    
    def _show_error(self, message):
        """Show error message."""
        self._clear_path()
        error = QLabel(f"❌ {message}")
        error.setAlignment(Qt.AlignCenter)
        error.setStyleSheet("color: #ff3b30; font-size: 13px; padding: 40px;")
        self.path_layout.addWidget(error)

