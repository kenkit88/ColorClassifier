# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup as Soup
import urllib2
import json
import urllib
import lxml
import cv2
import os


def get_links(query_string, num_images):
    links = []
    # step by 100 because each return gives up to 100 links
    for i in range(0, num_images, 100):
        url = 'https://www.google.com/search?ei=1m7NWePfFYaGmQG51q7IBg&hl=en&q='+query_string+'\
&tbm=isch&ved=0ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ&start='+str(i)+'\
&yv=2&vet=10ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ.1m7NWePfFYaGmQG51q7IBg\
.i&ijn=1&asearch=ichunk&async=_id:rg_s,_pms:s'

        request = urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0'})

        json_string = urllib2.urlopen(request).read()

        page = json.loads(json_string)

        html = page[1][1]

        new_soup = Soup(html, 'lxml')

        imgs = new_soup.find_all('img')

        for j in range(len(imgs)):
            links.append(imgs[j]["src"])

    return links



def get_images(links, directory, pre):
    print("Download process will be start...")
    # when start downloads the photo, the photo file name will start with 1.jpg
    pic_num = 1
    length = len(links)
    for i in range(length):
        try:
            urllib.urlretrieve(links[i], "./"+directory+"/"+str(pre)+str(pic_num)+".jpg")
            # info = os.path.join(os.getcwd()+"/woman", str(pre)+str(pic_num)+".jpg")
            # img = cv2.imread(info)
            # #img = cv2.imread(os.getcwd()+"/"+directory+"/" +str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            #print img
            # #print os.getcwd()+"/"+directory+"/" +str(pic_num)+".jpg"
            # resized_image = cv2.resize(img, (100, 100))
            # cv2.imwrite(os.getcwd()+"/woman/"+ str(pre)+str(pic_num)+".jpg",resized_image)
            print "Complete count: " + str(pic_num)
	    #pic_num is the download file, file name cannot be same.
            pic_num += 1

        except Exception as e:
            print str(e)


def search_images(base, terms, num_images):
    print("Image is searching...")
    for y in range(len(base)):
        for x in range(len(terms)):
            all_links = get_links(base[y]+'+'+terms[x], num_images)
	    #"neg" is the file name,you can change it.
            get_images(all_links, "photo", x)

if __name__ == '__main__':
    terms = ["red"]
    print "Search string: " + str(terms)
    base = [""]
    search_images(base, terms, 2000)

