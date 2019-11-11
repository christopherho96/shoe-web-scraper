#encoding=utf8
import requests
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

user_shoe_size_input = input("Enter your shoe size: " )

url = "https://www.sportchek.ca/categories/men/footwear/basketball-shoes.html?page=1#preselectedBrandsNumber=0&preselectedCategoriesNumber=3&q1=Men&q2=Shoes+%26+Footwear&q3=Basketball&q4=Men&q5={0}&x1=c.category-level-1&x2=c.category-level-2&x3=c.category-level-3&x4=gender&x5=size".format(user_shoe_size_input)

driver = webdriver.Chrome()
driver.get(url)
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'clips-cards ')))
except TimeoutException:
    print('Page timed out after 10 secs.')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

products = soup.find_all(class_="product-grid__list-item")

with open('shoes.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["Product Name", "Price", "Image URL"])
    for product in products:
        product_price = product.find(attrs={'class': 'product-price-text'}).text
        product_title = product.find(attrs={'class': 'product-title-text'}).text
        product_image_url = product.find(attrs={'class': 'product-grid-image'})['src'][2:]
        writer.writerow([product_title,product_price, product_image_url])

csvFile.close()
