###############
##  IMPORTS  ##
###############

from datetime import datetime
from bs4 import BeautifulSoup
from pprint import pprint
import numpy as np
import unicodedata
import requests
import random
import ujson
import time
import math
import json
import copy
import ast
import sys
import re
import os

###############################
##  TEXT CLEANING FUNCTIONS  ##
###############################

# Remove Non-Ascii Characters
def clean_string(string):
    string = unicodedata.normalize('NFKD',string).encode('ascii','ignore').decode("utf-8")
    string = string.replace('\\u','u:')
    return string

# Cleaning Punctuation
def clean_punctuation(string):
    string = string.replace('(',' ( ').replace(')',' ) ').replace('[',' [ ').replace(']',' ] ')
    string = string.replace(',',' , ').replace(';',' ; ').replace(':',' : ').replace("'"," ' ")
    string = string.replace('<',' < ').replace('>',' > ').replace('%',' % ')
    string = string.replace('\t',' ').replace('\r',' ').replace('\n',' ')
    string = string.replace('. ',' . ').replace('! ',' ! ').replace('? ',' ? ')
    if string[-1] in ['.','!','?']: string = string[0:-1]
    string = re.sub('[ ]{2,}', ' ', string)
    string = string.strip()
    return string

# Join Token Into Bigrams Where Possible
def collapse_bigrams(title, valid_bigrams):
    ln_t = len(title)
    bgrm_title = []; loop_counter = 0
    if ln_t == 1: return title
    while loop_counter < (ln_t-1):
        i = loop_counter
        if title[i] + '_' + title[i+1] in valid_bigrams:
            bgrm_title.append(title[i] + '_' + title[i+1])
            loop_counter += 1
        else:
            bgrm_title.append(title[i])
            if i == (ln_t-2): bgrm_title.append(title[i+1])
        loop_counter += 1
    return bgrm_title

###################################
##  FOLDER PROCESSING FUNCTIONS  ##
###################################

# Removing Contents From A Folder
def clear_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path): os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

##############################
##  WEB SCRAPING FUNCTIONS  ##
##############################

# Pulling Webpage Content
def pull_webpage(url, session_requests, method, cookie):
    headers = random_user_agents()
    try:
        page = session_requests.get(url, cookies={'cookie': cookie}, headers=headers)
        soup = BeautifulSoup(page.content, method)
    except:
        print('webpage pull failed; retrying in 3 seconds')
        time.sleep(3)
        page = session_requests.get(url, cookies={'cookie': cookie}, headers=headers)
        soup = BeautifulSoup(page.content, method)
    return soup

# Pulling A Random User Agent
def random_user_agents():
    user_agents = []
    f = open('user_agents.txt','r')
    for line in f:
        row = line.replace('\n','')
        user_agents.append(row)
    roll = random.randint(0, len(user_agents)-1)
    user_agent = {'User-Agent': user_agents[roll]}
    return user_agent

#############################
## DATA LOADING FUNCTIONS  ##
#############################

# Grabbing Mapping From Words To Ids
def grab_mapping(file_name):
    # Loading Mapping
    f_mapping = open(file_name,'r')
    for line in f_mapping: mapping = ast.literal_eval(line.replace('\n',''))
    f_mapping.close()
    return mapping

# Grabbing Vector Encodings
def grab_vector_encodings(file_name):
    encodings = {}
    f_enc = open(file_name, 'r')
    for line in f_enc: enc_str = line
    enc_str_len = len(enc_str)
    check_points = { int(i*math.floor(enc_str_len/4.0)):str(i*25) + '%' for i in range(1,5) }
    cur_key_val = ''
    for i in range(0,enc_str_len):
        c = enc_str[i]
        if (cur_key_val == '') and (c.isnumeric() == False): continue
        cur_key_val += c
        if i in check_points: print('loading encodings pct done: ' + str(check_points[i]))
        if c == ']':
            key, value = cur_key_val.split(': ')
            encodings[int(key)] = json.loads(value)
            cur_key_val = ''
            continue
    return encodings

# Grabbings Vector Embeddings For Each Vocab Word
def grab_vocab_embeddings(directory):
    # Loading Embeddings
    print('Loading model helper data...')
    vocab_embeddings = []
    f_vocab_embeddings = open(directory + '\\embedding_vectors.txt','r')
    for line in f_vocab_embeddings:
        vector = np.asarray(ast.literal_eval(line.replace('\n','')))
        vocab_embeddings.append(vector)
    # Adding 0-Vector Embedding
    len_embeddings = len(vocab_embeddings[0])
    vocab_embeddings.append([0.0]*len_embeddings)
    zero_idx = len(vocab_embeddings) - 1
    # Returning Output
    vocab_embeddings = np.asarray(vocab_embeddings)
    return vocab_embeddings, zero_idx


# Opening Data Files
def open_data_files(data_type, parent_dir, dset):
    print('Opening ' + dset + ' ' + data_type + '...')
    file_name = parent_dir + dset + '_data/' + dset + '_' + data_type + '.txt'
    f = open(file_name, 'r')
    return f, file_name


# Loading Data Variables
def data_variables_load(data_type, d, dset, max_data, encodings):
    print('Loading ' + dset + ' ' + data_type + '...')
    data = []; other = []; indicies = []; values = []; c = 0
    for line in d[dset]['file_' + data_type]:
        c += 1
        if c % 100000 == 0: print('\tloaded ' + str(c) + ' samples')
        if c == max_data: break
        row = ujson.loads(line.replace('\n','').replace("'",'"'))

        if data_type == 'data': 
            if type(row['vector'][0]) == type(0): vec_row = encodings[row['vector'][0]]
            else: vec_row = row['vector'][0]
            vec_row = np.asarray(vec_row)
            row = row['series']
            row = np.asarray([ encodings[row[i]] if type(row[i]) == type(0) else row[i]
                               for i in range(0,len(row)) ])
            other.append(vec_row)

        if data_type == 'context': row = { 'email':row[0], 'offer':row[1], 'date':row[2] }

        if data_type == 'labels':
            label_type, label = row
            if label_type == 'prediction': label_row = 100; value_row = 100
            else: label_row = float(label); value_row = float(label)
            row = label_row
            values.append(value_row)

        data.append(row)
        indicies.append(c-1)

    if data_type == 'data': 
        d[dset]['data'] = np.asarray(data)
        d[dset]['other'] = np.asarray(other) 
        d[dset]['indicies'] = np.asarray(indicies)

    if data_type == 'context':
        d[dset]['context'] = np.asarray(data)

    if data_type == 'labels': 
        d[dset]['labels'] = np.asarray(data)
        d[dset]['values'] = np.asarray(values)

    return d
    
###############################
## MODEL TRAINING FUNCTIONS  ##
###############################

# Balancing Classes Among Data Samples
def class_balance(data, balance, method, max_size):
    print('Balancing classes...')
    # Finding Largest Class For Determining Class Size
    classes = {}
    for label in data['labels']:
        if label not in classes: classes[label] = 0
        classes[label] = classes[label] + 1
    class_size = max(classes.values()) if method == 'max' else min(classes.values())
    class_size = min(class_size,max_size)
    min_class_size = min(classes.values())
    iterations = int(math.ceil(class_size / min_class_size)) if balance == True else 1
    print('Pre-Class balance: ' + str(classes))
    # Pulling Necessary Samples
    new_data = { key:[] for key in data if 'file' not in key }
    classes = {}; samples = 0.0
    for m in range(0,iterations):
        for i in range(0,len(data['labels'])):
            label = data['labels'][i]
            if label not in classes: classes[label] = 0
            if classes[label] >= class_size: continue
            classes[label] = classes[label] + 1
            samples = samples + 1.0
            for key in new_data: new_data[key].append(data[key][i])
    # Return Output
    for key in new_data: new_data[key] = np.asarray(new_data[key])
    for key in data:
        if key not in new_data: new_data[key] = data[key]
    new_data['data'] = new_data['data'].astype(np.float32)
    print('Class balance: ' + str(classes))
    for cl in classes: print('Class ' + str(cl) + ' percentage: ' + str(classes[cl] / samples))
    return new_data, classes

# Randomize Data
def randomize_data(data):
    print('Randomizing data...')
    # Randomizing
    rand_data = { key:[] for key in data if 'file' not in key }
    ordering = [j for j in range(0,len(data['labels']))]
    random.shuffle(ordering)
    for j in range(0,len(data['labels'])):
        cur_idx = ordering[j]
        for key in data: 
            if 'file' not in key: rand_data[key].append(data[key][cur_idx])
    # Return
    for key in rand_data: rand_data[key] = np.asarray(rand_data[key])
    for key in data:
        if key not in rand_data: rand_data[key] = data[key]
    rand_data['data'] = rand_data['data'].astype(np.float32)
    return rand_data

# Data Augmenting
def data_augmenting(data, augs):
    print('Augmenting data...')
    data_stats = { j:[] for j in range(0,len(data['data'][0][0])) }
    for i in range(0,30000):
        for row in data['data'][i]:
            for j in range(0,len(row)):
                data_stats[j].append(row[j])
    for key in data_stats: data_stats[key] = {'std':np.std(data_stats[key])}
    new_data = { key:[] for key in data }
    new_data['original'] = []
    for i in range(0,len(data['labels'])):
        for key in data: new_data[key].append(data[key][i])
        new_data['original'].append(1)
        aug = augs[data['labels'][i]]
        for s in range(0,aug):
            cur = copy.deepcopy(data['data'][i])
            for r in range(0,len(cur)):
                for j in range(0,len(cur[r])):
                    if random.random() < 0.1:
                        cur[r][j] = cur[r][j] + ( (data_stats[j]['std'] * 0.0627) * (2*random.random()-1) )
            for key in data: 
                if key == 'data': new_data[key].append(cur)
                else: new_data[key].append(data[key][i])
            new_data['original'].append(0)
    for key in new_data: new_data[key] = np.asarray(new_data[key])
    new_data['data'] = new_data['data'].astype(np.float32)
    return new_data


