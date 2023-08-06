#coding: utf-8
from bs4 import BeautifulSoup
import re
import os
import sys
from incolumepy.utils.files import realfilename
from unicodedata import normalize
sys.path.append(os.path.abspath(os.path.join('..', '..', '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from incolumepy.saj_projects import legis
from inspect import stack
import logging


def limpar(conteudo):
    ''''''
    # logger.debug('elementos <br> substituídos por <p>')
    html = replace_break(conteudo)

    # logger.debug('espaços brancos reduzidos')
    html = limpar_espacos(html)

    # logger.debug('Criado objeto soup')
    # soup = BeautifulSoup(html, 'html5lib')

    # Remove cabeçalho de tabela
    html = remover_tags(html, tags=['table'])

    # desatachar 'div[id="art"]'
    html = desatachar_tags(html, tags=['div[id="art"]'])

    # Desatachar tags
    nowish = ['link', 'center', 'big', 'u', 'font', 'span', 'strong', 'small']
    html = desatachar_tags(html, nowish)

    # Marca class trash em elementos com Texto específico
    elem_txt_nowish = [
        'Texto compilado',
        'Texto compilado'
    ]

    soup = BeautifulSoup(html, 'html5lib')
    for k in elem_txt_nowish:
        # logger.debug(k)
        container = soup.find_all(string=re.compile(k, re.I))
        # logger.debug(F'container: {container}')
        try:
            for j, i in enumerate(container):
                # logger.debug('{}, {}'.format(j, i.parent))
                legis.check_parent(soup=i, tag_name='p', key='class', value='trash')
        except AttributeError:
            container[0].wrap(soup.new_tag('p', **{'class': 'trash'}))
    html = soup.prettify()

    # remove tags ou tags com os atributos indicados
    tags = [
        '[class="trash"]', '[name="generator"]', '[class="tela"]',
        'style', '[class="alert alert-danger"]', '[a=""]', 'script'
    ]
    html = remover_tags(html, tags)

    # attrs remove
    tags = ['xmlns', 'bgcolor', 'align', 'style', 'width']
    html = remover_tags(html, tags)

    # remove classes MS
    html = remover_attr(html, ['[class*="Ms"]'])

    return html


def ordinais(codigo: str) -> str:
    codigo = re.sub('<sup>\s*<u>\s*o\s*</u>\s*</sup>', 'º ', codigo, flags=re.I)
    codigo = re.sub('<sup>\s*<u>\s*a\s*</u>\s*</sup>', 'ª ', codigo, flags=re.I)
    soup = BeautifulSoup(codigo, "html5lib")

    tag0 = soup.find_all('sup', string=re.compile('\s*o\s*', re.I))
    if tag0:
        # print(tag0)
        for tag in tag0:
            tag.string = "º "
            tag.unwrap()

    tag1 = soup.find_all('sup', string=re.compile('a', re.I))
    if tag1:
        # print(tag1)
        for tag in tag1:
            tag.string = "ª "
            tag.unwrap()

    u = soup.find_all('u', string=re.compile('º|ª', re.I))
    if u:
        # print(u)
        for tag in u:
            tag.unwrap()

    return soup.prettify()


def remover_tag_string(conteudo: str, lista_indesejados: list=None, tag_referencia:str='p')-> str:
    '''Marca class trash em elementos com Texto específico'''
    if not lista_indesejados:
        lista_indesejados = [
            'Texto compilado',
            'Texto completo'
        ]
    assert isinstance(lista_indesejados, list), "Error lista_indesejados not list"
    soup = BeautifulSoup(conteudo, 'html5lib')

    for s in lista_indesejados:
        container = soup.find_all(string=re.compile(s, re.I))
        try:
            for item in container:
                if item.parent.name == tag_referencia:
                    item.parent.decompose()
        except AttributeError:
            container[0].wrap(soup.new_tag(tag_referencia, **{'class': 'trash'}))
    return soup.prettify()


def replace_break(codigo: str)->str:
    return re.sub(r'<\s*br[\s/]*>', '</p><p>', codigo, flags=re.I)


def __staff(*args, **kwargs):
    pass

def replace_another_element(codigo:str, elem: str) -> str:
    ''' Substitui elementos intermediarios pelo imediatamente superior na hierarquia html.'''
    parents = ['p', 'h4', 'h5', 'h6']
    soup = BeautifulSoup(codigo, 'html.parser')
    elements = soup.select(elem)
    logging.info(f"Quantidade encontrada: {len(elements)} tag(s) '{elem}' encontrada(s).")
    for item in elements:
        parent = item.parent.name
        logging.debug(f'soup.{item}.parent.name = {parent}')

        tag_parent = legis.locate_parent(soup=item, tag_name='p').name
        if tag_parent:
            logging.debug(f'parent: {tag_parent}')


        tag_h4 = legis.locate_parent(soup=item, tag_name='h4').name
        if tag_h4:
            logging.debug(f'parent: {tag_h4}')
        tag_h5 = legis.locate_parent(soup=item, tag_name='h5').name
        if tag_h5:
            logging.debug(f'parent: {tag_h5}')
        tag_h6 = legis.locate_parent(soup=item, tag_name='h6').name
        if tag_h6:
            logging.debug(f'parent: {tag_h6}')
    return False


def remove_break(codigo: str) -> str:
    return remover_tags(['br'])


def replace_espacos(codigo: str) -> str:
    '''
    Espaçamento duplo entre mensagens de alterações legislativas
    :param codigo: str contendo código HTML
    :return: str HTML
    '''
    assert isinstance(codigo, str), "codigo deve ser instancia de str"
    return re.sub('\)\s+\(', '\)&nbsp;&nbsp;\(', codigo, flags=re.M)


def limpar_espacos(codigo: str)->str:
    codigo = re.sub(r'&nbsp;', ' ', codigo, flags=re.I)
    codigo = re.sub('\s+', ' ', codigo, flags=re.I)
    return codigo


def desatachar_tags(codigo: str, tags: list=None)->str:
    '''Desatachar tags'''
    soup = BeautifulSoup(codigo, 'html5lib')
    if not tags:
        tags = [
            'link',
            'center',
            'big',
            'u',
            'font',
            'span',
            'small',
        ]
    for tag in tags:
        container = soup.select(tag)
        for n, item in enumerate(container):
            item.unwrap()
    return soup.prettify()


def remover_tags(codigo: str, tags: list=None)->str:
    '''remove tags, seus atributos e todo seus conteudos'''
    soup = BeautifulSoup(codigo, 'html5lib')
    if not tags:
        tags = [
            'link[rel*="STYLESHEET"]',
            'meta[name="GENERATOR"]',
            '[class="trash"]',
            '[name="generator"]',
            '[class="tela"]',
            'style',
            '[class="alert alert-danger"]',
            '[a=""]',
            'script'
        ]
    for tag in tags:
        container = soup.select(tag)
        for item in container:
            item.decompose()
    return soup.prettify()


def remover_attr(codigo: str, atributos: list=None)->str:
    soup = BeautifulSoup(codigo, 'html5lib')
    if not atributos:
        atributos = [
            'class*="Ms"',
            'xmlns',
            'bgcolor',
            'align',
            'style',
            'width'
        ]
    for atributo in atributos:
        container = soup.select('[{}]'.format(atributo))
        for item in container:
            del item[atributo]
    return soup.prettify()


def remover_acentos(txt: str)-> str:
    ''' Remove acentos de caracteres não ascii
    :param txt: string
    :return: string sem caracteres especiais

    >>> remover_acentos('áàãâäÁÀÃÂÄ! éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.')
    'aaaaaAAAAA! eeeeEEEEE? iiiiIIIII, oooooOOOOO; uuuuUUUUU.'
    '''
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def one_line(codigo_html: str) -> str:
    '''Retorna o codigo html sem quebras'''
    return re.sub('&nbsp;|\n', ' ', limpar_espacos(codigo_html), flags=re.MULTILINE)


def elemento_discartar(soup, elemento: str, pos: int):
    logging.debug(f'Descarta "{elemento}" da posição ({pos}) indicada')
    for item in soup.select(f'{elemento}:nth-of-type({pos})'):
        logging.debug(f'Elemento decomposed: {item}')
        item.decompose()


def elemento_desatachar(soup, elemento: str, pos: int):
    logging.debug(f'desatacha "{elemento}" da posição ({pos})')
    for item in soup.select(f'{elemento}:nth-of-type({pos})'):
        logging.debug(f'Elemento unwraped: {item}')
        item.unwrap()


class Clean_html:
    TXT = '[ACENTUAÇÃO] açaí: áàãâäÁÀÃÂÄ! éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.'

    def __init__(self):
        self.file = None
        self.data = []
        self.conteudo = None
        self.filename = None
        self.path = None

    @classmethod
    def remover_acentos(self, txt):
        ''' Remove acentos de caracteres não ascii
        :param txt: string
        :return: string sem caracteres especiais

        >>> remover_acentos('áàãâäÁÀÃÂÄ! éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.')
        'aaaaaAAAAA! eeeeEEEEE? iiiiIIIII, oooooOOOOO; uuuuUUUUU.'
        '''
        return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

    def get_file_content(self):
        try:
            with open(self.file) as file:
                self.data.append(file.read())
                self.path = os.path.dirname(file.name)
                self.filename = os.path.basename(file.name)
        except:
            with open(self.file, encoding='iso8859-1') as file:
                self.data.append(file.read())
                self.path = os.path.dirname(file.name)
                self.filename = os.path.basename(file.name)

    def clean(self):
        try:
            if not self.conteudo:
                self.get_file_content()

            if not self.data:
                self.data.append(self.conteudo)

            self.data.append(re.sub('&nbsp;|\n', ' ', str(BeautifulSoup(self.data[0], 'html5lib')), flags=re.MULTILINE))
            self.data[1] = re.sub('\s+', ' ', self.data[1], flags=re.MULTILINE)
            self.data[1] = re.sub('<sup>\s?o\s?</sup>', 'º ', self.data[1], flags=re.MULTILINE)
            self.data[1] = re.sub('<sup>\s?a\s?</sup>', 'ª ', self.data[1], flags=re.MULTILINE)
            soup = BeautifulSoup(self.data[-1], 'html.parser')

            # remover tags e seu conteudo
            tag = []
            tag.append('meta[name="GENERATOR"]')
            tag.append('link[rel*="STYLESHEET"]')
            tag.append('style')
            for j in tag:
                container = soup.select(j)
                for a, i in enumerate(container):
                    # print(a, i.parent)
                    i.decompose()

            ## desatachar tags
            tag = []
            tag.append('big')
            tag.append('u')
            tag.append('font')
            tag.append('span')
            tag.append('strong')
            tag.append('small')
            tag.append('html')
            tag.append('body')
            for j in tag:
                container = soup.select(j)
                for i in container:
                    i.unwrap()

            # attrs remove
            tag = []
            tag.append('xmlns')
            tag.append('bgcolor')
            tag.append('align')
            tag.append('style')
            tag.append('width')
            for i in tag:
                container = soup.select('[{}]'.format(i))
                for j in container:
                    del j[i]

            # remove classes MS
            container = soup.select('[class*="Ms"]')
            for i in container:
                del i['class']

            # adding str html e body
            soup = BeautifulSoup('<html><body>{}</body></html>'.format(str(soup)), 'html.parser')

            # wrap body
            tag = soup.new_tag('body')
            #soup.new_tag('body').wrap(soup)
            #tag.append(soup)

            #for item in soup.find_all():
            #    tag.append(item.extract())
            #soup = tag

            # wrap html
            #soup.wrap(soup.new_tag('html'))
            #container = soup.find_parents('head')
            #print(container)

            # Realocar head
            soup.html.insert(0, soup.body.head.extract())

            self.conteudo = soup.prettify()
        except IOError:
            raise

    def write(self):
        os.rename(os.path.join(self.path, self.filename), realfilename(os.path.join(self.path, self.filename)))
        with open(realfilename(os.path.join(self.path, self.filename)), 'w') as file:
            file.write(self.conteudo)
        return True

    @staticmethod
    def run(file='../file.html'):
        a = Clean_html()
        try:
            assert os.path.isfile(file)
            a.file = file
        except AssertionError:
            a.file = '../../testes/file.html'

        a.clean()
        print(a.__dict__)
        print(a.filename)
        print(a.write())
        print(a.remover_acentos(a.TXT))
        print(Clean_html.remover_acentos(Clean_html.TXT))


if __name__ == '__main__':
    Clean_html.run()
