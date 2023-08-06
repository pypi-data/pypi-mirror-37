#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "@britodfbr"
__copyright__ = "Copyright 2007, incolume.com.br"
__credits__ = ["Ricardo Brito do Nascimento"]
__license__ = "GPL"
__version__ = "1.0a"
__maintainer__ = "@britodfbr"
__email__ = "contato@incolume.com.br"
__status__ = "Production"


import re
import os
import sys
import locale
import platform
import json
import numpy as np
import pandas as pd
import logging
from inspect import stack
from bs4 import BeautifulSoup, Doctype, Comment, CData
from bs4.element import NavigableString, Tag
from datetime import datetime as dt
from os.path import abspath, join, isfile
from unicodedata import normalize
from selenium import webdriver
from time import sleep
from random import randint
from functools import lru_cache
sys.path.append(os.path.abspath(os.path.join('..', '..', '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
# print(sys.path)
try:
    from incolumepy.saj_projects import clean
except ModuleNotFoundError:
    from src.incolumepy.saj_projects import clean


def includeDelOnLineThrough(conteudo: str) -> str:
    ''' Inclui <del> onde houber style com "line-through" '''
    soup = BeautifulSoup(conteudo, 'html.parser')
    through = soup.find_all(style=re.compile("line-through"))
    for i in through:
        i.wrap(soup.new_tag('del'))
    return clean.one_line(soup.prettify())

def replaceLineThrough2Del(conteudo: str)-> str:
    ''' Substituir line-through '''
    soup = BeautifulSoup(conteudo, 'html.parser')
    through = soup.find_all(style=re.compile("line-through"))
    for i in through:
        logging.debug(f'{stack()[3][0]}:{i!s}')
        change_parent(soup=i, tag_name='span', new_tag_name='del')
    return clean.one_line(soup.prettify())

def locate_parent(**kwargs):
    '''
    :param kwargs: soup and tag_name both strings
    :return: bs4 with element finded
    '''
    # assert isinstance(kwargs.get('soup'), BeautifulSoup) \
    #        or isinstance(kwargs.get('soup'), Tag) \
    #        or isinstance(kwargs.get('soup'), NavigableString), "Not instance bs4"

    if kwargs.get('soup').name == kwargs.get('tag_name'):
        return kwargs.get('soup')
    return locate_parent(soup=kwargs.get('soup').parent,
                  tag_name=kwargs.get('tag_name'))

def change_parent(**kwargs):
    ''''''
    # assert isinstance(kwargs.get('soup'), BeautifulSoup) \
    #        or isinstance(kwargs.get('soup'), Tag) \
    #        or isinstance(kwargs.get('soup'), NavigableString), "Not instance bs4"
    try:
        # print(kwargs.get('soup'))
        kwargs.get('soup').name
    except AttributeError as e:
        #raise AttributeError('Object "{}" not instance bs4, Error: {}'.format(kwargs.get('soup'), e))
        logging.warning(F"{kwargs.get('soup')}: {e}")
        return None

    if kwargs.get('soup').name == kwargs.get('tag_name'):
        kwargs.get('soup').name = kwargs.get('new_tag_name')
        return kwargs.get('soup')
    return change_parent(soup=kwargs.get('soup').parent,
                  tag_name=kwargs.get('tag_name'),
                  new_tag_name=kwargs.get('new_tag_name'))


def extract_soup_set_tag_class(soup, nova_tag='p', class_value='ementa', modo_texto=True):
    assert isinstance(soup, BeautifulSoup) \
           or isinstance(soup, Tag) \
           or isinstance(soup, NavigableString), "Not instance bs4"
    nsoup = BeautifulSoup('', 'html.parser')
    # print('>', nsoup)
    tag = nsoup.new_tag(nova_tag, **{'class': class_value})
    # print('>', soup.text.strip())
    if modo_texto:
        tag.string = soup.text.strip()
    else:
        tag.append(soup)
    # print('>', tag)
    return tag


def check_parent(**kwargs):
    '''
    :param kwargs: soup, tag_name, key, value
    :return: soup with setted <tag_name key="value" />
    '''
    assert isinstance(kwargs.get('soup'), BeautifulSoup) \
        or isinstance(kwargs.get('soup'), Tag) \
        or isinstance(kwargs.get('soup'), NavigableString), "Not instance bs4"

    if kwargs.get('soup').name == kwargs.get('tag_name'):
        kwargs.get('soup')[kwargs.get('key')] = kwargs.get('value')
        return kwargs.get('soup')
    return check_parent(soup=kwargs.get('soup').parent,
                 tag_name=kwargs.get('tag_name'),
                 key=kwargs.get('key'), value=kwargs.get('value'))


def presidente_identify(soup, json_file, content=''):
    '''Identifica o presidente no soup recebido'''
    if not soup and content:
        soup = BeautifulSoup(content, 'html5lib')

    with open(abspath(json_file)) as jf:
        presidentes = json.load(jf)


    for item in presidentes['presidentes'].values():
        #print(item)
        for i in [x for x in item['nome'].split() if len(x) > 2]:
            #print(i)
            result = soup.find_all(string=re.compile(i, re.I), limit=10)
            if result:
                p = result[0].replace('.', '')
                #print(p)
                if set([x.lower() for x in p.split() if len(x)>2]).issubset(set(item['nome'].lower().split())):
                    return result
    return False


def governo_ano(json_file, ano=dt.today().strftime('%Y')):
    '''recebe o ano do governo e retorna str com o nome do presidente'''
    # print(ano)
    with open(os.path.abspath(json_file)) as jf:
        presidentes = json.load(jf)

    # print(presidentes)
    for item in presidentes['presidentes'].values():
        # print(item['imandato'], item['fmandato'])
        if dt.strptime(item['imandato'], "%d de %B de %Y") < dt.strptime(ano, "%Y") < dt.strptime(item['fmandato'], "%d de %B de %Y"):
            #print(item['nome'])
            return item['nome'].upper()

    return False


def presidente_em_exercicio(soup, json_file, content=''):
    '''identifica o nome do presidente em exercício'''
    if not soup and content:
        soup = BeautifulSoup(content, 'html5lib')

    with open(abspath(json_file)) as jf:
        presidentes = json.load(jf)

    vices =[]

    for item in presidentes['presidentes'].values():
        # print(item)
        for i in [x for x in item['nome'].split() if len(x) > 2]:
            # print(i)
            result = soup.find_all(string=re.compile(i, re.I), limit=10)
            if result:
                p = result[0].replace('.', '')
                # print(p)
                if set([x.lower() for x in p.split() if len(x) > 2]).issubset(set(item['nome'].lower().split())):
                    return result
        if isinstance(item['vice'], str):
            vices.append(item['vice'])
        elif isinstance(item['vice'], list):
            vices += item['vice']

    for vice in vices:
        for i in [x for x in vice.split() if len(x) > 2]:
                result = soup.find_all(string=re.compile(i, re.I), limit=10)
                if result:
                    p = result[0].replace('.', '')
                    if set([x.lower() for x in p.split() if len(x) > 2]).issubset(set(vice.lower().split())):
                        return result
    return False

def loc_president_exerc(soup, presidentes_file=None):
    '''

    :param soup: Objeto bs4
    :param presidentes_file: base com presidentes
    :return: str
    '''
    if presidentes_file:
        presidentes_file = abspath(presidentes_file)
    else:
        presidentes_file = abspath(join('data', 'base_presidente_exercicio.csv'))
    assert isinstance(soup, NavigableString) \
           or isinstance(soup, Tag) \
           or isinstance(soup, BeautifulSoup), '"soup" deverá ser instancia de bs4'
    assert os.path.isfile(presidentes_file), "Arquivo {} indisponível".format(presidentes_file)

    df = pd.read_csv(presidentes_file)
    for item in df.nome:
        print(type(item))
        # print(remover_acentos(item))
    return []


def loc_presidente_exercicio(soup, presidentes_file=abspath(join('data', 'presidente_exercicio.csv'))):
    '''

    :param soup:
    :param presidentes_file:
    :return:
    '''
    # logger.debug('Inicio de {}'.format(stack()[0][3]))
    presidentes_file = abspath(presidentes_file)
    assert isfile(presidentes_file), "Arquivo {} não disponível.".format(presidentes_file)
    assert isinstance(soup, BeautifulSoup), '"soup" deverá ser instancia de bs4.BeautifulSoup'
    df = pd.read_csv(presidentes_file)

    sf0 = pd.concat([df.nome.str.strip().dropna(), df.vice.str.strip().dropna()]).str.upper()
    sf = sf0[~sf0.str.contains('NONE')]
    #for i, j in enumerate(sf):
    #    print(i, j)

    result = pd.Series(np.sort(sf.str.strip().unique()))
    #for i, j in enumerate(result):
    #    print(i, j)
    munus3 = lambda s: normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    for i, presidente in enumerate(result):
        # logger.info('Presidente em exercício: #{:4} {}'.format(i, presidente))
        for j in [x for x in presidente.split() if len(x)>3]:
            # print(j)
            queries = soup.find_all(string=re.compile(j, re.I), limit=1)
            if queries:
                # logger.debug(queries)
                # logger.info('>> Conteúdo de queries: {}'.format(queries[-1].strip()))
                # logger.warning('>> {}'.format(set(queries[-1].strip().upper().split())))
                if set(
                        [munus3(x).upper() for x in queries[-1].strip().replace('.','').split()]
                       ).issubset([munus3(x) for x in presidente.split()]):
                    # logger.info('Presidente localizado: {}'.format(queries[-1].strip()))
                    return queries

    # logger.info('Presidente não localizado')
    # logger.debug('Finalização de {}'.format(stack()[0][3]))
    return []

@lru_cache(maxsize=2000)
def loc_ministro(soup, referenda='data/referendas.csv'):
    '''
    Localiza o ministro pelo nome dentro do soup fornecido.
    :param soup: Objeto SOUP
    :param referenda: lista com o nome de ministros
    :return: Lista com todos os ministros identificados no Ato
    '''

    assert isinstance(soup, BeautifulSoup) \
        or isinstance(soup, Tag) \
        or isinstance(soup, NavigableString), 'Not is instance bs4'

    # logger.debug('Inicio de {}'.format(stack()[0][3]))
    dataframe = pd.read_csv(abspath(referenda), encoding='iso8859-1',
                            names=['sigla', 'orgao', 'titular', 'interino', 'posse', 'afastamento'], header=0)
    sf = pd.concat([dataframe.titular.str.strip().dropna(), dataframe.interino.str.strip().dropna()])

    sf = sf[~sf.str.contains('\*|um dos', regex=True, case=False)]
    munus1 = lambda s: re.sub('\)', '', string=s).strip()
    munus2 = lambda s: s.split('(')[-1]
    munus3 = lambda s: normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    referenda = set()
    df = pd.DataFrame(sf)
    df['1'] = sf.apply(munus1).apply(munus2).apply(munus3)
    df.columns = ["old", "new"]
    result = pd.Series(np.sort(df.new.str.strip().unique()))

    for i, ministro in enumerate(result):
        # logger.info('Ministro #{:4}: {}'.format(i, ministro))
        for j in [x for x in ministro.split() if len(x)>3]:
            result = soup.find_all(string=re.compile(j, re.I), limit=20)
            if result:
                # logger.debug(result)
                for nome in result:
                    # logger.info('>> Conteúdo de Result: {}'.format(nome))
                    if set([munus3(x).upper() for x in
                            nome.replace('.','').split()]).issubset([x for x in ministro.split()]):
                        referenda.add(nome.strip())
    if referenda:
        # logger.debug('Ministro Localizado: {}'.format(referenda))
        # logger.debug('Finalização de {}'.format(stack()[0][3]))
        return referenda

    # logger.warning('Ministro não encontrado.')
    # logger.debug('Finalização de {}'.format(stack()[0][3]))
    return False


def vice_identify(json_file, ano=dt.today().strftime('%Y')):
    '''recebe o ano do governo e retorna str com o nome do vice-presidente'''
    ano = str(ano)
    # print(ano)
    if platform.system() == 'Linux':
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    else:
        locale.setlocale(locale.LC_ALL, 'pt_BR')

    with open(abspath(json_file)) as jf:
        presidentes = json.load(jf)
    try:
        # print(presidentes)
        for item in presidentes['presidentes'].values():
            # print(item['imandato'], item['fmandato'])
            if dt.strptime(item['imandato'], "%d de %B de %Y") < dt.strptime(ano, "%Y") < dt.strptime(item['fmandato'],
                "%d de %B de %Y"):
                print(f"presidente: {item['nome']}\nvice: {item['vice']}")
                return item['vice'].upper().strip()
    except (NameError, AttributeError):
       return []


def save_html_file(conteudo, filename, encoding='iso8859-1'):
    assert isinstance(conteudo, str), '"conteudo" deve ser um código HTML do tipo "str"'
    if '~' in filename:
        filename = os.path.join(os.path.join(os.path.commonpath(os.get_exec_path()), *filename.split(os.sep)))
    else:
        filename = os.path.abspath(os.path.join(os.path.abspath(os.sep), *filename.split(os.sep)))
    soup = BeautifulSoup(conteudo, 'html5lib')
    output_path = os.path.dirname(filename)
    logging.debug(f'Verificado "{os.path.dirname(filename)}"')
    os.makedirs(output_path, 0o777, True)
    with open(filename, 'wb') as file_out:
        file_out.write(soup.prettify(encoding=encoding))
    logging.debug(F'Arquivo "{filename}" gravado.')
    return True

def get_conteudo(filename=None, url=None, encoding='iso8859-1'):
    assert filename or url, "filename or url are required"
    if filename:
        return get_conteudo_file(filename, encoding)
    return get_conteudo_url(url)


def get_conteudo_file(filename: str, encoding: str="iso8859-1") -> str:
    if '~' in filename:
        filename = os.path.abspath(os.path.join(os.path.commonpath(os.get_exec_path()),
                                            *os.path.expanduser(filename).split(os.sep)))
    else:
        filename = os.path.abspath(os.path.join(*filename.split(os.sep)))
    assert os.path.isfile(filename), "Arquivo '{}' indisponível".format(filename)
    with open(filename, encoding=encoding) as f:
        logging.debug('filename: "{}" readed'.format(f.name))
        return f.read()


def get_conteudo_url(url: str) -> str:
    navegador = ''
    try:
        # firefoxbin = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'drivers', 'geckodriver'))
        firefoxbin = os.path.abspath(os.path.join(os.path.dirname(__file__), 'drivers', 'geckodriver'))
        assert os.path.isfile(firefoxbin), "Driver \"{}\" não disponível.".format(firefoxbin)
        navegador = webdriver.Firefox(executable_path=firefoxbin)
        navegador.get(url)
    except NameError:
        raise
    else:
        s = randint(3, 9)
        logging.debug('sleep({})'.format(s))
        sleep(s)
        logging.debug(navegador.title)
        conteudo = navegador.page_source

        # Retorno do conteudo do arquivo
        return conteudo
    finally:
        navegador.close()


def definir_titulos(codigo: str, titulos: list=[], tag: str='p', nova_tag: str='h4') -> str:
    ''' Definir titulos '''
    # Titulos nível 4
    fixos = [
        'PREÂMBULO',
        'TÍTULO\s[xivcm]+',
        'CAPÍTULO\s[xivcm]+',
        'Seção\s[xivcm]+',
        'Subseção\s[xivcm]+',
        'SECÇÃO\s[xivcm]+',
        'SUBSECÇÃO\s[xivcm]+',
        'livro\s*[xivcm]*'
    ]
    if not titulos:
        titulos += fixos
    titulos = set([x.strip().lower() for x in titulos])
    # logging.debug(titulos)
    soup = BeautifulSoup(codigo, 'html.parser')
    for titulo in titulos:
        container = soup.find_all(string=re.compile('^\s+{}\s+$'.format(titulo), re.I))
        for item in container:
            logging.debug('{} {} ({} -> {})'.format(type(item), item.strip(), tag, nova_tag))
            change_parent(soup=item, tag_name=tag, new_tag_name=nova_tag)
    return str(soup)


class Legis:
    ''' Classe Legis '''

    def __init__(self, **kwargs):
        self.soup = None
        self.file = None
        self.urls = []
        self.date = None
        for item, value in kwargs.items():
            self.__dict__[item] = value

    @staticmethod
    def definir_titulos(soup: any, titulos: list=[], tag: str='p', nova_tag: str='h4') -> None:
        ''' Definir titulos '''
        # Titulos nível 4
        fixos = [
            'PREÂMBULO',
            'TÍTULO\s[xivcm]+',
            'CAPÍTULO\s[xivcm]+',
            'Seção\s[xivcm]+',
            'Subseção\s[xivcm]+',
            'SECÇÃO\s[xivcm]+',
            'SUBSECÇÃO\s[xivcm]+',
            'Livro\s?[xivcm]*'
        ]
        titulos += fixos
        #assert isinstance(soup, BeautifulSoup), "Não é BeautifulSoup"

        # logger.debug(titulos)
        for titulo in titulos:
            # logger.debug(titulo)
            print(titulo)
            container = soup.find_all(string=re.compile('^\s+{}\s+$'.format(titulo), re.I))
            for item in container:
                print(item)
                soup = BeautifulSoup(change_parent(soup=item, tag_name=tag, new_tag_name=nova_tag),
                                     'html.parser')

    @staticmethod
    def replace_tag(soup, tag_name, new_tag_name):
        l = soup.find_all(tag_name)
        for item in l:
            change_parent(soup=item, tag_name=tag_name, new_tag_name=new_tag_name)

    @staticmethod
    def loc_dou(soup):
        regex = "Este\s+texto\s+não\s+substitui\s+o\s+publicado\s+n[ao]\s+(D.O.U.|DOU|CLBR)(\.,)?"
        tags = soup.find_all(string=re.compile(regex, re.I))
        try:
            check_parent(soup=tags[0], tag_name='p', key='class', value='dou')
        except IndexError as e:
            print(e)

    @staticmethod
    def loc_data_assinatura(soup):
        '''Data de assinatura (DOU)'''
        # regex = r"(Rio de Janeiro|Brasília|senado*)(.+(República|Independência)){1,2}(\.,)?\w+"
        regex = r"(Rio de Janeiro|Brasília|senado*)(.*)(Independência|República){1,2}(.*)"
        tags = soup.find_all(string=re.compile(regex, re.I))
        # logger.info(f'Data de assinatura (DOU): {tags}')
        try:
            check_parent(soup=tags[0], tag_name='p', key='class', value='data')
        except IndexError as e:
            # logger.warning(f'Data de publicação DOU não identificada: {e}')
            print(e)

    @staticmethod
    def loc_epigrafe(soup):
        '''Localiza ementa e define p[class="epigrafe"]'''

        # assert isinstance(soup, BeautifulSoup) \
        #        or isinstance(soup, Tag) \
        #        or isinstance(soup, NavigableString), 'Not is instance bs4'
        # regex = r"(DECRETO-LEI|DECRETO|LEI)\s*n\w{1}\s*(\d\.?)+,?\s*\w{,2}\s*(\d{1,2}\w?)\s*\w{,2}\s*\w+\s*\w{,2}\s*\d{4}\.?"
        regex = r"(LEI|DECRETO-LEI|DECRETO)\s+N\s+\w\s+(\d\.?)+,?  DE  \d{1,2}  DE  \w{4,8}  DE  \d{4}."
        tags = soup.find_all(string=re.compile(regex, re.I), limit=1)
        print('tags', tags)
        check_parent(
            soup=tags[0],
            tag_name='p',
            key='class',
            value='epigrafe'
        )
        return True

    @staticmethod
    def link_css(**kwargs) -> BeautifulSoup:
        '''

        :param kwargs: url
        :return: soup with tag link of type css
        '''
        urls=["http://www.planalto.gov.br/ccivil_03/css/legis_3.css",
              "https://www.planalto.gov.br/ccivil_03/css/legis_3.css"]
        # urls.append('../../../css/legis_3.css')

        if 'url' in kwargs:
            urls.append(kwargs['url'])

        soup = BeautifulSoup('', 'html.parser')
        for item in urls:
            soup.append(soup.new_tag('link', type="text/css", rel="stylesheet", href=item))
        return soup

    @staticmethod
    def charset(**kwargs) -> BeautifulSoup:
        ''''''
        soup = BeautifulSoup('', 'lxml')
        tag = soup.new_tag('meta')
        tag2 = soup.new_tag('meta')
        tag3 = soup.new_tag('meta')
        try:
            tag['content'] = 'text/html; charset={}'.format(kwargs['charset'])
            tag2['charset'] = kwargs['charset']
        except:
            tag['content'] = 'text/html; charset=UTF-8'
            tag2['charset'] = 'UTF-8'
        finally:
            tag['http-equiv'] = "Content-Type"
            tag3['http-equiv'] = "Content-Language"
            tag3['content'] = "pt-br"
            soup.append(tag3)
            soup.append(tag)
            soup.append(tag2)

        return soup

    @staticmethod
    def meta(**kwargs):
        itens = {'numero': None, 'tipo': 'decreto', 'ano': dt.today().strftime('%Y'),
            'situacao': "vigente ou revogado", 'origem': 'Poder Executivo', 'chefe_de_governo': '',
            'referenda': '','correlacao': '', 'veto': '', 'dataassinatura': '',"generator_user": "@britodfbr",
            'publisher': 'Centro de Estudos Jurídicos da Presidência da República',
            "Copyright": 'PORTARIA Nº 1.492 DE 5/10/2011. http://www.planalto.gov.br/ccivil_03/Portaria/P1492-11-ccivil.htm',
            'fonte': '', 'presidente_em_exercicio': '', 'vice_presidente': '',
            'revised': dt.today().strftime('%Y-%m-%d %X %z'),
            'description': 'Atos Normativos Federais do Governo Brasileiro',
            'keywords':'', 'robots': 'index, nofollow', 'googlebot': 'index, follow',
            'generator': 'Centro de Estudos Juridicos (CEJ/SAJ/CC/PR)',
            'reviewer': ''
        }
        soup = BeautifulSoup('', 'html.parser')

        for key, value in itens.items():
            tag = soup.new_tag('meta')
            tag['content'] = value
            tag['name'] = key
            soup.append(tag)

        return soup

    @staticmethod
    def nav(min_li: int=5):
        '''
        <nav>
        <ul>
        <li class="fixo">
           <a class="show-action" href="#">Texto completo</a>
           <a class="hide-action" href="#view">Texto original</a>
        </li>
        <li class="fixo"><a class="textoimpressao" href="#textoimpressao">Texto para impressão</a></li>
        <li class="fixo"><a href="#">Vide Recurso extraordinário nº 522897</a></li>
        <li  class="fixo"> </li>
        <li  class="fixo"> </li>
        <li  class="fixo"> </li>
        <li class="fixo">
            <label for="something" class="abrir"> Ver mais.. </label>
        </li>
        <li>
            <label for="something"> Ocultar </label>
        </li>
        </ul>
        </nav>
        :return:
        '''

        soup = BeautifulSoup('', 'lxml')
        soup.append(soup.new_tag('nav'))
        soup.nav.append(soup.new_tag('ul'))
        soup.nav.ul.append(soup.new_tag('input', **{'type': "checkbox", 'id':"something"}))

        a = soup.new_tag('a', **{'href': "#view", 'class': "hide-action"})
        a.string = 'Texto compilado'


        a1 = soup.new_tag('a', **{'href': "#", 'class': "show-action"})
        a1.string = 'Texto original'


        li = soup.new_tag('li', **{'class': 'fixo'})
        li.append(a)
        li.append(a1)
        soup.nav.ul.append(li)

        a2 = soup.new_tag('a', **{'href': "#textoimpressao", 'class': "textoimpressao"})
        a2.string = 'Texto para impressão'
        li1 = soup.new_tag('li', **{'class': 'fixo'})
        li1.append(a2)
        soup.nav.ul.append(li1)

        label = soup.new_tag('label', **{'for': "something", 'class': "abrir"})
        label.string = 'Ver mais..'

        label1 = soup.new_tag('label', **{'for': "something"})
        label1.string = 'Ocultar'

        li2 = soup.new_tag('li', **{'class': 'fixo last'})
        li2.append(label)

        li3 = soup.new_tag('li', **{'class': 'last'})
        li3.append(label1)

        soup.nav.ul.append(li2)
        soup.nav.ul.append(li3)

        for i in range(min_li - 2):
            soup.nav.ul.append(soup.new_tag('li', **{'class': 'fixo'}))

        return soup


    @staticmethod
    def baseurl(**kwargs):
        soup = BeautifulSoup('', 'lxml')
        if 'target' not in kwargs:
            kwargs['target'] = '_self'
        if 'href' not in kwargs:
            raise ValueError('href nao definido')
        soup.append(soup.new_tag('base', target=kwargs['target'], href=kwargs['href']))
        return soup

    @staticmethod
    def header(**kwargs):
        '''  <header>
        <h1>
        Presidência da República
        </h1>
        <h2>
        Casa Civil
        </h2>
        <h3>
        Subchefia para Assuntos Jurídicos
        </h3>
        </header>'''
        if not kwargs:
            kwargs['h1'] = 'Presidência da República'
            kwargs['h2'] = 'Casa Civil'
            kwargs['h3'] = 'Subchefia para Assuntos Jurídicos'

        soup = BeautifulSoup('', 'lxml')
        soup.append(soup.new_tag('header'))
        soup.header.append(soup.new_tag('h1'))
        soup.header.append(soup.new_tag('h2'))
        soup.header.append(soup.new_tag('h3'))
        soup.header.h1.string = kwargs['h1']
        soup.header.h2.string = kwargs['h2']
        soup.header.h3.string = kwargs['h3']
        return soup

    @staticmethod
    def doctype(text='', default='html5'):
        DTD={'html5':'html',
            'html_401s':'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"',
            'html_401t': 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"',
            'html_401f':'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"',
            'xhtml_11': 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"',
            'xhtml_10f': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"',
            'xhtml_10t': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"',
            'xhtml_10s': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"'
             }
        if not text:
            text = DTD[default]
        tag = Doctype(text)
        return tag

    @staticmethod
    def comment(text):
        tag = Comment(text)
        return tag

    @staticmethod
    def dou(text=None):
        soup = BeautifulSoup('', 'lxml')
        tag = soup.new_tag('p', **{'class': "dou"})
        tag.string = 'Este texto não substitui o publicado no D.O.U.'
        if text:
            tag['string'] = text
        return tag

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if value:
            self._file = os.path.abspath(value)

    def get_soup_from_file(self, parser_index=0):
        parser = ["html.parser", 'lxml', 'lxml-xml', 'xml', 'html5lib']
        if not self._file:
            raise ValueError('self.file not defined')
        try:
            f = open(self._file).read()
        except:
            f = open(self._file, encoding='iso8859-1').read()

        self.soup = BeautifulSoup(f, parser[parser_index])
        return self.soup


    def replace_brastra(self, img=None, index=0):
        img_l=['http://www.planalto.gov.br/ccivil_03/img/Brastra.gif',
             'http://www.planalto.gov.br/ccivil_03/img/Brastra.png',
             'http://www.planalto.gov.br/ccivil_03/img/Brastra01.png',
             'http://www.planalto.gov.br/ccivil_03/img/brasaorep.png'
             ]
        logo = self.soup.select('img[src*="Brastra"]')
        if img:
            logo[0]['src'] = img
        else:
            logo[0]['src'] = img_l[index]
        return True, logo

    @classmethod
    def date_conv(cls, date):
        ''' convert date to timestamp
                :param date: ' de 8 de Janeiro de 1900'
                :return: 1900/1/8
        '''
        if platform.system() == 'Linux':
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        else:
            locale.setlocale(locale.LC_ALL, 'pt_BR')

        date = date.lower().replace('.', '').strip()

        try:
            return dt.strptime(date, 'de %d de %B de %Y').strftime('%Y/%m/%d')
        except ValueError:
            return dt.strptime(date, 'de %dº de %B de %Y').strftime('%Y/%m/%d')

    def set_date(self):
        tag = self.soup.select('p[class="epigrafe"]')[0].text.strip()
        epigrafe = re.split('[,–.-]', tag)
        if epigrafe[-1]:
            self.date = self.date_conv(epigrafe[-1])
        else:
            self.date = self.date_conv(epigrafe[-2])
        return self.date


def run():
    a = Legis()
    print(type(a.link_css()))
    print((a.link_css().prettify()))

    print('*'*20)
    print(type(a.meta(numero=1234)))
    print(a.meta(numero=1234).prettify())
    print('*'*20)
    print(a.header().prettify())
    print('*'*20)
    print(a.nav().prettify())
    print('*'*20)
    print(a.baseurl(href='http://www.planalto.gov.br/ccivil_03/', target='_blank'))
    print('*' * 20)

    print(a.doctype())
    print(type(a.comment('Comentario de teste.')))

    print('*' * 20)
    a.file = '../../../CCIVIL_03/decreto/1980-1989/1985-1987/D95578.htm'
    print(a.file)
    print('*' * 20)
    print(a.get_soup_from_file())
    print('*' * 20)
    print(a.replace_brastra('http://www.planalto.gov.br/ccivil_03/img/Brastra.png'))
    print(a.soup)

    print('*' * 20)
    a.file = '../../../CCIVIL_03/decreto/D3630.htm'
    (a.get_soup_from_file())
    print(a.replace_brastra())
    print(a.soup)

    print(a.date_conv(' DE 8 DE MAIO DE 2018'))
    print(a.dou())
    print(a.meta(charset='UTF-8'))
    print(type(a.doctype()), a.doctype())

    soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    soup.insert(0, a.doctype(default='xhtml_11'))
    soup.body.append(a.comment("It's a comment!"))
    print(soup.prettify())

    soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    soup.insert(0, a.doctype())
    print(soup.prettify())

    soup = BeautifulSoup('', 'lxml')
    soup.append(a.baseurl(href='http://www.planalto.gov.br/ccivil_03'))
    print(soup.prettify())

    print(a.nav().prettify())

    print(a.charset())


if __name__ == '__main__':
    run()
