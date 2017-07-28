import argparse
import os
import numpy as np

verboseprint = lambda *a, **k: None

def count_below_val(word_counts):
    max_val = int(np.amax(word_counts,axis = 0)[0])
    print(max_val)
    return_good = [None]*(max_val)
    return_bad = [None]*(max_val)
    bad_vid_ids = []
    good_vids = []

    for word_count_max in range(0,max_val):
        bad_vid_ids = []
        good_vids = []
        temp = 0
        for word_count in word_counts:
            if(word_count[0] <= word_count_max):
                good_vids.append(word_count)
            else:
                bad_vid_ids.append(word_count[1])

        bad_vid_ids = np.unique(bad_vid_ids)

        for bad_id in bad_vid_ids:
            for good_vid in good_vids:
                if(good_vid[1] == bad_id):
                    good_vids.remove(good_vid)

        return_good[word_count_max] = (len(good_vids))
        return_bad[word_count_max] = (len(bad_vid_ids))

        verboseprint('through one vid')
    return (return_good,return_bad)



def main(args):
    global verboseprint
    verboseprint = print if args.v else lambda *a, **k: None

    total_line_time = 0
    total_number_lines = 0
    total_number_words = 0
    list_line_time = []
    list_line_word = []
    bad_file_count = 0

    #histogram



    file_id = 0

    for file in os.listdir(args.input):
        verboseprint("reading file %s" % file)
        file_o = open(os.path.join(args.input,file),'r')
        temp_line = file_o.readline()
        while(temp_line != ''):
            line_list = temp_line.split(',')
            if(line_list[0] != ''):
                total_number_words += len(line_list[0].split())
                list_line_word.append((len(line_list[0].split()),file_id))

            if((line_list[-2] != '') and (line_list[-1] != '')):
                try:
                    total_number_lines += 1
                    temp_time = float(line_list[-1]) - float(line_list[-2])
                    total_line_time += temp_time
                    list_line_time.append((temp_time,file_id))
                except:
                    bad_file_count +=1
                    print(file)
            temp_line = file_o.readline()
        file_id += 1


    word_count_max = int(np.amax(list_line_word,axis=0)[0])
    x_plot_words = [None]*(word_count_max)
    for i in range(0,word_count_max):
        x_plot_words[i] = i
    sentences,lost_vids = count_below_val(list_line_word)

    time_count_max = int(np.amax(list_line_time,axis=0)[0])
    x_plot_times = [None]*(time_count_max)
    for i in range(0,time_count_max):
        x_plot_times[i] = i
    sentences,lost_vids = count_below_val(list_line_time)


    hist, bin_edges = (np.histogram(list_line_word, bins=20,range=(0.0,40.0)))


    hist, bin_edges = (np.histogram(list_line_time, bins=20,range=(0.0,20.0)))


    print('Total Number of Lines: %d' % total_number_lines)
    print('')
    print('Average Line Time: %f' % (total_line_time / total_number_lines))
    print('Median Line Time: %f' % (np.median(list_line_time)))
    print('Standard Deviation Line Time: %f' % (np.std(list_line_time)))
    print('')
    print('Average Words per Line: %f' % (total_number_words / total_number_lines))
    print('Median Words per Line: %f' % (np.median(list_line_word)))
    print('Standard Deviation Words per Line: %f' % (np.std(list_line_word)))
    print('')



def parse_args():
    parser = argparse.ArgumentParser(description='Splitting video transcripts')
    parser.add_argument('-i', required = True, dest = 'input',
        action='store', help='input directory')
    parser.add_argument('-v', action='store_true', required = False,
        help='enable verbose')


    args = parser.parse_args()
    main(args)

parse_args()