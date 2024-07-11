import asyncio
import logging
import sys
from idlelib.undo import Command
from os import getenv
from pyexpat.errors import messages

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
from sqlalchemy.testing.suite.test_reflection import users

import view

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    user = view.User(message.from_user.id)
    user_create = user.create_user(message.chat.username)
    await message.answer(user_create)
    # await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#         await message.answer(f"user id: {str(message.from_user.id)}")
#
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


@dp.message(Command("task"))
async def add_task(message: Message) -> None:
    user = view.User(message.from_user.id)
    task = user.create_task("dsada", "sdad")
    await message.answer(task)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
