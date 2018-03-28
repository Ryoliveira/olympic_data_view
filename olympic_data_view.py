import json
import sqlite3


def select_country():
    """Display list of countries matching user selected letter."""
    with open('countries.json', 'r') as fh:
        countries = json.load(fh)

    country_found = False
    while not country_found:
        letter = input('Enter first letter of country: ').upper()
        if len(letter) == 1 and letter.isalpha() and letter in countries.keys():
            for num, item in enumerate(countries[letter], start=1):
                print(str(num) + ":", item)
            valid_entry = False
            while not valid_entry:
                try:
                    print('-----------------')
                    choice = int(input("Choose Country: "))
                    print('-----------------')
                    if choice <= 0:
                        raise IndexError
                    else:
                        country = countries[letter][choice - 1]
                except (IndexError, ValueError):
                    if IndexError:
                        print("Choice out of range, try again.")
                        continue
                    if ValueError:
                        print("Enter a number, try again.")
                        continue
                valid_entry = True

            country_found = True
        else:
            if len(letter) > 1 or not letter.isalpha():
                print("Enter only a single letter")
            else:
                print("No countries found!")
    return country


def total_athletes(cur):
    """Displays total athletes participating for specific country"""
    country = select_country()
    cur.execute("SELECT athlete_num FROM country WHERE country_name = ?", (country,))
    print(cur.fetchone()[0], "Athlete(s) for", country)


def display_by_sport(cur):
    """Displays countries that participated in selected sport"""
    cur.execute("SELECT sport FROM sports")
    sports = sorted(cur.fetchall())
    print("Sports:")
    for i, sport in enumerate(sports, start=1):
        if i % 5 != 0:
            print(sport[0], end=', ')
        else:
            print()
    found = False
    while not found:
        selected_sport = input('Enter sport name: ').title()
        for sport in sports:
            if selected_sport == sport[0]:
                found = True
                cur.execute('''SELECT country.country_name
                                   FROM country JOIN sports
                                   ON country.sport1 = sports.id OR country.sport2 = sports.id OR country.sport3 = sports.id
                                   OR country.sport4 = sports.id OR country.sport5 = sports.id OR country.sport6 = sports.id 
                                   OR country.sport7 = sports.id OR country.sport8 = sports.id OR country.sport9 = sports.id 
                                   OR country.sport10 = sports.id OR country.sport11 = sports.id OR country.sport12 = sports.id 
                                   OR country.sport13 = sports.id OR country.sport14 = sports.id OR country.sport15 = sports.id 
                                   WHERE sport = ?''', (selected_sport,))
                print("-" * 50)
                print("Countries participating in sport:", selected_sport)
                print("-" * 50)
                for country in sorted(cur.fetchall()):
                    print(country[0])
                print("-" * 50)
        if not found:
            print("Error: Sport not found")


def min_max_athletes(cur):
    """"Displays countries with athletes between selected window"""
    error = True
    while error:
        try:
            min, max = input("Enter min, max number of athletes: ").split(', ')
            if min.isnumeric() and max.isnumeric() and 0 < int(min) <= int(max) > 0:
                cur.execute("SELECT country_name FROM country WHERE athlete_num BETWEEN ? and ?", (min, max))
                print("Countries with {} to {} athletes".format(min, max))
                for country in sorted(cur.fetchall()):
                    print(country[0])
                error = False
            else:
                raise ValueError
        except ValueError:
            print("Error: Enter two valid NUMBERS.")


def main():
    conn = sqlite3.connect('olympicInfo.DB')
    cur = conn.cursor()
    choice = ''
    while choice != '0':
        print()
        print("========================================================\n"
              "1. Display total athlete number of country\n"
              "2. Display countries by sport\n"
              "3. Display country with certain number of athletes\n"
              "========================================================")
        print()
        choice = input('Enter Selection or enter \'0\' to exit: ')
        if choice == '1':
            total_athletes(cur)
            continue
        if choice == '2':
            display_by_sport(cur)
            continue
        if choice == '3':
            min_max_athletes(cur)
            continue
        if choice != '0':
            print('Error: Enter a valid choice')
    print("Good-Bye!")


if __name__ == '__main__':
    main()
