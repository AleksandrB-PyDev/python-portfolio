import sqlite3
from datetime import datetime

DB_FILENAME = 'expenses.db'

def get_float(prompt):
    while True:
        try: return float(input(prompt))
        except ValueError:
            print("Это не число, попробуйте снова")

class ExpenseTracker:
    def __init__(self):
        with sqlite3.connect(DB_FILENAME) as conn:
            c = conn.cursor()
            c.execute('''
                    CREATE TABLE IF NOT EXISTS expenses(
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        amount REAL,
                        date TEXT
                )
            ''')

    def add_expense(self):
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            category_name = input("введите название категории расхода===>>>")
            value = get_float("введите потраченную сумму===>>>")

            now = datetime.now()
            today = now.strftime("%Y-%m-%d")

            cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category_name, value, today))
        print("расход добавлен в базу данных")

    def show_expenses(self):
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses")
            rows = cursor.fetchall()
            if not rows:
                print("база пуста")
            else:
                for row in rows:
                    print(f"id: {row[0]}, Категория: {row[1]}, Сумма: {row[2]}, Дата: {row[3]}")

    def show_total(self):
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses")
            rows = cursor.fetchall()
            if not rows:
                print("база пуста")
            else:
                total = 0
                for row in rows:
                    total += row[2]
                print(f"потрачено всего: {total}")

    def show_by_category(self):
        category_name = input("введите название категории===>>>")
        with sqlite3.connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses WHERE category = ?", (category_name,))
            rows = cursor.fetchall()
            if not rows:
                print("в категории нет расходов")
            else:
                for row in rows:
                    print(f"id: {row[0]}, сумма: {row[2]}, дата: {row[3]}")

    def main(self):
        while True:
            print('''
--- ТРЕКЕР РАСХОДОВ ---
1.добавить расход
2.показать все расходы
3.показать общую сумму
4.показать расходы по категории
5.выход
''')

            choice = input("сделайте выбор===>>>")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.show_expenses()
            elif choice == "3":
                self.show_total()
            elif choice == "4":
                self.show_by_category()
            elif choice == "5":
                print("до встречи!")
                break
            else:
                print("неизветсная команда")

if __name__ == "__main__":
    exp = ExpenseTracker()
    exp.main()