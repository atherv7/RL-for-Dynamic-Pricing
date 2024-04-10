import customer as cu
import grid_operator as go
import service_provider as sp
import random
class DynamicPricingModel:
    def __init__(self, time_length=24, iterations=1, termination_delta=0.0000000001, display=False):
        self.time_length = time_length
        self.customers = []
        self.total_customers = 0
        self.grid_op = None
        self.service_provider = None
        self.termination_delta = termination_delta
        self.iterations = iterations
        self.display = display
        self.daily_avg_diss_p_iter = []
        self.daily_tot_prof_p_iter = []

    def add_customer(self, an, bn, dmin, dmax, energy_demands, elastic_coeffs):
        customer = cu.Customer(an, bn, dmin, dmax, energy_demands, elastic_coeffs)
        self.customers.append(customer)
        self.total_customers += 1

    def add_grid_operator(self, wholesale_prices):
        if self.grid_op != None:
            print("A grid operator is already initialized")
            return 
        self.grid_op = go.Grid_Operator(wholesale_prices)

    def add_service_provider(self, k1, k2, min_wholesale, max_wholesale, customers, customer_demands, profit_importance, N0):
        if self.service_provider != None:
            print("A service provider is already initialized")
            return 
        self.service_provider = sp.Service_Provider(k1, k2, min_wholesale, max_wholesale, customers, customer_demands, profit_importance, N0)

    def train(self):
        if self.total_customers == 0:
            raise Exception("No customers initialized")
        elif self.grid_op == None:
            raise Exception("No grid operator initialized")
        elif self.service_provider == None:
            raise Exception("No service provider initialized")
        else:
            random.seed(10) 
            prev_q_values = [[0] * self.time_length for _ in range(self.total_customers)]
            best_q_values = [[0] * self.time_length for _ in range(self.total_customers)]
            best_time_prices = [[0] * self.time_length for _ in range(self.total_customers)]
            for i in range(self.iterations):
                curr_q_values = [[0] * self.time_length for _ in range(self.total_customers)]
                curr_time_prices = [[0] * self.time_length for _ in range(self.total_customers)]
                self.service_provider.calculate_epsilon(i) 
                for t in range(self.time_length):
                    wholesale_price_t = self.grid_op.get_price_at_time(t) 
                    for n in range(self.total_customers):
                        curr_customer = self.customers[n]
                        energy_demand_t_n = curr_customer.get_energy_demand_t(t)
                        elastic_coeff_t = curr_customer.get_elasticity_coeff_t(t)
                        best_price, q_table_value, max_ind = self.service_provider.get_best_action_and_value_for_n_t(t, n)
                        curr_q_values[n][t] = q_table_value
                        curr_time_prices[n][t] = best_price
                        energy_consume_t_n = curr_customer.consumption_t(best_price, wholesale_price_t, energy_demand_t_n, elastic_coeff_t)
                        dissatisfaction_t = curr_customer.dissatisfaction_t(energy_demand_t_n, energy_consume_t_n)
                        self.service_provider.calculate_learning_rate(t) 
                        reward = self.service_provider.update_q_value(q_table_value, n, t, max_ind, wholesale_price_t, energy_consume_t_n, dissatisfaction_t)
                        if self.display: 
                            print("reward for customer " + str(n) + " at time " + str(t) + " at iteration " + str(i) + ": " + str(reward))
##                if self.check_passing_condition(curr_q_values, prev_q_values):
##                    return curr_q_values, curr_time_prices
##                else:
                self.transfer_arrays(curr_q_values, prev_q_values)
                self.transfer_arrays(curr_q_values, best_q_values)
                self.transfer_arrays(curr_time_prices, best_time_prices)
##                if i % 1000 == 0:
##                    tot_con = self.check_total_consumption(best_time_prices) 
##                    tot_prof = self.check_total_profit(best_time_prices, tot_con)
##                    avg_dis = self.average_dissatisfaction(tot_con)
##                    daily_prof = sum(tot_prof)
##                    daily_avg_dis = sum(avg_dis)/len(avg_dis)
##                    self.daily_avg_diss_p_iter.append(daily_avg_dis) 
##                    self.daily_tot_prof_p_iter.append(daily_prof) 
            return best_q_values, best_time_prices  

    def check_passing_condition(self, curr, prev):
        for i in range(len(curr)):
            for j in range(len(curr[i])):
                if abs(curr[i][j] - prev[i][j]) > self.termination_delta:
                    return False
        return True

    def check_total_consumption(self, best_prices):
        total_consumption = [[0] * self.time_length for _ in range(self.total_customers)]
        for customer in range(self.total_customers):
            for time in range(self.time_length):
                cust = self.customers[customer]
                elasticity_t = cust.get_elasticity_coeff_t(time)
                wholesale_t = self.grid_op.get_price_at_time(time)
                best_price = best_prices[customer][time]
                energy_demand = cust.get_energy_demand_t(time)
                total_consumption[customer][time] = cust.consumption_t(best_price, wholesale_t, energy_demand, elasticity_t)
        return total_consumption

    def check_total_profit(self, best_prices, total_consumption):
        total_profit_for_time = [0] * self.time_length
        for time in range(self.time_length):
            wholesale_t = self.grid_op.get_price_at_time(time)
            profit_over_customers = 0
            for customer in range(self.total_customers):
                profit_over_customers += (best_prices[customer][time] - wholesale_t)*(total_consumption[customer][time])
            total_profit_for_time[time] = round(profit_over_customers,2) 
        return total_profit_for_time

    def average_dissatisfaction(self, total_consumption):
        avg_dis_time = [0] * self.time_length
        for time in range(self.time_length):
            wholesale_t = self.grid_op.get_price_at_time(time)
            total_diss = 0
            for customer in range(self.total_customers):
                demand_t = (self.customers[customer]).get_energy_demand_t(time)
                consumption_t = total_consumption[customer][time]
                total_diss += (self.customers[customer]).dissatisfaction_t(demand_t, consumption_t)
            avg_dis_time[time] = total_diss/self.total_customers
        return avg_dis_time 
        

    def transfer_arrays(self, curr, prev):
        for i in range(len(prev)):
            for j in range(len(prev[i])):
                prev[i][j] = curr[i][j]
    
    

    
