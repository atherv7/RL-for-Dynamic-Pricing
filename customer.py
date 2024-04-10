import math

class Customer:
    # initializer takes
    # attitude constant: an
    # per-determined constant: bn
    # min-max tolerance for demand and consumption difference: dmin and dmax
    # energy demands over time period: energy_demands
    # elasticity coefficients over time period: elasticity_coeffs
    def __init__(self, an, bn, dmin, dmax, energy_demands, elasticity_coeffs):
        self.an = an
        self.bn = bn
        self.dmin = dmin
        self.dmax = dmax
        self.energy_demands = energy_demands
        self.elasticity_coeffs = elasticity_coeffs

    # gets the elasticity coefficient for the customer
    # at a specific time 
    def get_elasticity_coeff_t(self, time):
        if time >= len(self.energy_demands):
            raise Exception("Invalid time input")
        return self.elasticity_coeffs[time] 

    # this function gets the demand for electricity at
    # a specific time 
    def get_energy_demand_t(self, time):
        if time >= len(self.energy_demands):
            raise Exception("Invalid time input")
        return self.energy_demands[time] 

    # function calculates the consumption of this customer based
    # of the demand at the time and the retail price at the time
    # and the elasticity of the customer at the time and wholesale
    # price of the electricity at the time 
    def consumption_t(self, retail_t, wholesale_t, demand_curt_t, elasticity_t):
        if elasticity_t >= 0:
            raise Exception("Invalid elasticity_t constant")
        # quick fix for the information
        curr_consumption_calculation = ((demand_curt_t)*(1 + ((elasticity_t)*((retail_t-wholesale_t)/wholesale_t))))
        difference = demand_curt_t - curr_consumption_calculation
        if difference <= self.dmin*demand_curt_t or difference >= self.dmax*demand_curt_t:
            average_bw = (self.dmin*demand_curt_t) + (self.dmax*demand_curt_t)
            average_bw /= 2
            return -1*(average_bw - demand_curt_t)
        else:
            return curr_consumption_calculation 

    # function for calculating the dissatisfaction of this customer
    # based off the demand of this customer at the time and the
    # actual consumption of this customer at the time 
    def dissatisfaction_t(self, demand_curt_t, consumption_curt_t):
        difference = demand_curt_t - consumption_curt_t
        if difference <= self.dmin*demand_curt_t or difference >= self.dmax*demand_curt_t:
            raise Exception("difference in demand and consumption for customer outside of Dmin and Dmax range")
        return ((self.an/2)*(math.pow(difference,2)) + (self.bn)*(difference))

    
