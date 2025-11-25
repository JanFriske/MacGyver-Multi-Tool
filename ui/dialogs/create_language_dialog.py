"""
Create Custom Language Dialog
Allows users to create new custom languages
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QComboBox, QMessageBox, QFormLayout
)
from PySide6.QtCore import Qt

class CreateLanguageDialog(QDialog):
    """Dialog for creating a new custom language"""
    
    def __init__(self, custom_lang_service, i18n_service, parent=None):
        super().__init__(parent)
        self.custom_lang_service = custom_lang_service
        self.i18n_service = i18n_service
        self.created_lang_code = None
        
        self.setWindowTitle("Create New Language")
        self.setMinimumWidth(500)
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(
            "Create a custom language with your own translations.\n"
            "The language will be based on English or German."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Language name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Esperanto, Leichte Sprache, etc.")
        form_layout.addRow("Language Name:", self.name_edit)
        
        # Language code
        code_layout = QHBoxLayout()
        code_prefix = QLabel("custom_")
        code_prefix.setStyleSheet("color: #666; font-family: monospace;")
        self.code_edit = QLineEdit()
        self.code_edit.setPlaceholderText("esperanto")
        code_layout.addWidget(code_prefix)
        code_layout.addWidget(self.code_edit)
        form_layout.addRow("Language Code:", code_layout)
        
        # Description (optional)
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText("Optional description...")
        form_layout.addRow("Description:", self.description_edit)
        
        # Base language
        self.base_combo = QComboBox()
        self.base_combo.addItem("English", "en")
        self.base_combo.addItem("German (Deutsch)", "de")
        form_layout.addRow("Based on:", self.base_combo)
        
        layout.addLayout(form_layout)
        
        # Info about what happens
        help_label = QLabel(
            "ℹ️ After creation, all ~260 translation keys will be available.\n"
            "You can then customize each translation in the Translation Editor."
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; font-size: 11px; margin-top: 10px;")
        layout.addWidget(help_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        create_btn = QPushButton("Create")
        create_btn.setDefault(True)
        create_btn.clicked.connect(self._create_language)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(create_btn)
        
        layout.addLayout(button_layout)
    
    def _create_language(self):
        """Create the custom language"""
        name = self.name_edit.text().strip()
        code = self.code_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        base_lang = self.base_combo.currentData()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a language name.")
            return
        
        if not code:
            QMessageBox.warning(self, "Invalid Input", "Please enter a language code.")
            return
        
        # Sanitize code
        code = ''.join(c for c in code if c.isalnum() or c == '_').lower()
        
        if not code:
            QMessageBox.warning(self, "Invalid Input", "Language code must contain at least one alphanumeric character.")
            return
        
        # Create
        try:
            self.custom_lang_service.create_custom_language(
                name=name,
                code=code,
                description=description,
                base_language=base_lang
            )
            
            self.created_lang_code = f"custom_{code}" if not code.startswith("custom_") else code
            
            QMessageBox.information(
                self,
                "Language Created",
                f"Custom language '{name}' created successfully!\n\n"
                f"Language code: {self.created_lang_code}\n"
                f"Based on: {base_lang}\n\n"
                f"You can now customize translations in the Translation Editor."
            )
            
            self.accept()
            
        except ValueError as e:
            QMessageBox.warning(self, "Creation Failed", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create language:\n{str(e)}")
    
    def get_created_language_code(self):
        """Get the code of the created language"""
        return self.created_lang_code
