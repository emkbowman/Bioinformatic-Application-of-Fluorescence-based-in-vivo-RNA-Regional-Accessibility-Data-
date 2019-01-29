#!/bin/python
##---------------------------------------------------------------------------------------------
## read in fasta genome file an make a string of it to index
genomefasta = open ("NC_000913.3_aka_U00096.3fasta.fasta","r")

linecounter = 0
genomestring = ""

for line in genomefasta:
    linecounter += 1
    line = line.strip()
    if linecounter > 1:
        genomestring+=(line)

print("genome saved")

genomefasta.close()

## -------------------------------------------------------------------------------------------
## source of UTR left and right coordinates.

UTRcoords = open ("Mia_minus_200_to_plus_100_K12.txt","r") ## this is your input .txt of genomic coords

linecounter = 0
UTR_Name_list = list()
UTR_direction_list = list()
UTR_left_coord_list = list()
UTR_right_coord_list = list()


for line in UTRcoords:
    linecounter += 1
    line = line.strip()
    linelist = line.split("\t")
    if linecounter > 1:
        UTR_Name_list.append(linelist[0])
        UTR_direction_list.append(linelist[1])
        UTR_left_coord_list.append(linelist[2])
        UTR_right_coord_list.append(linelist[3])


UTRcoords.close()
Number_UTRs = len(UTR_Name_list)
print("UTR specs saved")


## -------------------------------------------------------------------------------------------
##  Write sequence of UTRs from genome. UTRs on R are written as 5' to 3' in the final output, i.e. the reverse of the + strand genome sequence.
 
outputfile = open("Mia_minus_200_to_plus_100_K12.txt","w")   
outputfasta= open("outputfasta.fasta","w")
for i in range(0,Number_UTRs):
    UTR_L_coord = int(UTR_left_coord_list[i])
    UTR_R_coord = int(UTR_right_coord_list[i])
    UTR_Dir = UTR_direction_list[i]


    if UTR_Dir == "F":
        UTR_5to3_Seq = genomestring[UTR_L_coord - 1:UTR_R_coord] 
        
    if UTR_Dir == "R":
        UTR_prelim_Seq = genomestring[UTR_L_coord - 1:UTR_R_coord] 
        UTR_5to3_Seq = str()
        for nt in UTR_prelim_Seq:
            if nt == "A":
                UTR_5to3_Seq = "T" + UTR_5to3_Seq
            if nt == "G":
                UTR_5to3_Seq = "C" + UTR_5to3_Seq
            if nt == "T":
                UTR_5to3_Seq = "A" + UTR_5to3_Seq
            if nt == "C":
                UTR_5to3_Seq = "G" + UTR_5to3_Seq

    outputfasta.write(">" + UTR_Name_list[i] + "\n" + UTR_5to3_Seq + "\n")


    outputfile.write( UTR_Name_list[i] + "\t" + UTR_direction_list[i] + "\t" +
                      str(UTR_left_coord_list[i]) + "\t" + str(UTR_right_coord_list[i]) + "\t" +
                      UTR_5to3_Seq + "\n")

print("Loop for SEQ writing is finished")

outputfile.close()               
outputfasta.close()
