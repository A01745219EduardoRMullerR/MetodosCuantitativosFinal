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
sRTT = 50 #ms   Average Round trip time. 
T = 0.5  # Peso moral de su proyecto, profe. 
acksRTT = 0 # Numero de paquetes del archivo txt. 
Tcwnd = 0 # Target Congestion window. 
cwnd = 0 # Actual Congestion window. 
bk = 0  # Average flow
sst = 0 # Slow Start Time.  
alpha = 0 # Parametro de congestion de paqueqtes

# Load data. 
def loadData(txt): 
    global acksRTT
    
    file = open(txt, 'r')
    lines = file.readlines()
    acksRTT = len(lines) # Numero de paquetes del archivo txt
    file.close()
    return lines

# Calculate target cwnd
def calculateTcwnd():
    global minRTT  
    global sRTT 
    global Tcwnd 
    global cwnd  
    global alpha
    a = (minRTT/sRTT) * cwnd + alpha
    b = -0.5 * cwnd 
    Tcwnd = min((2*cwnd), (b + 0.5*a))

# Calculate Average flow throughput Bk

def calculateBk():
    global sRTT
    global T  
    global acksRTT 
    global bk 
    bk = T * bk +  (1 - T )*(acksRTT/sRTT) 
    acksRTT = 0

# Calculate ack cwnd 
def calculateACKcwnd():
    global acksRTT 
    global Tcwnd 
    global cwnd 
    if (Tcwnd > cwnd and acksRTT > 0):
        cwnd = (Tcwnd - cwnd)/acksRTT
    elif(Tcwnd < cwnd):
        cwnd = Tcwnd

# if Loss 
def calculateIfLoss():
    global Tcwnd 
    global cwnd 
    global sst  
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

# Calculate alpha 
def calculateAlpha():
    global bk
    global alpha
    a1=8
    a2=20
    a3=200
    m0m1=1500
    m1m0=1250
    m1m2=15000
    m2m1=12500
    bk = int(bk)

    if(alpha == a1 & bk >= m0m1):
        alpha = a2
    elif(alpha == a2 & bk <= m1m0):
        alpha = a1
    elif(alpha == a2 & bk >= m1m2):
        alpha = a3
    elif(alpha == a3 & bk <= m2m1):
        alpha = a2
    else:
        print("gg no alpha: ", alpha)
    
    return alpha

def testAck():
    init_time = time.time()
    sender = loadData("TestTimeout.txt")
    receiver = []
    global cwnd
    cwnd = .01
    Tcwnd = .01
    for line in sender:
        delta = time.time() - init_time
        print("Delta", delta)
        print("CWND: ", cwnd)
        if (delta > cwnd):
            print("There's congestion \nDelta CWND: ", delta, cwnd)
            cwnd += 1
            calculateACKcwnd()
        else:
            receiver.append(line)
            
            
def testLoss():
    print("---------------------------------------------------------------------------------------------------")
    print("------------------------TEST LOSS------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------\n\n")
    init_time = time.time()
    file = open("TestLoss.txt", 'r')
    lines = file.readlines()
    sender = lines
    receiver = []
    Tcwnd = .001
    receiver.append(sender[0])
    delta = time.time() - init_time
    cwnd = delta
    print("Initial Parameters: \n\tTcwnd: ", Tcwnd, "\n\tCwnd: ", cwnd)
    
    
def TestTimeOut():
    init_time = time.time()
    file = open("TestTimeout.txt", 'r')
    lines = file.readlines()
    sender = lines
    receiver = []
    Tcwnd = .001
    receiver.append(sender[0])
    delta = time.time() - init_time
    cwnd = delta

# main
def main(): 
    
    global acksRTT 
    global Tcwnd 
    global cwnd  
    global alpha
    receiver = []

    # Enviar paquetes 
    data_to_send = loadData("TestAck.txt") 
    
    for line in  data_to_send:
        init_time = time.time() #Timestamp
        
        receiver.append(line) #Line from one list goes to the other

        delta = time.time() - init_time #How much time it took
        # Calcular BK
        calculateBk()
        # Calcular alpha inicial.
        calculateAlpha()

        # Si acksRtt > alpha algo Loss 
        if ( acksRTT > alpha ):
            calculateIfLoss()

        # if Tcwnd > cwnd calcular cwnd 
        if (Tcwnd > cwnd):
            calculateTcwnd()

        # Llamar cada 20ms 
        if ((int(delta*10))%2 == 0):
            calculateTcwnd()

        # Llamar cada 200 s
        if (int(delta/100)%2 == 0):
            calculateAlpha()
        print("Parameters: \n\tTcwnd: ", Tcwnd, "\n\tCwnd: ", cwnd)


    
main()