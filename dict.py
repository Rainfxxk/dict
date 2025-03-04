import sys
import words
import db
import tui


def getch():
    # get a char from command line
    if sys.platform == 'win32':
        import msvcrt
        return msvcrt.getch().decode()
    else:
        return sys.stdin.read(1).decode()


def show_word(word_info):
    index = 0 
    word = word_info['word']
    pronounce = word_info['pronounce']
    def_num = len(word_info['definitions'])
    while index < def_num: 
        tui.show_word(word_info, def_num, index)
        
        # 读取单个字符输入
        while True:
            input_char = getch()
            if input_char.isdigit():
                index = int(input_char)
                continue
            elif input_char.lower() == 'h':
                if index > 0:
                    index -= 1
                    break
            elif input_char.lower() == 'l':
                if index < def_num - 1:
                    index += 1
                    break
            elif input_char.lower() == 'n':
                tui.clear()
                return
            elif input_char.lower() == 'q':
                exit(0)
                
        tui.clear()


if __name__ == "__main__":
    tui.clear()
    while True:
        # try:
            # 命令行输入
            word = input("Query: ").lower()
            if (len(word) < 1):
                # 输入 q 则退出程序
                continue

            if (word == 'q'):
                break
        
            tui.clear()
            word_info = words.get_word_meaning(word)
            show_word(word_info)
            db.insert_word(word_info)
        # except Exception as e:
        #     print(e)
        #     print("something wrong T^T")
