TOKENS = {
    "bg": "#F5F7FA",
    "card": "#FFFFFF",
    "text": "#1F2937",
    "primary": "#2563EB",
    "border": "#D1D5DB",
}

APP_QSS = f"""
QWidget {{ background: {TOKENS['bg']}; color: {TOKENS['text']}; font-family: 'Microsoft YaHei', 'Segoe UI'; font-size: 13px; }}
QFrame {{ background: {TOKENS['card']}; border: 1px solid {TOKENS['border']}; border-radius: 10px; }}
QPushButton {{ background: {TOKENS['primary']}; color: white; border: none; border-radius: 6px; padding: 6px 12px; }}
QPushButton:checked {{ background: #1D4ED8; }}
QTextEdit {{ background: white; border: 1px solid {TOKENS['border']}; border-radius: 6px; }}
"""
