import math
import numpy as np
import random
class Service_Provider:
    # initializer takes in various parameters for the agent that represents variables that occur in
    # the real life situation of this problem 
    def __init__(self, k1, k2, min_wholesale, max_wholesale, customers, customer_demands, profit_importance, N0, epsilon=1):
        self.bottom_price = k1*min_wholesale
        self.top_price = k2*max_wholesale
        self.actions = []
        self.num_actions = 0
        self.define_actions()
        self.q_table = [None] * customers
        self.define_qtable(customer_demands)
        self.profit_importance = profit_importance
        self.N0 = N0
        self.learning_rate = -1 
        self.calculate_learning_rate(0)
        self.discount_rate = 0.9
        self.epsilon = epsilon 

    # defines the exact prices (actions) the agent can take
    # the actions are based off the bottom price and top price
    # (represents contractual agreements) 
    def define_actions(self):
        for i in range(math.ceil(self.bottom_price), math.floor(self.top_price)+1):
            self.actions.append(i)

        self.num_actions = len(self.actions)

    # decays the epsilon based of iteration
    def calculate_epsilon(self, iteration):
        self.epsilon = 1/(iteration + 1) 

    # decays the learning rate based of time 
    def calculate_learning_rate(self, time):
        self.learning_rate = self.N0 * math.exp(0.0005*time) 

    # defines a qtable based of the time period number of customers and
    # number of actions 
    def define_qtable(self, demands):
        if  len(self.q_table) != len(demands):
            raise Exception("demands and number of customers is not the same") 
        for i in range(0, len(self.q_table)):
            self.q_table[i] = [[0] * (self.num_actions) for _ in range(len(demands[i]))]

    # gets the best action, but is based of epsilon-greedy
    # so picks the argmax action 1-epsilon percent of the times
    # picks a random action epsilon percent of times 
    def get_best_action_and_value_for_n_t(self, time, customer):
        if time >= len(self.q_table[customer]):
            time = len(self.q_table[customer]) - 1 
        max_ind = np.argmax(self.q_table[customer][time]) if random.random() > self.epsilon else random.randint(0, (len(self.q_table[customer][time])-1))
        return self.actions[max_ind], self.q_table[customer][time][max_ind], max_ind

    # computes the reward which is the overall profit for agent and cost for customers. 
    def compute_reward(self, retail_t_n, wholesale_t, total_consume, dissatisfaction):
        sp_prof = self.profit_importance * ((retail_t_n - wholesale_t)*(total_consume))
        cu_cost = (1 - self.profit_importance) * ((retail_t_n * total_consume) + dissatisfaction)
        return sp_prof - cu_cost

    # updates the q value for an action at a time for a specific customer 
    def update_q_value(self, prev_val, customer, time, max_ind, wholesale_t, total_consume, dissatisfaction):
        reward = self.compute_reward(self.actions[max_ind], wholesale_t, total_consume, dissatisfaction)
        _, next_max_q, _ = self.get_best_action_and_value_for_n_t(time+1, customer)
        max_next_reward = (self.discount_rate) * next_max_q 
        self.q_table[customer][time][max_ind] = prev_val + ((self.learning_rate) * (reward + max_next_reward - prev_val))            
        return reward    
    

        
    
