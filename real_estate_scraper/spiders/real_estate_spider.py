import re
from datetime import datetime

import scrapy
from scrapy.http import Response

from real_estate_scraper.items import RealEstate


class RealEstateSpider(scrapy.Spider):
    name = "real_estate_spider"
    allowed_domains = ["lun.ua"]
    start_urls = [
        "https://lun.ua/uk/"
        "%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6-"
        "%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-"
        "%D1%96%D0%B2%D0%B0%D0%BD%D0%BE-"
        "%D1%84%D1%80%D0%B0%D0%BD%D0%BA%D1%96%D0%B2%D1%81%D1%8C%D0%BA"
    ]

    def parse(self, response: Response, **kwargs):
        for real_state in response.css("div.realty-preview__base"):
            yield self.scrape_single_real_estate(real_state)

        next_page = response.css("a.paging-nav--right::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def scrape_single_real_estate(self, response: Response) -> RealEstate:
        return RealEstate(
            address=self._scrape_address(response),
            price=self._scrape_price(response),
            area=self._scrape_area(response),
            number_of_rooms=self._scrape_number_of_rooms(response),
            renovation=self._scrape_renovation(response),
            publication_date=self._scrape_publication_date(response)
        )

    @staticmethod
    def _scrape_address(response: Response) -> str | None:
        if address := response.css("h3.realty-preview-title > button::text").get():
            return address

        return None

    @staticmethod
    def _scrape_price(response: Response) -> int | None:
        if price := response.css(".realty-preview-price::text").get():
            return int("".join(re.findall(r"\d+", price)))

        return None

    @staticmethod
    def _scrape_area(response: Response) -> float | None:
        try:
            if area := response.css("span.realty-preview-info::text"):
                return float(area[1].get().strip(r"\n").strip())
            return None

        except ValueError:
            return None

    @staticmethod
    def _scrape_number_of_rooms(response: Response) -> int | None:
        if rooms := response.css("span.realty-preview-info::text"):
            return int(rooms.get().strip(r"\n").strip().split()[0])

        return None

    @staticmethod
    def _scrape_renovation(response: Response) -> str | None:
        if renovation := response.css("div.Grid-module_col__der3x"):
            renovation = renovation.css("div.realty-preview-properties-item")[3]
            return renovation.css("span::text").get().strip(r"\n").strip()

        return None

    def _scrape_publication_date(self, response: Response) -> datetime | None:
        if publication_date := response.css(".realty-preview-dates > .Grid-module_container__1mSeI"):
            publication_date = publication_date.css("span::text")[-1].get()
            return self._convert_to_datetime(publication_date)

        return None

    @staticmethod
    def _convert_to_datetime(date_str) -> datetime | None:
        current_year = datetime.now().year
        months = {
            "січня": 1, "лютого": 2, "березня": 3, "квітня": 4, "травня": 5, "червня": 6,
            "липня": 7, "серпня": 8, "вересня": 9, "жовтня": 10, "листопада": 11, "грудня": 12
        }

        parts = date_str.split()

        if len(parts) >= 2:
            day_str = parts[0]
            month_str = parts[1]
            year_str = parts[2] if len(parts) == 4 else None

            if month_str.lower() in months:
                month = months[month_str.lower()]
                day = int(day_str) if day_str.isdigit() else None

                if day and month:
                    if not year_str:
                        year_str = str(current_year)
                    date_str = f"{day} {month} {year_str}"
                    return datetime.strptime(date_str, "%d %m %Y")

        return datetime.today()
