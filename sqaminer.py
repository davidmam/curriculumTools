#AHparser

import openpyxl

wb = openpyxl.Workbook()
ws= wb.active 

infile = 'ah-course-spec-biology.pdf.txt'

part =''
sectnum = 0
sect = ''
subsectnum =0
subsect=''
subsubsectnum =0
subsubsect = ''
lastline =''
LO = ''
ofh = open('ah-biology.tsv', 'w')
with open(infile) as fh:
    line=fh.readline()
    while not line.startswith('===='):
        line=fh.readline().strip()
    
    for line in fh:
        line=line.strip()
        if line.startswith('===='):
            LO=lastline
            break
        if line.strip() == part:
            continue
        if not line:
            continue
        if line[0] in '1234567890':
            num,sect = line.strip().split(maxsplit=1)
            part = lastline
            sectnum = int(num)
            subsect=''
            subsectnum=''
            subsubsect=''
            subsubsectnum=''
        elif line.startswith('('):
            if line[1] in 'abcdefgh':
                pnum,subsect = line.strip().split(maxsplit=1)
                subsectnum = pnum[1:-1]
                subsubsect=''
                subsubsectnum=''
            else:
                pnum,subsubsect = line.strip().split(maxsplit=1)
                subsubsectnum = pnum[1:-1]
        else:    
            LO=lastline 
            ws.append([part,sectnum,sect,subsectnum,subsect,subsubsectnum,subsubsect,LO])
            print("\t".join([str(x) for x in [part,sectnum,sect,subsectnum,subsect,subsubsectnum,subsubsect,LO]]), file=ofh)
            if len(line) >3:
                lastline=line.strip() 
ws.append([part,sectnum,sect,subsectnum,subsect,subsubsectnum,subsubsect,LO])
ofh.close()
wb.save('ah-biology.xlsx')