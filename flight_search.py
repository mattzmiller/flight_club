import requests
import ast
from data_manager import DataManager


TEQUILA_API_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
TEQUILA_API_KEY = "T-Lg9LLSyDuaiso5XggwumzjCJj95WGi"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "apikey": TEQUILA_API_KEY
        }
        self.api_endpoint = TEQUILA_API_ENDPOINT,
        self.api_key = TEQUILA_API_KEY
        self.city_codes = []
        try:
            with open("city_codes.txt") as file:
                data = file.readlines()
                self.city_codes = [ast.literal_eval(city.replace("\n", "")) for city in data]
                print(self.city_codes)
        except FileNotFoundError:
            self.get_iata_codes()

    def get_iata_codes(self):
        data_manager = DataManager()
        cities = data_manager.cities
        with open("city_codes.txt", mode="w") as file:
            for idx in range(len(cities)):
                response = requests.get(url=TEQUILA_API_ENDPOINT, params={"term": f"{cities[idx][idx + 2]}"},
                                        headers=self.headers)
                response.raise_for_status()
                city_code = response.json()["locations"][0]["code"]
                city_code_formatted = {(idx + 2): city_code}

                file.write(f"{city_code_formatted}\n")
                self.city_codes.append(city_code_formatted)

                data_manager.add_city_code(city_code_formatted)

