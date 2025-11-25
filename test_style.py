#!/usr/bin/env python
"""Test script to verify Mac-style is working"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QStyleFactory
from PySide6.QtCore import QFile, QTextStream

def main():
    app = QApplication(sys.argv)
    
    # Show available styles
    print("Available styles:", QStyleFactory.keys())
    
    # Set Fusion style
    app.setStyle("Fusion")
    print("Current style:", app.style().objectName())
    
    # Load and apply stylesheet
    qss_file = QFile("ui/styles/mac_light.qss")
    if qss_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(qss_file)
        qss = stream.readAll()
        qss_file.close()
        app.setStyleSheet(qss)
        print(f"Loaded QSS: {len(qss)} characters")
        print("First 100 chars of QSS:", qss[:100])
    else:
        print("Failed to load QSS file")
    
    # Create a simple window
    window = QMainWindow()
    window.setWindowTitle("Mac Style Test")
    window.setMinimumSize(400, 300)
    
    central = QWidget()
    layout = QVBoxLayout()
    label = QLabel("🧰 Mac-Style Test Window")
    layout.addWidget(label)
    central.setLayout(layout)
    window.setCentralWidget(central)
    
    window.show()
    
    print("\nWindow is now showing. Check if Mac-style is applied.")
    print("If the background is light gray (#ececec), it's working!")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
