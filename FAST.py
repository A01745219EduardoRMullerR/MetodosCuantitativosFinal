from email.utils import localtime
import math
import time

# Load data. 
def loadData(txt,acksRTT): 
    file = open(txt, 'r')
    lines = file.readlines()
    acksRTT = len(lines) # Numero de paquetes del archivo txt
    file.close()
    return lines, acksRTT

# Calculate target cwnd
def calculateTcwnd(alpha,cwnd,Tcwnd,sRTT,minRTT):
    a = (minRTT/sRTT) * cwnd + alpha
    b = -0.5 * cwnd 
    Tcwnd = min((2*cwnd), (b + 0.5*a))

# Calculate Average flow throughput Bk

def calculateBk(sRtt, T, acksRTT, bk):
    bk = (T * bk) +  (1 - T)*(acksRTT/sRtt) 
    acksRTT -= 1
    return bk, acksRTT

# Calculate ack cwnd 
def calculateACKcwnd(acksRTT, Tcwnd, cwnd):
    if (Tcwnd > cwnd and acksRTT > 0):
        cwnd = (Tcwnd - cwnd)/acksRTT
    elif(Tcwnd < cwnd):
        cwnd = Tcwnd

# if Loss 
def calculateIfLoss(Tcwnd,cwnd,sst):
    cwnd = cwnd/2
    Tcwnd = cwnd
    sst = cwnd

# Calculate Timeout
def calculateTimeout(minRTT,sRTT,T,acksRTT,Tcwnd,cwnd,bk,sst,alpha):
    sst = max((cwnd/2),sRTT)
    cwnd = sRTT
    Tcwnd = cwnd

# Calculate alpha 
def calculateAlpha(bk,alpha):
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
    # else:
    #     print("gg no alpha: ", alpha)
            
    
    
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
    # Initial global variables 
    minRTT = 20 #ms minimum Round trip time 
    sRTT = 50 #ms   Average Round trip time. 
    T = 0.5  # Peso moral de su proyecto, profe. 
    acksRTT = 0 # Numero de paquetes del archivo txt. 
    Tcwnd = 0 # Target Congestion window. 
    cwnd = 0 # Actual Congestion window. 
    bk = 0  # Average flow
    sst = 0 # Slow Start Time.  
    alpha = 8 # Parametro de congestion de paqueqtes
    receiver = []

    # Enviar paquetes 
    data_to_send, acksRTT = loadData("TestTimeout.txt",acksRTT) 
    print("acksRTT",acksRTT)
    for line in  data_to_send:
        init_time = time.time() #Timestamp
        
        receiver.append(line) #Line from one list goes to the other

        delta = time.time() - init_time #How much time it took
        # Calcular BK
        bk, acksRTT = calculateBk(sRTT, T, acksRTT, bk)
        print(bk)
        # Calcular alpha inicial.
        calculateAlpha(bk, alpha)

        # Si acksRtt > alpha algo Loss 
        if ( acksRTT > alpha ):
            calculateIfLoss(Tcwnd,cwnd,sst)
            # if misma situacion por x timepo llama a timeout. 

        # if Tcwnd > cwnd calcular cwnd 
        if (Tcwnd > cwnd):
            calculateTcwnd(alpha,cwnd,Tcwnd,sRTT,minRTT)

        # Llamar cada 20ms 
        if ((int(delta*10))%2 == 0):
            calculateTcwnd(alpha,cwnd,Tcwnd,sRTT,minRTT)

        # Llamar cada 200 s
        if (int(delta/100)%2 == 0):
            calculateAlpha(bk, alpha)
        #print("Parameters: \n\tTcwnd: ", Tcwnd, "\n\tCwnd: ", cwnd)
    
main()