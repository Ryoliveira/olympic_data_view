import json
import sqlite3
import requests
from bs4 import BeautifulSoup as BS
import time


def get_page():
    """Fetches all country names and corresponding links"""
    page = requests.get('https://www.olympic.org/pyeongchang-2018/results/en/general/nocs-list.htm')
    soup = BS(page.content, 'lxml')
    countries = [name.text for name in soup.find_all('strong', class_="center-block")]
    links = [link.get('href') for link in soup.findAll('a', class_='center-block')]
    link_data = tuple(zip(countries, links))
    return link_data


def get_data(country):
    """Fetches sports and total athletes for country"""
    sports = []
    country_page = requests.get('https://www.olympic.org/pyeongchang-2018/results/' + country[1][6:])
    page_soup = BS(country_page.content, 'lxml')
    stats = page_soup.find('table', class_='ResTableFull')
    rows = stats.find_all('tr')
    for row in rows[1:]:
        sport = row.find('td').text.strip()
        if sport != 'Total':
            sports.append(sport)
        else:
            total = row.find_all('b')
            total_athlete = total[1].text.strip()

    return sports, total_athlete


def create_tables(cur):
    """Create tables country to store all country names, total athletes and corresponding sports
       create table sport that stores all sport names with corresponding ids"""
    # Create country table
    cur.execute("DROP TABLE IF EXISTS country")
    cur.execute('''CREATE TABLE country(
                    country_name TEXT NOT NULL UNIQUE PRIMARY KEY,
                    athlete_num INTEGER NOT NULL,
                    sport1 INTEGER, sport2 INTEGER, sport3 INTEGER,
                    sport4 INTEGER, sport5 INTEGER, sport6 INTEGER,
                    sport7 INTEGER, sport8 INTEGER, sport9 INTEGER,
                    sport10 INTEGER, sport11 INTEGER, sport12 INTEGER,
                    sport13 INTEGER, sport14 INTEGER, sport15 INTEGER)''')

    # Create Sports table
    cur.execute("DROP TABLE IF EXISTS sports")
    cur.execute('''CREATE TABLE sports(
                   id INTEGER UNIQUE PRIMARY KEY,
                   sport TEXT NOT NULL UNIQUE ON CONFLICT IGNORE)''')


def insert_data(countries, cur):
    """Insert data athlete and sport data into tables"""
    for country in countries:
        sports, total_athletes = get_data(country)
        cur.execute("INSERT INTO country (country_name, athlete_num) VALUES (?, ?)", (country[0], total_athletes))
        for i, sport in enumerate(sports, start=1):
            cur.execute("INSERT INTO sports (sport) VALUES (?)", (sport,))
            cur.execute("SELECT id FROM sports WHERE sport = ?", (sport,))
            sport_id = cur.fetchone()[0]
            cur.execute('''UPDATE country
                               SET sport{} = ?
                               WHERE country_name = ?'''.format(i), (sport_id, country[0]))
        time.sleep(1)  # sleep for one second to avoid connection error from too many requests
    cur.close()


def create_country_json(countries):
    """Creates default dictionary that stores countries in groups
    based off first letter in name and stores it in a json file"""
    country_dict = {}
    for country in countries:
        letter = country[0][0].upper()
        if letter not in country_dict.keys():
            country_dict.setdefault(letter, [])
            country_dict[letter].append(country[0])
        else:
            country_dict[letter].append(country[0])
    with open('countries.json', 'w') as fh:
        json.dump(country_dict, fh, indent=3)


def main():
    conn = sqlite3.connect('olympicInfo.DB')
    cur = conn.cursor()

    countries = get_page()
    create_tables(cur)
    insert_data(countries, cur)
    create_country_json(countries)
    conn.commit()
    conn.close()
    print("Table and JSON file created with no errors")


if __name__ == '__main__':
    main()
