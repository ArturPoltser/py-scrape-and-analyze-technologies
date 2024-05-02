# Scraping and Analysis of the real estate market in Ivano-Frankivsk

## Features
- Web Scraping: Utilizes Scrapy to crawl and extract information from lun.ua.
- Added randomized User Agent header, to prevent detecting.

- Data Analysis: Provides statistical analysis on the collected data.

## Installation

To clone this project from GitHub, follow these steps:

1. **Open your terminal or command prompt.**
2. **Navigate to the directory where you want to clone the project.**
3. **Run the following commands:**
```shell
git clone https://github.com/ArturPoltser/py-scrape-and-analisys-of-real-estate-market.git
cd py-scrape-and-analisys-of-real-estate-market
python -m venv venv
venv\Scripts\activate  #for MacOS/Linux use: source venv/bin/activate
```

4. **Install requirements:**

```shell
pip install -r requirements.txt
```

5. **Run the Web Scraping Script:**
```shell
scrapy crawl real_estate_spider -O real_estate.csv
```

## Files Structure

- `real_estate_scraper/spiders/real_estate_spider.py`: File that contains all main logic for scraping data.
- `real_estate_analysis/analysis.ipynb`: Jupyter Notebook file containing the analysis of data.
