import csv
import urllib.request
import requests
import os
from bs4 import BeautifulSoup


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_book_info(book_url):
    soup = get_soup(book_url)
    title = soup.find('h1').text
    upc = soup.select_one("tr:nth-of-type(1) th + td").text
    price_excluding_tax = soup.select_one("tr:nth-of-type(3) th + td").text.replace('£', '')
    price_including_tax = soup.select_one("tr:nth-of-type(4) th + td").text.replace('£', '')
    number_available = soup.select_one("tr:nth-of-type(6) th + td").text.replace('In stock (', '')\
        .replace(' available)', '')
    if soup.select_one('#product_description'):
        product_description = soup.select_one('#product_description + p').text
    else:
        product_description = ''
    category = soup.select_one('.breadcrumb li:nth-of-type(3) a').text
    review_rating = soup.select_one('.star-rating')['class'][1]
    if review_rating == "One":
        review_rating = 1
    elif review_rating == "Two":
        review_rating = 2
    elif review_rating == "Three":
        review_rating = 3
    elif review_rating == "Four":
        review_rating = 4
    elif review_rating == "Five":
        review_rating = 5
    else:
        review_rating = 0
    image_url = 'https://books.toscrape.com/' + soup.find('img')["src"].replace('../', '')

    def download_image(url, file_path, file_name):
        full_path = f"{file_path}{file_name}.jpg"
        urllib.request.urlretrieve(url, full_path)

    image_title = title.replace(' ', '-').replace(':', '-').replace('/', '-').replace('.', '-').replace(',', '-')\
        .replace('"', '-').replace('\\', '-').replace('*', '').replace('?', '')
    download_image(image_url, f"books-data/{category.replace(' ', '')}/images/", image_title)

    return {
        'title': title,
        'upc': upc,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url,
        'product_page_url': book_url
    }


def get_category_books(category_page_url):
    books_link = []
    soup = get_soup(category_page_url)
    books = soup.find_all('h3')
    for book in books:
        for link in book.find_all('a'):
            new_link = link['href'].replace('../', '')
            books_link.append('https://books.toscrape.com/catalogue/' + new_link)
    while soup.select_one('.next'):
        page_number = soup.select_one('.next a')['href']
        new_category_page_url = category_page_url.replace('index.html', page_number)
        soup = get_soup(new_category_page_url)
        books = soup.find_all('h3')
        for book in books:
            for link in book.find_all('a'):
                new_link = link['href'].replace('../', '')
                books_link.append('https://books.toscrape.com/catalogue/' + new_link)

    return books_link


def get_categories():
    categories_info = []
    soup = get_soup('https://books.toscrape.com/')
    categories = soup.select('.side_categories .nav li ul li a')
    for category in categories:
        link = category['href']
        full_link = 'https://books.toscrape.com/' + link
        name = category.text.replace(' ', '').replace('\n', '')
        category_info = [name, full_link]
        categories_info.append(category_info)

        try:
            os.makedirs(f"books-data/{name}/images", exist_ok=True)
        except OSError as errors:
            print(errors)

    return categories_info


categories_elm = get_categories()
book_count = 0
for category_name, category_url in categories_elm:
    books_info = []
    book_urls = get_category_books(category_url)
    for x in book_urls:
        book_info = get_book_info(x)
        books_info.append(book_info)
        book_count += 1
        print(f'{book_count}/1000 books completed')
    with open(f"./books-data/{category_name}/{category_name}.csv", 'w', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'upc', 'price_including_tax', 'price_excluding_tax',
                                               'number_available', 'product_description', 'category', 'review_rating',
                                               'image_url', 'product_page_url'])
        writer.writeheader()
        writer.writerows(books_info)
    print(f'{category_name} category completed')
print('------------------Scraping completed------------------')
