from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '7985603336:AAHMGuEskuBYRWBC3KT1YAFdnPTRWLy5ifA'
ADMIN_BOT_TOKEN = '7845929114:AAFl93wBPBP19e3NHE-4KaNF2ELrw7Rb6Zo'
ADMIN_ID = '@aziz_izi'
REVIEW_CHANNEL = '@aziz_otzzz'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    waiting_for_ff_id = State()
    waiting_for_payment = State()

@dp.message_handler(commands='start')
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer("Привет! Пожалуйста, отправь свой Free Fire ID:")
    await Form.waiting_for_ff_id.set()

@dp.message_handler(state=Form.waiting_for_ff_id)
async def get_ff_id(message: types.Message, state: FSMContext):
    await state.update_data(ff_id=message.text)
    await message.answer("Теперь отправь скриншот оплаты:")
    await Form.waiting_for_payment.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=Form.waiting_for_payment)
async def get_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ff_id = data['ff_id']
    photo = message.photo[-1].file_id

    caption = f"💎 Новый заказ!
👤 @{message.from_user.username}
🆔 FF ID: {ff_id}"
    admin_bot = Bot(token=ADMIN_BOT_TOKEN)
    await admin_bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=caption)
    await message.answer("Спасибо! Ваш заказ принят. Мы скоро с вами свяжемся.")
    await state.finish()

def get_rating_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=5)
    buttons = [InlineKeyboardButton(text=str(i), callback_data=f"rate_{i}") for i in range(1, 11)]
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands='rate')
async def ask_rating(message: types.Message):
    await message.answer("Оцените нашего бота от 1 до 10 ⭐", reply_markup=get_rating_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith('rate_'))
async def process_rating(callback: types.CallbackQuery):
    rating = callback.data.split("_")[1]
    await bot.send_message(REVIEW_CHANNEL, f"⭐ Оценка от @{callback.from_user.username}: {rating}/10")
    await callback.answer("Спасибо за вашу оценку!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
