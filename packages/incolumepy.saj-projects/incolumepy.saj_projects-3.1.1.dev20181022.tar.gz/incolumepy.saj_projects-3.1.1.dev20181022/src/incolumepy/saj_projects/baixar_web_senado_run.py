import src.incolumepy.saj_projects.baixar_web_senado as senado
import pandas as pd

file = '../../relatorios/Normas_senado.xlsx'


def truncus03():
    xlsx = pd.ExcelFile(file)
    planilha = xlsx.sheet_names
    df = xlsx.parse(planilha[0])
    cols = ['num', 'links']
    df.columns=cols

    #remove os nulos do Dataframe
    df = df[pd.notnull(df['links'])]
    #iteraçao loop
    for i, linha in df.iterrows():
        num, link = linha
        try:
            print('["{}"] = "{}"'.format(num, link))
            texto = senado.baixar_web_senado(link)
            texto = senado.limpar_senado(texto)
            texto = senado.formatar_senado(texto)
            senado.gravar_fromSenado(texto, path='/home/brito/Documentos/CEJ/Atos')
        except TypeError as e:
            print(num, e, link)
        except ValueError as e:
            print(num, e)


if __name__ == '__main__':
    truncus03()
