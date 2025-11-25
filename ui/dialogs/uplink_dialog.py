"""
MacGyver Uplink Dialog
UI for Secure P2P Translation Sync
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QTabWidget, QWidget, QProgressBar, QMessageBox, QGroupBox,
    QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QClipboard, QGuiApplication

from core.services.uplink_service import get_uplink_service
from core.services.i18n_service import I18nService

class UplinkWorker(QThread):
    """Worker thread for network operations"""
    finished = Signal(bool, object) # success, result (code or data)
    
    def __init__(self, mode, data=None, code=None):
        super().__init__()
        self.mode = mode # 'send' or 'receive'
        self.data = data
        self.code = code
        self.service = get_uplink_service()
        
    def run(self):
        if self.mode == 'send':
            success, result = self.service.generate_uplink_code(self.data)
            self.finished.emit(success, result)
        elif self.mode == 'receive':
            success, result = self.service.receive_uplink_data(self.code)
            self.finished.emit(success, result)

class UplinkDialog(QDialog):
    def __init__(self, i18n_service: I18nService, parent=None):
        super().__init__(parent)
        self.i18n_service = i18n_service
        self.setWindowTitle("MacGyver Uplink 🚀")
        self.setMinimumSize(600, 500)
        self.received_data = None
        
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("<h2>MacGyver Uplink</h2><p>Securely sync translations without servers.</p>")
        header.setTextFormat(Qt.RichText)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_send_tab(), "📤 Send")
        self.tabs.addTab(self._create_receive_tab(), "📥 Receive")
        layout.addWidget(self.tabs)
        
        # Status Bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666;")
        layout.addWidget(self.status_label)
        
    def _create_send_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Options
        group = QGroupBox("What to send?")
        g_layout = QVBoxLayout()
        
        self.send_current = QRadioButton(f"Current Language ({self.i18n_service.current_language})")
        self.send_current.setChecked(True)
        self.send_all = QRadioButton("All My Overrides")
        
        g_layout.addWidget(self.send_current)
        g_layout.addWidget(self.send_all)
        group.setLayout(g_layout)
        layout.addWidget(group)
        
        # Generate Button
        self.btn_generate = QPushButton("🚀 Generate Magic Code")
        self.btn_generate.setMinimumHeight(40)
        self.btn_generate.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.btn_generate.clicked.connect(self._start_upload)
        layout.addWidget(self.btn_generate)
        
        # Progress
        self.send_progress = QProgressBar()
        self.send_progress.setVisible(False)
        layout.addWidget(self.send_progress)
        
        # Result Area
        self.code_display = QLineEdit()
        self.code_display.setReadOnly(True)
        self.code_display.setPlaceholderText("Magic Code will appear here...")
        self.code_display.setStyleSheet("font-family: monospace; font-size: 16px; padding: 10px;")
        layout.addWidget(self.code_display)
        
        self.btn_copy = QPushButton("📋 Copy to Clipboard")
        self.btn_copy.clicked.connect(self._copy_code)
        self.btn_copy.setEnabled(False)
        layout.addWidget(self.btn_copy)
        
        layout.addStretch()
        return tab
        
    def _create_receive_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input
        layout.addWidget(QLabel("Enter Magic Code:"))
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("MG-XXXX-YYYY...")
        self.code_input.setStyleSheet("font-family: monospace; font-size: 16px; padding: 10px;")
        layout.addWidget(self.code_input)
        
        # Download Button
        self.btn_download = QPushButton("📥 Download & Decrypt")
        self.btn_download.setMinimumHeight(40)
        self.btn_download.clicked.connect(self._start_download)
        layout.addWidget(self.btn_download)
        
        # Progress
        self.recv_progress = QProgressBar()
        self.recv_progress.setVisible(False)
        layout.addWidget(self.recv_progress)
        
        # Preview
        layout.addWidget(QLabel("Preview:"))
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        layout.addWidget(self.preview_text)
        
        # Merge Button
        self.btn_merge = QPushButton("✨ Merge Translations")
        self.btn_merge.setEnabled(False)
        self.btn_merge.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.btn_merge.clicked.connect(self._merge_data)
        layout.addWidget(self.btn_merge)
        
        return tab
        
    def _start_upload(self):
        # Prepare Data
        data = {}
        if self.send_current.isChecked():
            lang = self.i18n_service.current_language
            overrides = self.i18n_service.get_all_user_overrides(lang)
            if not overrides:
                QMessageBox.warning(self, "Empty", "No overrides found for current language.")
                return
            data = {
                "type": "single",
                "language": lang,
                "translations": overrides
            }
        else:
            all_langs = {}
            for lang in self.i18n_service.get_all_language_codes():
                overrides = self.i18n_service.get_all_user_overrides(lang)
                if overrides:
                    all_langs[lang] = overrides
            if not all_langs:
                QMessageBox.warning(self, "Empty", "No overrides found at all.")
                return
            data = {
                "type": "multi",
                "languages": all_langs
            }
            
        # UI Update
        self.btn_generate.setEnabled(False)
        self.send_progress.setVisible(True)
        self.send_progress.setRange(0, 0) # Indeterminate
        self.status_label.setText("Encrypting and Uploading...")
        
        # Start Thread
        self.worker = UplinkWorker('send', data=data)
        self.worker.finished.connect(self._on_upload_finished)
        self.worker.start()
        
    def _on_upload_finished(self, success, result):
        self.btn_generate.setEnabled(True)
        self.send_progress.setVisible(False)
        
        if success:
            self.code_display.setText(result)
            self.btn_copy.setEnabled(True)
            self.status_label.setText("Upload Successful! Share this code.")
            QMessageBox.information(self, "Success", "Magic Code generated!\nValid for 24 hours.")
        else:
            self.status_label.setText("Error")
            QMessageBox.critical(self, "Upload Failed", result)
            
    def _copy_code(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.code_display.text())
        self.status_label.setText("Code copied to clipboard!")
        
    def _start_download(self):
        code = self.code_input.text().strip()
        if not code.startswith("MG-"):
            QMessageBox.warning(self, "Invalid Code", "Code must start with 'MG-'")
            return
            
        # UI Update
        self.btn_download.setEnabled(False)
        self.recv_progress.setVisible(True)
        self.recv_progress.setRange(0, 0)
        self.status_label.setText("Downloading and Decrypting...")
        self.preview_text.clear()
        
        # Start Thread
        self.worker = UplinkWorker('receive', code=code)
        self.worker.finished.connect(self._on_download_finished)
        self.worker.start()
        
    def _on_download_finished(self, success, result):
        self.btn_download.setEnabled(True)
        self.recv_progress.setVisible(False)
        
        if success:
            self.received_data = result
            self.status_label.setText("Data Received! Review and Merge.")
            
            # Show Preview
            import json
            preview = json.dumps(result, indent=2, ensure_ascii=False)
            self.preview_text.setText(preview)
            self.btn_merge.setEnabled(True)
        else:
            self.status_label.setText("Error")
            QMessageBox.critical(self, "Download Failed", str(result))
            
    def _merge_data(self):
        if not self.received_data:
            return
            
        try:
            count = 0
            dtype = self.received_data.get("type")
            
            if dtype == "single":
                lang = self.received_data.get("language")
                translations = self.received_data.get("translations", {})
                for k, v in translations.items():
                    self.i18n_service.save_user_override(lang, k, v)
                    count += 1
            elif dtype == "multi":
                languages = self.received_data.get("languages", {})
                for lang, translations in languages.items():
                    for k, v in translations.items():
                        self.i18n_service.save_user_override(lang, k, v)
                        count += 1
                        
            QMessageBox.information(self, "Success", f"Successfully merged {count} translations!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Merge Error", str(e))
