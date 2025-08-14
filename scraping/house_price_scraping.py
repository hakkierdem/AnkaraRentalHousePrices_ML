from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

data = []

for count in range(1,51):

    url = "https://www.example.com/" + str(count)

    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.text,"lxml")

    announcements = soup.find_all("div",class_ = "styles_contentWrapper__HHxxw")

    for announcement in announcements:
        
        try:

            county,neighborhood = announcement.find("span",class_ = "styles_location__ieVpH").text.split(" - ")
            name,room_num,floor,m2 = announcement.find("div",class_ = "styles_quickinfoWrapper__F5BBD").text.split(" | ")
            
            if room_num == "1 Oda" or room_num == "Stüdyo":
                room_num = "1+0"

            room,saloon = room_num.split("+")
            price = announcement.find("span",class_ = "styles_price__8Z_OS").text.replace("TL","")
            
            if name == "Daire":
                data.append({
                    "County" : county,
                    "Neighborhood" : neighborhood,
                    "Room" : float(room),
                    "Saloon" : int(saloon),
                    "m2" : int(m2.replace(" m²","")),
                    "Price" : int(price.replace(".",""))
                    })
                
        except Exception as e:
            print("Error: ",e)
            continue
        
    time.sleep(1)

df = pd.DataFrame(data)

df.to_csv("ankara_house_prices.csv")
        