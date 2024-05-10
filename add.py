import sqlite3

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Kullanıcılar tablosunu oluşturma
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL
                    )''')

    # Örnek kullanıcı verileri
    users = [
        ('John Doe', 30),
        ('Jane Smith', 25),
        ('Alice Johnson', 35)
    ]

    # Veri eklemek için INSERT INTO kullanarak kullanıcıları ekleyin
    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)

    # Değişiklikleri kaydetmek için commit yapın
    conn.commit()

    # Bağlantıyı ve imleci kapat
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database("example.db")
