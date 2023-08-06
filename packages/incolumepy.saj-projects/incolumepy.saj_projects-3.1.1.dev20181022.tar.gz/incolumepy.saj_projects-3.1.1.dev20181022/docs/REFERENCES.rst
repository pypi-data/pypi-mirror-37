Gravar informações Path SO em CSV
==================================

    find CCIVIL_03/ -type f |while read a; do echo $(awk -F. '{print $NF}' <<< $a)\; $a\;$(ls --full-time $a|awk '{print $6, $7}') |tee -a ~/Documentos/Projetos/saj_projects/relatorios/files_$(date +%s).csv; done

Proteger nomes com espaços
-----------------------

    epoch=$(date +%s); find CCIVIL_03/ -type f |while read a; do echo $a\;$(ls --full-time "${a}"|awk '{print $6, $7}') |tee -a ~/projetos/saj_projects/relatorios/file_systems/files_${epoch}.csv; done

    epoch=$(date +%s); find CCIVIL_03/ -type f |while read a; do echo $a\;$(ls --full-time "${a}"|awk '{print $6, $7}') |tee -a ~/projetos/saj_projects/relatorios/files_${epoch}.csv; done

    find CCIVIL_03/ -type f |while read a; do echo $a\;$(ls --full-time "${a}"|awk '{print $6, $7}') |tee -a ~/projetos/saj_projects/relatorios/files_1528738638.csv; done

Relatorio com pandas
====================
Pandas e uma ferramenta em python para processamento de informaçoes tabulares.

Noçoes Basicas
--------------
    http://wilsonfreitas.github.io/posts/lista-da-forbes-de-2013-com-python-e-pandas.html
    https://www.vooo.pro/insights/12-tecnicas-pandas-uteis-em-python-para-manipulacao-de-dados/
    https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

Datetime
----------
    https://www.youtube.com/watch?v=yCgJGsg0Xa4&index=25&list=PL5-da3qGB5ICCsgW1MxlZ0Hq8LL5U3u9y
    https://pandas.pydata.org/pandas-docs/stable/api.html#datetimelike-properties
    https://www.youtube.com/watch?v=r0s4slGHwzE
    http://pandas.pydata.org/pandas-docs/version/0.22/timeseries.html

Pandas merge
------------
    https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/
    https://chrisalbon.com/python/data_wrangling/pandas_join_merge_dataframe/

Pandas replace
-------------
    https://chrisalbon.com/python/data_wrangling/pandas_replace_values/


