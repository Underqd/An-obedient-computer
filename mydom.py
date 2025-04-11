import speech_recognition as sr
import os
import paramiko
import time
import subprocess
import psutil
import webbrowser
import winsound  # Это добавил для звуков виндовс


GAME_EXE_PATH = r"C:\uuu\csc\To\GTA.exe"  # Это для ся делал чтоб запускал игру
SCRIPT_PATH = r"C:\работыы/mydom.py"  # Путь к моему файлу

def shutdown_pc():
    try:
        os.system("shutdown /s /t 1")
    except Exception as e:
        print(f"Error shutting down PC: {e}")

def open_game():
    try:
        subprocess.Popen([GAME_EXE_PATH])
        print("Game opened.")
    except FileNotFoundError:
        print(f"Error: Game executable not found at: {GAME_EXE_PATH}")
    except Exception as e:
        print(f"Error opening game: {e}")

def open_code():
    try:
        subprocess.Popen([SCRIPT_PATH])
        print("Script opened.")
    except FileNotFoundError:
        print(f"Error: Script not found at: {SCRIPT_PATH}")
    except Exception as e:
        print(f"Error opening script: {e}")

def close_game():
    GAME_NAME = "Multi Theft Auto.exe"
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == GAME_NAME:
                proc.kill()
                print("Game closed.")
                return
        print("Game not found.")
    except Exception as e:
        print(f"Error closing game: {e}")

def open_youtube():
    try:
        webbrowser.open("https://www.youtube.com")
        print("Opening YouTube.")
    except Exception as e:
        print(f"Error opening YouTube: {e}")

def recognize_speech():
    """Recognizes speech and returns text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
             print("Timeout. No speech detected.")
             return ""
    try:
        command = r.recognize_google(audio, language="ru-RU")
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Не удалось запросить результаты от службы распознавания речи; {e}")
        return ""
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return ""

def play_go_sound():
     """Plays a short sound to signify that Go mode is activated."""
     winsound.Beep(1000, 150)
     
def reboot_router_ssh(hostname, username, password, command="reboot"):
    """
    Перезагружает роутер через SSH.
    """

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, username=username, password=password)

        print(f"Выполнение команды: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        print("Вывод:", output)
        if error:
            print("Ошибка:", error)

        ssh_client.close()
        print("Роутер перезагружается. Подождите...")
        time.sleep(60) # Пауза для перезагрузки (может потребоваться больше времени) (НА ВАШЕ УСМОТРЕНИЕ)

    except paramiko.AuthenticationException:
        print("Ошибка аутентификации. Неверные имя пользователя или пароль.")
    except paramiko.SSHException as e:
        print(f"Ошибка SSH: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def main():
    print("Запущена программа голосового управления. Для начала скажите Вперед")
    go_mode = False
    while True:
        command = recognize_speech()

        if "go" in command and not go_mode:
            print("Обнаружен сбой. Ждем команд...")
            play_go_sound()
            go_mode = True
            continue
        
        if go_mode:
             if "выключи компьютер" in command:
                 print("Выполняю команду выключения")
                 shutdown_pc()
                 go_mode = False
             elif "играть" in command or "запустить игру" in command:
                print("Выполняю команду открытия игры")
                open_game()
                go_mode = False
             elif "скрипт" in command or "запустить скрипт" in command:
                open_code()
                go_mode = False
             elif "закрыть игру" in command:
                print("Выполняю команду закрытия игры")
                close_game()
                go_mode = False
             elif "youtube" in command:
                print("Выполняю команду открытия YouTube")
                open_youtube()
                go_mode = False
             elif "рестарт" in command or "перезагрузи роутер" in command: # Старый код у меня где то была новей версия возможно у вас не будет работать нормально
                 print("Перезагружаю роутер...")
                 router_ip = ""  # Замените на IP-адрес вашего роутера
                 router_username = ""  # Замените на имя пользователя вашего роутера
                 router_password = ""  # Замените на пароль вашего роутера
                 reboot_router_ssh(router_ip, router_username, router_password)
                 go_mode = False
                 
                 
                 # Так же вы можете добавлять свои функции :
                #elif "cvoe" in command:
                #print("Выполняю команду  cvoe")                                             ^
                #cvoe()  нужно сделать функцию " def cvoe()  "  (И что он будет делать дать ему выше |)
                #go_mode = False
                 
                 
             elif "выйти" in command or "стоп" in command:
                print("Завершаю программу")
                break
             elif command:
                print("Неизвестная команда")
                

        time.sleep(1)
        
        
router_ip = ""  # Замените на IP-адрес вашего роутера
router_username = ""  # Замените на имя пользователя вашего роутера
router_password = ""  # Замените на пароль вашего роутера

reboot_router_ssh(router_ip, router_username, router_password)


if __name__ == "__main__":
    main()