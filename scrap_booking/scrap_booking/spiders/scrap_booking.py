import scrapy
from scrapy_playwright.page import PageMethod

class ScrapBookingSpider(scrapy.Spider):
    name = "scrap_booking"

    booking_base_url = "https://www.booking.com"

    search_url = "searchresults.fr.html?order=bayesian_review_score&ss="

    cities = [
        "Mont Saint Michel",
        "St Malo",
        "Bayeux",
        "Le Havre",
        "Rouen",
        "Paris",
        "Amiens",
        "Lille",
        "Strasbourg",
        "Chateau du Haut Koenigsbourg",
        "Colmar",
        "Eguisheim",
        "Besancon",
        "Dijon",
        "Annecy",
        "Grenoble",
        "Lyon",
        "Gorges du Verdon",
        "Bormes les Mimosas",
        "Cassis",
        "Marseille",
        "Aix en Provence",
        "Avignon",
        "Uzes",
        "Nimes",
        "Aigues Mortes",
        "Saintes Maries de la mer",
        "Collioure",
        "Carcassonne",
        "Ariege",
        "Toulouse",
        "Montauban",
        "Biarritz",
        "Bayonne",
        "La Rochelle"
    ]

    async def start(self):
        yield self.next_city_request()


    def next_city_request(self):
        if len(self.cities):
            new_city = self.cities.pop(0)

            return scrapy.Request(
                f"{self.booking_base_url}/{self.search_url}{new_city}",
                callback=self.parse_hotels,
                cb_kwargs={'city': new_city},
                meta={
                    "playwright": True,  # Enables Playwright for JavaScript rendering
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "body"),
                    ],
                },
        )

    def parse_hotels(self, response, city):
        hotels_list = response.css("div[data-testid=property-card]")
        self.logger.info(f"{city} : {len(hotels_list)}")

        for hotel in hotels_list[:20]:
            url_hotel = hotel.css("h3 a::attr(href)").get()
            self.logger.info(f"To scrape --> {city} : {url_hotel}")

            yield response.follow(
                url_hotel, 
                callback=self.parse_a_hotel, 
                cb_kwargs={'city': city, 'url_hotel': url_hotel},
                meta= {
                    "playwright": True,  # Enables Playwright for JavaScript rendering
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "body"),
                    ],
                },
                dont_filter=True
            )

        if len(self.cities):
            yield self.next_city_request()


    def parse_a_hotel(self, response, city, url_hotel):
        self.logger.info(f"STATUS {response.status} : {url_hotel}")
        self.logger.info(f"Process {city} : {url_hotel}")

        hotel_gps = response.css("div[data-testid=PropertyHeaderAddressDesktop-wrapper] a::attr(data-atlas-latlng)").get()
        hotel_lat, hotel_lon = hotel_gps.split(",") if hotel_gps else (None, None)

        yield {
            "city": city,
            "lat": hotel_lat, 
            "lon": hotel_lon,
            "name": response.css("h2::text").get(),
            "url": url_hotel,
            "review_score": (response.css("div[data-testid=review-score-right-component] div::text").get() or "").replace("Avec une note de ", ""),
            "desc": (response.css("p[data-testid=property-description]::text").get() or "").replace("\xa0", " ")
            
        }
