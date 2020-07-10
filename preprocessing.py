import pandas as pd
import json
from nltk.tokenize import word_tokenize
import numpy as np

def sum_java_words(X: pd.DataFrame) -> pd.DataFrame:
    '''Sums the total number of java keywords present on a test token file.'''
    
    java_words = ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 
                  'class', 'continue', 'default', 'do', 'double', 'else', 'enum', 'exports', 
                  'extends', 'final', 'finally', 'float', 'for', 'if', 'implements', 'import', 
                  'instanceof', 'int', 'interface', 'long', 'modules', 'native', 'new', 'package', 
                  'private', 'protected', 'public', 'requires', 'return', 'short', 'static', 
                  'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 
                  'try', 'void', 'volatile', 'while', 'true', 'null', 'false', 'const', 'goto']

    keyword_count = 0
    for word in java_words:
        try:
            keyword_count += X[word]
        except KeyError:
            pass
        
    return pd.DataFrame(keyword_count)      


def concat_loc_sum(matrix, full_data):
    '''Adds new column keywordcount, counting all Java words, and loc count.'''
    
    matrix['loc'] = full_data['loc'].to_numpy()
    matrix['keywordcount'] = sum_java_words(matrix)
    return matrix


def document_to_synonims(document, synset_option):
    '''Replaces tokens of a document by its synonims/semantic related words.
        Synset_option: 1 = synonims 
                       2 = semantic related words'''
    
    synonims = []
    for word in document:
        synset = thesaurus.get(word)    
        if bool(synset):
            for syn in synset[synset_option]:  
                synonims.append(syn)
        else:
            synonims.append(word)
            
    return ' '.join(map(str, synonims))


def preprocess_tokens(data, synset_option=2):
    '''Tokenizes each document before replacing synonims.
        Returns: list of processed documents'''
    
    processed_tokens = [] 
    for row in data['token']:
        tokenized_row = word_tokenize(row)
        processed_row = document_to_synonims(tokenized_row, synset_option)
        processed_tokens.append(processed_row)
        
    return processed_tokens


def convert_to_sparse(df):
    """
    Converts columns of a data frame into SparseArrays and returns the data frame with transformed columns.
    Use exclude_columns to specify columns to be excluded from transformation.
    :param df: pandas data frame
    :return: pandas data frame
    """
    
    df = df.copy()
    exclude_columns = set(['loc','keywordcount'])

    for (columnName, columnData) in df.iteritems():
        if columnName in exclude_columns:
            continue
        df[columnName] = pd.SparseArray(columnData.values, dtype='uint8')

    return df


def load_thesaurus():
    path = open('data/SEThesaurus/SEDict.json')
    return json.load(path)

thesaurus = load_thesaurus()