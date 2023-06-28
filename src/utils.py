import json
import os
from abc import ABC, abstractmethod

import requests


class get_info(ABC):

    @abstractmethod
    def __init__(self):
        pass


class get_info_hh(get_info):

    def __init__(self, word, quantity):
        """
        Инициализируем сервис с указанными параметрами
        """
        self.quantity = quantity
        self.word = word

    def get_info(self):
        ready_info = []
        params = {
            'text': 'NAME:' + self.word,
            'area': 1,
            'page': 0,
            'per_page': self.quantity
        }
        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()
        req.close()
        vacancy_list = json.loads(data)
        q = 0
        for i in vacancy_list['items']:
            q += 1
            try:
                salary = f"{i['salary']['from']} - {i['salary']['to']}"
                if salary.split(' - ')[0] == 'None':
                    salary = 'до ' + salary.split(' - ')[1]
                elif salary.split(' - ')[1] == 'None':
                    salary = 'от ' + salary.split(' - ')[0]
            except TypeError:
                salary = 'з/п не указана'
            ready_info.append({q: {'Должность': i['name'],
                                   'Работодатель': i['employer']['name'],
                                   'з/п': salary,
                                   'Опыт': i['experience']['name'],
                                   'Требования': i['snippet']['requirement'],
                                   'Ссылка': i['alternate_url']}})

        with open('data.json', 'w', encoding="utf-8") as file:
            json.dump(ready_info, file, indent=2, ensure_ascii=False)


class get_info_sj(get_info):

    def __init__(self, word, quantity):
        """
        Инициализируем сервис с указанными параметрами
        """
        self.quantity = quantity
        self.word = word

        ready_info_sj = []
        SuperJob_API_KEY = os.environ.get('SuperJob_API_KEY')

        headers = {'X-Api-App-Id': SuperJob_API_KEY}
        params = {'town': 4, 'count': self.quantity, 'keyword': self.word}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                params=params,
                                headers=headers)
        vacancys = response.json()
        q = 0
        for i in vacancys['objects']:
            q += 1
            if i['payment_from'] != 0:
                salary = i['payment_from']
            else:
                salary = 'з/п не указана'
            ready_info_sj.append({q:{'платформа': 'SuperJob',
                                    'должность': i['profession'],
                                    'Работодатель': i['firm_name'],
                                    'зарплата_от': salary,
                                    'описание': i['candidat'],
                                    'ссылка': i['link']}})
        with open('data_sj.json', 'w', encoding="utf-8") as file:
            json.dump(ready_info_sj, file, indent=2, ensure_ascii=False)
        print(ready_info_sj[0])
