import re, os
from pytube import YouTube, Playlist 
import http.client
from tkinter import Tk, TclError, Message
import tkinter.messagebox as msgb


YOUTUBE_STREAM_AUDIO = '140'

if os.name == 'posix':
	CONVERT = False
	AUDIO_DIR = '/storage/emulated/0/Download/Audiobooks'
	DIR_SEP = '/'
	WIN_WIDTH_RATIO = 1
	WIN_HEIGHT = 800	
else:
	CONVERT = False # can be set to True
	AUDIO_DIR = 'D:\\Users\\Jean-Pierre\\Downloads\\Audiobooks'
	DIR_SEP = '\\'
	WIN_WIDTH_RATIO = 0.8
	WIN_HEIGHT = 500	

class YoutubeAudioDownloader:
	def __init__(self):
		self.root = Tk()
		winWidth = int(self.root.winfo_screenwidth() * WIN_WIDTH_RATIO)
		self.root.geometry("{}x{}".format(winWidth, WIN_HEIGHT)) 
		self.msg = Message(self.root, aspect=winWidth - 10)
		self.msg.grid(row=2, column=0, columnspan=2, padx=2) 
		self.msgText = ''  

		self.playlistUrl = self.getPlaylistUrlFromClipboard()

	def getPlaylistUrlFromClipboard(self):
		playlistUrl = None

		try:
			playlistUrl = self.root.clipboard_get()
		except TclError as e:
			# playlistUrl remains None
			pass

		return playlistUrl
		
	def displayError(self, msg):
		return msgb.showerror(message=msg)
		
	def getConfirmation(self, msg):
		return msgb.askquestion(message=msg)

	def doDownload(self):
		if self.playlistUrl == None:
			self.displayError('Playlist URL not in clipboard. Program closed.')

			return

		playlist = None
		
		try:
			playlist = Playlist(self.playlistUrl)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
		except KeyError as e:
			self.displayError('Playlist URL not in clipboard. Program closed.')			
			return
		except http.client.InvalidURL as e:
			self.displayError(str(e))
			return
		
		playlistTitle = playlist.title()
		
		if 'Oops' in playlistTitle:
			self.displayError('The URL obtained from clipboard is not pointing to a playlist. Program closed.')
			return
			
		targetAudioDir = AUDIO_DIR + DIR_SEP + playlistTitle
		
		if not os.path.isdir(targetAudioDir):
			if self.getConfirmation("Directory {} will be created. Continue with download ?".format(targetAudioDir)) != 'yes':
				return
				
			os.makedirs(targetAudioDir)
				
		for video in playlist.videos:
			audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
			videoTitle = video.title
			self.msgText = self.msgText + 'downloading ' + videoTitle + '\n'
			self.msg.configure(text=self.msgText)
			self.root.update()
			audioStream.download(output_path=targetAudioDir)

		for file in [n for n in os.listdir(targetAudioDir) if re.search('mp4', n)]:
			mp4FilePathName = os.path.join(targetAudioDir, file)
			mp3FilePathName = os.path.join(targetAudioDir, os.path.splitext(file)[0] + '.mp3')

			if CONVERT:
				import moviepy.editor as mp  # not working on Android
			#	clip = mp.AudioFileClip(full_path).subclip(10, )  # disable if do not want any clipping
				clip = mp.AudioFileClip(mp4FilePathName)
				clip.write_audiofile(mp3FilePathName)
			else:
				if os.path.isfile(mp3FilePathName):
					os.remove(mp3FilePathName)

				os.rename(mp4FilePathName, mp3FilePathName)

if __name__ == "__main__":
	downloader = YoutubeAudioDownloader()
	downloader.doDownload()
		

