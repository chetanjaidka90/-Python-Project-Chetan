import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_movies(genre):
    try:
        url = f"https://www.imdb.com/search/title/?genres={genre}&sort=user_rating,desc"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        movies = soup.find_all('div', class_='lister-item-content')
        data = []
        for movie in movies:
            title = movie.find('a').text
            rating = movie.find('strong').text
            data.append({'Title': title, 'Rating': rating, 'Genre': genre})
        return data
    except Exception as e:
        print(f"Error: {e}")

def get_movies(genre):
    try:
        df = pd.read_csv('movies.csv')
        return df[df['Genre'] == genre]
    except Exception as e:
        print(f"Error: {e}")

def suggest_movies(genre):
    movies = get_movies(genre)
    return movies.sort_values(by='Rating', ascending=False).head(10)

def main():
    genres = ['action', 'comedy', 'drama']
    data = []
    for genre in genres:
        data.extend(scrape_movies(genre))
    df = pd.DataFrame(data)
    df.to_csv('movies.csv', index=False)
    
    genre = input("Enter a genre: ")
    print(suggest_movies(genre))

if __name__ == "__main__":
    main()