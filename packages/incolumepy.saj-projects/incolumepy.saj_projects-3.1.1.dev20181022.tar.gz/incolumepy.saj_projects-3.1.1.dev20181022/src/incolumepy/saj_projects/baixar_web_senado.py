import os
import re
import requests
from bs4 import BeautifulSoup, Comment
from src.incolumepy.saj_projects.legis import Legis
from incolumepy.utils.files import realfilename


proxies={
    'http': 'http://10.1.101.101:8080',
    'https': 'http://10.1.101.101:8080',
    'ftp': 'http://10.1.101.101:8080',
}


def baixar_web_senado(url, proxies=proxies, timeout=5):
    try:
        page = requests.get(url, timeout=timeout)
    except:
        page = requests.get(url, proxies=proxies, timeout=timeout)
    soup = BeautifulSoup(page.content, 'html.parser')

    ato = soup.select('[id="conteudoPrincipal"]')
    result = ato[0].find('html')
    return result.prettify()

def limpar_senado(conteudo):
    conteudo = re.sub('N\.', 'Nº', conteudo, re.I)
    conteudo = re.sub(' [–-]', ',', conteudo, re.I)
    soup = BeautifulSoup(conteudo, 'html.parser')
    del soup.html['xmlns:o']
    for child in soup.head.children:
        if isinstance(child, Comment):
            child.extract()

    # descarte dos titulos pre-existentes
    tags = []
    tags.append(soup.select("h2:nth-of-type(1)"))
    tags.append(soup.select("h3:nth-of-type(1)"))
    tags.append(soup.select("h4:nth-of-type(1)"))
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
    tags.append('div:nth-of-type(3)')

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
    for j in tags:
        container = soup.select(j)
        for i in container:
            i.decompose()

    try:
        tags = soup.find_all(string=re.compile("decreto", re.I), limit=1)[0].parent
        tags.name = 'p'
    except IndexError as e:
        raise ValueError('Ato sem conteudo.')

    return soup.prettify()


def formatar_senado(conteudo):
    elem = Legis()
    conteudo = re.sub('\n', '', conteudo, re.I)
    soup = BeautifulSoup(conteudo, 'html.parser')
    soup.html['xmlns'] = "http://www.w3.org/1999/xhtml"
    soup.html.insert(0, soup.new_tag('head'))
    soup.head.append(elem.meta())
    soup.head.append(elem.link_css())
    soup.body['id'] = 'void'
    soup.body.insert(1, elem.header())
    soup.body.insert(3, elem.nav())
    soup.body.append(elem.dou())

    try:
        container = soup.select('p[class="Epgrafe"]')[0]
        container['class'] = 'epigrafe'
    except IndexError:
        container = soup.find_all(string=re.compile("decreto", re.I), limit=1)[0].parent
        container['class'] = 'epigrafe'
        pass

    container = soup.select('[class="Ementa"]')
    if container:
        container[0]['class'] = 'ementa'
    container = soup.select('[class="Date"]')
    if container:
        container[0]['class'] = 'data'
    container = soup.select('[class="Assinatura1"]')
    if container:
        container[0]['class'] = 'presidente'
    container = soup.find_all(class_="Assinatura2")
    if container:
        for i in container:
            i['class'] = 'ministro'

    epigrafe = soup.select('p[class="epigrafe"]')[0].text.strip().split(',')
    tipo = epigrafe[0].split()[0].lower()
    try:
        a, b = epigrafe[0].split()[-1].split('-')
        num = '{:0>5}{}'.format(''.join([i for i in a if i.isdigit()]), b)
    except:
        num = '{:0>5}'.format(''.join([i for i in epigrafe[0].split()[-1] if i.isdigit()]))
    date = Legis.date_conv(epigrafe[-1])
    try:
        ano = ''.join([i for i in epigrafe[-1].split()[-1] if i.isdigit()])
    except:
        ano = ''.join([i for i in epigrafe[-2].split()[-1] if i.isdigit()])

    container = soup.select('meta[name="ano"]')
    container[0]['content'] = ano

    container = soup.select('meta[name="dataassinatura"]')
    container[0]['content'] = date

    container = soup.select('meta[name="chefegoverno"]')
    presidente = soup.select('p[class="presidente"]')
    if presidente:
        container[0]['content'] = presidente[0].text.strip()
    else:
        container[0]['content'] = ''

    container = soup.select('meta[name="numero"]')
    container[0]['content'] = num

    container = soup.select('meta[name="tipo"]')
    container[0]['content'] = tipo
    try:
        soup.title.string = epigrafe[0]
    except:
        soup.head.append(soup.new_tag('title'))
        soup.title.string = epigrafe[0]
    soup = BeautifulSoup(re.sub('\n', ' ', soup.prettify(), re.I), 'html.parser')
    return soup.prettify()

def gravar_fromSenado(conteudo, path=''):
    soup = BeautifulSoup(conteudo, 'html.parser')

    ano = soup.select('meta[name="ano"]')[0]['content']
    num = soup.select('meta[name="numero"]')[0]['content']
    tipo = soup.select('meta[name="tipo"]')[0]['content']

    print(ano, num)
    with open(realfilename(os.path.join(path, tipo, ano,'D{}.html'.format(num))), 'wb') as file:
        file.write(soup.prettify(encoding='iso8859-1'))

    return True
    pass

if __name__ == '__main__':

    try:
        texto = baixar_web_senado('http://legis.senado.leg.br/legislacao/ListaTextoSigen.action?norma=512863&id=14248167&idBinario=15645032')
        texto = limpar_senado(texto)
        texto = formatar_senado(texto)
        print(texto)
    except ValueError as e:
        print(e)


