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
	output_file = open(args.output,'w+')
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

	#This is the distribution of sentences wanted:
	distribution = [2500,2500,2500,2500,2500,2500,2500]

	list_sent_dicts = [None] * 7
	list_selected_sents = [None] * 7
	chans_to_delete = set([])

	num_chans = len(channels)
	for i in range(0,7):

		sent_level = i

		sent_count = 0
		for chan in channels:
			for sent in channels[chan]:
				if(sent[3] == str(sent_level)):
					sent_count += 1
		sentences_taken_sent = []

		if(sent_count <= distribution[i]):
			for chan in channels:
				for sent in channels[chan]:
					if(len(sent[4].split(" ")) <= 3):
						continue
					if(sent[3] == str(sent_level)):
						sentences_taken_sent.insert(0,sent)
			list_sent_dicts[i] = copy.deepcopy(channels)
			list_selected_sents[i] = sentences_taken_sent
			print("Sentences Taken from sent " + str(i) + ' = ' + str(len(sentences_taken_sent)))
			continue


		list_sent_dicts[i] = copy.deepcopy(channels)

		chans_to_delete = set([])

		avg_sentences_needed = int(distribution[i] / float(num_chans))
		while(len(sentences_taken_sent) < distribution[i]):
			if(len(list_sent_dicts[i]) == 0):
				break
			avg_sentences_needed = max(int((float(distribution[i] - len(sentences_taken_sent))) / float(len(list_sent_dicts[i]))),1)
			for chan in list_sent_dicts[i]:
				sentences_taken_chan = 0
				for sent in list_sent_dicts[i][chan]:
					if(sentences_taken_chan >= avg_sentences_needed):
						break
					if(len(sent[4].split(" ")) <= 3):
						continue
					#checks if the given sentence has the sentiment that we're currently looking at
					if(sent[3] == str(sent_level)):
						sentences_taken_sent.insert(0,sent)
						sentences_taken_chan += 1
						if(len(sentences_taken_sent) >= distribution[i]):
							break
				if(sentences_taken_chan < avg_sentences_needed):
					chans_to_delete.add(chan)
				if(len(sentences_taken_sent) >= distribution[i]):
					break
				# if(sentences_taken_sent >= avg_sentences_needed):
				# 	break
			for chan in chans_to_delete:
				(list_sent_dicts[i]).pop(chan,None)
		list_selected_sents[i] = sentences_taken_sent
		print("Sentences Taken from sent " + str(i) + ' = ' + str(len(sentences_taken_sent)))


	for sent_list in list_selected_sents:
		for line in sent_list:
			output_file.write(','.join(line))
	output_file.close()


def parse_args():
	parser = argparse.ArgumentParser(description="""Take in files of transcript
		sentences and p2fa files and return text files of relevant videos and
		channels""")

	parser.add_argument("-i", required=True, dest="input", action="store")
	parser.add_argument("-o", required=True, dest="output", action="store")
	parser.add_argument('-v', action='store_true', required = False,
		help='enable verbose')

	args = parser.parse_args()

	return main(args)

print(parse_args())



