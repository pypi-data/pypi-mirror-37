# !/bin/env python
# coding: utf-8

__author__ = '@britodfbr'
import re
import os
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
from urllib.error import URLError
from incolumepy.saj_projects.legis import Legis
from incolumepy.utils.files import realfilename




proxies={
    'http': 'http://10.1.101.101:8080',
    'https': 'http://10.1.101.101:8080',
    'ftp': 'http://10.1.101.101:8080',
}


def baixar_camara(url, proxies=proxies, timeout=5):
    try:
        page = requests.get(url, timeout=timeout)
    except:
        page = requests.get(url, proxies=proxies, timeout=timeout)
    soup = BeautifulSoup(page.content, 'html.parser')

    ato = soup.select('[id="content"]')
    result = ato[0]
    return result.prettify()


def limpar_camara(conteudo):
    conteudo = re.sub('\n', '', conteudo)
    # conteudo = re.sub('<br[ /]*>', '</p><p>', conteudo)
    conteudo = re.sub('N\.', 'Nº', conteudo, re.I)
    conteudo = re.sub(' [–-]', ',', conteudo, re.I)
    soup = BeautifulSoup(conteudo, 'html.parser')
    #del soup.html['xmlns:o']
    #for child in soup.head.children:
    #    if isinstance(child, Comment):
    #        child.extract()

    # descarte dos titulos pre-existentes
    tags = []
    #tags.append(soup.select("h2:nth-of-type(1)"))
    #tags.append(soup.select("h3:nth-of-type(1)"))
    #tags.append(soup.select("h4:nth-of-type(1)"))
    tags.append(soup.select("head"))
    for i in tags:
        if i:
            i[0].decompose()


    #remove attr
    tags = []
    tags.append('bgcolor')
    tags.append('align')
    tags.append('style')
    tags.append('width')
    tags.append('valign')
    tags.append('nowrap')
    tags.append('xmlns:o')
    for i in tags:
        container = soup.select('[{}]'.format(i))
        for j in container:
            del j[i]

    # desatachar tags
    tags = []
    tags.append('big')
    tags.append('u')
    tags.append('font')
    tags.append('span')
    tags.append('strong')
    tags.append('center')
    tags.append('fontface')
    tags.append('small')
    tags.append('s')
    # tags.append('div:nth-of-type(3)')
    tags.append('div[class="texto"]')
    tags.append('div[class="textoNorma"]')

    for j in tags:
        container = soup.select(j)
        for i in container:
            i.unwrap()

    # remove classes MS
    tags = []
    tags.append('[class="Prembulo"]')
    tags.append('[class="Dec"]')
    tags.append('[class="Artigo"]')
    tags.append('[class*="MS"]')
    tags.append('[class="Normal0"]')
    for j in tags:
        container = soup.select(j)
        for i in container:
            del i['class']

    # remove tags ou tags com os atributos indicados
    tags = []
    tags.append('[class="Header"]')
    tags.append('[name="generator"]')
    tags.append('[class="tela"]')
    tags.append('style')
    tags.append('[class="alert alert-danger"]')
    tags.append('meta')
    tags.append('[class="vejaTambem"]')
    tags.append('[class="documentFirstHeading"]')
    tags.append('[class="publicacoesTI"]')
    #tags.append('br')
    for j in tags:
        container = soup.select(j)
        for i in container:
            i.decompose()

    #try:
    #    tags = soup.find_all(string=re.compile("decreto", re.I), limit=1)[0].parent
    #    tags.name = 'p'
    #except IndexError as e:
    #    raise ValueError('Ato sem conteudo.')

    return soup.prettify()


def formatar_camara(conteudo):
    elem = Legis()
    conteudo = re.sub('\n', '', conteudo, re.I)
    soup = BeautifulSoup(conteudo, 'html.parser')

    tags = soup.select('div[id="content"]')
    tags[0].name = 'body'
    tags[0]['id'] = 'void'

    soup.body.wrap(soup.new_tag('html'))
    soup.insert(0, elem.doctype())
    soup.html['lang'] = 'pt-br'
    soup.html.insert(0, soup.new_tag('head'))

    soup.head.append(elem.meta(charset='UTF-8'))
    soup.head.append(elem.link_css())

    tags = soup.select("h1:nth-of-type(1)")
    tags[0].name = 'p'
    tags[0]['class'] = 'epigrafe'

    soup.body.insert(0, elem.header())
    #tags = soup.select('[class="ementa"]')
    soup.body.insert(5, elem.nav())
    #print(tags)

    # DOU
    tags = soup.select('[class="rodapeTexto"]')
    #print(tags)
    try:
        tags[0].name = 'p'
        tags[0]['class'] = 'dou'
        meta = soup.select('meta[name="fonte"]')
        meta[0]['content'] = tags[0].text.strip()
    except:
        print(sys.exc_info())

    # Epigrafe
    container = soup.select('[class="epigrafe"]')
    epigrafe = container[0].text

    # Data
    meta = soup.select('meta[name="dataassinatura"]')
    print('"'+epigrafe.split(',')[-1]+'"')
    print('D: ', Legis.date_conv(epigrafe.split(',')[-1]))
    meta[0]['content'] = Legis.date_conv(epigrafe.split(',')[-1])

    # Ano
    meta = soup.select('meta[name="ano"]')
    meta[0]['content'] = epigrafe.split(',')[-1].split()[-1]

    # Numero
    meta = soup.select('meta[name="numero"]')
    try:
        a, b = epigrafe.split(',')[0].split()[-1].split('-')
        num = '{:0>5}{}'.format(''.join([i for i in a if i.isdigit()]), b)
    except:
        num = '{:0>5}'.format(''.join([i for i in epigrafe.split(',')[0].split()[-1] if i.isdigit()]))
    meta[0]['content'] = num


    #tipo
    meta = soup.select('meta[name="tipo"]')
    meta[0]['content'] = epigrafe.split(',')[0].split()[0].lower()


    return soup.prettify()

def gravar_camara(conteudo, path=''):
    soup = BeautifulSoup(conteudo, 'html.parser')

    ano = soup.select('meta[name="ano"]')[0]['content']
    num = soup.select('meta[name="numero"]')[0]['content']
    tipo = soup.select('meta[name="tipo"]')[0]['content']

    print(ano, num)
    with open(realfilename(os.path.join(path, tipo, ano,'D{}.html'.format(num))), 'wb') as file:
        file.write(soup.prettify(encoding='iso8859-1'))

    return True


def run():
   pass

if __name__ == '__main__':
    run()
