import sqlite3

import pandas as pd
from django.shortcuts import render


# UTILS
def prepare_df():
    with sqlite3.connect('db.sqlite3') as conn:
        df = pd.read_sql_query("SELECT * FROM analytics_recordswcities", conn, parse_dates=['published_at'])
        df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
        return df


def demand_task_2_4_helper(pattern=False):
    df = prepare_df()
    if pattern:
        df = df.loc[df['name'].str.contains('|'.join(PATTERN), case=False)]
    df1 = df[['year', 'name']].groupby('year').count()
    df1 = df1.sort_values(by='year', ascending=False)
    return df1


def demand_task_1_3_helper(pattern=False):
    df = prepare_df()
    if pattern:
        df = df.loc[df['name'].str.contains('|'.join(PATTERN), case=False)]
    df1 = df[['year', 'salary_from', 'salary_to']].groupby('year').mean().round()
    df1['salary'] = (df1['salary_from'] + df1['salary_to']) / 2
    df1 = df1.sort_values(by='year', ascending=False)
    return df1


PATTERN = ('system admin', 'сисадмин', 'сис админ',
           'системный админ', 'администратор систем', 'системний адміністратор')


# URLS

#  ГЛАВНАЯ
def index(request):
    return render(request, 'analytics/index.html')


#  ВОСТРЕБОВАННОСТЬ

def demand_task_1(request):
    df = demand_task_1_3_helper()
    res = df.to_dict()['salary']
    ctx = [{'year': i, 'salary': res[i]} for i in res]
    return render(request, 'analytics/demand/task_1.html', context={'ctx': ctx})


def demand_task_2(request):
    df1 = demand_task_2_4_helper()
    res = df1.to_dict()['name']
    ctx = [{'year': i, 'count': res[i]} for i in res]
    return render(request, 'analytics/demand/task_2.html', context={'ctx': ctx})


def demand_task_3(request):
    df = demand_task_1_3_helper(True)
    res = df.to_dict()['salary']
    ctx = [{'year': i, 'salary': res[i]} for i in res]
    return render(request, 'analytics/demand/task_3.html', context={'ctx': ctx})


def demand_task_4(request):
    df = demand_task_2_4_helper(True)
    res = df.to_dict()['name']
    ctx = [{'year': i, 'count': res[i]} for i in res]
    return render(request, 'analytics/demand/task_4.html', context={'ctx': ctx})


#  ГЕОГРАФИЯ
def geography_task_1(request):
    df = prepare_df()
    df1 = df.loc[df['name'].str.contains('|'.join(PATTERN), case=False)]
    df1 = df1[['area_name', 'salary_from', 'salary_to']].groupby('area_name')
    df1 = df1.mean().round()
    df1['salary'] = (df1['salary_from'] + df1['salary_to']) / 2
    df1 = df1.sort_values(by='salary', ascending=False).head(10)
    res = df1.to_dict()['salary']
    ctx = [{'city': i, 'vac': res[i]} for i in res]
    return render(request, 'analytics/geography/geography_task_1.html', {'ctx': ctx})


def geography_task_2(request):
    df = prepare_df()
    df1 = df.loc[df['name'].str.contains('|'.join(PATTERN), case=False)]
    df1 = df1[['area_name', 'name']].groupby('area_name').count()
    df1['name'] = (df1['name'] / df1['name'].sum()) * 100
    df1 = df1.loc[df1['name'] >= 1]
    df1 = df1.sort_values(by='name', ascending=False).round()
    res = df1.to_dict()['name']
    ctx = [{'city': i, 'salary': res[i]} for i in res]
    return render(request, 'analytics/geography/geography_task_2.html', {'ctx': ctx})


#  НАВЫКИ
def skills(request):
    return render(request, 'analytics/skills.html')


#  ПОСЛЕДНИЕ ВАКАНСИИ
def recent(request):
    return render(request, 'analytics/recent.html')
