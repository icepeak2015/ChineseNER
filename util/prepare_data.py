# coding=utf-8

import os
import re
import codecs

def removePostfix(file):
    with codecs.open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        flen = len(lines)-1
        strs = ['.NAM', '.NOM']
        for i in range(flen):
            if '.NAM' in lines[i]:
                lines[i] = lines[i].replace('.NAM', '')
            if '.NOM' in lines[i]:
                lines[i] = lines[i].replace('.NOM', '')

    codecs.open(file, 'w', encoding='utf8').writelines(lines)

if __name__=="__main__":
    removePostfix('weiboNER.conll.train')