
import argparse
import copy
import numpy as np
import matplotlib.pyplot as plt

def main(args):

	sent_dict = {}

	input_file = open(args.input,'r')
	one_line = input_file.readline()
	while (one_line != '\n') and (one_line != ''):
		line_list = one_line.split(',')
		cid = line_list[0]
		vid = line_list[1]
		sent = line_list[3]
		try:
			sent_dict[sent][cid] += [one_line]
		except:
			try:
				sent_dict[sent][cid] = [one_line]
			except:
				sent_dict[sent] = {cid: one_line}

		one_line = input_file.readline()

	all_vals = {}
	for sent in sent_dict:
		count = 0
		y_values = []
		print(len(sent_dict[sent]))
		for cid in sent_dict[sent]:
			sent_dict[sent][cid]
			vids_in_chan = len(sent_dict[sent][cid])
			if(vids_in_chan > 40):
				print(cid)
			y_values.insert(0,vids_in_chan)
		all_vals[count] = y_values

		word_count_max = len(y_values)
		x_plot_words = [None]*(word_count_max)
		for i in range(0,word_count_max):
			x_plot_words[i] = i
		plt.plot(x_plot_words, y_values,'ro')
		plt.title('Sent value:' + sent)
		plt.axis([0, len(x_plot_words), 0, 100])
		plt.show()

		count += 1
		print(y_values)

	print(len(all_vals))




def parse_args():
	parser = argparse.ArgumentParser(description="""Take in files of transcript
		sentences and p2fa files and return text files of relevant videos and
		channels""")

	parser.add_argument("-i", required=True, dest="input", action="store")
	parser.add_argument('-v', action='store_true', required = False,
		help='enable verbose')

	args = parser.parse_args()

	return main(args)

print(parse_args())