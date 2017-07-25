# This script will take in a pkl file, a folder containing videos and
# transcripts, and a folder containing p2fa aligned files, and a lsit of
# sentence diliniators and return a folder in which each video has its own csv
# file. This csv file will be organized with sentence, start time, end time

#TODO: always update end of sentences

import argparse
from typing import List, Dict, Tuple
import os
from nltk.tag import pos_tag
from copy import deepcopy

incorrect_count = 0


verboseprint = lambda *a, **k: None

def find_match(word:str, p2fa, p2fa_line_count, is_first_word, is_last_word):
    p2fa_file = open(p2fa,'r')

    #words with '-' are sometimes put into parts in p2fa

    if('-' in word):
        multi_words = word.split('-')
        i = 0
        found_word_count = 0
        triplets_count = 0
        start = ''
        end = ''

        for word in multi_words:
            (found_word,triplets_read,potential_start,
                potential_end) = find_match(word,p2fa,p2fa_line_count, 
                is_first_word and (i == 0),is_last_word)
            if(found_word):
                found_word_count += 1
                p2fa_line_count += (3*triplets_read)
                triplets_count += triplets_read
                start = potential_start
                end = potential_end
            else:
                break
            i += 1

        if(found_word_count == len(multi_words)):
            return(True,triplets_count,start,end)

    while(p2fa_line_count > 0):
        p2fa_file.readline()
        p2fa_line_count -= 1
    triplets_read = 0
    temp = ''
    found_word = False
    test_count = 3
    flag = is_first_word
    potential_start = ''
    potential_end = ''

    while(test_count > 0):
        triplets_read += 1
        for i in range(0,3):
            temp = p2fa_file.readline()
            if(flag and (i == 0)):
                flag = False
                potential_start = temp
            if(i==1):
                potential_end = temp

        #print(temp)
        #print(word)
        if((word.upper()) == (temp[1:-2])):
            found_word = True
            break
        test_count -= 1

    if(found_word and is_last_word):
        for i in range(0,3):
            temp = p2fa_file.readline()
        if(('sp') == (temp[1:-2])):
            triplets_read += 1


    return(found_word,triplets_read,potential_start,potential_end)





def readOneFile(video_id:str, p2fa_path:str, video_path:str, output_path:str,
    diliniators:str):

    list_diliniators = diliniators.split('|')

    p2fa = os.path.join(p2fa_path, video_id + "_word.txt")
    transcript = os.path.join(video_path, video_id +
            "-user.en.vtt")

    #verboseprint(video_id)
    #verboseprint(p2fa)

    p2fa_file = open(p2fa, 'r')
    try:
        transcriptFile = open(transcript, 'r')
    except:
        return
    outFile = open(os.path.join(output_path, video_id + ".csv"), 'w+')

    #this removes the first 4 lines which hold useless information
    for i in range(0,4):
        transcriptFile.readline()

    for i in range(0,3):
        p2fa_file.readline()

    p2fa_line_count = 4

    num_words = p2fa_file.readline()

    total_transcript = []

    while(transcriptFile.readline() != ""):
        transcriptLine = (transcriptFile.readline())
        total_transcript.extend(transcriptLine.split())

        transcriptLine = (transcriptFile.readline())
        while(transcriptLine != '\n'):
            total_transcript.extend(transcriptLine.split())
            transcriptLine = transcriptFile.readline()

    temp_sent_start = ''
    temp_sent_end = ''
    temp_sent = ""

    missed_words_count = 0

    #total_transcript.reverse()

    verboseprint(total_transcript)

    global incorrect_count



    while(total_transcript != []):
        verboseprint('going through vid: %s', video_id)
        # if(missed_words_count >= 3):
        #     verboseprint("Bad file - too many misses")
        #     break
        curr_word = total_transcript.pop(0)
        real_word = deepcopy(curr_word)
        verboseprint(curr_word)

        count = 0;
        for char in real_word:
            if char.isalpha():
                break
            else:
                count += 1
        if(count > 0):
            real_word = real_word[count:]
        

        if ((len(curr_word) > 0) and (curr_word[-1]).isalpha()):
            (found, number_skipped,potential_start,potential_end) = find_match(real_word,
                p2fa, p2fa_line_count,(temp_sent_start == ''), False)

            if found:
                if(potential_start != ''):
                    temp_sent_start = potential_start
                if(potential_end != ''):
                    temp_sent_end = potential_end
                while(number_skipped > 0):
                    number_skipped -= 1
                    p2fa_file.readline()
                    p2fa_file.readline()
                    p2fa_file.readline()
                    p2fa_line_count += 3
                temp_sent += (curr_word + ' ')
            else:
                temp_sent += (curr_word + ' ')
                
        elif((len(curr_word) > 1) and (curr_word[-2]).isalpha() and (curr_word[-1] in diliniators)):
            
            (found, number_skipped,potential_start,potential_end) = find_match(real_word[:-1],
                p2fa, p2fa_line_count,(temp_sent_start == ''), (curr_word[-1] in diliniators))

            if found:
                if(potential_start != ''):
                    temp_sent_start = potential_start
                if(potential_end != ''):
                    temp_sent_end = potential_end
                while(number_skipped > 0):
                    number_skipped -= 1
                    p2fa_file.readline()
                    p2fa_file.readline()
                    p2fa_file.readline()
                    p2fa_line_count += 3
                if(curr_word[-1] in diliniators):
                    str_to_print = (temp_sent + curr_word + ',' + (temp_sent_start[:-1]) + ','
                        + (temp_sent_end[:-1]) + '\n')
                    outFile.write(str_to_print)
                    temp_sent = ''
                    temp_sent_start = ''
                    #temp_sent_end = ''
                else:
                    temp_sent += (curr_word + ' ')
            else:
                if(curr_word[-1] in diliniators):
                    str_to_print = (temp_sent + curr_word + ',' + (temp_sent_start[:-1]) + ','
                        + (temp_sent_end[:-1]) + '\n')
                    outFile.write(str_to_print)
                    temp_sent = ''
                    temp_sent_start = ''
                else:
                    temp_sent += (curr_word + ' ')

        else:
            count = 0;
            for char in real_word[::-1]:
                if char.isalpha():
                    break
                else:
                    count += 1
            if(count > 0):
                real_word = real_word[:(-1 * count)]
            if(real_word == ''):
                temp_sent += (curr_word + ' ')
            else:
                (found, number_skipped,potential_start, potential_end) =find_match(real_word,
                    p2fa, p2fa_line_count,(temp_sent_start ==''),False)

                if found:
                    if(potential_start != ''):
                        temp_sent_start = potential_start
                    if(potential_end != ''):
                        temp_sent_end = potential_end
                    while(number_skipped > 0):
                        number_skipped -= 1
                        p2fa_file.readline()
                        p2fa_file.readline()
                        p2fa_file.readline()
                        p2fa_line_count += 3
                    temp_sent += (curr_word + ' ')
                else:
                    temp_sent += (curr_word + ' ')

    if(temp_sent != ''):
        str_to_print = (temp_sent + ',' + (temp_sent_start[:-1]) + ','
            + (temp_sent_end[:-1]) + '\n')
        outFile.write(str_to_print)

    temp = p2fa_file.readline()
    if(temp != '\n' and temp !=''):
        p2fa_file.readline()
        temp2 = p2fa_file.readline()
        if((temp2[1:-2] != 'sp') and (p2fa_file.readline() != '\n')):
            print('Missed one on vid: %s' % video_id)
            print('With last p2fa line: %s' % temp2[1:-2])
            print('Soemtimes useful (3rd to last line): %s' % temp)
            incorrect_count += 1
                
                        
    outFile.close()







    #verboseprint(total_transcript)


# the files that have p2fa allignment are .textGrid
def main(args):
    global verboseprint
    verboseprint = print if args.v else lambda *a, **k: None
    delineators = List[str]
    delineators = args.diliniators.split('|')

    for file in os.listdir(args.p2fa):
        #verboseprint(file[:11])
        if file[11:] == "_word.txt":
            verboseprint("reading one")
            video_id = file[:11]
            readOneFile(video_id, args.p2fa, args.videos, args.output,args.diliniators)

    global incorrect_count
    print(incorrect_count)



    #verboseprint(delineators)

#parses arguments and then calls main with them
def parse_args():
    parser = argparse.ArgumentParser(description='Splitting video transcripts')
    parser.add_argument('-d', required = False, dest =
        'dbFile', action='store', help='database file (not currently in use)')
    parser.add_argument('-vids', required = True, dest = 'videos', action='store',
        help='folder containing videos and transcripts')
    parser.add_argument('-p', required = True, dest = 'p2fa', action='store',
        help='folder containing the p2fa allignments for each video')
    parser.add_argument('-s', required = True, dest = 'diliniators',
        action='store', help='string of | seperated deliniators')
    parser.add_argument('-o', required = True, dest = 'output',
        action='store', help='folder to house output')
    parser.add_argument('-v', action='store_true', required = False,
        help='enable verbose')

    args = parser.parse_args()
    main(args)

parse_args()