import imp
from os import listdir
import PyPDF2
from PyPDF2 import PdfFileReader
from os.path import isfile, join

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from keybert import KeyBERT
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .Text_outline import*



def pdf2text(pdfRdr : PdfFileReader):
    page_num = pdfRdr.numPages
    pdf_text = ''

    for i in range(page_num):
        pageObj = pdfRdr.getPage(i)
        pdf_text += pageObj.extract_text()
        pdf_text += ' '
    

    cleanText = ''
    
    for myWord in pdf_text:
        if myWord != '\n':
            cleanText += myWord
        else:
            cleanText += ' '
    
    
    token = word_tokenize(cleanText)
    
    final_pdf_text = ''
    lemmatizer = WordNetLemmatizer()
    
    for word in token:
        if(word.isalnum() and len(word) > 1):
            word = word.lower()
            new_word = lemmatizer.lemmatize(word)

            final_pdf_text += new_word
            final_pdf_text += ' '
    
    return cleanText, final_pdf_text


def find_key_word(text):
    kw_model = KeyBERT()
    key_word = kw_model.extract_keywords(text, top_n=10, keyphrase_ngram_range=(1,1), stop_words='english')
    return key_word


def to_chart(key_word, id):
    name_list = [word[0] for word in key_word]
    val_list = [word[1] for word in key_word]
    dic = {'Key_word' : name_list, 'Correlation': val_list}
    df = pd.DataFrame(data=dic)

    fig, ax = plt.subplots()

    sns.set_theme(style="whitegrid")

    pal = sns.color_palette('flare', desat=0.9 , n_colors=10)
    pal.reverse()

    font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 18}

    matplotlib.rc('font', **font)

    #matplotlib.pyplot.figure(figsize=(13,8), facecolor=(0.9,0.8,0.8))

    plt.rcParams['figure.facecolor'] = (0.9,0.8,0.8)

    sns.barplot(palette=pal, data=df, x="Correlation", y="Key_word", label="Total", color="b", width=0.65)
    plt.title("Top 10 key words", color=(0.9,0.2,0.2), fontdict=font)

    
    sns.despine(left=True, bottom=True)

    plt.xticks(np.arange(0, key_word[0][1] + 0.1, 0.05))
    plt.ylabel('')

    fig.set_tight_layout(True)

    plt.savefig(f'static/image/{id}.png')
    plt.show()

#new to_chart
# def to_chart(key_word, id):
#     name_list = [word[0] for word in key_word]
#     val_list = [word[1] for word in key_word]
#     dic = {'Key_word' : name_list, 'Correlation': val_list}
#     df = pd.DataFrame(data=dic)

#     plt.rcParams['figure.facecolor'] = (0.87,0.75,0.78)
#     fig = plt.figure()

#     pal = sns.color_palette('flare', desat=0.9 , n_colors=10)
#     pal.reverse()

#     font = {'family' : 'monospace',
#             'weight' : 'bold',
#             'size'   : 11}
    
#     font_title = {'family' : 'monospace',
#             'weight' : 'bold',
#             'size'   : 15}
    
#     font_xlabel = {'family' : 'monospace',
#             'weight' : 'bold',
#             'size'   : 13}

#     matplotlib.rc('font', **font)
    
#     sns.barplot(palette=pal, data=df, x="Correlation", y="Key_word", label="Total", color="b", width=0.65)
#     plt.title("Top 10 key words", color=(0.9,0.2,0.2), fontdict=font_title)
#     plt.xlabel("Correlation", fontdict=font_xlabel)
#     plt.xticks(color='b')
    
#     sns.despine(left=True, bottom=True)

#     plt.xticks(np.arange(0, key_word[0][1] + 0.1, 0.1))
#     plt.ylabel('')

#     fig.set_tight_layout(True)

#     plt.savefig(f'{id}.png')

def execute():
    #pdf的位置
    mypath = 'C:\\Users\\Administrator\\all_data_test\\label1_muscle'
    all_pdf_name = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    sm = Summarize()
    

    for file in all_pdf_name:
        pdfFileObj = open(join(mypath, file), 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        
        pdf_one_line_text, pdf_final_text = pdf2text(pdfReader)
        
        #輸出摘要跟keyword
        pdf_sum = sm.summarize(pdf_one_line_text) #stirng
        key_word = find_key_word(pdf_final_text)  #list
        
        #存取圖片
        to_chart(key_word, )

# execute()