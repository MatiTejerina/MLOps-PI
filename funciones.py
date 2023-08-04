import ast
import json
import pandas as pd
import numpy as np
from collections import Counter

rows = []
with open('steam_games.json', 'r') as f:
    for line in f.readlines():
        rows.append(ast.literal_eval(line))

df = pd.DataFrame(rows)

def get_top_5(diccionario):
    diccionario = dict(sorted(diccionario.items(), key=lambda x: x[1], reverse=True))
    primeros_5_valores = {}
    contador = 0
    for clave, valor in diccionario.items():
        primeros_5_valores[clave] = valor
        contador += 1
        if contador == 5:
            break
    return primeros_5_valores

def generos_por_año(year):
    if type(year) != str:
        year = str(year)
    generos_list = []
    aux_df = df.loc[df['release_date'].str.contains(year) == True]
    aux_df.reset_index()
    for i in aux_df['genres']:
        if type(i) == list:
            for x in i:
                generos_list.append(x)
    conteo = dict(Counter(generos_list))
    return {year: get_top_5(conteo)}


def juegos_por_año(year: str):
    data = df.loc[df['release_date'].str.contains(year) == True]
    data = data.dropna(subset=['app_name'])
    names_list = [i for i in data['app_name'] if i]
    return {year: names_list}

def specs_por_año(year: str):
    specs_list = []
    data = df.loc[df['release_date'].str.contains(year) == True]
    data.reset_index()
    for i in data['specs']:
        if type(i) == list:
            for x in i:
                specs_list.append(x)
    conteo = dict(Counter(specs_list))
    result = get_top_5(conteo)
    return {year: result}

def earlyaccess_por_año(year: str):
    data = df.loc[df['release_date'].str.contains(year) == True]
    data_filtered = data.loc[data['early_access'] == True]
    result = str(len(data_filtered))
    return {year: result}

def sentiment_por_año(year: str):
    sentiments_list = ['Mixed', 'Mostly Positive', 'Very Positive', 'Overwhelmingly Positive', 'Very Negative', 'Positive', 'Mostly Negative', 'Negative', 'Overwhelmingly Negative']
    data = df.loc[df['release_date'].str.contains(year) == True]
    data_filt = data.loc[data['sentiment'].isin(sentiments_list)]
    result = []
    for i in sentiments_list:
        result.append((i, len(data_filt.loc[data_filt['sentiment'] == i])))
    result = dict(result)
    return {year: result}

def metascore_por_año(year: str):
    data = df.loc[df['release_date'].str.contains(year) == True]
    data = data.dropna(subset=['app_name'])
    data_sorted = data.sort_values(by='metascore', ascending=False)
    top_5 = data_sorted.head(5)
    result = {}
    for idx, row in top_5.iterrows():
        result[row['app_name']] = row['metascore']
    return {year: result}