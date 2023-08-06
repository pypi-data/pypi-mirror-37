from __future__ import print_function
import re
import os
import inflect

def parse_numbers(s_):
    p = inflect.engine()
    numbers = re.findall('[0-9]+', s_)
    for number in numbers:
        s_ = s_.replace(number, p.number_to_words(int(number)))
    s_ = re.sub('[- ]+','',s_)

    return s_



def update_result(results_file, key_value, trailing_xspace=True, format_="{:.3f}", units=None, silent=False):
    #if the file doesn't exist, touch it.
    if not(os.path.isfile(results_file)):
        with open(results_file,'w') as F:
            pass

    #if we want the trailing xspace, add it in here.
    if trailing_xspace:
        ending='\\xspace}'
    else:
        ending='}'

    #read the file
    with open(results_file, 'r') as F:
        s_ = F.read()
    s_new = s_

    #for each key in the dictionary
    for key in key_value:
        vkey = parse_numbers(key)
        #build a regex
        pattern = re.compile(r'\\newcommand\{\\' + str(vkey) + '\}\{.*(?:\})')
        if units is not None:
            units_ = "\\ \mathrm{" + units + "}"
        else:
            units_ = ""

        #decide on the new text
        line_text = '\\\\newcommand{\\\\' + str(vkey) + '}{' + format_.format(key_value[key]) + units_ + ending
        if pattern.search(s_new) is not None:
            #if the key is already in the file, substitute its old value with the new one
            s_new = pattern.sub(line_text, s_new)
            if not silent:
                print ("Key updated: {}".format(line_text))
        else:
            #otherwise append the new newcommand line to the file
            line_text = '\\newcommand{\\' + str(vkey) + '}{' + format_.format(key_value[key]) + units_ + ending
            s_new = s_new  + line_text + '\n'
            if not silent:
                print ("Key added: {}".format(line_text))

    #save the resulting file
    with open(results_file,'w') as F:
        F.write(s_new)


