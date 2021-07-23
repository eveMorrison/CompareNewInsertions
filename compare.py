from pprint import pprint
import re

strain9_file = "newLocation9.bed"
strain160_file = "newLocation160.bed"
newFile = None

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

            if(seq_ID == seq_name and seq_len160 == seq_len9):
                #print (values)
                yield values, seq_ID
        return(values, seq_ID)


if newFile:
        newFile.close()
new_filename = 'newInsertionsLeng.bed'
newFile = open(new_filename, "w")

for entry in parse_strain160(strain160_file):
    chromosome = entry[0]
    left_coord = entry[1]
    right_coord = entry[2]
    seq_ID = entry[3]
    found160 = entry[4]

    seqLen160 = int(right_coord) - int(left_coord)
    
    for match in find_match(strain9_file, seq_ID, seqLen160):
        
        found9 = match[0]
        str160 = ("\t".join(found160))
        newFile.write(str160+"\n")
        str9 = ("\t".join(found9))
        newFile.write(str9+"\n")
        
    
    #print ("Chromosome: " + chromosome + "\tSequence ID: "+seq_ID+"\tLeft: "+left_coord+"\tRight: "+right_coord+"\n")


        