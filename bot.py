import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

@dp.message_handler()
async def chat_with_estonian(message: types.Message):
    prompt = f"Vasta sellele lausele eesti keeles: {message.text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sa oled eesti keelt oskav vestluspartner."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = response['choices'][0]['message']['content']
        await message.answer(reply)
    except Exception as e:
        await message.answer("Vabandust, tekkis tehniline probleem.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
