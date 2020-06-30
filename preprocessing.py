import pandas as pd

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