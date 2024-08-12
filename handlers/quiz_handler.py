from aiogram import types
from aiogram.filters.command import Command
from aiogram import F
from config import dp
from utils.db_utils import get_quiz_index, update_quiz_index, save_user_answer, get_user_stats, clear_user_answers
from utils.quiz_data import quiz_data, generate_options_keyboard

@dp.message(F.text == "Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await clear_user_answers(message.from_user.id)  # Очистка предыдущих данных
    await new_quiz(message)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    stats = await get_user_stats(message.from_user.id)
    if stats:
        await message.answer(f"Последний результат: {stats['correct_answers']} из {len(quiz_data)} правильных.")
    else:
        await message.answer("Статистика не найдена.")
