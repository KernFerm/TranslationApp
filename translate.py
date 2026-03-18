import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QComboBox, QMessageBox, QMenuBar, QAction, QMainWindow
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Free API endpoint (Google Translate - via translate.googleapis.com)
API_URL = "https://translate.googleapis.com/translate_a/single"
# MyMemory supported languages (common ones)
SUPPORTED_LANGS = [
    {"code": "en", "name": "English"},
    {"code": "es", "name": "Spanish"},
    {"code": "fr", "name": "French"},
    {"code": "de", "name": "German"},
    {"code": "it", "name": "Italian"},
    {"code": "pt", "name": "Portuguese"},
    {"code": "ru", "name": "Russian"},
    {"code": "ja", "name": "Japanese"},
    {"code": "ko", "name": "Korean"},
    {"code": "zh", "name": "Chinese (Simplified)"},
    {"code": "zh-tw", "name": "Chinese (Traditional)"},
    {"code": "ar", "name": "Arabic"},
    {"code": "hi", "name": "Hindi"},
    {"code": "nl", "name": "Dutch"},
    {"code": "sv", "name": "Swedish"},
    {"code": "da", "name": "Danish"},
    {"code": "no", "name": "Norwegian"},
    {"code": "fi", "name": "Finnish"},
    {"code": "pl", "name": "Polish"},
    {"code": "tr", "name": "Turkish"},
    {"code": "he", "name": "Hebrew"},
    {"code": "th", "name": "Thai"},
    {"code": "vi", "name": "Vietnamese"},
    {"code": "uk", "name": "Ukrainian"},
    {"code": "cs", "name": "Czech"},
    {"code": "hu", "name": "Hungarian"},
    {"code": "ro", "name": "Romanian"},
    {"code": "bg", "name": "Bulgarian"},
    {"code": "hr", "name": "Croatian"},
    {"code": "sk", "name": "Slovak"},
    {"code": "sl", "name": "Slovenian"},
    {"code": "et", "name": "Estonian"},
    {"code": "lv", "name": "Latvian"},
    {"code": "lt", "name": "Lithuanian"},
    {"code": "fa", "name": "Persian (Farsi)"},
    {"code": "ur", "name": "Urdu"},
    {"code": "bn", "name": "Bengali"},
    {"code": "ta", "name": "Tamil"},
    {"code": "te", "name": "Telugu"},
    {"code": "ml", "name": "Malayalam"},
    {"code": "kn", "name": "Kannada"},
    {"code": "gu", "name": "Gujarati"},
    {"code": "pa", "name": "Punjabi"},
    {"code": "mr", "name": "Marathi"},
    {"code": "ne", "name": "Nepali"},
    {"code": "si", "name": "Sinhala"},
    {"code": "my", "name": "Myanmar (Burmese)"},
    {"code": "km", "name": "Khmer (Cambodian)"},
    {"code": "lo", "name": "Lao"},
    {"code": "ka", "name": "Georgian"},
    {"code": "hy", "name": "Armenian"},
    {"code": "az", "name": "Azerbaijani"},
    {"code": "kk", "name": "Kazakh"},
    {"code": "ky", "name": "Kyrgyz"},
    {"code": "uz", "name": "Uzbek"},
    {"code": "mn", "name": "Mongolian"},
    {"code": "af", "name": "Afrikaans"},
    {"code": "sw", "name": "Swahili"},
    {"code": "am", "name": "Amharic"},
    {"code": "is", "name": "Icelandic"},
    {"code": "mt", "name": "Maltese"},
    {"code": "eu", "name": "Basque"},
    {"code": "cy", "name": "Welsh"},
    {"code": "ga", "name": "Irish"},
    {"code": "mk", "name": "Macedonian"},
    {"code": "be", "name": "Belarusian"},
    {"code": "sq", "name": "Albanian"},
    {"code": "ca", "name": "Catalan"},
    {"code": "gl", "name": "Galician"}
]

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Translator")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(self.modern_style())
        self.init_menu_bar()
        self.init_ui()
        self.populate_languages()

    def init_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        clear_action = QAction('Clear All', self)
        clear_action.setShortcut('Ctrl+N')
        clear_action.triggered.connect(self.clear_all)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        copy_action = QAction('Copy Translation', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy_translation)
        edit_menu.addAction(copy_action)
        
        swap_action = QAction('Swap Languages', self)
        swap_action.setShortcut('Ctrl+S')
        swap_action.triggered.connect(self.swap_languages)
        edit_menu.addAction(swap_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        title = QLabel("Translation App")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Set much larger bold font for all widgets (accessibility)
        font_main = QFont("Segoe UI", 22, QFont.Bold)
        font_label = QFont("Segoe UI", 18, QFont.Bold)
        font_button = QFont("Segoe UI", 22, QFont.Bold)

        # Language selectors
        lang_layout = QHBoxLayout()
        self.from_lang = QComboBox()
        self.from_lang.setFont(font_main)
        self.to_lang = QComboBox()
        self.to_lang.setFont(font_main)
        from_label = QLabel("From:")
        from_label.setFont(font_label)
        to_label = QLabel("To:")
        to_label.setFont(font_label)
        lang_layout.addWidget(from_label)
        lang_layout.addWidget(self.from_lang)
        lang_layout.addWidget(to_label)
        lang_layout.addWidget(self.to_lang)
        layout.addLayout(lang_layout)

        # Input text
        self.input_text = QTextEdit()
        self.input_text.setFont(font_main)
        self.input_text.setPlaceholderText("Enter text to translate...")
        layout.addWidget(self.input_text)

        # Translate button
        self.translate_btn = QPushButton("Translate")
        self.translate_btn.setFont(font_button)
        self.translate_btn.clicked.connect(self.translate_text)
        layout.addWidget(self.translate_btn)

        # Output text
        self.output_text = QTextEdit()
        self.output_text.setFont(font_main)
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Translation will appear here...")
        layout.addWidget(self.output_text)

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()
    
    def copy_translation(self):
        text = self.output_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Copied", "Translation copied to clipboard!")
        else:
            QMessageBox.warning(self, "No Text", "No translation to copy.")
    
    def swap_languages(self):
        from_index = self.from_lang.currentIndex()
        to_index = self.to_lang.currentIndex()
        self.from_lang.setCurrentIndex(to_index)
        self.to_lang.setCurrentIndex(from_index)
        # Also swap the text content
        input_text = self.input_text.toPlainText()
        output_text = self.output_text.toPlainText()
        self.input_text.setPlainText(output_text)
        self.output_text.setPlainText(input_text)
    
    def show_about(self):
        QMessageBox.about(self, "About Translation App", 
            "Modern Translator v0.0.1\n\n"
            "A user-friendly translation application\n"
            "Built with PyQt5 and Google Translate API\n\n"
            "Features:\n"
            "• Large, accessible fonts\n"
            "• 65+ supported languages\n"
            "• Modern Windows theme\n"
            "• Free translation service")

    def modern_style(self):
        return """
            QWidget {
                background: #f3f6fa;
            }
            QLabel {
                color: #222;
                font-size: 20px;
            }
            QComboBox, QTextEdit {
                font-size: 22px;
                border: 1px solid #bfc7d5;
                border-radius: 6px;
                padding: 10px;
                background: #fff;
            }
            QPushButton {
                background: #0078d7;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 16px 0;
                font-size: 22px;
            }
            QPushButton:hover {
                background: #005fa3;
            }
        """

    def populate_languages(self):
        try:
            self.from_lang.clear()
            self.to_lang.clear()
            for lang in SUPPORTED_LANGS:
                self.from_lang.addItem(f"{lang['name']} ({lang['code']})", lang['code'])
                self.to_lang.addItem(f"{lang['name']} ({lang['code']})", lang['code'])
            # Set defaults
            self.from_lang.setCurrentText("English (en)")
            self.to_lang.setCurrentText("Spanish (es)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load languages: {e}")

    def sanitize_text(self, text):
        # Remove dangerous or unsupported characters, limit length, etc.
        sanitized = text.strip()
        # Optionally, limit to 1000 chars for API safety
        sanitized = sanitized[:1000]
        return sanitized

    def translate_text(self):
        import json
        text = self.input_text.toPlainText()
        sanitized = self.sanitize_text(text)
        if not sanitized:
            QMessageBox.warning(self, "Input Required", "Please enter text to translate.")
            return
        source = self.from_lang.currentData()
        target = self.to_lang.currentData()
        # Check language codes are valid and not empty
        if not source or not target:
            QMessageBox.critical(self, "Error", "Language selection is invalid. Please reload the app.")
            return
        if source == target:
            QMessageBox.warning(self, "Invalid Selection", "Source and target languages must be different.")
            return
        # Google Translate API parameters
        params = {
            "client": "gtx",
            "sl": source,
            "tl": target, 
            "dt": "t",
            "q": sanitized
        }
        try:
            resp = requests.get(API_URL, params=params, timeout=10)
            if resp.status_code != 200:
                raise Exception(f"{resp.status_code} {resp.reason}: {resp.text}")
            
            result = resp.json()
            # Google Translate returns nested arrays: [[[translated_text, original_text, ...]]]
            if result and len(result) > 0 and len(result[0]) > 0:
                translated = result[0][0][0]
                self.output_text.setPlainText(translated)
            else:
                raise Exception("No translation returned from API")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Translation failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())
