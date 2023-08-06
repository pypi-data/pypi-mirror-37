# !/bin/env python
# coding: utf-8

import os
import time
import logging
import pandas as pd
from os.path import basename, abspath, getsize, join
__author__ = '@britodfbr'

# create logger
# levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
filelog = basename(__file__).replace('py', 'log')
str_format = '%(asctime)s;%(levelname)-8s;%(name)s;%(module)s;%(funcName)s;%(message)s'
logging.basicConfig(filename=filelog, level=logging.DEBUG, format=str_format, datefmt='%Y/%m/%d %H:%M:%S %z')

console = logging.StreamHandler()
formatter = logging.Formatter(str_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger()


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def fs_report(path='./'):
    regs = []
    epoch = int(time.time())
    logger.debug(f'Init logfile epoch {epoch}')
    files = [join(p, file) for p, _, files in os.walk(abspath(path)) for file in files]

    for i, item in enumerate(files):
        reg = {}
        # print(i, item)
        # print(item.encode('iso8859-1'))

        # encode transforma em Bytes codes
        item = item.encode('utf-8', 'surrogateescape')
        # transforma em latin-1
        reg['path'] = str(item, 'iso8859-1')
        reg['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime(os.path.getctime(item))).strip()
        reg['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime(os.path.getmtime(item))).strip()
        reg['atime'] = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime(os.path.getatime(item))).strip()
        reg['size'] = getsize(item)
        logger.info(f'#{i:0>6}:{reg}')
        regs.append(reg)

    # print(regs)
    df = pd.DataFrame(regs)
    df = df.sort_values(['mtime', 'path'])
    df['path'] = df['path'].str.replace('/home/brito/Documentos/castelo_internet/', '')

    # print(df.head())
    outputfile1 = os.path.abspath(os.path.join(os.getcwd(), f'../../relatorios/file_systems/files_{epoch}.csv'))
    outputfile2 = os.path.abspath(os.path.join(os.getcwd(), f'relatorios/file_systems/files_{epoch}.csv'))
    cvsfile = ''
    try:
        cvsfile = outputfile1
        df.to_csv(cvsfile, index=False)
    except FileNotFoundError:
        cvsfile = outputfile2
        os.makedirs(os.path.dirname(cvsfile), 0o777, True)
        df.to_csv(cvsfile, index=False)
    logger.debug(f'write {abspath(cvsfile)} with {getsize(cvsfile)}k')
    return True


def run(path=None):
    path = '/home/brito/Documentos/castelo_internet/CCIVIL_03/' if not path else path
    try:
        fs_report(path)
    except KeyError:
        negativa = 'n no not não false'.split()
        msg = f"{BColors.FAIL}Falha: \"{path}\" indisponível.{BColors.ENDC}"
        logger.error(msg)
        answer = input(f'{msg}\n{BColors.WARNING}Deseja continuar em modo teste?{BColors.ENDC}')
        if answer.lower() in negativa:
            logger.info('Execução terminada.')
            exit(0)
        answer2 = input("Informe o caminho do diretório: ")
        if os.path.isdir(answer2):
            path = os.path.abspath(answer2)
        else:
            path = './'
        logger.info('Inicio modo teste, em {path}')
        fs_report(path)


if __name__ == '__main__':
    # print(os.path.isdir('../../relatorios/file_systems/'))
    run()
