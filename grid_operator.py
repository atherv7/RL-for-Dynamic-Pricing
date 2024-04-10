class Grid_Operator:
    # initializer takes in wholesale_prices which is an array of wholesale
    # prices per time section in a given time period 
    def __init__(self, wholesale_prices):
        self.wholesale_prices = wholesale_prices

    # get the wholesale price for the electricity for a time
    def get_price_at_time(self, time):
        if time >= len(self.wholesale_prices):
            raise Exception("Invalid time input") 
        return self.wholesale_prices[time] 
