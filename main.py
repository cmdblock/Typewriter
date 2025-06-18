import argparse
import sys
import threading  # 导入threading模块
import time

import keyboard
import pyautogui


def press_enter_back_tab(duration: int, tab_nums: int) -> None:
    """按下 tab 键"""
    time.sleep(duration / 1000)
    pyautogui.press("esc")  # 回到 normal 模式
    pyautogui.press("esc")
    time.sleep(duration / 1000)
    pyautogui.press("0")  # 移动到当前行的开头
    time.sleep(duration / 1000)
    pyautogui.press("i")  # 进入插入模式
    time.sleep(duration / 1000)

    for i in range(tab_nums):
        time.sleep(duration / 1000)
        pyautogui.press("tab")


def on_hotkey(code_lines: list[str], duration: int, spaces: list[int]):
    """当按下 Alt + F2 时触发"""
    time.sleep(2)  # 给用户时间切换到目标窗口
    pyautogui.press("i")  # 进入插入模式
    line_nums = len(code_lines)

    for i in range(line_nums):
        char_nums = len(code_lines[i])
        if i > 0:
            tab_nums = spaces[i] // 4
            press_enter_back_tab(duration, tab_nums)
        for j in range(spaces[i], char_nums):
            if j == char_nums - 1:
                time.sleep(duration / 1000)
                pyautogui.press("esc")
                pyautogui.press("esc")
                time.sleep(duration / 1000)
                pyautogui.press("o")
            else:
                time.sleep(duration / 1000)
                pyautogui.write(code_lines[i][j])


def exit_program():
    """退出程序"""
    print("打印完成，程序退出")
    sys.exit(0)


def read_file(filename: str) -> list[str]:
    """读取文件"""
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()


def space_nums(code_lines: list[str]) -> list[int]:
    """获取每行代码的空格数"""
    spaces = []
    for line in code_lines:
        count = 0
        for char in line:
            if char == " ":
                count += 1
            else:
                break
        spaces.append(count)
    return spaces


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="文件名字")
    args = parser.parse_args()

    filename = args.file
    shortcut = "alt+f2"
    code = read_file(filename)
    spaces = space_nums(code)

    print("程序已启动，按 " + shortcut + " 键, 2 秒钟后开始打印", flush=True)

    done = threading.Event()  # 创建事件对象

    def on_hotkey_wrapper():
        """包装函数，用于触发事件"""
        on_hotkey(code, 100, spaces)
        done.set()  # 任务完成，设置事件

    keyboard.add_hotkey(shortcut, on_hotkey_wrapper)
    done.wait()  # 等待事件被触发
    exit_program()  # 退出程序


