import dynamic_pricing_model as dpm
import os
import matplotlib.pyplot as plt

iters = int(input("Enter the number of iterations: "))
disp = int(input("Enter 1 to display: ")) == 1
DPM = dpm.DynamicPricingModel(iterations=iters, display=disp)

# adding customers to the model
elastic_coeffs = [-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.5,-0.5,-0.5,-0.5,-0.7,-0.7,-0.7,-0.7,-0.7,-0.5,-0.5,-0.5]

# customer 1
an = 0.8
bn = 0.1
dmin = 0.1
dmax = 0.5
energy_demand_1 = [19, 18.5, 18.7, 18.5, 18.2, 17, 17.2, 18, 19, 21.8, 23, 23.2, 23.5, 24.4, 25.1, 27, 27.2, 27.3, 27.2, 27.35, 27, 25.4, 24.1, 22]
DPM.add_customer(an, bn, dmin, dmax, energy_demand_1, elastic_coeffs)

# customer 2
an = 0.5
bn = 0.1
dmin = 0.1
dmax = 0.5
energy_demand_2 = [19.5, 18.7, 18.5, 18.7, 20.6, 20.9, 23.8, 27.4, 31.6, 33, 35.8, 35.9, 36.1, 38, 40.5, 39.4, 38.2, 36.4, 33.1, 33, 31.1, 27.6, 26.8, 23.6]
DPM.add_customer(an, bn, dmin, dmax, energy_demand_2, elastic_coeffs)

# customer 3
an = 0.3
bn = 0.1
dmin = 0.1
dmax = 0.5
energy_demand_3 = [20.3, 20, 19.9, 20, 20.4, 21.6, 24.7, 27.4, 31.4, 33.2, 36.4, 37.3, 38.2, 40.5, 40.6, 40.5, 39.6, 38.2, 36.8, 36.1, 33.1, 27.8, 24.2, 22.1]
DPM.add_customer(an, bn, dmin, dmax, energy_demand_3, elastic_coeffs) 

# adding a grid operator
wholesale_prices = [0.6,0.7,0.5,0.6,0.4,0.1,0.4,1.3,2.1,1.8,1.9,1.8,1.6,1.3,4.6,5.9,0.3,0.4,1.3,2.2,4.1,2.5,1.3,0.2]
DPM.add_grid_operator(wholesale_prices)

# adding a service provider
k1 = 1.5
k2 = 1.5
profit_importance = 0.9
min_wholesale_price = min(wholesale_prices)
max_wholesale_price = max(wholesale_prices)
customers = 3
energy_demands = [energy_demand_1, energy_demand_2, energy_demand_3]
N0 = 1
DPM.add_service_provider(k1, k2, min_wholesale_price, max_wholesale_price, customers, energy_demands, profit_importance, N0)

# training the model
_, best_time_prices = DPM.train()


##daily_avgdiss_p_iter = DPM.daily_avg_diss_p_iter
##daily_tot_p_iter = DPM.daily_tot_prof_p_iter
##iter_tracker = [i*1000 for i in range(len(daily_avgdiss_p_iter))]
##parent_direct = "D:/Desktop/dynamic_pricing/"
##name_of_direct = "performance_of_model_ovr_iterations"
##path = os.path.join(parent_direct, name_of_direct)
##try:
##    os.mkdir(path)
##except OSError as error:
##    print("overwritting plots")
##
##plt.title("daily average dissatisfaction over iterations")
##plt.xlabel("iterations")
##plt.ylabel("daily average dissatisfaction")
##plt.plot(iter_tracker, daily_avgdiss_p_iter)
##plt.savefig(path + "/daily_avg_diss.png")
##plt.clf()
##
##plt.title("daily total profit over iterations")
##plt.xlabel("iterations")
##plt.ylabel("daily total profit")
##plt.plot(iter_tracker, daily_tot_p_iter)
##plt.savefig(path + "/daily_total_profit.png")
##plt.clf()


total_consumption = DPM.check_total_consumption(best_time_prices)
total_profits = DPM.check_total_profit(best_time_prices, total_consumption)
avg_dissatisfaction = DPM.average_dissatisfaction(total_consumption)
print("total consumption: ")
for i in range(len(total_consumption)):
    print("Customer " + str(i) + ": " + str(total_consumption[i]))

print("total profits: ")
print(total_profits)

print("average dissatisfaction: ")
print(avg_dissatisfaction)

parent_direct = "D:/Desktop/dynamic_pricing/"
name_of_direct = "iteration_" + str(iters)

path = os.path.join(parent_direct, name_of_direct)

try:
    os.mkdir(path)
except OSError as error:
    print("folder already exists, files will be overwritten")

with open(path + "/total_consumption.txt", "w") as file:
    for i in range(len(total_consumption)):
        file.write("Customer " + str(i) + "\n")
        file.write("-------------------------\n")
        file.write("time : total consumption\n===========\n") 
        for j in range(len(total_consumption[i])):
            file.write("time " + str(j) + ": " + str(total_consumption[i][j]) + "\n")

with open(path + "/total_profits.txt", "w") as file:
    file.write("time : total profit over all customers\n======================\n")
    for i in range(len(total_profits)):
        file.write("time " + str(i) + ": " + str(total_profits[i]) + "\n")

with open(path + "/average_dissatisfaction.txt", "w") as file:
    file.write("time : average dissatisfaction over all customers\n============================\n")
    for i in range(len(avg_dissatisfaction)):
        file.write("time " + str(i) + ": " + str(avg_dissatisfaction[i]) + "\n")

time_x_axis = [i for i in range(24)]

plt.title("total_consumption over time")
plt.xlabel("time")
plt.ylabel("total consumption")
plt.plot(time_x_axis, total_consumption[0])
plt.plot(time_x_axis, total_consumption[1])
plt.plot(time_x_axis, total_consumption[2])
plt.savefig(path + "/total_consumption.png")

plt.clf()
plt.title("average dissatisfaction over time")
plt.xlabel("time")
plt.ylabel("average dissatisfaction")
plt.plot(time_x_axis, avg_dissatisfaction)
plt.savefig(path + "/avg_diss_plot.png")

plt.clf()
plt.title("total profit (all customers) over time")
plt.xlabel("time")
plt.ylabel("total profit")
plt.plot(time_x_axis, total_profits)
plt.savefig(path + "/total_profits.png") 
