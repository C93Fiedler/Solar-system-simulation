##Cezary Fiedler
##
##This program simulates the motion of the solar system,
## calculates the position of the barycenter and saves it and the distance,
##both relative to the sun.
##Some code uses visual python module, but it was all commented out as it
##was only there to check the stability of the program.

from __future__ import division
from time import gmtime, strftime
import datetime, threading
###########################################################################
##from visual import *
###########################################################################
##global variables
global dt, Bodies, Spheres
##gravitational constant and time step of -3 hours
G=6.67384e-11
dt=-10800

###########################################################################
####visual python code to check the simulation is running smoothly
####
####thread for updating the position on the screen separately
####from the calculation
####so that the speed of the calculation is not affected
##class Visual_Thread(threading.Thread):
##    def __init__(self,ID):
##        threading.Thread.__init__(self)
##        self.ID=ID
##        ##stop variable so that the thread can be stopped at
##        ##some point if neccessary
##        self.Stop=False
##    def run(self):
##        global Bodies, Spheres
##        while self.Stop==False:
##            rate(25)
##            for Counter in range(0, len(Bodies)):
##                ##update the positions
##                Spheres[Counter].pos=Bodies[Counter].Position
###########################################################################           
class Body():
    ##a separate class from spheres so that the simulation can be run without
    ##the visual python module
    def __init__(self, Name, Mass, Position, Velocity):
        self.Name=Name
        self.Mass=Mass
        self.Position=Position
        self.Velocity=Velocity
        self.Acceleration=[0,0,0]
    def Update(self):
    ##function to update velocity and position
        global dt
        for Counter in range(0,3):
            self.Velocity[Counter]+=self.Acceleration[Counter]*dt
            self.Position[Counter]+=self.Velocity[Counter]*dt
        self.Acceleration=[0,0,0]

def Distance(v1,v2,Squared):
    ##function to work out the distance between two objects
    r2=(v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2
    if Squared:
        return r2
    return r2**(0.5)

def Mag(v):
    ##function to work out the magnitude of a vector
    return (v[0]**2+v[1]**2+v[2]**2)**(0.5)

def Save_Barycenter(Bodies):
    ##function to work out the coordinates of the barycenter of the system
    Total_Mass=0
    for Body in Bodies:
        Total_Mass+=Body.Mass
    Total_Moment=[0,0,0]
    for Body in Bodies:
        for Counter in range(0,3):
            Total_Moment[Counter]+=Body.Mass*Body.Position[Counter]
    Barycenter=[Total_Moment[0]/Total_Mass,Total_Moment[1]/Total_Mass,
                Total_Moment[2]/Total_Mass]
    for Counter in range(0,3):
        Barycenter[Counter]-=Bodies[0].Position[Counter]
    return Barycenter

def Distance_Save_File(Data):
    ##save distance data to a file
    File=open("Distance Data With Mercury.txt", "w")
    File.write("Distance (m)\tTime (years)\n")
    for Data_Point in Data:
        File.write(str(Mag(Data_Point[0]))+"\t"+str(Data_Point[1])+"\n")
    File.close

def Position_Save_File(Data):
    ##save position data of the sun relative to the barycenterto a file
    File=open("Position Data With Mercury.txt", "w")
    File.write("x (m)\ty (m)\tz (m)\tTime (years)\n")
    for Data_Point in Data:
        File.write(str(-Data_Point[0][0])+"\t"+str(-Data_Point[0][1])+"\t"+
                   str(-Data_Point[0][2])+"\t"+str(Data_Point[1])+"\n")
    File.close
    
def Relabel_Data_Points(Data):
    ##function to change time values to be given in years for easy plotting
    ##3 hours divided by 8766 hours in a 1-year period, assuming a year has
    ##365.25 days
    Time_Step=3/8766
    ##loop over all data points backwards, as the first date is
    ##1600-01-01 02:00:00 and it is easier to work from there forward in time
    for x in range(1, len(Data)+1):
        ##date is always stored in the last position
        Data[-x][-1]=1600+2/876600+(x-1)*Time_Step
    return Data
        
            

##bodies store holds parameters of the sun, the eight planets and pluto
##all data obtained from http://ssd.jpl.nasa.gov/?horizons
##data corresponding to the time A.D. 2014-Dec-15 17:00:00.0000 CT
Current_Simulation_Time=datetime.datetime(2014, 12, 15, 17)
##time difference of 3 hours for use with datetime variables
Time_Delta=datetime.timedelta(0,0,0,0,0,3)
##variable for determining when the simulation should stop
##corresponds to A.D. 1600-Jan-01 00:00:00.0000 CT
Stop_Time=datetime.datetime(1600, 01, 01)
Bodies=[]
Bodies.append(Body("Sun", 1.989e30, [0,0,0], [0,0,0]))
Bodies.append(Body("Mercury", 3.302e23,[7502.762366480218e6,
                                        -6814.803724364910e7,
                                        -6256.586108144255e6],
                   [3865.078716563220e1,
                    7833.068180028987, -2906.059784647593]))
Bodies.append(Body("Venus",48.685e23,[4311.962115210310e7,
                                      -9992.935376925892e7,
                                      -3857.976889148322e6],
                   [3191.845728065822e1,  1375.773817138126e1,
                    -1653.428474963004]))
Bodies.append(Body("Earth",5.972e24,[1684.896793060777e7,
                                     1462.754754185983e8,
                                     -4766.646454334288e3],
                   [-3007.923403074708e1,  3306.984519112139,
                    -1075.826039865618e-3]))
Bodies.append(Body("Mars",6.419e23,[1917.784861386029e8,
                                    -7668.599501484169e7,
                                    -6313.884976784745e6],
                   [9924.569646596309,  2457.024304170871e1,
                    2712.251732712747e-1]))
Bodies.append(Body("Jupiter",1898e24,[-5444.430594673783e8,
                                      5794.778592065459e8,
                                      9776.146395945920e6],
                   [-9687.654342264706, -8336.919797313161,
                    2514.014189187982e-1]))
Bodies.append(Body("Saturn",5.683e26,[-8196.772303626006e8,
                                      -1241.539217129072e9,
                                      5421.518698252863e7],
                   [7527.361980177939, -5356.644070401951,
                    -2061.409416048469e-1]))
Bodies.append(Body("Uranus",86.081e24,[2890.377981397986e9,
                                       7767.985595002608e8,
                                       -3454.630677872520e7],
                   [-1823.657235608216,  6250.428514831001,
                    4695.458108812854e-2]))
Bodies.append(Body("Neptune",102.4e24,[4114.988703900040e9,
                                       -1778.731462985824e9,
                                       -5819.082633544001e7],
                   [2113.734306537582,  5013.236052034588,
                    -1517.246511347902e-1]))
Bodies.append(Body("Pluto",1.307e22,[1099.096328546764e9,
                                     -4775.167972749305e9,
                                     1929.639641398818e8],
                   [5396.591172086938,  8999.778242775021e-2,
                    -1595.295426370992]))
##Save the barycenter at the starting time
Barycenter_Data=[[Save_Barycenter(Bodies),Current_Simulation_Time]]
##print time when the simulation starts
print "Simulation started at " +str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
###########################################################################
####visual python code to check the simulation is running smoothly
####Spheres contains all the spheres on the visual display
##Spheres=[]
##for Body in Bodies:
##    Spheres.append(sphere(pos=Body.Position, color=color.yellow,
##                          radius=2e10))
####initialize and start the thread
##Thread1=Visual_Thread(1)
##Thread1.start()
###########################################################################
while Stop_Time<Current_Simulation_Time:
    Current_Simulation_Time-=Time_Delta
    Body_Counter=-1
    for Body1 in Bodies:
        Body_Counter+=1
        ##use a temporary store to make the code easy to read and only
        ##loop over every body as few times as possible
        Temp_Counter=Body_Counter
        Temp_Store=Bodies[Body_Counter+1:]
        for Body2 in Temp_Store:
            Temp_Counter+=1
            ##displacement vector from body1 to body2
            r=[Body2.Position[0]-Body1.Position[0],
               Body2.Position[1]-Body1.Position[1],
               Body2.Position[2]-Body1.Position[2]]
            ##update acceleration using a=mGr/r^3, where r is the
            ##displacement vector and r^3 is the distance cubed
            Bodies[Body_Counter].Acceleration[0]+=(
                G*Bodies[Temp_Counter].Mass*r[0]/(Mag(r)**3))
            Bodies[Body_Counter].Acceleration[1]+=(
                G*Bodies[Temp_Counter].Mass*r[1]/(Mag(r)**3))
            Bodies[Body_Counter].Acceleration[2]+=(
                G*Bodies[Temp_Counter].Mass*r[2]/(Mag(r)**3))
            Bodies[Temp_Counter].Acceleration[0]-=(
                G*Bodies[Body_Counter].Mass*r[0]/(Mag(r)**3))
            Bodies[Temp_Counter].Acceleration[1]-=(
                G*Bodies[Body_Counter].Mass*r[1]/(Mag(r)**3))
            Bodies[Temp_Counter].Acceleration[2]-=(
                G*Bodies[Body_Counter].Mass*r[2]/(Mag(r)**3))
        if len(Temp_Store)==1:
            Temp_Store=[]
        Temp_Store=Temp_Store[1:]
    for Body in Bodies:
        Body.Update()
    ##after every loop is completed save the position of the barycenter relative to the Sun
    Barycenter_Data.append([Save_Barycenter(Bodies),Current_Simulation_Time])
print "Simulation ended at "+str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print "Saving data to files"
Relabel_Data_Points(Barycenter_Data)
Distance_Save_File(Barycenter_Data)
Position_Save_File(Barycenter_Data)
##error is returned if the user presses enter without typing anything, so
##if error is detected ignore it
try:
    input("Data saved. Press enter key to exit.")
except Exception:
    pass
