# disclaimers about the nltk mechanics of this package:
# this *exclusively* uses the python nltk libraries, and no other engine
# non UTF-8 encoded characters are thrown off - assumptions about the composition
# of text character is made explicitly within this package.

import re
import json
import pandas as pd
from nltk import sent_tokenize, word_tokenize, ngrams, pos_tag
import nltk
import os
import string
from collections import defaultdict
from collections import Counter

def compute_usage(corpus, gram_length):
    entropylist = defaultdict(list)
    # entropylist represents a nested breakdown of all the words associated
    # before and after the appearance of another word
    '''
    Only punctuation and special characters are removed from the corpus.
    All other elements are kept.
    '''
    removals = string.punctuation + '``'

    for com in corpus:
        ngram_statement = [str(i) for i in ngrams([iter for iter in word_tokenize(com) if iter not in removals], gram_length)]
        counter = 0
        recent_list = []
        for gram in ngram_statement:
            '''
            This manipulation of the length of each gram is done because
            of the formatting that is applied to the string format when
            being passed through word_tokenize.
            '''
            if gram_length == 1:
                gram_clean = gram[2:len(gram)-3]
            else:
                gram_clean = ''.join(gram)

            if gram_length == 1:
                if counter == 0:
                    '''
                    Depending on the position and length of the gram, it is
                    necessary to denote the beginning of a statement.
                    '''
                    entropylist['[start]'].append(gram_clean.lower())
                    recent_list.append(gram_clean.lower())
                    counter += 1
                elif counter > 0:
                    entropylist[str(recent_list[len(recent_list)-1])].append(str(gram_clean.lower()))
                    recent_list.append(gram_clean.lower())
                    counter += 1
                elif counter == len(ngram_statement):
                    entropylist[str(recent_list[len(recent_list)-1])].append('[end]')
                    recent_list.append('[end]')
                    counter += 1
            else:
                if counter == 0:
                    '''
                    Depending on the position and length of the gram, it is
                    necessary to denote the beginning of a statement.
                    '''
                    entropylist['[start]'].append(gram_clean.lower())
                    recent_list.append(gram_clean.lower())
                    counter += 1
                elif counter > 0:
                    entropylist[str(recent_list[len(recent_list)-gram_length])].append(str(gram_clean.lower()))
                    recent_list.append(gram_clean.lower())
                    counter += 1
                elif counter == len(ngram_statement):
                    entropylist[str(recent_list[len(recent_list)-gram_length])].append('[end]')
                    recent_list.append('[end]')
                    counter += 1


    # Usage count represents the appearance of words (in their respective order)
    # and the counts of THOSE words
    usage_count = {}
    for key in entropylist:
        count_vals = {}
        '''
        Increment the appearance of the grams that appear within the gram.
        This will allow us to then determine the conditional probability of the
        appearnace of the next phrase in a sequence.
        '''
        for val in entropylist[key]:
            if str(val) in count_vals:
                count_vals[str(val)] += 1
            else:
                count_vals[str(val)] = 1

        usage_count[str(val)] = [count_vals]

    return {'usage':usage_count, 'entropylist':entropylist}

# @compute_usage # is this the correct usage of a decorator?
def transition_table(corpus, gram_length=1):
    '''
    Slated improvements to this function:
    - allow for custom stopwords to be removed from the various grams being measured
    - allow the corpus to be either a list of verbatims, or a pandas dataframe
      for segementation
    '''

    '''
    Description:
    - Returns the set of transition tables (transition tables) based on the
      length of gram_length supplied by the user (default length 1)
    - 'corpus' must be a (python) list of statements
    - 'gram_length' must be a whole integer
    '''
    all_entropy = {}
    usage_info = compute_usage(corpus, gram_length)

    for key in usage_info['entropylist']:
        cond_prob_val = {}
        relative_usage = Counter(usage_info['entropylist'][key])
        relative_words_len = sum(relative_usage.values())

        for following_gram in relative_usage:
            cond_prob_val[following_gram] = float(relative_usage[following_gram]) / float(relative_words_len)

        all_entropy[key] = cond_prob_val

    '''forcing everyone to move to JSON read/write :) '''
    return json.dumps(all_entropy)


def gram_stats(corpus, gram_length=1):
    '''
    Slated improvements to this function:
    - None at this time
    '''

    '''Description:
    - Returns a JSON file that describes how grams (default length 1)
    - Fields of interest returned include:
        - gram,
        - % usage across corpus (by row)
    '''
    usage_info = compute_usage(corpus, gram_length)

    # iterate through all the different grams, perform pattern matching, and then
    # return the overall % appearance within the corpus
    appearance_dict = {}
    total_rows = len(corpus)
    flat_keys = list(set([item for item in usage_info['usage']]))
    removals = string.punctuation + '``'

    for key in flat_keys:
        gram_appear = 0
        for r in removals:
            key = key.replace(r, '')

        for row in corpus:
            if key in row:
                gram_appear += 1

        appearance_dict[new_key] = [round(float(gram_appear) / float(total_rows), 8)]
    return json.dumps(appearance_dict)

def statements_type(corpus):
    # Rewrite this function to return a paragraph json dictionary that
    # writes out how a paragraph can be decompased into itsdifferent statements
    sentences = [nltk.sent_tokenize(verbatim) for verbatim in corpus]
    endings = {}
    for sent in sentences:
        for statement in sent:
            words = nltk.word_tokenize(statement)
            if words[len(words)-1] in string.punctuation and words[len(words)-1] in endings:
                endings[str(words[len(words)-1])] += 1
            elif words[len(words)-1] in string.punctuation and words[len(words)-1] not in endings:
                endings[str(words[len(words)-1])] = 1
            else:
                pass
    return endings

def compute_pos(corpus):
    # look at the composition of statements' parts of speech
    pos_corpus = []
    pos_dict = {}
    for verbatim in corpus:
        temp_sent = nltk.sent_tokenize(verbatim)
        pos_sent = []
        for sent in temp_sent:
            word_temp = nltk.word_tokenize(sent)
            pos_temp = nltk.pos_tag(word_temp)
            pos_only = []
            counter = 0
            for tag in pos_temp:
                pos_only.append(pos_temp[counter][1])
                if pos_temp[counter][1] in pos_dict:
                    pos_dict[pos_temp[counter][1]].append(pos_temp[counter][0])
                else:
                    pos_dict[pos_temp[counter][1]] = [pos_temp[counter][0]]
                counter += 1
            pos_only_statement = ' '.join(pos_only)
            pos_sent.append(pos_only_statement)
        pos_corpus.append(' '.join(pos_sent))
    usage_info = transition_table(pos_corpus)
    return {'pos_usage':usage_info, 'pos_table':pos_dict}


# create a melted dataframe that takes the json output and turns it into a csv
# for visualization outside of javascript entities
def melt_transition_table(json_output):
    flat_output = []
    for key in json_output:
        for foll in json_output[key]:
            temp_row = [key, foll, json_output[key][foll]]
            flat_output.append(temp_row)
    pd_flat = pd.DataFrame(flat_output)
    headers = ['parent', 'relation', 'percentage']
    pd_flat.columns = headers
    return pd_flat


# new function: piece together the various string options,
# prompt the user to provide a set of depth options that
# they can specify in order to parse the tree
# Output should be a list of lists that specifies the:
#   - rank of the probability of statement
#   - total conditional probability of each statement
#   - meta data on the

def statement_tree(list_of_starts, transition_table_dictionary, length, optionality=1):
    # list_of_starts - a list of start words to each sentence; i.e. ['[start]']
    # transition_table_dictionary - a model of statement / gram relationships
    # length - N-Gram length of each statement (in grams); i.e. this can be both unigram or N-Gram
    #   ... however, this assumes that the list_of_starts phrases match the length
    #   ... of the requested N-Gram statement.
    #       more... - The purpose of this is to constrain the statements so that
    #               ... output is not generated endlessly until a statement runs out.
    #               ... There are a BUNCH of challenges that I foresee with this -
    #               ... the largest being that unless you know _exactly_ what you want,
    #               ... the user may end up generating a bunch of useless half-statements
    #               ... without much content.
    # optionality - how many alternative statements should be created for each phrase from
    #   ... each starting phrase.
    gen_statements = defaultdict(list)
    statement_counter_absolute = 0
    optionality_counter = 0
    for st in list_of_starts:
        # start off the dummy statement
        temp_statements = {}
        temp_statements[str(statement_counter_absolute) + '-' + str(optionality_counter)].append(st)

        most_recent = []
        for pos in range(length):
            # find the most likely next word in the transition table
            for opts in range(optionality):
                transition_vals = transition_table_dictionary[st]
                reverse_tv = {v: k for k, v in transition_vals.iteritems()}
                reverse_tv_list = [int(x) for x in reverse_tv.keys()]
                reverse_tv_next = reverse_tv[reverse_tv_list[len(reverse_tv_list)-opts]]
                most_recent.append(reverse_tv_next)
                temp_statements[str(statement_counter_absolute) + '-' + str(optionality_counter)].append(st)

        statement_counter_absolute += 1
        optionality_counter += 1

    return json.dumps(gen_statements)
