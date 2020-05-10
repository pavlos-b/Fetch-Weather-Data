import requests
from bs4 import BeautifulSoup
from collections import namedtuple

def get_url():
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 
    # to search 
    city = input("For which city would you like to know the current weather? ")
    query = city + " weather bbc"
    results = []  
    for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
        results.append(j)
    return(results[0])

def get_weather(href):
    r = requests.get(href)
    soup = BeautifulSoup(r.text, 'html.parser')  
    Weather = namedtuple('Weather','temperature humidity visibility observations city')
    results = soup.find_all('span', attrs={'class':'wr-hide-visually'})
    temperature = results[-7].contents[0]
    city = results[-8].contents[0][3:]
    results_2 = soup.find_all('li', attrs={'class':'wr-c-station-data__observation gel-long-primer gs-u-pl0 gs-u-mv--'})
    humidity = results_2[0].contents[1][1:]
    visibility = results_2[1].contents[1][1:]
    results_3 = soup.find_all('span', attrs={'class':'wr-c-observations__timestamp gel-long-primer gs-u-mt--'})
    obsv_time = results_3[0].find('p').text[0:-2]
    obsv_day = results_3[0].find_all('p')[1].text
    observations = obsv_time + ' ' + obsv_day
    data = Weather(temperature = temperature, humidity = humidity, visibility = visibility, observations = observations, city = city)
    return data

def print_weather(data):
    print('Current weather data from station {}'.format(data.city) + ":")
    print("Temperature: " + data.temperature + "\nHumidity: " + data.humidity + "\nVisibility: " + data.visibility + "\nObservations: " + data.observations)

def main():
    href = get_url()
    data = get_weather(href)
    print_weather(data)

if __name__ == "__main__":
    main()