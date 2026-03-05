# Translation App

A modern, user-friendly desktop translation application built with Python and PyQt5. Features large, bold fonts for accessibility and uses Google Translate's free API for accurate translations.

## Features
- ✅ Translate text between 65+ popular languages
- ✅ Large, bold fonts for accessibility
- ✅ Modern Windows-style theme with clean UI
- ✅ Free Google Translate API (no registration required)
- ✅ Input sanitization and error handling
- ✅ Menu bar with File, Edit, View, and Help options
- ✅ Responsive design with minimum 800x600 resolution

## Supported Languages
**Major Languages:**
- English, Spanish, French, German, Italian, Portuguese
- Russian, Japanese, Korean, Chinese (Simplified & Traditional)
- Arabic, Hindi, Dutch, Swedish, Danish, Norwegian, Finnish, Polish

**Asian Languages:**
- Thai, Vietnamese, Bengali, Tamil, Telugu, Malayalam, Kannada
- Gujarati, Punjabi, Marathi, Nepali, Sinhala, Myanmar, Khmer, Lao

**European Languages:**
- Turkish, Hebrew, Ukrainian, Czech, Hungarian, Romanian, Bulgarian
- Croatian, Slovak, Slovenian, Estonian, Latvian, Lithuanian
- Icelandic, Maltese, Basque, Welsh, Irish, Macedonian, Belarusian
- Albanian, Catalan, Galician

**Other Languages:**
- Persian (Farsi), Urdu, Georgian, Armenian, Azerbaijani
- Kazakh, Kyrgyz, Uzbek, Mongolian, Afrikaans, Swahili, Amharic

## Requirements
- Python 3.7+
- PyQt5
- requests

## Installation & Setup
1. Clone or download this repository
2. Install dependencies:
   ```sh
   pip install pyqt5 requests
   ```
3. Run the application:
   ```sh
   python m.py
   ```

## User-Friendly Executable

- Just double-click `TranslationApp.exe` to launch the app instantly.


## Usage
1. Select source and target languages from dropdown menus
2. Enter text to translate in the input area
3. Click "Translate" button
4. View the translated text in the output area

## Technical Details
- Uses Google Translate's free API endpoint
- Built with PyQt5 for cross-platform desktop compatibility
- Implements accessibility features with large, bold fonts
- Input is sanitized and limited to 1000 characters for API safety
- Modern UI with Windows-style theme and proper error handling

## Notes
- This app uses Google Translate's free public API
- No API key or registration required
- For production use, consider implementing rate limiting
