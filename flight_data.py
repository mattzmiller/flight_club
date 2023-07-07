import pandas
from data_manager import DataManager
from flight_search import FlightSearch

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.flights = DataManager().get_csv().to_dict()

    def process_flights(self):
        flight_search = FlightSearch()
        for key, value in self.flights["IATA Code"].items():
            flight_search.get_lowest_price(value)
