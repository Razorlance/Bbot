from aiogram import Dispatcher

from config import dp, executor, shutdown

import Commands.commands_list

# 381495566 - Ваня
# 367622073 - Я

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
