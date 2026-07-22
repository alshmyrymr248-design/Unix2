from telegram import ReplyKeyboardMarkup


def main_menu():
    keyboard = [
        ["📚 المواد الدراسية", "📁 الملخصات"],
        ["📝 التكاليف", "📄 الامتحانات السابقة"],
        ["⏰ الدوام", "📍 أماكن القاعات"],
        ["📢 الإعلانات", "🧠 UniX2 AI"],
        ["👤 المندوب", "💰 مسؤول التكاليف"],
        ["👨‍💻 مهندس النظام", "ℹ️ عن النظام"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
