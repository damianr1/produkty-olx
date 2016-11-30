# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import gmtime, strftime
import requests
import csv
import pandas as pd
import os.path
from apscheduler.schedulers.blocking import BlockingScheduler
from shutil import copyfile
import sys
#import importlib

#importlib.reload(sys)
#sys.setdefaultencoding('utf8')

main_page_url = "https://www.olx.pl/uslugi-firmy/kielce/?page="

def save_to_csv(array):
    file_new = sys.argv[1] + 'OLX_actual_hour.csv'
    file_old = sys.argv[1] + 'OLX_one_hour_ago.csv'
    copyfile(file_new, file_old)
    f = open(file_new, "w")
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    for item in array:
        writer.writerow(item)


# sprawdzanie liczby stron - zrobił Dominik
def page_count(address):
    import requests
    r = requests.get(address)
    dest = r.history[0].headers['Location']
    return dest.split('?page=')[1]


# task that will run each hour (or another const time)
def check_views():
    results = []
    #print(page_count(main_page_url + "501"))
    for i in range(1, 130):
    #for i in range(1, 2):
        print("Parsing page no: " + str(i))
        request = requests.get(main_page_url + str(i))
        soup = BeautifulSoup(request.text, "html.parser")

        for link in soup.findAll('a', {'class': 'marginright5'}):
            url = link['href']
            # check only not promoted links
            if ";promoted" not in url:
                # get inside link from main page
                request = requests.get(url)
                soup2 = BeautifulSoup(request.text, "html.parser")

                # find bottom bar div
                bottomBar = soup2.find('div', {'id': 'offerbottombar'})

                # extract children div
                bottomBarChildren = bottomBar.findAll('div', {'class': 'pdingtop10'})
                offer_count = bottomBarChildren[1].text.strip().split('Wyświetleń:', 1)[1]

                # text_with_id example value: 'ID ogłoszenia: 1234423432'
                text_with_offer_id = soup2.find('div', {'class': 'offer-titlebox__details'}).find('small').text

                offer_id = text_with_offer_id.strip().split(" ")[-1]

                results.append([int(offer_id), url, strftime("%Y-%m-%d %H:%M:%S", gmtime()), int(offer_count)])

    save_to_csv(results)

    # create result file (comparing new and old file
    df_actual = pd.read_csv(sys.argv[1] + 'OLX_actual_hour.csv', names=['ID', 'Link', 'Data', 'Liczba_wyswietlen'])
    df_ago = pd.read_csv(sys.argv[1] + 'OLX_one_hour_ago.csv', names=['ID', 'Link', 'Data', 'Liczba_wyswietlen'])
    df = pd.concat([df_actual, df_ago])

    # remove single rows (just added or removed during last hour)
    df = df[df.groupby('ID').ID.transform(len) > 1]

    # unnecessary now
    del df['Data']

    # Ciezko odejmowac wartosci miedzy roznymi wierszami, wspomoglem sie stworzeniem kolumny max i min, aby pozniej stworzyc kolumne z ich roznicy
    df = df.groupby(['ID', 'Link']).Liczba_wyswietlen.agg(['max', 'min'])
    df['Liczba_wyswietlen'] = df['max'] - df['min']

    # unnecessary to result
    del df['max']
    del df['min']

    # sort by 10 best results and save
    df = df.sort_values(['Liczba_wyswietlen'], ascending=[False])
    df2 = df[0:10]
    df2.to_csv(sys.argv[1] + 'Top_10.csv', header=False)
    df2.to_html(sys.argv[1] + 'index.html', header=False)

scheduler = BlockingScheduler()
scheduler.add_job(check_views, 'interval', minutes=15)
scheduler.start()
#check_views()


# if os.path.isfile('OLX_actual_hour.csv'):
#    writer = csv.writer('OLX_actual_hour.csv', quoting=csv.QUOTE_NONNUMERIC)
#    for item in array:
#        writer.writerow(item)




