import math

# Initial variables 
minRTT = 20 #ms minimum Round trip time 
sRTT = 50 #ms   Average Roung 
T = 0.5  # Peso moral de su proyecto, profe. 
acksRTT = 0 # Numero de paquetes del archivo txt. 
Tcwnd = 0 # Target Congestion window. 
cwnd = 0 # Actual Congestion window. 
Bk = 0  # Average flow
sst = 0 # Slow Start Time.  
alpha = 0

# Load data. 
def loadData():
    acksRTT = 0 # Numero de paquetes del archivo txt

# Calculate target cwnd
def calculateTcwnd():
    a = (minRTT/sRTT) * cwnd + alpha
    b = -0.5 * cwnd 
    Tcwnd = min((2*cwnd), (b + 0.5*a))

# Calculate Average flow throughput Bk

def calculateBk():
    Bk = T * Bk +  (1 - T )*(acksRTT/sRTT) 
    acksRTT = 0

# Calculate ack cwnd 
def calculateACKcwnd(): 
    if (Tcwnd > cwnd and acksRTT > 0):
        cwnd = (Tcwnd - cwnd)/acksRTT
    elif(Tcwnd < cwnd):
        cwnd = Tcwnd

# if Loss 
def calculateIfLoss():
    cwnd = cwnd/2
    Tcwnd = cwnd
    sst = cwnd

# Calculate Timeout
def calculateTimeout():
    sst = max((cwnd/2),sRTT)
    cwnd = sRTT
    Tcwnd = cwnd

# Calcculate alpha 
def calculateAlpha():
    alpha = 0           


# main
def main(): 
    # Enviar paquetes 

    # Calcular acksRtt 

    # Si acksRtt > a algo Loss 

    # if Tcwnd > cwnd calcular cwnd 

    # Llamar cada 20ms 
    calculateBk()
    # Llamar cada 200 s
    calculateAlpha()