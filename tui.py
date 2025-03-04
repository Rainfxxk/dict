import sys

# ANSI颜色代码
BLUE = '\x1b[94m'
RED = '\033[31m'
YELLOW = '\033[33m'
GREEN = '\033[32m'
RESET = '\033[0m'
CLEAR_SCREEN = '\033[H\033[J'


def clear():
    print(CLEAR_SCREEN, end='')


def show_word(word_info, def_num, index):
    word = word_info['word']
    pronounce = word_info['pronounce']
    sense_block = word_info['definitions'][index]
    part_of_speech = sense_block['part_of_speech']

    output = f'''{word} {GREEN}{pronounce}{RESET}
{BLUE}<{part_of_speech}>{RESET}
{RED}{sense_block['english_def']}{RESET}
{YELLOW}{sense_block['chinese_translation']}{RESET}
'''
        
    for example in sense_block['examples']:
        output += f'''{RED}- {example['sentence']}{RESET}
{YELLOW}  {example['translation']}{RESET}
'''

    output += f'[{index + 1}/{def_num}]'
    print(output)
