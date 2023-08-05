import MeCab
import subprocess


def get_dic_path():
    return str(subprocess.check_output('echo `mecab-config --dicdir`"/mecab-ipadic-neologd"', shell=True))[2:-3]


def get_mecab_tagger(option='-Owakati', d=None):
    if not d:
        d = get_dic_path()
    m = MeCab.Tagger(f'{option} -d {d}')
    # https://qiita.com/kasajei/items/0805b433f363f1dba785
    m.parse("")
    return m
