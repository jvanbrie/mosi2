"""
for each sentiment rating:  
	run this recursive algorithm:
		find the average sentences needed from each channel (avg)
		take min(avg,max num of sentences for given channel) sentences from each channel
		recurr

"""

import argparse
import copy

def main(args):
	#first get videos for the two extremes
	#make a function that takes in the sentiment level and the number of videos needed and grabs that many
	#also takes in percentage actual wanted (it will fudge the sentiment level a bit in order to get enough videos)

	input_file = open(args.input,'r')
	channels = {}

	one_line = input_file.readline()
	line_list = one_line.split(',')
	while((one_line != '') and (one_line != '\n')):
		cid = line_list[0]
		vid = line_list[1]
		try:
			channels[cid] += [line_list]
		except:
			channels[cid] = [line_list]
		one_line = input_file.readline()
		line_list = one_line.split(',')

	print(len(channels))

	list_sent_dicts = [None] * 5
	list_selected_sents = [None] * 5
	chans_to_delete = set([])

	num_chans = len(channels)
	for i in range(0,5):
		list_sent_dicts[i] = copy.deepcopy(channels)
		sent_level = i
		chans_to_delete = set([])

		avg_sentences_needed = int((float(args.target) / float(5)) / float(num_chans))
		print(avg_sentences_needed)
		sentences_taken_sent = []
		while(len(sentences_taken_sent) < int((float(args.target) / float(5)))):
			if(len(list_sent_dicts[i]) == 0):
				print("wtf")
				break
			avg_sentences_needed = max(int((float((int(args.target) - len(sentences_taken_sent))) / float(5)) / float(len(list_sent_dicts[i]))),1)
			for chan in list_sent_dicts[i]:
				sentences_taken_chan = 0
				for sent in list_sent_dicts[i][chan]:
					if(sentences_taken_chan >= avg_sentences_needed):
						break
					#checks if the given sentence has the sentiment that we're currently looking at
					if(sent[2] == str(sent_level)):
						sentences_taken_sent.insert(0,sent)
						sentences_taken_chan += 1
				if(sentences_taken_chan < avg_sentences_needed):
					chans_to_delete.add(chan)
				# if(sentences_taken_sent >= avg_sentences_needed):
				# 	break
			print(len(chans_to_delete))
			for chan in chans_to_delete:
				(list_sent_dicts[i]).pop(chan,None)
		list_selected_sents[i] = sentences_taken_sent
		print("number of sents found: %d" % len(list_selected_sents[i]))


		#remove when one iteration works as expected

def parse_args():
	parser = argparse.ArgumentParser(description="""Take in files of transcript
		sentences and p2fa files and return text files of relevant videos and
		channels""")

	parser.add_argument("-i", required=True, dest="input", action="store")
	parser.add_argument("-t", required=True, dest="target", action="store")
	parser.add_argument("-o", required=True, dest="output", action="store")
	parser.add_argument('-v', action='store_true', required = False,
		help='enable verbose')

	args = parser.parse_args()

	return main(args)

print(parse_args())



