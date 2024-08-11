from aiogram.types import Message

from Config.config import SUPPORTBOT


async def get_support(message: Message):
    await message.answer(f"🔘 Если возник какой-то вопрос напиши нам:\n[⚙️ Техподдержка]({SUPPORTBOT})",
                         disable_web_page_preview=True, parse_mode='Markdown', reply_markup=None)
