from email.utils import localtime
import math
import time


global minRTT  
global sRTT
global T  
global acksRTT 
global Tcwnd 
global cwnd 
global bk 
global sst  
global alpha


# Initial global variables 
minRTT = 20 #ms minimum Round trip time 
sRTT = 50 #ms   Average Roung 
T = 0.5  # Peso moral de su proyecto, profe. 
acksRTT = 0 # Numero de paquetes del archivo txt. 
Tcwnd = 0 # Target Congestion window. 
cwnd = 0 # Actual Congestion window. 
bk = 0  # Average flow
sst = 0 # Slow Start Time.  
alpha = 0

# Load data. 
def loadData():
    global minRTT  
    global sRTT
    global T  
    global acksRTT 
    global Tcwnd 
    global cwnd 
    global bk 
    global sst  
    global alpha
    acksRTT = 0 # Numero de paquetes del archivo txt

# Calculate target cwnd
def calculateTcwnd():
    global minRTT  
    global sRTT
    global T  
    global acksRTT 
    global Tcwnd 
    global cwnd 
    global bk 
    global sst  
    global alpha
    a = (minRTT/sRTT) * cwnd + alpha
    b = -0.5 * cwnd 
    Tcwnd = min((2*cwnd), (b + 0.5*a))

# Calculate Average flow throughput Bk

def calculateBk():
    global minRTT  
    global sRTT
    global T  
    global acksRTT 
    global Tcwnd 
    global cwnd 
    global bk 
    global sst  
    global alpha
    bk = T * bk +  (1 - T )*(acksRTT/sRTT) 
    acksRTT = 0

# Calculate ack cwnd 
def calculateACKcwnd():
    global minRTT  
    global sRTT
    global T  
    global acksRTT 
    global Tcwnd 
    global cwnd 
    global bk 
    global sst  
    global alpha 
    if (Tcwnd > cwnd and acksRTT > 0):
        cwnd = (Tcwnd - cwnd)/acksRTT
    elif(Tcwnd < cwnd):
        cwnd = Tcwnd

# if Loss 
def calculateIfLoss():
    global minRTT  
    global sRTT
    global T  
    global acksRTT 
    global Tcwnd 
    global cwnd 
    global bk 
    global sst  
    global alpha
    cwnd = cwnd/2
    Tcwnd = cwnd
    sst = cwnd

# Calculate Timeout
def calculateTimeout():
    global minRTT  
    global sRTT
    global T  
    global acksRTT 
    global Tcwnd 
    global cwnd 
    global bk 
    global sst  
    global alpha
    sst = max((cwnd/2),sRTT)
    cwnd = sRTT
    Tcwnd = cwnd

# Calcculate alpha 
def calculateAlpha():
    alpha = 0           


def testAck():
    init_time = time.time()
    file = open("TestAck.txt", 'r')
    lines = file.readlines()
    sender = lines
    receiver = []
    global cwnd
    cwnd = .01
    for line in sender:
        delta = time.time() - init_time
        print(delta)
        if (delta > cwnd):
            print("congestion")
            cwnd += 1
            calculateACKcwnd()
        else:
            receiver.append(line)
            


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
    
testAck()
