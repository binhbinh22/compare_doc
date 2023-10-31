# hien thi 
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import messagebox, scrolledtext

import docx
import string 
from underthesea import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer 

import io

doc1 = ""
doc2 = ""
sim = 0.0

root = tk.Tk()
root.title('Text similarity')

#lay ra stop word
def create_stopwordlist():
    #f = open('vietnamese-stopword.txt', endcoding = 'utf-8')
    f = open('vietnamese-stopwords.txt')
    data = []
    null_data = []
    for i, line in enumerate(f):
        line = repr(line)
        line = line[1:len(line) - 3]
        data.append(line)
    return data

stopword_vn = create_stopwordlist()

#tach tu 
def tokenize(text):
    text = text.translate(str.maketrans('','', string.punctuation))
    return [word for word in word_tokenize(text.lower()) if word not in stopword_vn]

vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words=None)

# 2 van ban dau vao, lay ma tran nhan voi ma tran nghich dao 
# chuyen ve mang, co 2*2 lay 0,1
def consine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1,text2])
    return ((tfidf*tfidf.T).A)[0,1]

#doc file
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

lbl_doc1=tk.LabelFrame(root, text='Document 1:')
lbl_doc2=tk.LabelFrame(root, text='Document 2:')
ta_doc1  = scrolledtext.ScrolledText(lbl_doc1)
ta_doc2  = scrolledtext.ScrolledText(lbl_doc2)

def open_doc1():
    filename = askopenfilename(title= 'Choose file')
    #doc1 = open(filename,"r", encoding='cp1252').read()
    doc1 = getText(filename)
    ta_doc1.delete(1.0, 'end-1c')
    ta_doc1.insert('end-1c', doc1)

def open_doc2():
    filename = askopenfilename(title= 'Choose file')
    #doc1 = open(filename,"r", encoding='cp1252').read()
    doc2 = getText(filename)
    ta_doc2.delete(1.0, 'end-1c')
    ta_doc2.insert('end-1c', doc2)

def similarity():
    doc1 = ta_doc1.get("1.0", 'end-1c')
    doc2 = ta_doc2.get("1.0", 'end-1c')
    sim = consine_sim(doc1, doc2)
    messagebox.showinfo("Similaryty", str(round(sim, 4)*100)+'%')

btn_opendoc1 = tk.Button(lbl_doc1,text ="open file", command=open_doc1)
btn_opendoc2 = tk.Button(lbl_doc2,text ="open file", command=open_doc2)
btn_sim = tk.Button(root,text="similaryty", command=similarity)

lbl_doc1.grid(row=0, column =0, sticky=E+W+N+S)
btn_opendoc1.grid(row=1, column=0)
ta_doc1.grid(row=0, column = 0, sticky=E+W+N+S)
lbl_doc2.grid(row=0, column =1, sticky=E+W+N+S)
btn_opendoc2.grid(row=1, column=0)
ta_doc2.grid(row=0, column = 0, sticky=E+W+N+S)
btn_sim.grid(columnspan=2)



root.mainloop()