import threading
import random
from time import sleep

class Bank:
    def __init__(self):
        self.balance = 0  # Изначальный баланс
        self.lock = threading.Lock()  # Замок для потоков

    # Метод для пополнения средств
    def deposit(self):
        for _ in range(100):
            deposit_amount = random.randint(50, 500)  # Случайная сумма пополнения
            with self.lock:  # Блокировка для безопасного доступа к балансу
                self.balance += deposit_amount
                print(f"Пополнение: {deposit_amount}. Баланс: {self.balance}")

            # Если баланс >= 500 и замок заблокирован, снимаем блокировку
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()

            sleep(0.001)  # Имитация времени пополнения

    # Метод для снятия средств
    def take(self):
        for _ in range(100):
            withdrawal_amount = random.randint(50, 500)  # Случайная сумма снятия
            print(f"Запрос на {withdrawal_amount}")

            with self.lock:  # Блокировка для безопасного доступа к балансу
                if withdrawal_amount <= self.balance:  # Проверка, хватает ли средств
                    self.balance -= withdrawal_amount
                    print(f"Снятие: {withdrawal_amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    # Блокируем поток при недостатке средств
                    self.lock.acquire()

# Создаем объект банка
bk = Bank()

# Создаем два потока для пополнения и снятия средств
th1 = threading.Thread(target=bk.deposit)
th2 = threading.Thread(target=bk.take)

# Запуск потоков
th1.start()
th2.start()

# Ожидание завершения работы потоков
th1.join()
th2.join()

# Вывод итогового баланса
print(f'Итоговый баланс: {bk.balance}')
