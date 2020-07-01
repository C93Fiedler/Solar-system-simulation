##Cezary Fiedler
##
##This program turns the data into arbitrary units
##not many comments here because it is pretty much in pseudocode
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
    for Line in Data:
        ##convert values from string to number
        Line[0]=float(Line[0])
        Line[1]=float(Line[1])
    return Data

def Find_Extremes(Data):
    Minimum=Data[0][0]
    Maximum=Data[0][0]
    for Value in Data:
        if Value[0]<Minimum:
            Minimum=Value[0]
        elif Value[0]>Maximum:
            Maximum=Value[0]
    return [Minimum,Maximum]

def Arbitrary_Scale(Data,Min,Max):
    ##using the formula y=mx+c to map all values to [0,200] where 0
    ##corresponds to the shortest distance and 200 to the longest
    m=(200-0)/(Max-Min)
    c=200-Max*m
    for Value in Data:
        Value[0]=m*Value[0]+c
    return Data

def Save_File(Data, File_Name):
    ##save data to a file
    File=open(File_Name, "w")
    File.write("Arbitrary Units\tTime (years)\n")
    for Data_Point in Data:
        File.write(str(Data_Point[0])+"\t"+str(Data_Point[1])+"\n")
    File.close

print "Processing distance data."
Data=Load_Data("Distance Data With Mercury.txt")
Min_Max=Find_Extremes(Data)
Data=Arbitrary_Scale(Data,Min_Max[0],Min_Max[1])
Save_File(Data, "Distance For Graph.txt")
print "Processing speed data."
Data=Load_Data("Speed.txt")
Min_Max=Find_Extremes(Data)
Data=Arbitrary_Scale(Data,Min_Max[0],Min_Max[1])
Save_File(Data, "Speed For Graph.txt")
print "Processing acceleration data."
Data=Load_Data("Acceleration.txt")
Min_Max=Find_Extremes(Data)
Data=Arbitrary_Scale(Data,Min_Max[0],Min_Max[1])
Save_File(Data, "Acceleration For Graph.txt")
##error is returned if the user presses enter without typing anything, so
##if error is detected ignore it
try:
    input("Finished. Press enter to exit.")
except Exception:
    pass
