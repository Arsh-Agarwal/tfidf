from flask import Flask, render_template
from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import os
import pickle
import math

#########################################3
## load preprocessed files
##########################################

def load_data():
    with open('tfidf/vocab.pkl', 'rb') as f:
        vocab = pickle.load(f)
    with open('tfidf/invidx.pkl', 'rb') as f:
        invidx = pickle.load(f)
    with open('tfidf/docs.txt', 'r') as f:
        docs = f.readlines()
        docs = [doc.strip().split() for doc in docs]
    with open('tfidf/urldocs.txt', 'r') as f:
        urldocs = f.readlines()
    return (vocab, invidx, docs, urldocs)
    

vocab, invidx, docs, urldocs = load_data()

###################################################
## TFIDF stuff
####################################################

def gettf(word):
    ans = {}
    if word in invidx:
        for doc in invidx[word]:
            if doc in ans: ans[doc] += 1
            else: ans[doc] = 1
    for doc in ans:
        ans[doc] /= len(docs[doc])
    return ans

def getidf(word):
    return math.log(vocab[word])

def calcorder(words):
    ans = {}
    for word in words:
        if word not in vocab: continue
        tfvals = gettf(word)
        idfval = getidf(word)
        for doc in tfvals:
            if doc not in ans: ans[doc] = tfvals[doc]*idfval
            else: ans[doc] += tfvals[doc]*idfval
    for doc in ans:
        ans[doc] /= len(words)
    ans = dict(sorted(ans.items(), key=lambda item: item[1], reverse=True))
    res = [{'link': urldocs[key], 'score': val} for key, val in ans.items()]
    return res

##############################
## Server run and serve codes
##############################

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my-secret-key'
class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        words = [word.lower() for word in query.strip().split()]
        results = calcorder(words)
    return render_template('index.html', form=form, results=results)