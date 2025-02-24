from datetime import date


def verific(time_act, total_time_jira, date1, date2, stavka):
    global flag_time
    global flag_OK
    flag_OK = 0             #флаг если все проверки успешны примет 1
    flag_time = 0
    time_act = time_act.replace(',', '.')
    time_act = format(float(time_act), '.2f')
    if time_act == total_time_jira:
        flag_time = 1
        #text1 = 'Трудозатраты - Верно \n\n'
        text1 = ''
        cost_for_act = format(float(stavka) * float(time_act), '.2f')  #расчет стоимости проекта
    else:
        text1 = 'Проверьте введенные трудозатраты. В JIRA заведено - ' + total_time_jira + ' ч.) \n\n'


    # ---------------- проверка периода проверки----------------------------------------------------
    global flag_period
    flag_period = 0

    if date1 <= date2:
        flag_period = 1
        text11 = ''
    else:
        text11 = 'Дата начала оказания услуг старше даты окончания оказания услуг \n\n'
        text1 = ''

#------------------------формирование текста сообщения------------------------------------------
    if flag_time == 1 and flag_period == 1:
        text_message = 'Завершена роботизированная проверка данных за отчетный период.\nРезультат обработки: Согласовано.' + '\n\n' + 'Сформированные акт и заявка во вложении.'
        flag_OK = 1
    else:
        text_message = '' + text1 + text11 +''
    
    if flag_OK == 1:
        return [text_message, flag_OK, cost_for_act]
    if flag_OK == 0:
        return [text_message, flag_OK]