from pickle import FALSE, TRUE
from pprint import pprint
import re

strain9_file = "newLocation9.bed"
strain160_file = "newLocation160.bed"
newFile = None
newInsert_file = None

def parse_strain160(fname):
    with open(fname, "r") as fh:

        for line in fh:
            line = line.strip()
            values = line.split()
            chromosome = values[0]
            seq_start = values[1]
            seq_end = values[2]
            seq_ID= values[3]

            #return the chromosome, sequence start position and sequence end position and the sequence ID
            #the sequence ID contains the repeatmasker ID, nanopore ID, and TE element name
            yield chromosome, seq_start, seq_end, seq_ID, values
            #yield values

def find_match(fname,seq_name, seq_len160):
    with open(fname, "r") as fh:
        chromosome = ""
        seq_start = '\0'
        seq_end = '\0'
        seq_ID= ""

        for line in fh:
            line = line.strip()  # Remove trailing newline characters.
            values = line.split()
            chromosome = values[0]
            seq_start = values[1]
            seq_end = values[2]
            seq_ID= values[3]

            seq_len9 = int(seq_end) - int(seq_start)

            #if(seq_ID == seq_name):
            #    yield values, seq_ID
            if(seq_ID == seq_name and seq_len160 == seq_len9):
               yield values, seq_ID
        return(values, seq_ID)

def findRepeats(fname,arr):
    newInsert_file = fname
    print("160:" + arr[1])
    with open(fname, "r") as fh:
        for line in fh:
            line = line.strip()
            values = line.split()            
            if(values[0] == arr[0] and values[1] == arr[1]):
                return 1
    return 0
    print(newInsert_file)



if newFile:
        newFile.close()
new_filename = 'newInsertionsStrict.bed'
newFile = open(new_filename, "w")

previousRead = ""

for entry in parse_strain160(strain160_file):
    chromosome = entry[0]
    left_coord = entry[1]
    right_coord = entry[2]
    seq_ID = entry[3]
    found160 = entry[4]

    seqLen160 = int(right_coord) - int(left_coord)
    
    for match in find_match(strain9_file, seq_ID, seqLen160):
        if(previousRead != found160[1]):
            found9 = match[0]
            str160 = ("\t".join(found160))
            newFile.write(str160+"\n")
            str9 = ("\t".join(found9))
            newFile.write(str9+"\n")
            previousRead = found160[1]
        else:
            print(previousRead)
        #exists = findRepeats(new_filename,found160)
        #if(exists == 0 ):
        #    found9 = match[0]
        #    str160 = ("\t".join(found160))
        #    newFile.write(str160+"\n")
        #    str9 = ("\t".join(found9))
        #    newFile.write(str9+"\n")
        
    
    #print ("Chromosome: " + chromosome + "\tSequence ID: "+seq_ID+"\tLeft: "+left_coord+"\tRight: "+right_coord+"\n")


        