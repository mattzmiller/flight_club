import pandas
from data_manager import DataManager
from flight_search import FlightSearch

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.flights = DataManager().get_csv().to_dict()
        self.get_lowest_price()

    def get_lowest_price(self):
        flight_search = FlightSearch()
        values = []
        for key, value in self.flights["IATA Code"].items():
            flight_api_data = flight_search.get_flight_info(value)
            lowest_price = min([flight["price"] for flight in flight_api_data])
            self.flights["Lowest Price"][key] = lowest_price

