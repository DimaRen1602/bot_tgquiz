from aiogram import types
from aiogram import F
from config import dp
from utils.db_utils import get_quiz_index, update_quiz_index, save_user_answer, update_user_result, get_user_stats
from utils.quiz_data import quiz_data
from handlers.quiz_handler import get_question


@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['options'][quiz_data[current_question_index]['correct_option']]

    await save_user_answer(callback.from_user.id, current_question_index, correct=True)
    await callback.message.answer(f"Ваш ответ: {correct_option}.\nВерно!")

    await process_next_question(callback, current_question_index + 1)


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['options'][quiz_data[current_question_index]['correct_option']]

    await save_user_answer(callback.from_user.id, current_question_index, correct=False)
    await callback.message.answer(f"Ваш ответ: неверный.\nПравильный ответ: {correct_option}")

    await process_next_question(callback, current_question_index + 1)


async def process_next_question(callback, next_question_index):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await update_quiz_index(callback.from_user.id, next_question_index)

    if next_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await update_user_result(callback.from_user.id)
        # Получаем количество правильных ответов
        stats = await get_user_stats(callback.from_user.id)
        correct_answers = stats['correct_answers']
        total_questions = len(quiz_data)
        # Отправляем пользователю итоговое сообщение
        await callback.message.answer(
            f"Квиз завершен! Вы ответили правильно на {correct_answers} из {total_questions} вопросов.")
