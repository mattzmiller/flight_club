import requests
import ast
from data_manager import DataManager
import datetime as dt


TEQUILA_LOCATIONS_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
TEQUILA_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2"
TEQUILA_API_KEY = "T-Lg9LLSyDuaiso5XggwumzjCJj95WGi"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "apikey": TEQUILA_API_KEY
        }
        self.locations_endpoint = TEQUILA_LOCATIONS_ENDPOINT,
        self.search_endpoint = TEQUILA_SEARCH_ENDPOINT
        self.api_key = TEQUILA_API_KEY
        self.city_codes = []
        try:
            with open("city_data/city_codes.txt") as file:
                data = file.readlines()
                self.city_codes = [ast.literal_eval(city.replace("\n", "")) for city in data]
                # print(self.city_codes)
        except FileNotFoundError:
            self.get_iata_codes()

    def get_iata_codes(self):
        data_manager = DataManager()
        cities = data_manager.cities
        with open("city_data/city_codes.txt", mode="w") as file:
            for idx in range(len(cities)):
                response = requests.get(url=self.locations_endpoint, params={"term": f"{cities[idx][idx + 2]}"},
                                        headers=self.headers)
                response.raise_for_status()
                city_code = response.json()["locations"][0]["code"]
                city_code_formatted = {(idx + 2): city_code}

                file.write(f"{city_code_formatted}\n")
                self.city_codes.append(city_code_formatted)

                data_manager.add_city_code(city_code_formatted)

    def get_lowest_price(self, city_code):
        tomorrow = (dt.datetime.now() + dt.timedelta(1)).strftime("%d/%m/%Y")
        six_months_from_now = (dt.datetime.now() + dt.timedelta(180)).strftime("%d/%m/%Y")

        parameters = {
            "fly_from": "BOS",
            "fly_to": city_code,
            "date_from": tomorrow,
            "date_to": six_months_from_now
        }

        response = requests.get(url=self.search_endpoint, headers=self.headers, params=parameters)
        print(response.json())