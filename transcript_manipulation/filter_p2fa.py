
import argparse
import os
verboseprint = lambda *a, **k: None


def check_transcript(file, transcripts):
	one_p2fa_file = open(transcripts + "/" + file,"r")
	


def main(args):
	global verboseprint
	verboseprint = print if args.v else lambda *a, **k: None
	for file in os.listdir(args.transcripts):
		check_transcript(file, args.transcripts)
	for file in os.listdir(args.p2fa):
		check_p2fa(file,args.p2fa)




def parse_args():
	parser = argparse.ArgumentParser(description="""Take in files of transcript
		sentences and p2fa files and return text files of relevant videos and
		channels""")

	parser.add_argument("-t", required=True, dest="transcripts", action="store")
	parser.add_argument("-p", required=True, dest="p2fa", action="store")
	parser.add_argument('-v', action='store_true', required = False,
        help='enable verbose')

	args = parser.parse_args()

	main(args)

parse_args()
