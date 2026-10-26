import prompt

HELP_TEXT = (
    "\n<command> exit - выйти из программы\n"
    "<command> help - справочная информация"
)


def print_help():
    print(HELP_TEXT)


def welcome():
    print("Первая попытка запустить проект!")
    print("\n***")
    print_help()

    while True:
        command = prompt.string("Введите команду: ").strip()

        match command:
            case "exit":
                break
            case "help":
                print_help()
            case _:
                print(f"Неизвестная команда: {command}. Введите help.")
