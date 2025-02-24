from __future__ import annotations
import sys
import docx
import os
import json
from .post_message import send_message
from jira import JIRA
from datetime import datetime, timedelta, date
from .verification import verific
#from init import init_path, update_time
import time

#from read_mail_in_date import date_for_second_verific_mas, date_str
from pathlib import Path
from .insert_into_docs import create_docx
import re
#os.chdir("/")


def check_structure_ip(name_ip):
    myself = Path(__file__).resolve()
    with open(f'{myself.parents[0]}/check.json', 'r', encoding='utf-8') as f: # открытие файла для чтения
        data = json.load(f) # чтение данных из файла в формате JSON в объект Python

    if name_ip in data:
        structure = data[name_ip]
    else:
        structure = 'нет совпадения'
    return structure

def get_lead_email(lead): #получение почты РП
    myself = Path(__file__).resolve()
    with open(f'{myself.parents[0]}/lead_email.json', 'r', encoding='utf-8') as f: # открытие файла для чтения
        data = json.load(f) # чтение данных из файла в формате JSON в объект Python

    if lead in data:
        lead_email = data[lead]
    else:
        lead_email = ''
    return lead_email




# -----------------------------------------------создание экземпляра документа------------------------
def get_data_from_jira(project, stavka, date_start, date_end, time_of_work, user_name, user_second_name, user_surname, user_email, user_town, type_of_worker, number_act, number_contact, date_contact, name_of_work, result_of_work):
    print(f'данные передались - {project} {stavka} {date_start} {date_end} {time_of_work} {user_name} {user_second_name} {user_surname} {user_email} {user_town} {type_of_worker}')
    print('>>> Подключение к JIRA...')
    #jira = JIRA(server='https://jira.i-sol.eu', basic_auth=('tcontrol', '1voUP1')) #старая 
    jira = JIRA(server='https://jira-new.i-sol.eu', basic_auth=('tcontrol', 'jiOZINsQ6pgA')) #новая

    # ------------------------ Ввод ФИО---------------------
    date1 = date_start
    date2 = date_end
    # Преобразуем строку в объект datetime
    date_obj1 = datetime.strptime(date1, "%Y-%m-%d")
    date_obj2 = datetime.strptime(date2, "%Y-%m-%d")
    date1 = date1.replace('.', '/')
    date2 = date2.replace('.', '/')
    # Преобразуем объект datetime в нужный формат
    """ date1 = date_obj1.strftime("%d/%m/%Y")
    date2 = date_obj2.strftime("%d/%m/%Y") """

    date1 = date_obj1.strftime("%Y-%m-%d")
    date2 = date_obj2.strftime("%Y-%m-%d")

    datedelta = date.today() - timedelta(70)            # установка дельты для даты в днях для сокращения выгрузки данных из джира
    datedelta = datedelta.strftime("%Y-%m-%d")
    print(date1)
    print(date2)
    print(datedelta)

    print('OK')

    #--------------------------------- проверка есть внутри ИП другие участники -----------------------
    print('>>> Выгрузка дынных из JIRA...')
    new_name = check_structure_ip(f'{user_surname} {user_name} {user_second_name}')
    if new_name == 'нет совпадения':  # проверяем есть ли ФИО в базе ИП и переключаемся на другое ФИО если находим
        name_for_jira1 = f'{user_name} {user_surname}'
        name_for_jira1 = name_for_jira1.replace(' ', '').replace('ё', 'е')
        name_user = name_for_jira1
    else:
        name_user = new_name

    name_user = name_user.replace(" ", "")
    name_for_jira2 = f'{user_surname} {user_name}'
    name_for_jira2 = name_for_jira2.replace(' ', '').replace('ё', 'е')
    print(name_user)
    name_project = ''
    lead_email = ''
    lead = ''

     # ----------------------- получение задач проекта-----------------------
    all_project = jira.projects()                   #получение всех проектов
    pa ="".join(c for c in project if c.isalnum()) # удаление всех символов кроме букв и цифр
    pa = pa.replace(' ', '').lower()       #форматирование project
    for p in range(len(all_project)):
        #n = all_project[p].name.replace(' ', '').replace(':', '').replace(',', '').replace('.', '').replace('-', '').lower()
        n = "".join(c for c in all_project[p].name if c.isalnum()) # удаление всех символов кроме букв и цифр
        n = n.lower()
        if pa == n:                                 #если наименование проекта найдено
            name_project = all_project[p].key
            lead = jira.project(name_project).lead.displayName      #определение и присвоение имени руководителя проекта
            #print(get_lead_email(lead))
            lead_email = get_lead_email(lead)
            project_jira = n
            print(f'{name_project}  Руководитель проекта - {jira.project(name_project).lead.displayName}')
            #------------------------------------ перестановка имени и фамилии для второй проверки поиска РП
            if lead_email == '' or lead_email == 'нет совпадения':
                mas_lead_FIO = lead.split(' ')
                lead_name_first = mas_lead_FIO[1] + ' ' + mas_lead_FIO[0]
                #lead_name_first = lead_name_first.replace(' ', '')
                lead_name_first = lead_name_first.replace('ё', 'е')
                #print (lead_name_first)
                lead_email = get_lead_email(lead_name_first)
    print(lead_email)

    if name_project != '':                          #если наименование проекта найдено
        
            issues_in_proj = []
            # в следующей строке падает бот если группа пользователей не добавлена к проекту, поэтому нужно обработать исключение
            issues_in_proj = jira.search_issues(f'project={name_project} and updated > {datedelta}', maxResults=900)
            #proj = jira.project(name_project)
            #project_jira = proj.name

            #print(proj.name)  # имя проекта
            #print(issues_in_proj)
            #print(len(issues_in_proj))

            # ----------------------- поиск задач в которых есть ФИО-----------------------
            total_time_jira = 0
            for j in range(len(issues_in_proj)):   
                x = jira.worklogs(issue=issues_in_proj[j])

                time1 = 0
                author = '-'

                #print(issues_in_proj[j])
                for i in range(len(x)):

                    try: # для новой джиры пока попадаются учетки без атрибута display.name
                        author = x[i].author.displayName   # было author = x[i].updateAuthor.displayName
                        if author.count(' ') == 2:          # проверка если в имени 2 пробела, т.е. указали отчество
                            author = author.rsplit(' ', 1)[0] # удаление последнего слова в строке
                        str1 = author.replace(" ", "")
                        str1 = str1.replace("ё", "е")
                        index = x[i].started.split('T')  # разделение даты от времени
                        #print(index[0])
                        #print(index[1])
                        #date_jira = datetime.strptime(index[0], "%Y-%m-%d")  # дата джиры
                        date_jira = index[0] # дата джиры
                        time2 = x[i].timeSpentSeconds
                        #print(f'{str1} === {name_for_jira2} // {date1} === {date_jira} // {date2} === {date_jira} // {time2/3600}')
                        
                        if (str1 == name_user or str1 == name_for_jira2) and date1 <= date_jira and date2 >= date_jira:
                            #print(x[i].started)
                            #print(index)
                            #print(x[i].id)
                            #print(x[i].timeSpentSeconds)
                            #print(x[i].updateAuthor)
                            #print(x[i].comment)
                            time1 = x[i].timeSpentSeconds + time1
                    except:
                        pass

                #print(time1/3600)
                #print(j)

                total_time_jira = total_time_jira + time1


            total_time_jira = format(total_time_jira / 3600, '.2f')
            
            print('Трудозатраты в джире = ', total_time_jira)
            print('OK')

            # ----------------------------------------- проверка данных ------------------------------------
            print('>>> Проверка данных...')
            result_verific = []
            result_verific = verific(time_of_work, total_time_jira, date1, date2, stavka)
            print(result_verific)
            print('ОК')
            name_origin = f'{user_surname} {user_name} {user_second_name}'
            #------------------------------------------- создание документа -----------------------------------
            if result_verific[1] == 1:
                path_act = create_docx(number_act, user_town, name_origin, number_contact, date_contact, project, name_of_work, result_of_work, date_start, date_end, stavka, result_verific[2], time_of_work, type_of_worker)
                status = 'Complete'
                text_message = result_verific[0]
                # ----------------------------------------- отправка сообщения ------------------------------------
                print('>>> Отправка сообщения...')
                send_message(text_message, name_origin, path_act, number_act, result_verific[2] , result_verific[1], type_of_worker, project,user_email, lead_email)
                print('ОК')
            """ else:
                status = 'Error' """
                
            if result_verific[1] == 0:
                status = 'Error'
                text_message = result_verific[0]
                # ----------------------------------------- отправка сообщения ------------------------------------
                print('>>> Отправка сообщения...')
                send_message(text_message, name_origin, '', number_act, '' , result_verific[1], type_of_worker, project,user_email, lead_email)
                print('ОК')
            
    if name_project == '':  # если наименование проекта не найдено
        status = 'Error'
        text_message = 'Указанный проект не найден в JIRA. Наименование проекта должно соответствовать наименованию в Jira.'
        send_message(text_message, '', '', '', '', 0, '', '', '', lead_email)
        print('>>> Проект не найден, сообщение отправлено')
            
    
    return [status, text_message]
    name_origin = ''
    name1 = ''
    name2 = ''
    name3 = ''
    number_act = ''
    type_of_worker_origin = ''
    type_of_worker_formated = ''
    town = ''
    number_contract = ''
    date_contract = ''
    stavka = ''
    project_original = ''
    project_formated = ''
    name_of_work = ''
    result_of_work = ''
    date_start = ''
    date_end = ''
    time_of_work = ''
    flag_date_contract=flag_name=flag_date_end=flag_date_start=flag_name_of_work=flag_number_contract=flag_number_act=flag_town=flag_result_of_work=flag_project=flag_stavka=flag_time_of_work=flag_type_of_worker = 0
    flag_exit_from_cicle = 0 # флаг для выхода из цикла
    tipe_of_act = 0
    text1 = text2 = text3 = text4 = text5 = text6 = text7 = text8 = text9 = text10 = text11 = text12 = text13 = ''


    
