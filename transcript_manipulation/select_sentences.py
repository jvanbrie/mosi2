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
			channels[cid] += [one_line]
		except:
			channels[cid] = one_line
		one_line = input_file.readline()
		line_list = one_line.split(',')

	print(len(channels))

	list_sent_dicts = [None] * 5

	num_chans = len(channels)
	for i in range(0,5):
		list_sent_dicts[i] = copy.deepcopy(channels)
		sent_level = i+1

		avg_sentences_needed = int((float(target) / float(5)) / float(num_chans))
		sentences_of_one_sent
		for chan in channels:
			sentences_taken = []
			for sent in channels[chan]:
				if(len(sentences_taken) >= avg_sentences_needed):
					break
				#checks if the given sentence has the sentiment that we're currently looking at
				if(sent[3] == sent_level):
					sentences_taken += [sent]


		#remove when one iteration works as expected
		break













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



