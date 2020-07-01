##Cezary Fiedler
##
##This program is used to work out the speed and acceleration from
##displacement data.
from __future__ import division

def Load_Data(File_Name):
    File=open(File_Name, "r")
    Data=File.read()
    File.close
    #split the data into lines
    Data=Data.split("\n")
    #remove the first line which has the labels and the last line
    ##which is blank
    Data=Data[1:-1]
    for Counter in range(0,len(Data)):
        Data[Counter]=Data[Counter].split("\t")
        Data[Counter]=[[float(Data[Counter][0]),float(Data[Counter][1]),
                        float(Data[Counter][2])],float(Data[Counter][3])]
    return Data

def Differentiate(Data):
    ##function for numerical differentiation
    ##assuming time step of 3 hours
    New_Data=[]
    for Counter in range(1,len(Data)):
        New_Data.append([[(-Data[Counter][0][0]+Data[Counter-1][0][0])/10800,
                          (-Data[Counter][0][1]+Data[Counter-1][0][1])/10800,
                          (-Data[Counter][0][2]+Data[Counter-1][0][2])/10800],
                         Data[Counter][1]])
    return New_Data

def Magnitude_Save_File(Data, File_Name):
    ##function to save to a file
    File=open(File_Name, "w")
    File.write("Value\tTime (years)\n")
    for Data_Point in Data:
        File.write(str(Mag(Data_Point[0]))+"\t"+str(Data_Point[1])+"\n")
    File.close

def Mag(v):
    ##function to work out the magnitude of a vector
    return (v[0]**2+v[1]**2+v[2]**2)**(0.5)

print "Calculating velocity data."
Position_Data=Load_Data("Position Data With Mercury.txt")
Velocity_Data=Differentiate(Position_Data)
print "Calculating acceleration data."
Acceleration_Data=Differentiate(Velocity_Data)
print "Saving data"
Magnitude_Save_File(Velocity_Data, "Speed.txt")
Magnitude_Save_File(Acceleration_Data, "Acceleration.txt")
##error is returned if the user presses enter without typing anything, so
##if error is detected ignore it
try:
    input("Finished. Press enter to exit.")
except Exception:
    pass

