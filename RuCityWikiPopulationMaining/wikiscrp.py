
# coding: utf-8

# In[6]:


#Подгрузка библиотек:
import requests
import re
from lxml import html
from bs4 import BeautifulSoup

#Основная часть программы работает напрямую, чтение ссылок из файла использовалось при отладке
#Работаем с файлами (1) или напрямую (0):
work_with_file = 0


# In[7]:


#Выдергиваем ссылки
#Пишем их в список (url_lst) или в файл (links.txt), таблицу разбираем на строки и выбираем элементы выравненные влево (align:left)
#так как таких элементов несколько, искомый элемент каждый третий (видно из структуры таблицы)

url_lst=[]

links_url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8"
r = requests.get(links_url).text

url_soup = BeautifulSoup(r, "lxml")
url_data = url_soup.find('table').find_all('td', {'align':'left'})

for i in range(0,len(url_data),3):
#Вывод ссылок в массив:
    if work_with_file == 0:
        url_lst.append(url_data[i].find('a').get('href'))
#Вывод ссылок в файл:    
    else:
        with open('links.txt','a') as out_file:
            out_file.write(url_data[i].find('a').get('href'))
            out_file.write('\n')     


# In[ ]:


#Поиск минимального года, можно запустить один раз, потому что долго
reqtable = "Численность населения"
min_year = 2017
wiki_url = "https://ru.wikipedia.org"
i=0
#Пробежимся по всем страницам:
for cities in range(0,len(url_lst),1):
    
    url = wiki_url+url_lst[cities]
    r = requests.get(url).text

#Так как у таблицы с численностью населения нет отдельного идентификатора, то ищем все таблицы (find_all)
#и просматриваем их заголовки ('th'), на случай если у таблицы нет заголовка, вводим дополнительное условие (!=None)
#для того чтобы избежать ошибки обращения .text к None, затем определяем наименьший год (find и re.match)
#и сравниваем его с ранее найденным минимальным годом, для наглядности во время поиска выводится строка из '-'
#Результат выполнения функции минимальный год (min_year) и количество пройденных ссылок (i)

    min_soup = BeautifulSoup(r, "lxml")
    min_datas = min_soup.find_all('table', {'class':"standard"})
    
    for min_data in min_datas:
        mtable_name = min_data.find('th')
        
        if mtable_name != None and mtable_name.text == reqtable:
            i=i+1
            min_year_new = min_data.find('tr', {'class': 'bright'}).find('th').text
            min_year_new = int(re.match('\d\d\d\d', min_year_new).group())
            print('-', end = '')
            
            if min_year_new < min_year:
                min_year = min_year_new
            break
            
print("Минимальный год:", min_year,',',"Количество обработанных ссылок:",i)


# In[ ]:


reqtable = "Численность населения"
title =    "city/year"
min_year    = 1500
recent_year = 2017

tab_counter = 0 #Cчетчик таблиц

wiki_url = "https://ru.wikipedia.org"
#year_lst=[]
#data_lst=[]
city_lst=["city/year"]
first_city    = 0 #В целях отладки (чтобы проще было разобраться с проблемными городами)
num_of_cities = len(url_lst)
num_of_years  = len([0 for i in range(min_year,recent_year+1,1)])
#Сгенерируем список:
result = [[0 for i in range(0,num_of_years,1)] for j in range(first_city,num_of_cities+1,1)]


for i in range(len(result[0])):
    result[0][i] = min_year+i


#Дергаем значения:
for cities in range(first_city,num_of_cities,1):
    t=0
    twintab_counter = 0
    tab_counter     = 0 #Cчетчик таблиц
    
    year_lst=[]
    data_lst=[]
    
    print('*', end = '')
    
    url = wiki_url+url_lst[cities]
#   print(url)
    r = requests.get(url).text
    
    soup = BeautifulSoup(r, "lxml")
    datas = soup.find_all('table', {'class': ["standard","wikitable"]})
    
    num_of_tables = len(datas) #Число таблиц на странице
    
    city = soup.find('h1', {'class':"firstHeading"}).text 
    
#А вот нет у нас таблиц (datas = None и в цикл мы соответсвенно не войдем):  

    if datas == []:
        city_lst.append(city+" (Нет данных)") #Воизбежание повторов
        for column in range(0,num_of_years,1):
                    result[cities-first_city+1][column] = None

    for data in datas: 
        
        mtable_name = data.find('th')

        if mtable_name != None and mtable_name.text == reqtable and twintab_counter == 0:

#ГОРОДА:
            city_lst.append(city) #Воизбежание повторов
#ГОДА:
            items = data.find_all('tr', {'class': 'bright'})
            for item in items:
                years = item.find_all('th')
                for year in years:
                    output = year.text
                    output = re.match('\d\d\d\d', output)
                    
                    if output != None:
                        year_lst.append(int(output.group()))
                    else:
                        break

#ЦИФРЫ:                        
            items = data.find_all('tr', {'align':'center'})
            for item in items:
                peoples = item.find_all('td')
                for people in peoples:
                    output = people.text
                    output = re.sub(r'\D|\s','', output)
                    
                    if output != '':
                        data_lst.append(int(output))
                    else:
                        break
#            print(data_lst)               
#Заносим строки:
            for column in range(0,num_of_years,1):
                if t < len(data_lst) and result[0][column] == year_lst[t]:
                    result[cities-first_city+1][column] = data_lst[t]
                    t=t+1
                else:
                    result[cities-first_city+1][column] = None
             
            twintab_counter = 1
            
#Если таблицы с населением нет:
        else:
            if tab_counter == num_of_tables-1 or datas == None:
                city_lst.append(city+" (Нет данных)") #Воизбежание повторов
                for column in range(0,num_of_years,1):
                    result[cities-first_city+1][column] = None
            else:
                tab_counter = tab_counter+1          


# In[ ]:


#Запись в файл:
with open("output.txt",'w') as ouf:
    
    for cities in range(0, num_of_cities-first_city+1, 1):
        ouf.write(str(city_lst[cities]))
        ouf.write('\t')
        for years in range(0, num_of_years,1):
            ouf.write(str(result[cities][years]))
            ouf.write('\t')         
        ouf.write('\n')

