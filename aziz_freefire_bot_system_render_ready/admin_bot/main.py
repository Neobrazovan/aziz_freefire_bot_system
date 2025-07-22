from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '7845929114:AAFl93wBPBP19e3NHE-4KaNF2ELrw7Rb6Zo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def receive_photo(message: types.Message):
    await message.forward(chat_id=message.chat.id)  # Просто пересылает тебе же для контроля

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
