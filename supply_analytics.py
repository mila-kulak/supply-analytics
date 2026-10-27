import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

#Додаємо у код можливість передавати CSV як аргумент через 'argparse'
parser = argparse.ArgumentParser(description="Дані про доставки")
parser.add_argument("csv", help="Шлях до CSV")
args = parser.parse_args()
df = pd.read_csv(args.csv)

#Завантажуємо дані через "pandas"
try:
    supplies_table = pd.read_csv(args.csv,
            sep=",",
            decimal=".",
            names=["supplier", "category", "quantity", "price_per_unit", "date"])
except FileNotFoundError:
    raise SystemExit(f"Помилка... Файлу '{args.csv}' не існує")

except PermissionError:
    raise SystemExit(f"Помилка... Немає дозволу на прочитання файлу '{args.csv}'")

except pd.errors.EmptyDataError:
    raise SystemExit(f"Помилка... Файл '{args.csv}' порожній")

except pd.errors.ParserError:
    raise SystemExit(f"Помилка... Файл '{args.csv}' має некоректний CSV формат")


#Обчислюємо через "NumPy": середню ціну всіх препаратів, медіану кількості та стандартне відхилення ціни
prices = np.array(supplies_table["price_per_unit"])
average_price = np.mean(prices)
quantities = np.array(supplies_table["quantity"])
quantity_median = np.median(quantities)
price_deviation = np.std(prices)
# print(f"Average price: {average_price}, Quantity median: {quantity_median}, Price deviation: {price_deviation}")

#Знаходимо постачальника з найбільшим загальним прибутком
# df=pd.DataFrame(supplies_table)
df["total_price"] = df["quantity"]*df["price_per_unit"]
profits_of_supplier = df.groupby("supplier")["total_price"].sum()
supplier_with_the_largest_profits = profits_of_supplier.idxmax()

#Обчислюємо сумарну кількість препаратів за категоріями
medications_by_categories = df.groupby("category")["quantity"].sum()
# print (medications_by_categories)

#Відфільтровуємо всі записи, де кількість менша за 100
low_quantities = df[df["quantity"]<100]
# print(low_quantities)

#Зберігаємо у новий CSV
low_quantities.to_csv("low_supply.csv", index=False)

#Сортуємо дані за 'total_price' у порядку спадання, виводимо три перші рядки
df.sort_values("total_price", ascending=False).head(3)

#Створюємо текстовий звіт
with open("report.txt", "w", encoding="utf-8") as file:
    file.write(f"Середня ціна: {average_price}\n")
    file.write(f"Медіана кількості: {quantity_median}\n")
    file.write(f"Стандартне відхилення ціни: {price_deviation:.2f}\n")
    file.write(f"Постачальник з найбільшим прибутком: {supplier_with_the_largest_profits}\n")
    file.write(f"Назва файлу із дефіцитними поставками: 'low_supply.csv'\n")

# Будуємо графік через 'matplotlib'
medications_by_categories.plot(kind="bar")
plt.title("Кількість препаратів за категоріями")
plt.ylabel("Кількість")
plt.xlabel("Категорії")
plt.tight_layout()
plt.savefig("by_categories.png")
