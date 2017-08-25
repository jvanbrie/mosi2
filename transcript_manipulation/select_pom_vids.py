
import argparse
import os
import shutil
import sys
import subprocess
import psycopg2
import datetime
verboseprint = lambda *a, **k: None

video_file_extension = "/videos/Video/Full/"
p2fa_file_extension = "/p2fa/Segmented/"
transcript_file_extension = "/transcripts/reform/per_sem/"

command = """INSERT INTO videos_video
					   (search_type, id, search, search_time,
						download_attempted, channel_id, title,
						subtitle_type,face_percentage, pass_check,
						pass_p2fa_check)
						VALUES (0, %(video_id)s, %(pom)s, %(time)s,
							   true, %(speaker)s, %(pom)s, 1, %(fp)s,
							   %(t)s,%(t)s) """
	


def main(args):
	global verboseprint
	verboseprint = print if args.v else lambda *a, **k: None

	dbname = "mosi2_crawl"
	dbpw="multicomp"
	dbhost="localhost"

	try:
		conn = psycopg2.connect("dbname=%s password=%s host=%s" % (dbname, dbpw, dbhost))
	except:
		print("Database connection error")
		exit(0)
	cur = conn.cursor()

	def chosen_one(vid_id_line,pom_input,pom_output):
		vid_id = vid_id_line[0]
		args2 = {'video_id': "pom_" + vid_id,
				"speaker": vid_id_line[1],
				"fp": .99,
				"pom": "pom",
				"t": "t",
				"time": datetime.datetime.now()}
		try:
			cur.execute(command, args2)
			conn.commit()
		except:
			print("missed inserting one")

		shutil.copy(pom_input + video_file_extension + vid_id + ".mp4", pom_output + "/videos/")
		shutil.copy(pom_input + p2fa_file_extension + vid_id + "_aligned_final.txt", pom_output + "/p2fa/")
		shutil.copy(pom_input + transcript_file_extension + vid_id + ".csv", pom_output + "/transcripts/")

		print("inserted and printed vid with id: " + (vid_id))


	pom_db_file = open(args.pom_db,"r")
	temp_line = pom_db_file.readline()
	temp_line = pom_db_file.readline()
	line_list=[]
	speaker_set = set([])
	video_ids = []
	video_count = 0
	female_vids = []
	male_vids = []
	female_vid_count = 0
	male_vid_count = 0
	sent_vid_count = [0] * 5


	while((temp_line != "") and (temp_line != "\n")):
		line_list = temp_line.split(",")
		if(line_list[1] in speaker_set):
			pass
		else:

			video_ids.insert(0,line_list[0])
			speaker_set.add(line_list[1])
			video_count += 1
			if(line_list[4] == "f"):
				female_vids.insert(0,line_list[0])
				female_vid_count += 1
				chosen_one(line_list,args.pom_source,args.pom_dest)
			else:
				if(sent_vid_count[int(line_list[2])-1] > 66):
					continue
				else:
					sent_vid_count[int(line_list[2])-1] += 1
					male_vids.insert(0,line_list[0])
					male_vid_count += 1
					chosen_one(line_list,args.pom_source,args.pom_dest)

		temp_line = pom_db_file.readline()

	verboseprint("Number of videos: %d" % video_count)
	verboseprint("Number of female videos: %d" % female_vid_count)
	verboseprint("Number of male videos: %d" % male_vid_count)
	verboseprint(sent_vid_count)

	return video_ids





def parse_args():
	parser = argparse.ArgumentParser(description="""Take in files of transcript
		sentences and p2fa files and return text files of relevant videos and
		channels""")

	parser.add_argument("-d", required=True, dest="pom_db", action="store")
	parser.add_argument("-p", required=True, dest="pom_source", action="store")
	parser.add_argument("-o", required=True, dest="pom_dest", action="store")
	parser.add_argument('-v', action='store_true', required = False,
		help='enable verbose')

	args = parser.parse_args()

	return main(args)

print(parse_args())