import sqlite3

import pandas as pd
from django.shortcuts import render


def index(request):
    return render(request, 'analytics/index.html')


def demand_task_1(request):
    with sqlite3.connect('db.sqlite3') as conn:
        df = pd.read_sql_query("SELECT * FROM analytics_recordswcities", conn, parse_dates=['published_at'])
        df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
        df1 = df[['year', 'salary_from', 'salary_to']].groupby('year').mean().round()
        df1['salary'] = (df1['salary_from'] + df1['salary_to']) / 2
        df1 = df1.sort_values(by='year', ascending=False)
        res = df1.to_dict()['salary']
        ctx = [{'year': i, 'salary': res[i]} for i in res]
    return render(request, 'analytics/demand/task_1.html', context={'ctx': ctx})


def demand_task_2(request):
    with sqlite3.connect('db.sqlite3') as conn:
        df = pd.read_sql_query("SELECT * FROM analytics_recordswcities", conn, parse_dates=['published_at'])
        df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
        df1 = df[['year', 'name']].groupby('year').count()
        df1 = df1.sort_values(by='year', ascending=False)
        res = df1.to_dict()['name']
        ctx = [{'year': i, 'count': res[i]} for i in res]
    return render(request, 'analytics/demand/task_2.html', context={'ctx': ctx})


def demand_task_3(request):
    with sqlite3.connect('db.sqlite3') as conn:
        df = pd.read_sql_query("SELECT * FROM analytics_recordswcities", conn, parse_dates=['published_at'])
        df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
        df1 = df[['year', 'salary_from', 'salary_to']].groupby('year').mean().round()
        df1['salary'] = (df1['salary_from'] + df1['salary_to']) / 2
        df1 = df1.sort_values(by='year', ascending=False)
        res = df1.to_dict()['salary']
        ctx = [{'year': i, 'salary': res[i]} for i in res]
    return render(request, 'analytics/demand/task_3.html', context={'ctx': ctx})


def demand_task_4(request):
    with sqlite3.connect('db.sqlite3') as conn:
        df = pd.read_sql_query("SELECT * FROM analytics_recordswcities", conn, parse_dates=['published_at'])
        df['year'] = pd.to_datetime(df['published_at'], utc=True).dt.year
        df1 = df[['year', 'name']].groupby('year').count()
        df1 = df1.sort_values(by='year', ascending=False)
        res = df1.to_dict()['name']
        ctx = [{'year': i, 'count': res[i]} for i in res]
    return render(request, 'analytics/demand/task_4.html', context={'ctx': ctx})


def geography(request):
    return render(request, 'analytics/geography.html')


def skills(request):
    return render(request, 'analytics/skills.html')


def recent(request):
    return render(request, 'analytics/recent.html')
