import csv, sqlite3

DB_FILENAME = 'students.db'
CSV_FILENAME = 'students.csv'

def get_int(prompt):
    while True:
        try: return int(input(prompt))
        except ValueError:
            print("это не число, попробуйте снова")

class StudentBase:
    def __init__(self):
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS students (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                age INTEGER,
                                grade INTEGER
                            )
                        ''')

    def add_student(self):
        name = input("введите имя студента===>>>")
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
            if cursor.fetchone():
                print("этот студент уже есть")
                return

            age = get_int("введите возраст студента===>>>")
            grade = get_int("введите оценку студента===>>>")

            cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
            print(f"студент {name} добавлен")

    def show_students(self):
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()

            if not rows:
                print("база пуста")
            else:
                for row in rows:
                    print(f"ID: {row[0]}, имя: {row[1]}, возраст: {row[2]}, оценка: {row[3]}")

    def find_student(self):
        name = input("введите имя студента для поиска===>>>")
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                print(f"найден ID: {row[0]}, имя: {row[1]}, возраст: {row[2]}, оценка: {row[3]}")
            else:
                print("студент не найден")

    def delete_student(self):
        name = input("введите имя студента которого хотите удалить===>>>")

        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
            if cursor.fetchone():
                cursor.execute("DELETE FROM students WHERE name = ?", (name,))
                print(f"студент {name} удалён")
            else:
                print("студент не найден")

    def export_to_csv(self):
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, age, grade FROM students")
            rows = cursor.fetchall()

            if not rows:
                print("экспортировать нечего")
                return

            with open(CSV_FILENAME, 'w',encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["name", "age", "grade"])
                writer.writerows(rows)
            print(f"экспортировано в {CSV_FILENAME}")

    def main(self):
        while True:
            print('''
--- БАЗА СТУДЕНТОВ (SQL) ---
1. Добавить студента
2. Показать всех
3. Найти студента
4. Удалить студента
5. Экспорт в CSV
6. Выход
''')

            choice = input("сделайте выбор===>>>")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.show_students()
            elif choice == "3":
                self.find_student()
            elif choice == "4":
                self.delete_student()
            elif choice == "5":
                self.export_to_csv()
            elif choice == "6":
                print("до встречи!")
                break
            else:
                print("неизвестная команда")

student = StudentBase()
student.main()