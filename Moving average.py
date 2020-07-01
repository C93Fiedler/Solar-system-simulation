##Cezary Fiedler
##
##This program calculates the moving average of the data and also
##reduces the number of data points if necessary
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
        Line[0]=float(Line[0])
        Line[1]=float(Line[1])
    return Data


def Save_File(Data, File_Name):
    ##save data to a file
    File=open(File_Name, "w")
    File.write("Arbitrary Units\tTime (years)\n")
    for Data_Point in Data:
        File.write(str(Data_Point[0])+"\t"+str(Data_Point[1])+"\n")
    File.close

def Moving_Average(Data, Point_Number):
    New_Data=[]
    for Counter in range(int(Point_Number/2), len(Data)-int(Point_Number/2)):
        ##next if statement used to reduce number of data points,
        ##remove it if working with the annual sunspot number.
        if Counter%2000==0:
            Sum=0
            for x in range(0,Point_Number):
                Sum+=Data[Counter-int(Point_Number/2)+x][0]
            New_Data.append([Sum/Point_Number, Data[Counter][1]])
    return New_Data

print "Processing distance data."
Data=Load_Data("Distance For Graph.txt")
Data=Moving_Average(Data, 33000)
Save_File(Data, "Moving Average Distance For Graph.txt")
print "Processing speed data."
Data=Load_Data("Speed For Graph.txt")
Data=Moving_Average(Data, 33000)
Save_File(Data, "Moving Average Speed For Graph.txt")
print "Processing acceleration data."
Data=Load_Data("Acceleration For Graph.txt")
Data=Moving_Average(Data, 33000)
Save_File(Data, "Moving Average Acceleration For Graph.txt")
##error is returned if the user presses enter without typing anything, so
##if error is detected ignore it
try:
    input("Finished. Press enter to exit.")
except Exception:
    pass
