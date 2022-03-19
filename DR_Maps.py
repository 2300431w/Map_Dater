import numpy as np
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from PIL import Image
import io
import cv2



#rand1 = random.randint(0,9999)
#rand2 = random.randint(0,9999)
#url = f"https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~34{rand1}~9010{rand2}"
#print(url)
#url = "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~340612
#~90108865"

while True:
    searching = True
    while searching == True:
        url = "http://www.davidrumsey.com/luna/servlet/as/fetchMediaSearch?&sort=Pub_List_No_InitialSort%2CPub_Date%2CPub_List_No%2CSeries_No&lc=RUMSEY%7E8%7E1&fullData=true&bs=25&random=true&os=0&callback=updateQueue"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        #print(html)
        if "David Rumsey Historical Map Collection" in html:
            if html.count("Atlas map") > 0:
                jpg_index = html.find('.jpg')
                #print()
                image_url = html[jpg_index-100:jpg_index].split('"')[-1] + ".jpg"
                if "RUMSEY~8~1" in image_url:
                    searching = False
    print("map count:", html.count("Atlas map"))
    image_url = html[jpg_index-100:jpg_index].split('"')[-1] + ".jpg"
    print(image_url)
    date_index = html.find('pub_date')
    print(date_index)
    date_line = html[date_index:date_index+20]
    date = int(date_line[-7:-3])
    print(date)

    img_data = requests.get(image_url).content

    print("got img data")
    img = Image.open(io.BytesIO(img_data))
    img = img.convert('RGB')
    print("Image in rgb")
    cv2.namedWindow("map", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
    cv2.resizeWindow("map", 720, 540) 
    cv2.imshow('map',np.array(img))
    cv2.waitKey(0)

answer = int(input("What year is this from?"))
if answer == date:
    print("You did it!")
else:
    print(f"You absolute idiot how could you not know it was {date}")
    
"""with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)"""


#soup = BeautifulSoup(html_bytes, 'html.parser')

#print(soup.prettify())

