from pickle import FALSE, TRUE
from pprint import pprint
import re


#Input files
#all of the flanks that didn't match to the 160 or 9 extended bed files
strain9_file = "newInsert9dys120000.bed"
strain160_file = "newInsert160dys120000.bed"
newFile = None
newInsert_file = None


#goes through each line of the 160 file
#for each line yields the chromosome, where the sequence starts and ends, 
# the sequence ID and the full line as an array
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


#parses through the strain 9 file looking for a sequence with the same name as the 160 sequence
# yields every match
# has the abilitiy to find sequences with the exact same length between 160 and 9 
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

            if(seq_ID == seq_name):
                yield values, seq_ID
            #if(seq_ID == seq_name and seq_len160 == seq_len9):
            #   yield values, seq_ID
        return(values, seq_ID)


#closes the file if already open
#opens a new file where common sequences from 160 and 9 are stored
if newFile:
        newFile.close()
new_filename = 'newInsertionsDys120000.bed'
newFile = open(new_filename, "w")


#to avoid having repeat reads stores the strting coordinate of the previous sequence
previousRead = ""


#begin parsing the 160 file
#when parse_strain160() yields back info thake information and look for match in 9 file
for entry in parse_strain160(strain160_file):
    chromosome = entry[0]
    left_coord = entry[1]
    right_coord = entry[2]
    seq_ID = entry[3]
    found160 = entry[4]

    seqLen160 = int(right_coord) - int(left_coord)
    

    #for everymatch find print to the output file the 160 match then the 9 match
    #for every sequence that is a new insertion should have 2 lines
    # one for 9 and one for 160
    for match in find_match(strain9_file, seq_ID, seqLen160):
        #if(previousRead != found160[1]):
            found9 = match[0]
            str160 = ("\t".join(found160))
            newFile.write(str160+"\n")
            str9 = ("\t".join(found9))
            newFile.write(str9+"\n")
            previousRead = found160[1]
        #else:
            #print(previousRead)        