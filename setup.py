from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "SimpleCrawler",
    version = "1.0.0",
    description = "SimpleCrawler",
    executables = [Executable("crawler/Main.py", base = base)],
    )