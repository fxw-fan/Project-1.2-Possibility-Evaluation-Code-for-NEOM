import pandas as pd
import math
import numpy as np

a = math.cos(50)
demand1 = pd.read_excel ('Predictions.xlsx')
demand = np.array(demand1.iloc[:,1])*1000 #array of demand 

df = pd.read_excel('AI DATA.xlsx')
wind_speed = np.array(df.iloc[52432:96431,9]) #array of wind speed
DNI = np.array(df.iloc[52432:96431,7])
DHI = np.array(df.iloc[52432:96431,8])
GHI = DHI + DNI*a #array of GHI
solar_power = (GHI*0.2)/1000 #array of solar power


wind_power = (0.5*wind_speed*wind_speed*wind_speed*1.23*0.4*math.pi*110*110)/1000 #array of wind power

total_solar_power= np.sum(solar_power)

total_wind_power= np.sum(wind_power)

total_demand= np.sum(demand)

solar_area = 1.1*(total_demand/total_solar_power)


turbines_num = 1.1*(total_demand/total_wind_power)

c = np.zeros((43999,100))
c[0:43999, 0] = solar_power
c[0:43999, 99] = wind_power
i = 1

while i <= 98: #loop to declare energy mix matrix (c)
    t= solar_power*(100-i) + wind_power*i
    c[0:43999, i] = t
    i += 1

initial_energy = 0

i = 0
h = np.zeros((43999,100))
while i <= 99: #loop to declare energy mix matrix (c)
   
    h[0:43999, i] = demand
    i += 1


storage1 = h - c 

storage1[0, 0:100] = storage1[0, 0:100] + initial_energy #add initial energy to storage


i= 1
while i <= 43998: #add previous rows of storage 
    u = i- 1
    storage1[i, 0:100] = storage1[i, 0:100] + storage1[u, 0:100]
    i += 1


r = np.count_nonzero(storage1 <= 0) #count zeros and negative elements in storage matrix 


while r > 0 : #remove elements less than or equal to zeros by incrementing initial energy of the storage matrix (storage1) 
    initial_energy += 10
    storage2 = h - c 
    storage2[0, 0:100] = storage2[0, 0:100] + initial_energy
    i= 1
    while i <= 43998:
        u = i -1
        storage2[i, 0:100] = storage2[i, 0:100] + storage2[u, 0:100]
        i += 1
    r = np.count_nonzero(storage2 <= 0)

#---------------------------------------------------------------#

storageMax = np.zeros([1 , 100]) # this is not done because i'm not sure where the storage matrix is
finalMatrix = np.zeros([1 , 100])


e = 100
HcostW = 603
solarPanelPrice = 1600
windTurbinePrice = 1750
HEnegDen = 39
while e > 0: # loop for the finalMatrix
    finalMatrix[0 , e] = (HcostW * storageMax ) + (e * total_solar_power * solarPanelPrice) + ((100 - e) * windTurbinePrice * total_wind_power)
    e -= 1



minOfFinalMatrix = finalMatrix[0,0]
columnNum = 0
a = 0 
while a < 99:
    if finalMatrix[0 , a+1] < minOfFinalMatrix:
        minOfFinalMatrix = finalMatrix[0 , a+1]
        columnNum = a + 1
    a += 1


rSolarArea = (columnNum / 100) * solar_area
rNumOfSolarModules = (columnNum / 100) * (solar_area / 2.4)
rNumOfWindTurbines = ((100 - columnNum) / 100) * turbines_num
rStorage = storage2[1 , columnNum]
hydrogen = rStorage / HEnegDen





