#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup

def search_product(product):
    # Format the search query
    search_query = product.replace(' ', '+')

    # Send a GET request to Amazon.in search page
    url = f'https://www.amazon.in/s?k={search_query}'
    response = requests.get(url)

    # Checkingf if the request was successful
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finding all the product elements on the page
        products = soup.find_all('div', {'data-component-type': 's-search-results"'})

        
        for product in products:
            # Extracting the product title
            title_element = product.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
            title = title_element.text.strip() if title_element else "N/A"

            # Extracting the product price
            price_element = product.find('span', {'class': 'a-price-whole'})
            price = price_element.text.strip() if price_element else "N/A"

            # Extracting the product rating
            rating_element = product.find('span', {'class': 'a-size-base s-underline-text'})
            rating = rating_element.text.strip() if rating_element else "N/A"

            # Print the product information
            print(f'Title: {title}')
            print(f'Price: {price}')
            print(f'Rating: {rating}')
            print('---')
    else:
        print(f"Failed to retrieve search results. Status Code: {response.status_code}")

product = input('Enter the product to search: ')


search_product(product)


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_product_details(product):
    # Format the search query
    search_query = product.replace(' ', '+')

    # DataFrame to store product details
    columns = ["Brand Name", "Name of the Product", "Price", "Return/Exchange", "Expected Delivery", "Availability", "Product URL"]
    product_df = pd.DataFrame(columns=columns)

    # Send a GET request to Amazon.in search page
    url = f'https://www.amazon.in/s?k={search_query}'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the total number of result pages
        total_pages_element = soup.find('ul', {'class': 'a-pagination'})
        total_pages = int(total_pages_element.find_all('li')[-2].text) if total_pages_element else 1

        # Iterate through the pages
        for page in range(1, min(total_pages, 4)):
            page_url = f'https://www.amazon.in/s?k={search_query}&page={page}'
            page_response = requests.get(page_url)

            if page_response.status_code == 200:
                page_soup = BeautifulSoup(page_response.content, 'html.parser')

                # Find all the product elements on the page
                products = page_soup.find_all('div', {'data-component-type': 's-search-result'})

                # Iterate over the products and extract relevant information
                for product in products:
                    brand_name_element = product.find('span', {'class': 'a-size-base-plus a-color-base'})
                    brand_name = brand_name_element.text.strip() if brand_name_element else "-"

                    product_name_element = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
                    product_name = product_name_element.text.strip() if product_name_element else "-"

                    price_element = product.find('span', {'class': 'a-offscreen'})
                    price = price_element.text.strip() if price_element else "-"

                    expected_delivery_element = product.find('div', {'class': 'a-row s-align-children-center'})
                    expected_delivery = expected_delivery_element.text.strip() if expected_delivery_element else "-"

                    availability_element = product.find('div', {'class': 'a-row a-size-base a-color-secondary'})
                    availability = availability_element.text.strip() if availability_element else "-"

                    product_url_element = product.find('a', {'class': 'a-link-normal a-text-normal'})
                    product_url = f"https://www.amazon.in{product_url_element['href']}" if product_url_element else "-"

                    # Append the product details to the DataFrame
                    product_df = product_df.append({
                        "Brand Name": brand_name,
                        "Name of the Product": product_name,
                        "Price": price,
                        "Return/Exchange": return_exchange,
                        "Expected Delivery": expected_delivery,
                        "Availability": availability,
                        "Product URL": product_url
                    }, ignore_index=True)

                # Introduce a delay between page requests to avoid being blocked
                time.sleep(2)

            else:
                print(f"Failed to retrieve search results on page {page}. Status Code: {page_response.status_code}")
                break  # Break out of the loop if unsuccessful

    else:
        print(f"Failed to retrieve search results. Status Code: {response.status_code}")

    return product_df

if __name__ == "__main__":
    # Take user input for the product to search
    product_input = input('Enter the product to search: ')

    # Call the scrape_product_details function with the user input
    product_details_df = scrape_product_details(product_input)

    # Display the DataFrame
    print(product_details_df)

    # Save the DataFrame to a CSV file
    product_details_df.to_csv('amazon_product_details.csv', index=False)



# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests

def scrape_images(keyword, num_images=10):
    # Set up Chrome WebDriver
    driver = webdriver.Chrome(executable_path='path/to/chromedriver')  # Update it with your path where chrome driver is there
    driver.get('https://images.google.com/')

    # Find the search bar element
    search_bar = driver.find_element('name', 'q')

    # Type the keyword into the search bar
    search_bar.send_keys(keyword)

    # Press Enter to perform the search
    search_bar.send_keys(Keys.RETURN)

    # Wait for the search results to load
    time.sleep(3)

    # Scroll down to load more images
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Find all image elements on the page
    images = driver.find_elements_by_css_selector('.rg_i')

    # Create a directory to save the images
    os.makedirs(keyword, exist_ok=True)

    # Download the first 10 images
    for i, image in enumerate(images[:num_images]):
        # Get the image source URL
        image_url = image.get_attribute('src')

        # Download the image
        response = requests.get(image_url, stream=True)
        with open(os.path.join(keyword, f'{keyword}_{i+1}.jpg'), 'wb') as img_file:
            for chunk in response.iter_content(chunk_size=128):
                img_file.write(chunk)

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    keywords = ['fruits', 'cars', 'Machine Learning', 'Guitar', 'Cakes']

    for keyword in keywords:
        scrape_images(keyword, num_images=10)


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_flipkart_smartphones(search_query):
    # Format the search query
    s_query = search_query.replace(' ', '%20')

    # Send a GET request to Flipkart search page
    url = f'https://www.flipkart.com/search?q={s_query}'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the product elements on the page
        products = soup.find_all('div', {'class': '_1AtVbE'}) ( Changf)
        # DataFrame to store smartphone details
        columns = ["Brand Name", "Smartphone Name", "Colour", "RAM", "Storage(ROM)", 
                   "Primary Camera", "Secondary Camera", "Display Size", 
                   "Battery Capacity", "Price", "Product URL"]
        smartphones_df = pd.DataFrame(columns=columns)

        # Iterate over the products and extract relevant information
        for product in products:
            brand_name = product.find('div', {'class': '_4rR01T'}).text.strip()
            smartphone_name = product.find('a', {'class': '_1fQZEK'}).text.strip()
            price = product.find('div', {'class': '_30jeq3'}).text.strip()
            product_url = 'https://www.flipkart.com' + product.find('a', {'class': '_1fQZEK'})['href']

            # Extracting details from the product URL
            product_details_response = requests.get(product_url)
            product_details_soup = BeautifulSoup(product_details_response.content, 'html.parser')

            details_dict = {}
            for li in product_details_soup.find_all('li', {'class': 'rgWa7D'}):
                key, value = li.text.split(":")
                details_dict[key.strip()] = value.strip()

            # Extracting required details
            colour = details_dict.get('Color', '-')
            ram = details_dict.get('RAM', '-')
            storage_rom = details_dict.get('Internal Storage', '-')
            primary_camera = details_dict.get('Primary Camera', '-')
            secondary_camera = details_dict.get('Secondary Camera', '-')
            display_size = details_dict.get('Display Size', '-')
            battery_capacity = details_dict.get('Battery Capacity', '-')

            # Append the smartphone details to the DataFrame
            smartphones_df = smartphones_df.append({
                "Brand Name": brand_name,
                "Smartphone Name": smartphone_name,
                "Colour": colour,
                "RAM": ram,
                "Storage(ROM)": storage_rom,
                "Primary Camera": primary_camera,
                "Secondary Camera": secondary_camera,
                "Display Size": display_size,
                "Battery Capacity": battery_capacity,
                "Price": price,
                "Product URL": product_url
            }, ignore_index=True)

        return smartphones_df

    else:
        print(f"Failed to retrieve search results. Status Code: {response.status_code}")
        return None

if __name__ == "__main__":
    # Take user input for the smartphone to search
    search_query = input('Enter the smartphone to search: ')

    # Call the scrape_flipkart_smartphones function with the user input
    smartphones_df = scrape_flipkart_smartphones(search_query)

    if smartphones_df is not None:
        # Display the DataFrame
        print(smartphones_df)

        # Save the DataFrame to a CSV file
        smartphones_df.to_csv('flipkart_smartphones.csv', index=False)


# In[ ]:


import googlemaps

def get_coordinates(api_key, city_name):
    gmaps = googlemaps.Client(key=api_key)

    try:
        geocode_result = gmaps.geocode(city_name)

        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            print(f"Coordinates for {city_name}: Latitude {latitude}, Longitude {longitude}")
        else:
            print(f"Unable to find coordinates for {city_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_api_key' with your actual Google Maps API key
api_key = 'your_api_key'
city_name = input("Enter the city name: ")

get_coordinates(api_key, city_name)


# In[ ]:


. import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_digit_best_gaming_laptops():
    # Send a GET request to digit.in's best gaming laptops page
    url = 'https://www.digit.in/top-products/best-gaming-laptops-40.html'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section containing the list of best gaming laptops
        laptops_section = soup.find('div', {'class': 'listing_container'})

        # DataFrame to store gaming laptop details
        columns = ["Name", "Processor", "RAM", "OS", "Storage", "Display", "Weight", "Price", "URL"]
        laptops_df = pd.DataFrame(columns=columns)

        # Find all the individual laptops
        laptops = laptops_section.find_all('div', {'class': 'TopNumbeHeading'})

        # Iterate over the laptops and extract relevant information
        for laptop in laptops:
            name = laptop.find('div', {'class': 'TopNumbeHeadingBox'}).text.strip()
            details_url = 'https://www.digit.in' + laptop.find('a')['href']

            # Send a GET request to the individual laptop details page
            details_response = requests.get(details_url)
            details_soup = BeautifulSoup(details_response.content, 'html.parser')

            # Extracting details from the individual laptop details page
            specs_table = details_soup.find('div', {'class': 'specifications'})

            processor = specs_table.find('div', text='Processor').find_next('div').text.strip()
            
            ram = specs_table.find('div', text='Memory').find_next('div').text.strip()
            
            os = specs_table.find('div', text='OS').find_next('div').text.strip()
            
            storage = specs_table.find('div', text='Storage').find_next('div').text.strip()
            
            display = specs_table.find('div', text='Display').find_next('div').text.strip()
            
            weight = specs_table.find('div', text='Weight').find_next('div').text.strip()
            
            price = details_soup.find('div', {'class': 'Block-price'}).text.strip()
            

            # Appending the laptop details to the DataFrame
            laptops_df = laptops_df.append({
                "Name": name,
                "Processor": processor,
                "RAM": ram,
                "OS": os,
                "Storage": storage,
                "Display": display,
                "Weight": weight,
                "Price": price,
                "URL": details_url
            }, ignore_index=True)

        return laptops_df

    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        return None

if __name__ == "__main__":
    # Call the scrape_digit_best_gaming_laptops function
    gaming_laptops_df = scrape_digit_best_gaming_laptops()

    if gaming_laptops_df is not None:
        # Display the DataFrame
        print(gaming_laptops_df)

        # Save the DataFrame to a CSV file
        gaming_laptops_df.to_csv('digit_best_gaming_laptops.csv', index=False)


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_forbes_billionaires():
    # Send a GET request to Forbes Billionaires page
    url = 'https://www.forbes.com/billionaires/'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section containing the list of billionaires
        billionaires_section = soup.find('div', {'class': 'forbes__paginated-content'})

        # DataFrame to store billionaire details
        columns = ["Rank", "Name", "Net Worth", "Age", "Citizenship", "Source", "Industry"]
        billionaires_df = pd.DataFrame(columns=columns)

        # Find all the individual billionaires
        billionaires = billionaires_section.find_all('div', {'class': 'person-info'})

        # Iterate over the billionaires and extract relevant information
        for billionaire in billionaires:
            rank = billionaire.find('div', {'class': 'rank'}).text.strip()
            name = billionaire.find('div', {'class': 'personName'}).text.strip()
            net_worth = billionaire.find('div', {'class': 'netWorth'}).text.strip()
            age = billionaire.find('div', {'class': 'age'}).text.strip()
            citizenship = billionaire.find('div', {'class': 'countryOfCitizenship'}).text.strip()
            source = billionaire.find('div', {'class': 'source-column'}).text.strip()
            industry = billionaire.find('div', {'class': 'category'}).text.strip()

            # Append the billionaire details to the DataFrame
            billionaires_df = billionaires_df.append({
                "Rank": rank,
                "Name": name,
                "Net Worth": net_worth,
                "Age": age,
                "Citizenship": citizenship,
                "Source": source,
                "Industry": industry
            }, ignore_index=True)

        return billionaires_df

    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        return None

if __name__ == "__main__":
    # Call the scrape_forbes_billionaires function
    billionaires_df = scrape_forbes_billionaires()

    if billionaires_df is not None:
        # Display the DataFrame
        print(billionaires_df)

        # Save the DataFrame to a CSV file
        billionaires_df.to_csv('forbes_billionaires.csv', index=False)


# In[ ]:


.  import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_hostelworld_london():
    # Sending a GET request to Hostelworld London page
    url = 'https://www.hostelworld.com/hostels/London/England'
    res = requests.get(url)

    if res.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(res.content, 'html.parser')

        # DataFrame to store hostel details
        columns = ["Hostel Name", "Distance", "Ratings", "Total Reviews", "Overall Reviews",
                   "Privates From Price", "Dorms From Price", "Facilities", "Property Description"]
        hostels_df = pd.DataFrame(columns=columns)

        # Finding all the individual hostels
        hostels = soup.find_all('div', {'class': 'flex-2 pr-20'})

        # Iterating over the hostels and extracting relevant information
        for hostel in hostels:
            hostel_name = hostel.find('h2', {'class': 'title-2'}).text.strip()
            distance = hostel.find('span', {'class': 'description'}).text.strip()
            ratings = hostel.find('div', {'class': 'score orange'}).text.strip()
            total_reviews = hostel.find('div', {'class': 'reviews'}).text.strip()
            overall_reviews = hostel.find('div', {'class': 'keyword'}).text.strip()
            privates_from_price = hostel.find('div', {'class': 'price-col'}).find_all('div')[0].text.strip()
            dorms_from_price = hostel.find('div', {'class': 'price-col'}).find_all('div')[1].text.strip()

            # Click on the hostel to get additional details
            hostel_url = 'https://www.hostelworld.com' + hostel.find('a')['href']
            hostel_response = requests.get(hostel_url)
            hostel_soup = BeautifulSoup(hostel_response.content, 'html.parser')

            # Extracting additional details from the hostel page
            facilities = ', '.join([item.text.strip() for item in hostel_soup.find_all('div', {'class': 'facilities-item'})])
            property_description = hostel_soup.find('div', {'class': 'description-container'}).text.strip()

            # Append the hostel details to the DataFrame
            hostels_df = hostels_df.append({
                "Hostel Name": hostel_name,
                "Distance": distance,
                "Ratings": ratings,
                "Total Reviews": total_reviews,
                "Overall Reviews": overall_reviews,
                "Privates From Price": privates_from_price,
                "Dorms From Price": dorms_from_price,
                "Facilities": facilities,
                "Property Description": property_description
            }, ignore_index=True)

        return hostels_df

    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        return None

if __name__ == "__main__":
    # Call the scrape_hostelworld_london function
    london_hostels_df = scrape_hostelworld_london()

    if london_hostels_df is not None:
        # Display the DataFrame
        print(london_hostels_df)

        # Save the DataFrame to a CSV file
        london_hostels_df.to_csv('hostelworld_london_hostels.csv', index=False)

