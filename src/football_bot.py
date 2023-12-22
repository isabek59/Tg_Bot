import json

from src.parser import parser
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# Bot token can be obtained via https://t.me/BotFather
# Please type your bot token
TOKEN = 'Bot token from BotFather'
# TOKEN = getenv(BOT_TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    """
    Handle the /start command and display a keyboard with news categories.

    Args: message (types.Message): The incoming message object.

    """
    parser("news")
    start_buttons = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="All news")],
        [types.KeyboardButton(text="Last 3 news")],
        [types.KeyboardButton(text="Fresh news")]
    ], resize_keyboard=True)

    await message.answer(text=f'Привет, {message.from_user.first_name}!')
    await message.answer("Choose the category", reply_markup=start_buttons)


@dp.message(F.text == "All news")
async def get_all_news(message: types.Message):
    """
    Display all news articles stored in the 'news.json' file.

    Args: message (types.Message): The incoming message object.

    """
    with open("news.json", "r", encoding="utf-8") as file:
        new_dict = json.load(file)

        for key, val in sorted(new_dict.items()):
            news = f"{val['article_date_timestamp']}\n" \
                   f"{val['article_url']}\n" \
                   f"{val['article_title']}\n"
            await message.answer(news)
        await message.answer("All news sent")


@dp.message(F.text == "Last 3 news")
async def get_all_news(message: types.Message):
    """
    Display the last 3 news articles stored in the 'news.json' file.

    Args: message (types.Message): The incoming message object.

    """
    with open("news.json", "r", encoding="utf-8") as file:
        new_dict = json.load(file)

        for key, val in sorted(new_dict.items())[-3:]:
            news = f"{val['article_date_timestamp']}\n" \
                   f"{val['article_url']}\n" \
                   f"{val['article_title']}\n"
            await message.answer(news)
        await message.answer("Last 3 news sent")


@dp.message(F.text == "Fresh news")
async def get_fresh_news(message: types.Message):
    """
    Display and update with fresh news articles not present in 'news.json'.

    Args: message (types.Message): The incoming message object.

    """
    parser("fresh_news")
    list_id = []

    with open("fresh_news.json", "r", encoding="utf-8") as file:
        new_dict = json.load(file)

    with open("../news.json", "r", encoding="utf-8") as file1:
        old_dict = json.load(file1)

    for news_id in new_dict.keys():
        if news_id not in old_dict.keys():
            list_id.append(news_id)

    if len(list_id) > 0:
        with open("news.json", "w", encoding="utf-8") as file1:
            json.dump(new_dict, file1, indent=4, ensure_ascii=False)
        for news_id in sorted(list_id):
            news = f"{new_dict[news_id]['article_date_timestamp']}\n" \
                   f"{new_dict[news_id]['article_url']}\n" \
                   f"{new_dict[news_id]['article_title']}\n"
            await message.answer(news)
        await message.answer("Fresh news sent")
    else:
        await message.answer("No fresh news, try later")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
