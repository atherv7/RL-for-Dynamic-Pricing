class Grid_Operator:
    def __init__(self, wholesale_prices):
        self.wholesale_prices = wholesale_prices

    def get_price_at_time(self, time):
        if time >= len(self.wholesale_prices):
            raise Exception("Invalid time input") 
        return self.wholesale_prices[time] 
