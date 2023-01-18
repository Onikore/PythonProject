from django.shortcuts import render

from analytics.utils import demand_task_1_3_helper, demand_task_2_4_helper, prepare_df, PATTERN


def index(request):
    return render(request, 'analytics/index.html')


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
    vac_id = 1
    for i in response:
        vac = {
            'vac_id': vac_id,
            'name': i['name']
        }
        specs = dict(requests.request('GET', url=url + f'/{i["vac_id"]}').json())
        desc = specs['description']
        desc = re.sub('<[^>]*>', '', desc)
        vac['description'] = desc.replace('\\', ' ') \
            .replace('&amp;', '&') \
            .replace('&quot;', '"') \
            .replace('&lt;', '<') \
            .replace('&gt;', '>')
        vac['skills'] = None if specs['key_skills'] == [] else ', '.join([i['name'] for i in specs['key_skills']])
        vac['employer'] = i['employer']['name']
        vac['salary_from'] = i['salary']['from']
        vac['salary_to'] = i['salary']['to']
        vac['area'] = i['area']['name']
        vac['published_at'] = datetime.strptime(i['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M')
        ctx.append(vac)
        vac_id += 1

    ctx = sorted(
        ctx, key=lambda x: (
            int(x['published_at'].split(' ')[1].split(':')[0]),
            int(x['published_at'].split(' ')[1].split(':')[1])
        ),
        reverse=True
    )

    return render(request, 'analytics/recent.html', {'ctx': ctx})
