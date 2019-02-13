# coding=utf8

import re
title_regex = '.*第\d+节'


def extract_chapter_no(chapter):
    tmp = chapter[3:]
    no = ''
    for c in tmp:
        if c.isdigit():
            no += c
        else:
            break
    return no


def create_chapter_file(fname, lines):
    path = 'charpters/' + fname
    content = '\n'.join(lines)
    with open(path, 'w') as f:
        f.write(content)


lines_of_charpter = []
with open('fendou.txt') as f:
    current_no = 1
    for line in f.readlines():
        clean_line = line.strip()
        if len(clean_line) == 0:
            continue
        lines_of_charpter.append(clean_line)
        if re.match(title_regex, clean_line):
            no = extract_chapter_no(clean_line)
            if int(no) == current_no + 1:
                print(no, current_no)
                fname = '0'+str(current_no) if current_no < 10 else str(current_no)
                create_chapter_file(fname, lines_of_charpter[:-1])
                current_no = int(no)
                lines_of_charpter = []
                lines_of_charpter.append(clean_line)

