

import sys
import subprocess
import psycopg2
import datetime
import os
import shutil
import sys
import argparse



def main(args):

	try:
		conn = psycopg2.connect("dbname=%s password=%s host=%s" % ('mosi2_crawl', 'multicomp', 'localhost'))
	except:
		print("Database connection error")
		exit(0)
	cur = conn.cursor()

	input_file = open(args.input,"r")
	output_file = open(args.output,"w+")

	channel_set = set([])

	one_line = input_file.readline()
	line_list = one_line.split(',')
	while((one_line != '') and (one_line != "\n")):
		vid_id = line_list[0][0:-4]
		print(vid_id)
		search_command = """SELECT channel_id
							FROM videos_video
							WHERE id=%(id)s"""

		try:
			cur.execute(search_command, {"id":vid_id})
			channel_ids = [a for (a,) in cur.fetchall()]
			channel_id = channel_ids[0]
			if(channel_id[-2:] == '_m') or (channel_id[-2:] == '_f'):
				channel_set.add(channel_id)
				output_file.write(channel_id + ',' + ','.join(line_list))
		except:
			pass


		one_line = input_file.readline()
		line_list = one_line.split(",")

	output_file.close()
	output_chans = open(args.output_chans,'w+')
	for chan in channel_set:
		output_chans.write(chan + '\n')

	output_chans.close()



def parse_args():
	parser = argparse.ArgumentParser(description="""Take in files of transcript
		sentences and p2fa files and return text files of relevant videos and
		channels""")

	parser.add_argument("-i", required=True, dest="input", action="store")
	parser.add_argument("-c", required=True, dest="output_chans", action="store")
	parser.add_argument("-o", required=True, dest="output", action="store")
	parser.add_argument('-v', action='store_true', required = False,
		help='enable verbose')

	args = parser.parse_args()

	main(args)

parse_args()
