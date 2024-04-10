This code is a python implementation of the research paper by the name "A Dynamic pricing demand response algorithm for smart grid:
Reinforcement learning approach" by Renzhi Lu, Seung Ho Hong, Xiongfeng Zhang. 

Purpose: 
The purpose of this project was to create a model-free RL algorithm that can dynamically decide retail price of electricity per time period 
given the demands of a customer for that time period and wholesale price for that time period. 
The model tries to maximize the profits for the service provider while minimizing the cost of the customers. The algorithm is able to account 
for the "attitude" of a customer and try to minimize the quantified "dissatisfaction" of the customer. The program is able to account for 
multiple customers and manage the retail price of the electricity by the specific demands of each customer. 

Results: 
The results using the default test cases are given in the directories of the name "iterations_{number of iterations}". The folder contains the ideal 
prices of the electricity for every time section per time period. It plots the dissatisfaction of the customers per time period, the total profit per time period, 
and the overall energy consumption of the customers per time period. 
The test contains three customers, with varying "attitudes" towards price for electricity. 
------------------------------------------------------------------------------------------------------------------------------------------------------
Another test folder is called "performance_of_model_over_iterations," which checks the daily total profit and the daily average dissatsifaction over all 
customers for the best price decided by the model with 1000 iterations. It contains the plot of these values per 1000 iterations and writes the values 
in the txt files. 
