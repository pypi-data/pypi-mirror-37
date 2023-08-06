# !/bin/env python
# coding: utf-8
import incolumepy.saj_projects.baixar_camara as camara
import pandas as pd


__author__ = '@britodfbr'
file = '../../data/collection_metadados.csv'

def truncus01():
    df = pd.read_csv(file)
    return df.columns

def truncus02():
    df = pd.read_csv(file)
    df = df.dropna()

    for j, url in enumerate(df['url_texto']):
        print(j, url)
        texto = camara.baixar_camara(url)
        texto = camara.limpar_camara(texto)
        texto = camara.formatar_camara(texto)
        texto = camara.gravar_camara(texto, path='')
        print(texto)


    return df.shape


def run():
    for i in ['truncus{:0>2}'.format(x) for x in range(1, 3)]:
        print(eval(i)())


if __name__ == '__main__':
    run()
