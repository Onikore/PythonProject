import sqlite3

import pandas as pd


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
