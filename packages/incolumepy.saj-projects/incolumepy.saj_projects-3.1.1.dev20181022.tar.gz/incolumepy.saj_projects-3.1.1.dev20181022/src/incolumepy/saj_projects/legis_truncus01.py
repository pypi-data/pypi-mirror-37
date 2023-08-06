#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from incolumepy.saj_projects.legis import Legis
from incolumepy.utils.files import ll


def truncus01():
    a = Legis()
    a.file = '../../../CCIVIL_03/decreto/D3630.htm'
    a.get_soup_from_file()
    print(a.replace_brastra(index=1))
    print(a.soup)


def truncus02(path='.'):
    for i in ll(path, ):
        print(i)


def truncus03(file='../../../exemplos/sican_others/normativos04/D70916.html'):

    a = Legis()
    a.file = file
    soup = a.get_soup_from_file()
    print('a.get_soup_from_file .. ok')
    #print(soup)
    epigrafe = soup.select('p[class="epigrafe"]')[0].text.strip().replace('.', '').split(',')
    print(epigrafe)
    print(a.date_conv(epigrafe[-1]))

def truncus04():
    a = Legis()
    a.file = '../../../exemplos/sican_others/normativos04/D70916.html'
    a.get_soup_from_file()
    print(a.date)
    print(a.set_date())
    print(a.date)
    pass

def truncus05():
    a = Legis()
    for file in ll(r'/home/brito/Documentos/castelo_saj/CENTRO DE ESTUDOS/normativos SICAN/normativos03', string=True):
        a.file = file
        print(a.file)
        a.get_soup_from_file()
        a.set_date()
        print(a.date, a.file)

def truncus06():
    a = Legis()
    for file in ll(r'/home/brito/Documentos/castelo_saj/CENTRO DE ESTUDOS/normativos SICAN/normativos04', string=True):
        a.file = file
        print(a.file)
        a.get_soup_from_file()
        a.set_date()
        print(a.date, a.file)

def run():
    #truncus04()
    #truncus02('/tmp')
    #truncus05()
    truncus06()


if __name__ == '__main__':
    run()
