import ast
import json
import pandas as pd
import numpy as np
import pickle
from collections import Counter

with open('modelo_xgboost.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

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
    names_list_distinct = []
    for i in names_list:
        if i not in names_list_distinct:
            names_list_distinct.append(i)
    return {year: sorted(names_list_distinct)}

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

def price_predictor(variables: str):
    string_numbers = variables.split(", ")
    integer_list = [int(number) for number in string_numbers]
    if len(integer_list) == 13:
        price_pred = loaded_model.predict(np.array(integer_list).reshape(1, -1))[0].round(2)
        RMSE = '4.68'
        return {'price prediction': str(price_pred), 'RMSE': RMSE}
    elif len(integer_list) < 13:
        return {'error': 'se insertaron variables de menos'}
    elif len(integer_list) > 13:
        return {'error': 'se insertaron variables demas'}