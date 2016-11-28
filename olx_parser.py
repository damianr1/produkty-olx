from bs4 import BeautifulSoup
from time import gmtime, strftime
import requests
import csv
import pandas as pd
import os.path
from apscheduler.schedulers.blocking import BlockingScheduler


# task that will run each hour (or nother const time)
def check_views():
    results = []
    # for i in range(1, page_count(adress)):
    for i in range(1, 2):
        request = requests.get("http://www.olx.pl/uslugi-firmy/piaseczno/?page=" + str(i))
        soup = BeautifulSoup(request.text, "html.parser")

        for link in soup.findAll('a', {'class': 'marginright5'}):
            url = link['href']

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


scheduler = BlockingScheduler()
scheduler.add_job(check_views, 'interval', minutes=2)
scheduler.start()


def save_to_csv(array):
    if os.path.isfile('OLX_actual_hour.csv'):
        writer = csv.writer('OLX_actual_hour.csv', quoting=csv.QUOTE_NONNUMERIC)
        for item in array:
            writer.writerow(item)
        df = pd.read_csv('OLX_actual_hour.csv')
        df.to_csv('OLX_one_hour_ago.csv', index=False)
        f = open("OLX_actual_hour.csv", "w")
        f.truncate()
        f.close()


# sprawdzanie liczby stron - zrobił Dominik
def page_count(adress):
    import requests
    r = requests.get(adress)
    dest=r.history[0].headers['Location']
    return dest.split('?page=')[1]


