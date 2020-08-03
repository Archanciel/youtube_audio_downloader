import re, os
from pytube import YouTube, Playlist
from tkinter import Tk
import tkinter.messagebox as msgb


YOUTUBE_STREAM_AUDIO = '140'

if os.name == 'posix':
	CONVERT = False
	DOWNLOAD_DIR = '/storage/emulated/0/Download'
	AUDIO_DIR = '/storage/emulated/0/Download/Audiobooks'
	DIR_SEP = '/'	
else:
	CONVERT = False # can be set to True
	DOWNLOAD_DIR = 'D:\\Users\\Jean-Pierre\\Downloads'
	AUDIO_DIR = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
	DIR_SEP = '\\'

class YoutubeAudioDownloader:
	def __init__(self):
		self.playlistUrl = self.getPlaylistUrlFromClipboard()
		a = 1
		
	def getPlaylistUrlFromClipboard(self):
		self.root = Tk()
		
		return self.root.clipboard_get()
		
	def displayError(self, msg):
		return msgb.showerror(message=msg)
		
	def getConfirmation(self, msg):
		return msgb.askquestion(message=msg)

	def doDownload(self):
		playlist = None
		
		try:
			playlist = Playlist(str(self.playlistUrl))
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		except BaseException as e:
			self.displayError('Playlist URL not in clipboard. Program closed.')
			
			return 
		
		targetAudioDir = AUDIO_DIR + DIR_SEP + playlist.title()
		
		if not os.path.isdir(targetAudioDir):
			if self.getConfirmation("Directory {} will be created. Continue with download ?".format(targetAudioDir)) != 'yes':
				return
				
			os.makedirs(targetAudioDir)
				
		for video in playlist.videos:
			audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
			audioStream.download(output_path=DOWNLOAD_DIR)

		for file in [n for n in os.listdir(DOWNLOAD_DIR) if re.search('mp4', n)]:
			fullPath = os.path.join(DOWNLOAD_DIR, file)
			outputPath = os.path.join(targetAudioDir, os.path.splitext(file)[0] + '.mp3')

			if CONVERT:
				import moviepy.editor as mp  # not working on Android
			#	clip = mp.AudioFileClip(full_path).subclip(10, )  # disable if do not want any clipping
				clip = mp.AudioFileClip(fullPath)
				clip.write_audiofile(outputPath)
			else:
				os.rename(fullPath, outputPath)

if __name__ == "__main__":
	downloader = YoutubeAudioDownloader()
	downloader.doDownload()
		

