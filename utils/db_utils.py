import aiosqlite
from config import DB_NAME

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            return results[0] if results else 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def save_user_answer(user_id, question_index, correct):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO user_answers (user_id, question_index, correct) VALUES (?, ?, ?)', (user_id, question_index, int(correct)))
        await db.commit()

async def update_user_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT COUNT(*) FROM user_answers WHERE user_id = (?) AND correct = 1', (user_id,)) as cursor:
            correct_answers = await cursor.fetchone()
            await db.execute('INSERT OR REPLACE INTO user_results (user_id, correct_answers) VALUES (?, ?)', (user_id, correct_answers[0]))
        await db.commit()

async def get_user_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT correct_answers FROM user_results WHERE user_id = (?)', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return {'correct_answers': result[0]} if result else None

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS user_answers (user_id INTEGER, question_index INTEGER, correct INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS user_results (user_id INTEGER PRIMARY KEY, correct_answers INTEGER)''')
        await db.commit()

async def clear_user_answers(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM user_answers WHERE user_id = ?', (user_id,))
        await db.commit()
