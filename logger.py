from datetime import datetime
from pathlib import Path

# 级别 → 数字，用来比较“该不该输出”
LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}


class Logger:
    def __init__(self, name="app", log_file=None, level="INFO",
                 console=True, file=True):
        self.name = name
        self.level = LEVELS.get(level.upper(), 20)   # 配置写错就按 INFO 处理
        self.log_file = Path(log_file) if log_file else None
        self.console = console
        # 没给路径就不写文件
        self.file = file and self.log_file is not None
        if self.file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, level, msg):
        # 级别不够，直接不输出
        if LEVELS[level] < self.level:
            return
        line = f"{datetime.now():%Y-%m-%d %H:%M:%S} [{level}] {self.name}: {msg}"

        if self.console:
            print(line)

        if self.file:
            try:
                # 'a' = 追加，千万别用 'w'，否则每次启动清空日志
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except OSError as e:
                print(f"[日志写文件失败] {e}")

    def debug(self, msg): self._write("DEBUG", msg)
    def info(self, msg):  self._write("INFO", msg)
    def warn(self, msg):  self._write("WARN", msg)
    def error(self, msg): self._write("ERROR", msg)