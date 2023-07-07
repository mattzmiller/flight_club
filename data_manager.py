import requests
import ast
import pandas

SHEETY_ENDPOINT = "https://api.sheety.co/2a7fb867a8003e04dcfec0a1bc51e2f1/flightDeals/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        try:
            with open("city_data/cities.txt") as file:
                data = file.readlines()
                self.cities = [ast.literal_eval(city.replace("\n", "")) for city in data]
        except FileNotFoundError:
            self.cities = []
            self.populate_cities()
            with open("city_data/cities.txt", mode="w") as cities_data_file:
                for city in self.cities:
                    cities_data_file.write(f"{city}\n")

    def populate_cities(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        response.raise_for_status()
        rows = response.json()["prices"]
        self.cities = [{city["id"]: city["city"]} for city in rows]

    def add_city_code(self, city_code):
        key = [key for key, value in city_code.items()][0]
        value = city_code[key]
        response = requests.put(url=f"{SHEETY_ENDPOINT}/{key}", json={"price": {"iataCode": value}})
        response.raise_for_status()
        print(response.json())
        print(key, value)

    def get_csv(self):
        return pandas.read_csv("city_data/flight_deals.csv")


