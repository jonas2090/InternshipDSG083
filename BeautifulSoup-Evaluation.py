#!/usr/bin/env python
# coding: utf-8

# 1) Write a python program to display IMDB’s Top rated 100 Indian movies’ data
# https://www.imdb.com/list/ls056092300/ (i.e. name, rating, year ofrelease) and make data frame.

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[3]:


# Send a GET request to the IMDb URL
url = "https://www.imdb.com/list/ls056092300/"
response = requests.get(url, verify=False)


# In[4]:


# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')


# In[5]:


# Find all the movie items
movie_items = soup.find_all('div', class_='lister-item-content')


# In[6]:


# Lists to store movie data
names = []
ratings = []
years = []


# In[7]:


# Extract data for each movie
for movie in movie_items:
    # Name of the movie
    name = movie.find('a').text.strip()
    names.append(name)
    
    # Rating of the movie
    rating = movie.find('span', class_='ipl-rating-star__rating').text.strip()
    ratings.append(float(rating))
    
    # Year of release
    year = movie.find('span', class_='lister-item-year').text.strip()
    years.append(year)

# Create DataFrame using pandas
df = pd.DataFrame({
    'Name': names,
    'Rating': ratings,
    'Year': years
})


# In[8]:


# Display the DataFrame
print(df)


# 2) Write a python program to scrape product name, price and discounts from
# https://peachmode.com/search?q=bags

# Skipped

# 3) Write a python program to scrape cricket rankings from icc-cricket.com. You have to scrape:
# 
# a) Top 10 ODI teams in men’s cricket along with the records for matches, points and rating.
# 
# b) Top 10 ODI Batsmen along with the records of their team and rating.
# 
# c) Top 10 ODI bowlers along with the records of their team and rating.

# Skipped

# 4) Write a python program to scrape details of all the posts from https://www.patreon.com/coreyms .Scrape the
# heading, date, content and the likes for the video from the link for the youtube video from the post.

# In[14]:


import requests
from bs4 import BeautifulSoup


# In[27]:


def scrape_patreon_posts(url):
    # Send a GET request to the URL
    response = requests.get(url, verify=False)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all post containers
        posts = soup.find_all('div', class_='postCard_3umV3R postType_article_Xs6A2p')

        # Loop through each post container
        for post in posts:
            # Extract heading
            heading = post.find('h4', class_='postCardTitle_a832Q1').text.strip()

            # Extract date
            date = post.find('time').text.strip()

            # Extract content
            content = post.find('div', class_='postCardContent_3R_Vhf').text.strip()

            # Extract likes for the YouTube video (if available)
            youtube_link = post.find('a', class_='playButton_2DDpz_')
            likes = None
            if youtube_link:
                youtube_url = youtube_link['href']
                likes = scrape_youtube_likes(youtube_url)

            # Print the extracted information
            print("Heading:", heading)
            print("Date:", date)
            print("Content:", content)
            print("Likes:", likes if likes else "Not available")
            print("-" * 50)

    else:
        print("Failed to retrieve page:", response.status_code)

def scrape_youtube_likes(youtube_url):
    # Send a GET request to the YouTube URL
    response = requests.get(youtube_url, verify=False)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract likes count
        likes_element = soup.find('button', {'aria-label': 'I like this'})
        likes = likes_element.find('span', class_='yt-uix-button-content').text.strip()

        return likes

    else:
        return None


# In[28]:


if __name__ == "__main__":
    # URL of the page to scrape
    url = "https://www.patreon.com/coreyms"

    # Call the scraping function
    scrape_patreon_posts(url)


# 5) Write a python program to scrape house details from mentioned URL. It should include house title, location, area, EMI and price from https://www.nobroker.in/ .Enter three localities which are Indira Nagar, Jayanagar, Rajaji Nagar.

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[16]:


def scrape_house_details(localities):
    for locality in localities:
        url = f"https://www.nobroker.in/property/sale/{locality}/bangalore"
          
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all house containers
            houses = soup.find_all('div', class_='card')

            print(f"House details for {locality}:")
            print("-" * 50)

            # Loop through each house container
            for house in houses:
                # Extract house title
                title = house.find('h2', class_='heading-6 font-semi-bold nb__1AShY').text.strip()

                # Extract location
                location = house.find('div', class_='nb__2CMjv').text.strip()

                # Extract area
                area = house.find('div', class_='nb__3oNyC').text.strip()

                # Extract EMI
                emi = house.find('div', class_='font-semi-bold heading-6', text='EMI').find_next('div').text.strip()

                # Extract price
                price = house.find('div', class_='font-semi-bold heading-6').text.strip()

                # Print the extracted information
                print("Title:", title)
                print("Location:", location)
                print("Area:", area)
                print("EMI:", emi)
                print("Price:", price)
                print("-" * 50)

        else:
            print(f"Failed to retrieve page for {locality}:", response.status_code)
        print()


# 6) Write a python program to scrape first 10 product details which include product name , price , Image URL from https://www.bewakoof.com/bestseller?sort=popular .

# In[8]:


import requests
from bs4 import BeautifulSoup


# In[15]:


def scrape_bewakoof_products(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product containers
        products = soup.find_all('div', class_='productCardWrapper-3Ts_h')

        # Iterate over the first 10 product containers
        for product in products[:10]:
            # Extract product name
            name = product.find('div', class_='productCardTitle-2L55D').text.strip()

            # Extract product price
            price = product.find('span', class_='productPrize-2dGGR').text.strip()

            # Extract image URL
            image_url = product.find('img')['src']

            # Print the extracted information
            print("Name:", name)
            print("Price:", price)
            print("Image URL:", image_url)
            print("-" * 50)

    else:
        print("Failed to retrieve page:", response.status_code)


# 7) Please visit https://www.cnbc.com/world/?region=world and scrap- 
# a) headings 
# b) date 
# c) News link

# In[11]:


import requests
from bs4 import BeautifulSoup


# In[19]:


def scrape_cnbc_news(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all news articles
        articles = soup.find_all('div', class_='Card-titleContainer-2-les')
        dates = soup.find_all('div', class_='Card-time-3eDlK')

        # Loop through each article
        for i, article in enumerate(articles):
            # Extract heading
            heading = article.find('a').text.strip()

            # Extract date
            date = dates[i].text.strip()

            # Extract news link
            news_link = "https://www.cnbc.com" + article.find('a')['href']

            # Print the extracted information
            print("Heading:", heading)
            print("Date:", date)
            print("News Link:", news_link)
            print("-" * 50)

    else:
        print("Failed to retrieve page:", response.status_code)


# 8) Please visit https://www.keaipublishing.com/en/journals/artificial-intelligence-in-agriculture/most-downloaded- articles/ and scrap- a) Paper title b) date c) Author

# In[21]:


import requests
from bs4 import BeautifulSoup

def scrape_most_downloaded_articles(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all article containers
        articles = soup.find_all('div', class_='resource-list-content')

        # Loop through each article
        for article in articles:
            # Extract paper title
            title = article.find('h5', class_='resource-title').text.strip()

            # Extract date
            date = article.find('span', class_='resource-date').text.strip()

            # Extract author
            author = article.find('span', class_='resource-authors').text.strip()

            # Print the extracted information
            print("Paper Title:", title)
            print("Date:", date)
            print("Author:", author)
            print("-" * 50)

    else:
        print("Failed to retrieve page:", response.status_code)

