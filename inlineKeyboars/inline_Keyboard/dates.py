from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_dates_keyboard(subject, dates):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=date, callback_data=f"date_{subject}_{date}")]
            for date in sorted(dates)
        ]
    )