import sqlite3

connection = sqlite3.connect('Users.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               password TEXT NOT NULL
)
""")


def create_user_data(id: int, username: str, password: str) -> None: 
    cursor.execute("""INSERT INTO Users (id, username, password) VALUES (?, ?, ?)""", (id, username, password))

def update_user_data(id: int, username: str, password: str, parameter: int) -> None:
    match parameter:
        case 1:
            cursor.execute("UPDATE Users SET username = ? WHERE id = ?", (username, id))
        case 2:
            cursor.execute("UPDATE Users SET password = ? WHERE id = ?", (password, id))
            
        case _:
            raise ValueError("Неверный параметр")

def delete_user_data(id: int) -> None:
    cursor.execute("DELETE FROM Users WHERE id = ?", (id, ))

def select_user_data(id: int):
    cursor.execute("SELECT username, password FROM Users WHERE id = ?", (id, ))
    result = cursor.fetchone()

    return result

def select_id() -> None:
    cursor.execute("SELECT id FROM Users")
    list = cursor.fetchall()

    result = []

    for i in list:
        new_elem = str(i).replace('(', '').replace(',', '').replace(')', '')
        result.append(new_elem)

    return result


def save_changes() -> None:
    connection.commit()
    connection.close()

if __name__ == "__main__":
    print(f"Файл {__name__}")