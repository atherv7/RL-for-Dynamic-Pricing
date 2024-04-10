import math

class Customer:
    def __init__(self, an, bn, dmin, dmax, energy_demands, elasticity_coeffs):
        self.an = an
        self.bn = bn
        self.dmin = dmin
        self.dmax = dmax
        self.energy_demands = energy_demands
        self.elasticity_coeffs = elasticity_coeffs

    def get_elasticity_coeff_t(self, time):
        if time >= len(self.energy_demands):
            raise Exception("Invalid time input")
        return self.elasticity_coeffs[time] 

    def get_energy_demand_t(self, time):
        if time >= len(self.energy_demands):
            raise Exception("Invalid time input")
        return self.energy_demands[time] 

    def consumption_t(self, retail_t, wholesale_t, demand_curt_t, elasticity_t):
        if elasticity_t >= 0:
            raise Exception("Invalid elasticity_t constant")
##        elif retail_t < wholesale_t:
##            raise Exception("wholesale_t is greater than retail_t")
        # quick fix for the information
        curr_consumption_calculation = ((demand_curt_t)*(1 + ((elasticity_t)*((retail_t-wholesale_t)/wholesale_t))))
        difference = demand_curt_t - curr_consumption_calculation
        if difference <= self.dmin*demand_curt_t or difference >= self.dmax*demand_curt_t:
            average_bw = (self.dmin*demand_curt_t) + (self.dmax*demand_curt_t)
            average_bw /= 2
            return -1*(average_bw - demand_curt_t)
        else:
            return curr_consumption_calculation 

    def dissatisfaction_t(self, demand_curt_t, consumption_curt_t):
        difference = demand_curt_t - consumption_curt_t
        if difference <= self.dmin*demand_curt_t or difference >= self.dmax*demand_curt_t:
            raise Exception("difference in demand and consumption for customer outside of Dmin and Dmax range")
        return ((self.an/2)*(math.pow(difference,2)) + (self.bn)*(difference))

    
