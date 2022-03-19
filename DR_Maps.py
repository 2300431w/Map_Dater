import numpy as np
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import io
import cv2
import PySimpleGUI as sg
from PIL import Image
from PIL import ImageTk

def get_map(show = False):
    searching = True
    while searching == True:
        url = "http://www.davidrumsey.com/luna/servlet/as/fetchMediaSearch?&sort=Pub_List_No_InitialSort%2CPub_Date%2CPub_List_No%2CSeries_No&lc=RUMSEY%7E8%7E1&fullData=true&bs=25&random=true&os=0&callback=updateQueue"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        if "David Rumsey Historical Map Collection" in html:
            if html.count(" map ") > 0:
                jpg_index = html.find('.jpg')

                image_url = html[jpg_index-100:jpg_index].split('"')[-1] + ".jpg"

                if "RUMSEY~8~1" in image_url:
                    searching = False

    image_url = html[jpg_index-100:jpg_index].split('"')[-1] + ".jpg"
    print(image_url)
    date_index = html.find('pub_date')

    date_line = html[date_index:date_index+20]
    date = int(date_line[-7:-3])


    img_data = requests.get(image_url).content


    img = Image.open(io.BytesIO(img_data))
    img = img.convert('RGB')
    img = img.resize((600,600))
    if show == True:
        cv2.namedWindow("map", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
        cv2.resizeWindow("map", 720, 540) 
        cv2.imshow('map',np.array(img))
        cv2.waitKey(0)
    return(img,date)

def local_app():

    #load_img = Image.open("loading.png")
    #load_img = ImageTk.PhotoImage(image = load_img)
    window = sg.Window(title="Map Dater", layout = [[sg.Text("What year is this from?",size = (20,1),font = ("Arial",18))],
                                                      [sg.Button('NewMap',size = (10,2))],
                                                      [sg.Image(size = (600,600),key = "-MAP-")],
                                                       [sg.Text("Year:"),sg.InputText()],
                                                      [sg.Button('Submit',size = (10,2)),sg.Text('Actual Date:'),sg.Text('',size = (20,1),font = ("Arial",18),key = '-DATE-')],
                                                    [sg.Text("Score: ",key = "-SCORE-",size = (20,1),font = ("Arial,24"))]])

    n = 0
    score = 0
    while True:
        n += 1
        event,values = window.read()
        window['-SCORE-'].update(f"score: {score}")
        
        print(event,values)
        if event == sg.WIN_CLOSED:
                break
        elif event == "NewMap":
            #load_img = ImageTk.PhotoImage(image = load_img)
            #window['-MAP-'].update(data=load_img)
            img,date = get_map()
            #img = Image.fromarray(img,'RGB')
            image = ImageTk.PhotoImage(image = img)
            window['-MAP-'].update(data=image)
            #window['-DATE-'].update(str(date))
            
        elif event == "Submit":
            guess = int(values[0])
            add = 100 - np.abs(date - guess)
            window['-DATE-'].update(str(date))
            print(f'Date: {date}, Guess: {guess}, diff: {np.abs(date - guess)}')
            if add >= 0:
                score += add

                
            else:
                add = 0
                score += add
            print("score: ",score)
            window['-SCORE-'].update(str(score))
            #load_img = ImageTk.PhotoImage(image = load_img)
            #window['-MAP-'].update(data=load_img)
            img,date = get_map()
            #img = Image.fromarray(img,'RGB')
            image = ImageTk.PhotoImage(image = img)
            window['-MAP-'].update(data=image)
            
        
    window.close()
local_app()
