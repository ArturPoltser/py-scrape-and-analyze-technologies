# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RealEstate:
    address: str
    area: float
    price: int
    number_of_rooms: int
    renovation: str
    publication_date: datetime
