import streamlit as st
from bs4 import BeautifulSoup
import requests
import openpyxl

def scrape_top_movies():
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = "Top Rated Movies on IMDB"
    sheet.append(["Rank", "Name", "Year", "Rating"])

    source = requests.get('https://www.imdb.com/chart/top/')
    source.raise_for_status()

    soup = BeautifulSoup(source.text, 'html.parser')

    movies = soup.find('tbody', class_="lister-list").find_all('tr')

    for movie in movies:
        name = movie.find('td', class_="titleColumn").a.text
        rank = movie.find('td', class_="titleColumn").get_text(strip=True).split('.')[0]
        year = movie.find('td', class_="titleColumn").span.text.strip('()')
        rating = movie.find('td', class_="ratingColumn imdbRating").strong.text

        sheet.append([rank, name, year, rating])

    excel.save("Imdb_Movie_Ratings.xlsx")

def main():
    st.title("IMDB Top Rated Movies Scraper")

    if st.button("Scrape and Save"):
        st.text("Scraping and saving the top-rated movies...")
        scrape_top_movies()
        st.success("Top-rated movies scraped and saved successfully!")

    st.subheader("Top Rated Movies:")
    wb = openpyxl.load_workbook("Imdb_Movie_Ratings.xlsx")
    sheet = wb.active
    movie_data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        movie_data.append(row)

    st.table(movie_data)

if __name__ == "__main__":
    main()
