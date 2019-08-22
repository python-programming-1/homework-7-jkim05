#!/usr/bin/env python
# coding: utf-8

# In[180]:


import os
import requests
from bs4 import BeautifulSoup

url_base = 'https://www.gocomics.com'
url_pbs = url_base + "/pearlsbeforeswine"

# get the main website's pearls before swine (pbs) page
req_pbs = requests.get(url_pbs)
req_pbs.raise_for_status()
soup_pbs = BeautifulSoup(req_pbs.text)

# go to the latest released comic for pbs
get_comics_link = soup_pbs.find_all(name="a", attrs={"data-link": "comics"})
comics_url = url_base + get_comics_link[0]["href"]
req_comics = requests.get(comics_url)

######## START 10x LOOP HERE #########
i = 1
while i <= 10:
    # find the comic url
    latest_soup_pbs = BeautifulSoup(req_comics.text)

    image_url = latest_soup_pbs.select("picture.item-comic-image")[0].contents[0].get('src') + ".png"
    image_req = requests.get(image_url)

    # save the image

    image_file = open(os.path.basename(image_url), 'wb') # save just the file image
    for chunk in image_req.iter_content(100000):
        image_file.write(chunk)
    image_file.close()

    # go to the previous day's comic
    back_button_url = url_base + latest_soup_pbs.select("div .gc-calendar-nav__previous")[0].contents[3].get('href')
    back_button_req = requests.get(back_button_url)
    
    # update the url for the variable "req_comics"
    req_comics = requests.get(back_button_url)
    
    # add to i so that it only loops 10 times
    i += 1


# In[ ]:




