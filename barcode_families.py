import csv

# filter_emptyrows method removes any rows that are completely empty from the csv file, returns new filtered csv
def filter_emptyrows(in_file,out_file):
    inp = open(in_file, 'r')
    output = open(out_file, 'w')
    writer = csv.writer(output)
    for row in csv.reader(inp):
        if any(row):
            writer.writerow(row)
    inp.close()
    output.close()

# filter_onlyAs method takes in a csv (no empty rows) and only keeps rows where there was a substituion to an A in at least one position, it takes these rows and returns them in a list called bc_families
def filter_onlyAs(in_file):
    with open('rpoB1_3new.csv', 'r') as f:
        data = f.readlines()

    bc_families=[]
    for line in data:
        line=line.strip('\n')
        bc_family=line.split(',')
        if 'A' in bc_family:
            bc_families.append(bc_family)
    return bc_families

# find_Cs method takes in a ROI sequence and returns a list of positions where a C was located in the ROI
def find_Cs(ROI):
    pos_lis=[]
    for i in range(len(ROI)):
        if ROI[i]=='C':
            pos_lis.append(i) 
    return pos_lis

# filters bc_families list to only barcode families that have at least one C->A substitution
def filter_CtoA(pos_lis,bc_families):
    filtered_bc_families=[]
    for pos in pos_lis:
        for family in bc_families:
            if family[pos]=='A':
                filtered_bc_families.append(family)
    return filtered_bc_families
    
ROI="TGTCTCAGTTTATGGACCAGAACAACCCGCTGTCTGAGATTACGCACAAACGTCGTATCTCCGCACTCGGCCCAGGCGGTCT"    
    'rpoB1_3summary.csv'
    'rpoB1_3new.csv'