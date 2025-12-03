import subprocess
import time
import sys, os
import datetime


def run_with_restart():
    while True:
        try:
            print(f"[{datetime.datetime.now()}] Запуск asunctgbot.py...")

            process = subprocess.Popen(
                [sys.executable, "asunctgbot.py"],
                stderr=subprocess.PIPE,
                text=True)
            process.wait()
            exit_code = process.returncode
            print(f"[{datetime.datetime.now()}] Скрипт упал (код: {exit_code}). Перезапуск через 10 секунды...")
            time.sleep(10)

        except KeyboardInterrupt:
            print(f"\n[{datetime.datetime.now()}] Остановлено пользователем")
            break

        except Exception as e:
            print(f"[{datetime.datetime.now()}] Ошибка: {e}")
            time.sleep(3)


if __name__ == "__main__":
    run_with_restart()