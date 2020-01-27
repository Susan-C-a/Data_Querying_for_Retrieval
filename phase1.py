import re
import string
import time

def getTerms(fname, ofname):
    
    inFile = open(fname, "r")
    row = inFile.readlines()
    
    outFile = open(ofname, "w")

    for r in row:
        if re.search('<mail>', r):                                  # find header <mail>
            
            # finding the row number:
            row_n = re.findall('<row>(.*?)</row>', r)
            row_num = row_n[0]
            
            # getting terms under subject 
            subj = re.findall('<subj>(.*?)</subj>', r)
           
            if subj != '':
                
                sub_split =  charReplace(subj)          # replace unwanted characters
                for i in range(len(sub_split)):
                
                    if len(sub_split[i]) > 2:
                        sWord = (re.findall('[0-9a-zA-Z_-]+', sub_split[i]))    # find all valid terms : [0-9a-zA-Z_-]+
                        
                        for word in range(len(sWord)):
                            sTerm = sWord[word]
                            if len(sTerm) > 2:          #checking length for terms
                                subject = "s-" + sTerm.lower() + ":" + row_num
                                outFile.write(subject + "\n")   #writing in to output file
            
            #getting terms under body
            body = re.findall('<body>(.*?)</body>', r)
            
            if body != '':
            
                bSplit = charReplace(body)                  #replace unwanted characters
                for i in range(len(bSplit)):
                    if len(bSplit[i]) > 2:
                        bWord = (re.findall('[0-9a-zA-Z_-]+', bSplit[i]))       # find all valid terms : [0-9a-zA-Z_-]+
                        
                        for word in range(len(bWord)):
                            bTerm = bWord[word]
                            if len(bTerm) > 2:              #checking length for terms
                                body1 = "b-" + bTerm.lower() + ":" + row_num
                                outFile.write(body1 + "\n")     #writing in to output file
 
    inFile.close()
    outFile.close()
    print("--- " + ofname + "  generated ---") 		#success message
    return

def charReplace(text):
    
    #replace terms: "&lt;, &gt;, &amp;, &apos; and &quot;" to <, >, &, ' and " "
    # in subj and body  
    
    e_l = ['&lt;', '&gt;', '&amp;', '&apos;', '&quot;', '&#10;', '@']
    replaced = text[0].replace(e_l[0],' ').\
        replace(e_l[1],' ').replace(e_l[2],' ').\
        replace(e_l[3],' ').replace(e_l[4],' ').replace(e_l[5],' ').replace(e_l[6],' ')
    
    # replace non-[0-9a-zA-Z_-] with space  characters for splicing
    
    replaced2 = re.sub('\W^-_', ' ', replaced)
    
    joined = ' '.join(replaced2.split())
    sub_split = re.split(" ",joined)

    return sub_split


def getEmails(fname, ofname):
    
    inFile = open(fname, "r")
    row = inFile.readlines()
    
    outFile = open(ofname, "w")
    for r in row:
        if re.search('<mail>', r):
            
            #get row number
            row_num = re.findall('<row>(.*?)</row>', r)[0]
            
            #get email from <to> field
            e_from = re.findall('<from>(.*?)</from>', r)
            if e_from[0] != '':                             #if <from> field is not empty
                outF = "from-" + e_from[0].lower() + ":" + row_num
                outFile.write(outF + "\n")
                
            #get emails from <to> field
            e_to = re.findall('<to>(.*?)</to>', r)
            if e_to[0] != '':                               # if field not empty
                if re.findall(',', e_to[0]):                # for multiple emails in <to> field
                    to_split = re.split(',', e_to[0])
    
                    for n in range(len(to_split)):
                        to1 = "to-" + to_split[n].lower() + ":" + row_num
                        outFile.write(to1 + "\n")
                else:
                    to2 = "to-" + e_to[0] + ":" + row_num
                    outFile.write(to2 + "\n")
            

            #get emails from <cc> field
            cc = re.findall('<cc>(.*?)</cc>', r)
            if cc[0] != '':                                 #if field <cc> is not empty
                if re.findall(',', cc[0]):                  #if there are multiple emails
                    cc_split = re.split(',', cc[0])
                    
                    for c in range(len(cc_split)):
                        cc1 = "cc-" + cc_split[c].lower() + ":" + row_num
                        outFile.write(cc1 + "\n") 
                else:
                    cc2 = "cc-" + cc[0] + ":" + row_num
                    outFile.write(cc2 + "\n")
                
            #get emails from <bcc> field
            bcc = re.findall('<bcc>(.*?)</bcc>', r)
            if bcc[0] != '':                            # if bcc is not empty
                if re.findall(',', bcc[0]):             #if there are multiple emails
                    bcc_split = re.split(',', bcc[0])
                    
                    for b in range(len(bcc_split)):
                        bcc1 = "bcc-" + bcc_split[b].lower() + ":" + row_num
                        outFile.write(bcc1 + "\n")
                        
                else:
                    bcc2 = "bcc-" + bcc[0] + ":" + row_num
                    outFile.write(bcc2 + "\n")  
    
    inFile.close()
    outFile.close()
    print("--- " + ofname + "  generated ---")          #success message

    return

def getDates(fname, ofname):
    
    inFile = open(fname, "r")
    row = inFile.readlines()

    outFile = open(ofname, "w")
    for r in row:
        if re.search('<mail>', r):
            date = re.findall('<date>(.*?)</date>', r)
            row_num = re.findall('<row>(.*?)</row>', r)

            if date[0] != '':               # if date is not empty
                output = date[0] + ":" + row_num[0]
                outFile.write(output + "\n")        
    
    inFile.close()
    outFile.close()
    print("--- " + ofname + "  generated ---")          #success message

    return


def getRecords (fname, ofname):
    
    
    inFile = open(fname, "r")
    row = inFile.readlines()
    outFile = open(ofname, "w")

    for r in row:
        if re.search('<mail>', r):
            row_num = re.findall('<row>(.*?)</row>', r)
            
            output = row_num[0] + ":" + r
            outFile.write(output)
    
    
    inFile.close()
    outFile.close()
    print("--- " + ofname + "  generated ---")          #success message    
    
    return


def main():
    
    print("----------Phase 1----------")
    filename = input("Enter the filename: ")
    
    # creating terms.txt for first file

    terms = input("To generate terms file, enter output filename: ")
    getTerms(filename, terms)               #function call to generate terms.txt
    
    #creating emails.txt
    emails = input("To generate emails file, enter output filename: ")
    getEmails(filename, emails)             #function call to generate emails.txt

    #creating dates.txt
    dates = input("To generate dates file, enter output filename: ")
    getDates(filename, dates)               #function call to generate dates.txt
    
    
    #generate recs.txt
    recs = input("To generate records file, enter output filename: ")
    getRecords(filename, recs)              #function call to generate recs.txt
    
    time.sleep(1)
    print("Phase 1, DONE! ")                # termination message

    return

if __name__ == "__main__":
    main()
