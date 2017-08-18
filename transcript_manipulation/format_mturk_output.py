
import argparse
verboseprint = lambda *a, **k: None



def main(args):
	global verboseprint
	verboseprint = print if args.v else lambda *a, **k: None

	mturk_file = open(args.input,"r")
	output_file = open(args.output,"w+")

	one_line = mturk_file.readline()
	prev_line_id = None
	line_list = None
	write_line = ""
	ann_count = 0
	while((one_line != "") and (one_line != "\n")):
		line_list = one_line.split(",")
		if((prev_line_id != None) and (prev_line_id == line_list[-2])):
			if(ann_count < 5):
				write_line = write_line + "," + line_list[-1][:-1]
		elif(prev_line_id == None):
			write_line = line_list[-1][:-1]
			prev_line_id = line_list[-2]
		else:
			if(ann_count > 4):
				output_file.write(write_line + "\n")
			write_line = line_list[-1][:-1]
			prev_line_id = line_list[-2]
			ann_count = 0

		ann_count += 1

		one_line = mturk_file.readline()

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

	main(args)

parse_args()
