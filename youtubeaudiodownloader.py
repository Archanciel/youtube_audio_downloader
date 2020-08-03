import re, os
from pytube import YouTube, Playlist

YOUTUBE_STREAM_AUDIO = '140'

if os.name == 'posix':
	CONVERT = False
	DOWNLOAD_DIR = '/storage/emulated/0/Download'
else:
	CONVERT = False # can be set to True
	DOWNLOAD_DIR = 'D:\\Users\\Jean-Pierre\\Downloads'

class YoutubeAudioDownloader:
	def __init__(self):
		pass

	def doDownload(self):
		playlist = Playlist('https://www.youtube.com/playlist?list=PLzwWSJNcZTMSW-v1x6MhHFKkwrGaEgQ-L')
		playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

		for video in playlist.videos:
			audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
			audioStream.download(output_path=DOWNLOAD_DIR)

		for file in [n for n in os.listdir(DOWNLOAD_DIR) if re.search('mp4', n)]:
			fullPath = os.path.join(DOWNLOAD_DIR, file)
			outputPath = os.path.join(DOWNLOAD_DIR, os.path.splitext(file)[0] + '.mp3')

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
		

