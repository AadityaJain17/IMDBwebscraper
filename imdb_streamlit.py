import streamlit as st
from bs4 import BeautifulSoup
import requests
import openpyxl
def scrape_top_movies():
    # Create an Excel workbook and sheet
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = "Top Rated Movies on IMDB"
    # Add headers to the sheet
    sheet.append(["Rank", "Name", "Year", "Rating"])
    # Fetch the webpage
    source = requests.get('https://www.imdb.com/chart/top/')
    source.raise_for_status()  # Raise an exception if the URL is invalid
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(source.text, 'html.parser')
    # Find all movie entries in the table
    movies = soup.find('tbody', class_="lister-list").find_all('tr')
    # Loop through each movie entry and extract the details
    for movie in movies:
        name = movie.find('td', class_="titleColumn").a.text
        rank = movie.find('td', class_="titleColumn").get_text(strip=True).split('.')[0]
        year = movie.find('td', class_="titleColumn").span.text.strip('()')
        rating = movie.find('td', class_="ratingColumn imdbRating").strong.text
        # Append the details to the sheet
        sheet.append([rank, name, year, rating])
    # Save the Excel file
    excel.save("Imdb_Movie_Ratings.xlsx")
def main():
    st.title("IMDB Top Rated Movies Scraper")
    # Button to trigger scraping and saving
    if st.button("Scrape and Save"):
        st.text("Scraping and saving the top-rated movies...")
        scrape_top_movies()
        st.success("Top-rated movies scraped and saved successfully!")
if __name__ == "__main__":
    main()