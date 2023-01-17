import sqlite3

import pandas as pd
from django.shortcuts import render


# UTILS
def prepare_df(query, pattern=False):
    with sqlite3.connect('db.sqlite3') as conn:
        df = pd.read_sql_query(query, conn, parse_dates=['published_at'])
        if pattern:
            df = df.loc[df['name'].str.contains('|'.join(PATTERN), case=False)]
        df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
        return df


def demand_task_2_4_helper(pattern=False):
    df = prepare_df("SELECT name,published_at FROM analytics_recordswcities", pattern)
    df1 = df[['year', 'name']].groupby('year').count()
    df1 = df1.sort_values(by='year', ascending=False)
    return df1


def demand_task_1_3_helper(pattern=False):
    df = prepare_df("SELECT name,salary_from,salary_to,published_at FROM analytics_recordswcities", pattern)
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
    df = prepare_df("SELECT name,salary_from,salary_to,area_name,published_at FROM analytics_recordswcities", True)
    df1 = df[['area_name', 'salary_from', 'salary_to']].groupby('area_name')
    df1 = df1.mean().round()
    df1['salary'] = (df1['salary_from'] + df1['salary_to']) / 2
    df1 = df1.sort_values(by='salary', ascending=False).head(10)
    res = df1.to_dict()['salary']
    ctx = [{'city': i, 'vac': res[i]} for i in res]
    return render(request, 'analytics/geography/task_1.html', {'ctx': ctx})


def geography_task_2(request):
    df = prepare_df("SELECT name,area_name,published_at FROM analytics_recordswcities", True)
    df1 = df[['area_name', 'name']].groupby('area_name').count()
    df1['name'] = (df1['name'] / df1['name'].sum()) * 100
    df1 = df1.loc[df1['name'] >= 1]
    df1 = df1.sort_values(by='name', ascending=False).round()
    res = df1.to_dict()['name']
    ctx = [{'city': i, 'salary': res[i]} for i in res]
    return render(request, 'analytics/geography/task_2.html', {'ctx': ctx})


#  НАВЫКИ
def skills(request):
    df = prepare_df("SELECT skills, published_at FROM analytics_recordswskills")
    df1 = df[['skills', 'year']].groupby('year')
    ctx = []
    for i in df1.groups.keys():
        lst = df1.get_group(i)['skills'].str.split('|').explode().value_counts().head(10)
        ctx.append({'year': i, 'skills': lst.to_dict()})
    return render(request, 'analytics/skills.html', {'ctx': ctx})


#  ПОСЛЕДНИЕ ВАКАНСИИ
def recent(request):
    import requests
    import re
    from datetime import datetime

    url = "https://api.hh.ru/vacancies"

    payload = {'text': ' OR '.join(PATTERN),
               'page': 1,
               'per_page': 10,
               'only_with_salary': True,
               'applicant_comments_order': 'creation_time_asc'}

    response = dict(requests.request('GET', url=url, data=payload).json())['items']
    ctx = []
    id = 1
    for i in response:
        vac = {}
        vac['id'] = id
        vac['name'] = i['name']
        specs = dict(requests.request('GET', url=url + f'/{i["id"]}').json())
        desc = specs['description']
        desc = re.sub('<[^>]*>', '', desc)
        desc = re.sub('&quot;', '', desc)
        vac['description'] = desc.replace('\\',' ')
        vac['skills'] = None if specs['key_skills'] == [] else ', '.join([i['name'] for i in specs['key_skills']])
        vac['employer'] = i['employer']['name']
        vac['salary_from'] = i['salary']['from']
        vac['salary_to'] = i['salary']['to']
        vac['area'] = i['area']['name']
        vac['published_at'] = datetime.strptime(i['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M')
        ctx.append(vac)
        id += 1

    # sort ctx by hours and minutes in published_at asc
    ctx = sorted(
        ctx, key=lambda x: (
            int(x['published_at'].split(' ')[1].split(':')[0]),
            int(x['published_at'].split(' ')[1].split(':')[1])
        ),
        reverse=True
    )

    return render(request, 'analytics/recent.html', {'ctx': ctx})
