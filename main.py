from src.telegram_bot import TelegramBot
from src.drive_bot import DriveBot

# bot = TelegramBot()
# bot.start()
drive_bot = DriveBot()
print(drive_bot.get_data())