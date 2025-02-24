
import smtplib                                      # Импортируем библиотеку по работе с SMTP
import os
import time
# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
import mimetypes                                          # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                # Импортируем энкодер
from email.mime.base import MIMEBase                      # Общий тип
from email.mime.text import MIMEText                      # Текст/HTML
from email.mime.image import MIMEImage                    # Изображения
from email.mime.audio import MIMEAudio                    # Аудио
from datetime import date, datetime




def send_message(text, name_act, path, number_act, total_cost, flag_OK, type_of_act, project_act, user_email, lead_mail):
    init_otladka = 1
    sender_email = user_email  # почта отправителя
    if sender_email == lead_mail:                   # проверка, если исполнитель = РП, то удаляем почту РП чтобы не дублировать письмо
        lead_mail = ''
    msg = MIMEMultipart()  # Создаем сообщение
    addr_from = "actbot@i-sol.ru"                       # Адресат

    if init_otladka == 1:
        #addr_to = "aleksandr.gusev@i-sol.ru"              # Получатели
        addr_to = "actbot@i-sol.ru"                             # Получатель
        if flag_OK == 1:
            msg['Subject'] = 'Акт согласован - ' + name_act + ' (' + project_act + ')' + f"{lead_mail}"  # Тема сообщения
        if flag_OK != 1:
            msg['Subject'] = f'Результат роботизированной проверки данных за отчетный период {lead_mail}'  # Тема сообщения
            time.sleep(2)                                           #Задержка
            password = "Parol1!"                                  # Пароль

            #msg = MIMEMultipart()                               # Создаем сообщение
            msg['From'] = addr_from                          # Адресат
            msg['To'] = addr_to                            # Получатель
            body = text
            msg.attach(MIMEText(body, 'plain'))                 # Добавляем в сообщение текст Тут нужно добавть лог, что такой-то пытается отправить данные, но у него такая то ошибка. 
            server = smtplib.SMTP('mail.flexcloud.ru', 587)           # Создаем объект SMTP
            server.set_debuglevel(True)                             # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
            server.starttls()                                       # Начинаем шифрованный обмен по TLS
            server.login(addr_from, password)                       # Получаем доступ
            server.send_message(msg)                                # Отправляем сообщение
            server.quit()                                           # Выходим
            time.sleep(3)                                           # Задержка
            return True
    else:
        pass
        """ if flag_OK == 1:
            msg['Subject'] = 'Данные согласованы - ' + name_act + ' (' + project_act + ')'  # Тема сообщения
            addr_to = "actbot@i-sol.ru" + ',' + f'{sender_email}' + ',' + f'{init_email_send()[0]}' + ',' + f'{init_email_send()[1]}' + ',' + f'{init_email_send()[2]}' + ',' + f'{init_email_send()[3]}' + ',' + f'{lead_mail}'
            #addr_to = "actbot@i-sol.ru" + ',' + f'{sender_email}' + ',' + f'{init_email_send()[0]}' + ',' + f'{init_email_send()[1]}' + ',' + f'{init_email_send()[2]}' + ',' + f'{init_email_send()[3]}' # для теста
        if flag_OK != 1 and flag_OK != 2:
            msg['Subject'] = 'Результат роботизированной проверки данных за отчетный период'  # Тема сообщения
            addr_to = "actbot@i-sol.ru" + ',' + f'{sender_email}' + ',' + f'{init_email_send()[1]}'
        if flag_OK == 2: # случай когда группа пользователей не добавлена к проекту
            msg['Subject'] = 'Результат роботизированной проверки данных за отчетный период'  # Тема сообщения
            addr_to = "actbot@i-sol.ru" """
        # addr_to = "actbot@i-sol.ru"                             # Получатель
    time.sleep(2)                                           #Задержка
    password = "Parol1!"                                  # Пароль

    #msg = MIMEMultipart()                               # Создаем сообщение
    msg['From'] = addr_from                          # Адресат
    msg['To'] = addr_to                            # Получатель

    #if flag_OK == 1:
        #msg['Subject'] = 'Акт согласован - ' + name_act + ' (' + project_act + ')'     # Тема сообщения
    #else:
        #msg['Subject'] = 'Результат роботизированной проверки акта'                    # Тема сообщения
    body = text
    msg.attach(MIMEText(body, 'plain'))                 # Добавляем в сообщение текст

    filepath = path  # Имя файла в абсолютном или относительном формате
    filename = os.path.basename(filepath)  # Только имя файла


    #print(get_sender(path, object_senders))

    if path.find('.docx') != -1:                                    # если отправляем docx
        ctype, encoding = mimetypes.guess_type(filepath)            # Определяем тип файла на основе его расширения
        if ctype is None or encoding is not None:                   # Если тип файла не определяется
            ctype = 'application/octet-stream'                      # Будем использовать общий тип
        maintype, subtype = ctype.split('/', 1)                     # Получаем тип и подтип
        if maintype == 'text':                                      # Если текстовый файл
            with open(filepath) as fp:                              # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)         # Используем тип MIMEText
                fp.close()                                          # После использования файл обязательно нужно закрыть
        else:                                                       # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)                  # Используем общий MIME-тип
                file.set_payload(fp.read())                         # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)                        # Содержимое должно кодироваться как Base64
        today_date = date.today() 
        currentDate = datetime.strftime(today_date, "%d-%m-%y")  # сегодняшняя дата
        if flag_OK == 1:
            if type_of_act == 0:
                file.add_header('Content-Disposition', 'attachment', filename=f'ИП {name_act} - Акт № {number_act} от {currentDate}г. ({total_cost}).docx')  # Добавляем заголовки
            if type_of_act == 1:
                file.add_header('Content-Disposition', 'attachment', filename=f'{name_act} - Акт № {number_act} от {currentDate}г. ({total_cost}).docx')  # Добавляем заголовки
        else:
            file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
        msg.attach(file)                                            # Присоединяем файл к сообщению

        server = smtplib.SMTP('mail.flexcloud.ru', 587)           # Создаем объект SMTP
        server.set_debuglevel(True)                             # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
        server.starttls()                                       # Начинаем шифрованный обмен по TLS
        server.login(addr_from, password)                       # Получаем доступ
        server.send_message(msg)                                # Отправляем сообщение
        server.quit()                                           # Выходим
        time.sleep(3)                                           # Задержка
        try:
            os.remove(filepath)                                     # удаление акта после отправки
            
        except:
            print('Ошибка - файл поврежден, удалить не удалось!')
    