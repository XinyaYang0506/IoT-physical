import os
import pikepdf
import PyPDF2 
from PyPDF2 import PdfFileReader
# import textract
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk.download()

filename = '/Users/xinya/Desktop/REU/manuals/Honeywell-gas-detector-EN.pdf' 
pdf = pikepdf.open(filename)
pdf.save(filename)
#open allows you to read the file
pdfFileObj = open(filename,'rb')
#The pdfFile variable is a readable object that will be parsed
pdfFile = PyPDF2.PdfFileReader(pdfFileObj)

if pdfFile.isEncrypted:
    try:
        pdfFile.decrypt('')
        print('File Decrypted (PyPDF2)')
    except:
        command = ("cp "+ filename +
            " temp.pdf; qpdf --password='' --decrypt temp.pdf " + filename
            + "; rm temp.pdf")
        os.system(command)
        print('File Decrypted (qpdf)')
        fp = open(filename)
        pdfFile = PdfFileReader(fp)
else:
    print('File Not Encrypted')

#discerning the number of pages will allow us to parse through all #the pages
num_pages = pdfFile.numPages
count = 0
text = ""
#The while loop will read each page
while count < num_pages:
    pageObj = pdfFile.getPage(count)
    count +=1
    text += pageObj.extractText()
#This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
if text != "":
   text = text
#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
else:
   text = textract.process(fileurl, method='tesseract', language='eng')
# Now we have a text variable which contains all the text derived #from our PDF file. Type print(text) to see what it contains. It #likely contains a lot of spaces, possibly junk such as '\n' etc.
# Now, we will clean our text variable, and return it as a list of keywords.

#The word_tokenize() function will break our text phrases into #individual words
tokens = word_tokenize(text)
#we'll create a new list which contains punctuation we wish to clean
punctuations = ['(',')',';',':','[',']',',','.','..','...']
#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
stop_words = stopwords.words('english')
#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

text = nltk.Text(keywords)
match = text.concordance('sensor')
# print(keywords)

# freq = nltk.FreqDist(keywords)
# for key,val in freq.items():
#     print(str(key) + ':' + str(val))
# freq.plot(20, cumulative=False)