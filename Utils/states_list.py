from aiogram.utils.helper import Helper, HelperMode, ListItem


class States(Helper):
    mode = HelperMode.snake_case
    CREATE_MAILING = ListItem()
    SEND_MAILING = ListItem()
    CREATE_EVENT = ListItem()
    SEND_EVENT = ListItem()
