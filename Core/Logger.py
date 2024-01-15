from colorama import Fore, Style


class Logger:
    def __init__(self):
        self.__colors = {
            "trace": Fore.WHITE,
            "info": Fore.CYAN,
            "warn": Fore.YELLOW,
            "error": Fore.RED,
        }

    def __log(self, level, tag, message):
        print(f"{Style.RESET_ALL}{Style.BRIGHT}{self.__colors[level]}"
              f"[{level}]: [{tag}] {message}")

    def trace(self, tag, message):
        self.__log("trace", tag, message)

    def info(self, tag, message):
        self.__log("info", tag, message)

    def warn(self, tag, message):
        self.__log("warn", tag, message)

    def error(self, tag, message):
        self.__log("error", tag, message)