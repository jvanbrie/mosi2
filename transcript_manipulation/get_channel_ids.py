


from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import sys
import subprocess
import psycopg2
import datetime
import youtube_dl
import os
import shutil
import numpy as np
import sys
import argparse


sys.path.insert(0, '.')
import secrets

# Developer key must be kept private!
DEVELOPER_KEY = secrets.DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
RELEVANT_LANGUAGE = 'en'


def main(args):

	try:
		conn = psycopg2.connect("dbname=%s password=%s host=%s" % (secrets.DBNAME, secrets.DBPW, secrets.DBHOST))
	except:
		print("Database connection error")
		exit(0)
	cur = conn.cursor()

	output_file = open(args.output,"w+")


	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
			developerKey=DEVELOPER_KEY)

	search_command = "SELECT id FROM videos_video WHERE channel_id='old' AND pass_check='t'"
	cur.execute(search_command,{})

	vid_ids = [a for (a,) in cur.fetchall()]

	for vid_id in vid_ids:

		search_response = youtube.videos().list(
			part = "snippet",
			id = vid_id).execute()

		for search_result in search_response.get("items", []):
			output_file.write(vid_id + "," + search_result['snippet']['channelId'] + "\n")

	output_file.close()


def parse_args():
	parser = argparse.ArgumentParser(description="""Take in files of transcript
		sentences and p2fa files and return text files of relevant videos and
		channels""")

	parser.add_argument("-o", required=True, dest="output", action="store")
	parser.add_argument('-v', action='store_true', required = False,
		help='enable verbose')

	args = parser.parse_args()

	main(args)

parse_args()
