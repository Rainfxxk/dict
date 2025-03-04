import sqlite3
import datetime

conn = sqlite3.connect('word_database.db', check_same_thread=False)
cursor = conn.cursor()


def update_revise():

    revise_curve = {
        1 : 2,
        2 : 4,
        4 : 7,
        7 : 15,
        15 : 30,
        30 : 60
    }

    yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1))
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    cursor.execute('SELECT * FROM revise where time = ?', (yesterday_str,))
    result = cursor.fetchall()
    for row in result:
        word_id = row[0]
        next_time = row[2]
        time = yesterday + datetime.timedelta(days=next_time)
        time_str = time.strftime('%Y-%m-%d')
        cursor.execute("UPDATE revise SET time =?, next_time =? WHERE word_id =?", (time_str, revise_curve[next_time], word_id))
    conn.commit()



def insert_revise(word_id):
    cursor.execute('select * from revise where word_id = ?', (word_id,))
    result = cursor.fetchone()
    time_str = datetime.datetime.now().strftime('%Y-%m-%d')
    if result is None:
        cursor.execute("INSERT INTO revise (word_id, time, next_time) VALUES (?, ?, ?)", (word_id, time_str, 1))
        conn.commit()
    else:
        cursor.execute("UPDATE revise SET time =?, next_time =? WHERE word_id =?", (time_str, 1, word_id))


def insert_example(meaning_id, example):
    cursor.execute("INSERT INTO examples (meaning_id, sentence, sentence_ch) VALUES (?,?,?)", (meaning_id, example['sentence'], example['translation']))


def insert_meaning(id, definition):
    cursor.execute("INSERT INTO meanings (word_id, pos, meaning, meaning_ch) VALUES (?,?,?, ?)", (id, definition['part_of_speech'], definition['english_def'], definition['chinese_translation']))
    id = cursor.lastrowid
    for example in definition['examples']:
        insert_example(id, example)


def insert_word(word):
    # 检查单词是否已经在数据库中
    cursor.execute('SELECT * FROM words WHERE word = ?', (word['word'],))

    # 单词不在数据库中，添加新单词
    result = cursor.fetchone()
    if result is None:
        pronounce = word['pronounce']
        cursor.execute("INSERT INTO words (word, pronounce) VALUES (?, ?)", (word['word'], pronounce))
        id = cursor.lastrowid
        for meaning in word['definitions']:
            insert_meaning(id, meaning)
        insert_revise(id)
        conn.commit()
    else:
        id = result[0]
        insert_revise(id)
        conn.commit()
