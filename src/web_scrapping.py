from bs4 import BeautifulSoup
import re
import requests
from datetime import date 
import logging

def find_between( s, first, last ):
    '''
    find the substring of s between first and last
    @param s: a string
    @param first: a substring of s
    @param last: a substring of s
    @return a substring of s
    '''
    try:
        start = s.index(first) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except:
        return None

def box_office_str_to_number(box_office):
    '''
    convert a box_office string to a number
    @param box_office: a string
    @return a number correspoing to the content of box_office string
    '''
    try:
        number=float(re.sub('[^0-9.]', '', box_office))
        if ("million" in box_office):
            logging.info('successfully get the box office for this movie')
            return number*(10**6)
        elif ("billion" in box_office):
            logging.info('successfully get the box office for this movie')
            return number*(10**9)
        else:
            logging.info('successfully get the box office for this movie')
            return number
    except:
        print("can't convert from box_office_string to number")
        logging.warning("fail to get box office value because can't convert from box_office_string to number")
        return None
    
def birthday_to_age(birthday):
    '''
    convert a birthday string to a number
    @param birthday: a string
    @return a number correspoing to the content of birthday string
    '''
    l=birthday.split('-')
    year=int(l[0].lstrip("0"))
    month=int(l[1].lstrip("0"))
    day=int(l[2].lstrip("0"))
    today = date.today()
    born=date(year, month, day)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
def find_movie_info(url):
    '''
    scrap the information from the url of a movie
    @param url: a string
    @return a triple (movie_name,box_office,actors)
    '''
    try:
        path_prefix="https://en.wikipedia.org"
        r=requests.get(url).text
        soup=BeautifulSoup(r,"html.parser")
    except:
        logging.debug('cannot be parsed because url the url is invalid')
        return None
    table=soup.find("table",{"class": "infobox vevent"})
    #table=soup.find("table",{"class": "infobox biography vcard"})
    try:
        movie_name=table.find("th").text
    except:
        logging.warning("can't be parsed because can't find the info table for this movie page")
        return None
    box_office_text=None
    try :
        box_office_text=table.find("th",string=re.compile("Box office")).find_next().text
    except:
        print("no box office information")
        logging.warning("can't be parsed because there is no box office information for this movie page")
        return None
    if (find_between(box_office_text, "$","[")!=None):
        box_office=find_between(box_office_text, "$","[")
    elif (find_between(box_office_text, "$","(")!=None):
        box_office=box_office=find_between(box_office_text, "$","(")
    else:
        logging.warning("fail to get box office value because can't find box_office string in the correct format")
        return None
    try:
        box_office=box_office_str_to_number(box_office)
    except:
        return None
    try:
        actor_table=table.find("th",string=re.compile("Starring")).find_next()
    except:
        logging.warning("fail to be parsed because there is no starring information for this movie page")
        return None
    rows=actor_table.find_all("li")
    actors={}
    for row in rows:
        try:
            actor_info=row.find('a')
            actors[actor_info['title']]=path_prefix+actor_info['href']
            #print("can't parse this actor")
        except:
            continue
    if (not actors):
        return None
    else:
        return (movie_name,box_office,actors)

def find_actor_info(url):
    '''
    scrap the information from the url of an actor
    @param url: a string
    @return a triple (actor_name,age,films)
    '''
    try:
        r=requests.get(url).text
        soup=BeautifulSoup(r,"html.parser")
    except:
        logging.debug('cannot be parsed because url the url is invalid')
        return None
    table=soup.find("table",{"class": "infobox biography vcard"})
    if (table==None):
        table=soup.find("table",{"class": "infobox vcard"})
        if (table==None):
            print("no info table for the actor")
            logging.warning("fail to be parsed because there is no info table for this actor page")
            return None
    #name
    actor_name=None
    try:
        actor_name=table.find("th").text
    except:    
        logging.warning("fail to be parsed because can't get actor name for this actor")
        return None
    #age
    age=""
    try:
        birthday=table.find("th",string=re.compile("Born")).find_next().find("span",{"class": "bday"}).text
        age=birthday_to_age(birthday)
        logging.info('successfully get the age for this actor')
    except:
        logging.warning("fail to be parsed because can't get age for this actor")
        return None
    films=extract_movies_1(soup)
    if (films==None):
        films=extract_movies_2(soup)
        if (films==None):
            logging.warning("fail to be parsed because can't get filmography for this actor")
            return None
    
    return (actor_name,age,films)

def web_scrapping(url,actor_no,movie_no):
    '''
    web scrapping at least actor_no actor pages and movie_no movie pages. start from the given url
    @param url: a string
    @return a tuple (actors,movies)  
    '''
    i=0
    j=0
    movie_links=[]
    actor_links=[url]
    actors=[]
    movies=[]
    processed_links=[]
    while (len(movie_links)+len(actor_links)>0):
        if (i>actor_no and j>movie_no):
            break;
        if (len(movie_links)>0 and (len(movie_links)<len(actor_links) or len(actor_links)==0)):
            link=movie_links.pop()
            if (link in processed_links):
                continue
            print("movie link: ",link)
            j=j+1
            movie_info=find_movie_info(link)
            if (movie_info==None):
                j=j-1
                continue
            processed_links=processed_links+[link]
            actor_links=list(movie_info[2].values())+actor_links
            movies.append(movie_info)
        else:
            link=actor_links.pop()
            if (link in processed_links):
                continue
            print("actor link: ",link)
            i=i+1
            actor_info=find_actor_info(link)
            if (actor_info==None):
                i=i-1
                continue
            processed_links=processed_links+[link]
            movie_links=extract_links(actor_info)+movie_links
            actors.append(actor_info)
    return (actors,movies)  


def extract_movies_1(soup):
    '''
    helper function for find_actor_info. get the information from type1 table
    @param soup: bs4 object
    @return a dictionary of films   
    '''
    path_prefix="https://en.wikipedia.org"
    table=soup.find("table",{"class": "infobox biography vcard"})
    if (table==None):
        table=soup.find("table",{"class": "infobox vcard"})
        if (table==None):
            return None
    #Filmography
    film_table=None
    rows=None
    try:
        film_table=soup.find("span",{"id": "Filmography"}).find_next().find_next().find_next()
        rows=film_table.find_all("li")
    except:
        return None
    films={}
    for row in rows:
        try:
            year=(int)(find_between(row.text,'(', ')'))
        except:
            continue
        film_info=row.find('a')
        if (film_info==None):
            continue
        title=film_info['title']
        link=path_prefix+film_info['href']
        if year in films:
            films[year]=films[year]+[(title,link)]
        else:
            films[year]=[(title,link)]
    if (not films):
        return None
    else:
        return (films)
    
def extract_movies_2(soup):
    '''
    helper function for find_actor_info. get the information from type2 table
    @param soup: bs4 object
    @return a dictionary of films   
    '''
    path_prefix="https://en.wikipedia.org" 
    #Filmography
    rows=None
    try:
        rows=soup.find("span",{"id": "Film"}).find_next("table").find_all("tr")
    except:
        return None
    films={}
    for row in rows:
        tds=row.find_all("td")
        flag=0
        year=-1
        for td in tds:
            if (flag==0):
                try:
                    year=(int)(td.text)
                except:
                    #print("no year for the movie")
                    break
                flag=1
            else:
                try:
                    if year in films:
                        films[year]=films[year]+[(td.find('a')["title"],path_prefix+td.find('a')["href"])]
                    else:
                        films[year]=[(td.find('a')["title"],path_prefix+td.find('a')["href"])]
                    break;
                except:
                    continue
    if (not films):
        return None
    else:
        return films

#helper function to for web_scrapping
def extract_links(actor_info):
    movie_info=(list)(actor_info[2].values())
    movie_links=[]
    for movies in movie_info:
        movies_of_the_year=[]
        for movie in movies:
            movies_of_the_year=movies_of_the_year+[movie[1]]
        movie_links=movie_links+movies_of_the_year
    return movie_links