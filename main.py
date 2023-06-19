import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import os
import os.path
cwd = os.getcwd()
data_folder = os.path.join(cwd, "runs", "detect", "predict")
import shutil





cur_catal = ""

catals = ["1", "2"]

# Объект бота
bot = Bot(token="6076406944:AAFM4nk2Pa8hycOCx3p4bArKZy-wdqerjlM")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

async def predict_photo(photo, message):
    os.system("yolo task=detect mode=predict model=best.pt conf=0.25 source="+photo+" save=True")
    with open(os.path.join(data_folder, photo), 'rb') as predicted_photo:
        await bot.send_photo(photo=predicted_photo, chat_id=message.chat.id)
    shutil.rmtree(data_folder)

@dp.message_handler(lambda message: message.text == "Вернуться в меню")
async def to_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Загрузить фото", "Каталоги"]
    keyboard.add(*buttons)
    await message.answer("Выбери опцию", reply_markup=keyboard)



@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Загрузить фото", "Каталоги"]
    keyboard.add(*buttons)
    await message.answer("Выбери опцию", reply_markup=keyboard)



@dp.message_handler(lambda message: message.text == "Каталоги")
async def catalogs(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Выбор каталога", "Удаление каталога", "Создание каталога", "Редактирование каталога", "Вернуться в меню"]
    keyboard.add(*buttons)
    await message.reply("Опции каталогов:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Выбор каталога")
async def choose_catalog(message: types.Message):
    #filler
    for i in catals:
        inkeyboard = types.InlineKeyboardMarkup()
        inkeyboard.add(types.InlineKeyboardButton(text=i, callback_data='catal_to_choose'+i))
        await message.answer("Каталог" + i, reply_markup=inkeyboard)

@dp.callback_query_handler(lambda message: message.data.startswith('catal_to_choose'))
async def choose_catalog_callback(call: types.CallbackQuery):
    cur_catal = call.data[len("catal_to_choose"):]
    print("Чел выбрал каталог "+cur_catal)
    print("Спарсить фото из каталогов")

    await call.message.reply("Каталог выбран", reply_markup=types.ReplyKeyboardRemove())
    await call.answer()



@dp.message_handler(lambda message: message.text == "Удаление каталога")
async def delete_catalog(message: types.Message):
    #filler
    for i in catals:
        inkeyboard = types.InlineKeyboardMarkup()
        inkeyboard.add(types.InlineKeyboardButton(text=i, callback_data='catal_to_delete'+i))
        await message.answer("Каталог" + i, reply_markup=inkeyboard)

@dp.callback_query_handler(lambda message: message.data.startswith('catal_to_delete'))
async def delete_catalog_callback(call: types.CallbackQuery):
    print(call.data[len("catal_to_delete"):])
    print("Удалить каталог")
    await call.message.reply("Каталог удалён", reply_markup=types.ReplyKeyboardRemove())



class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'

@dp.message_handler(lambda message: message.text == "Создание каталога")
async def create_catalog(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вернуться в меню"]
    keyboard.add(*buttons)
    await message.answer("Введите название нового каталога после команды /name ", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.startswith('/name '))
async def enter_new_catal(message: types.Message):
    new_catal = message.text[len('/name '):]
    print(new_catal)
    await message.answer("Каталог с именем "+new_catal+" успешно создан")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Загрузить фото", "Каталоги"]
    keyboard.add(*buttons)
    await message.answer("Выбери опцию", reply_markup=keyboard)




@dp.message_handler(lambda message: message.text == "Загрузить фото")
async def handle_photo(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вернуться в меню"]
    keyboard.add(*buttons)
    await message.reply("Загрузи в бот фото", reply_markup=keyboard)

@dp.message_handler(content_types=['photo'])
async def loading_photo(message):
    photo = 'loaded_photo.jpg'
    await message.photo[-1].download(photo)
    await predict_photo(photo, message)



if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)