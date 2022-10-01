import datetime
import os
from typing import Literal, Dict


class Logger:
    def __init__(
        self,
        name: str,
        filename: str = f"{datetime.datetime.now().date()}-log.log",
        console: bool = False,
    ):
        self.name: str = name
        self.filename: str = f"logs/{name}/{filename}"
        self.console: bool = console
        os.makedirs("logs", exist_ok=True)
        os.makedirs(f"logs/{name}", exist_ok=True)

    LEVEL_COLORS: Dict[str, str] = {
        "debug": "[0;1;34m{}[0m",
        "info": "[0;1;32m{}[0m",
        "warning": "[0;1;33m{}[0m",
        "error": "[0;1;31m{}[0m",
        "critical": "[0;1;31;47m{}[0m",
    }

    def to_file(self, fmt: str) -> None:
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(fmt)

    def format(
        self,
        message: str,
        *,
        level: Literal["debug", "info", "warning", "error", "critical"] = "debug",
    ) -> None:
        fmt: str = f"{datetime.datetime.now().strftime('%d/%m %H:%M:%S')}[{self.name.upper()}] {level.upper()}: {message}\n"
        self.to_file(fmt)
        if self.console:
            type = self.LEVEL_COLORS.get(level, "[0;1;35m{}[0m").format(
                level.upper() + f" {self.name}"
            )
            time = datetime.datetime.utcnow().strftime("%d/%m %H:%M:%S")
            print(f"[{type}] {time} {message}")

    def debug(self, message: str) -> None:
        self.format(message, level="debug")

    def info(
        self,
        message: str,
    ) -> None:
        self.format(message, level="info")

    def warn(
        self,
        message: str,
    ) -> None:
        self.format(message, level="warning")

    def warning(
        self,
        message: str,
    ) -> None:
        self.format(message, level="warning")

    def error(
        self,
        message: str,
    ) -> None:
        self.format(message, level="error")

    def critical(
        self,
        message: str,
    ) -> None:
        self.format(message, level="critical")
