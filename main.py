import pafy
import shutil
import os
import subprocess
#link = 'https://youtu.be/PIrWquI_mQ0'

def handleAudioFile(audio):
	cwd = os.getcwd()
	filename = audio.title + "." + audio.extension
	old_path = '/tmp/' + filename
	new_path = cwd + '/' + filename
	shutil.move(old_path, new_path)

def getInput():
	global link, tt, choice
	link = input("Enter video link:")
	try:
		tt = pafy.new(link)
	except Exception as e:
		print(e)
		print("Please enter correct video url!")
		exit()

	print("\n\nDetails:")
	print(tt)
	print("select mediatype you want to download:\n0: Audio\n1: Video")
	choice = int(input());

def handleVideoFile():
	# rename audio file to 'audio.webm'
	filepath = '/tmp/' + audio.title + "." + audio.extension
	os.rename(filepath, '/tmp/audio.webm')

	webm_videos = []
	for t in tt.videostreams:
		if t.extension == 'webm':
			webm_videos.append(t);
	print("select video quality:")

	for i, t in enumerate(webm_videos):
		print(i, ":", t.dimensions)

	c = int(input())

	global video
	video = webm_videos[c];
	
	video.download(quiet = False, filepath='/tmp')
	filepath = '/tmp/' + video.title + ".webm"
	os.rename(filepath, '/tmp/video.webm')
	
def mergeFiles():
	cmd = ['ffmpeg', '-i', '/tmp/video.webm', '-i' ,'/tmp/audio.webm' ,'-map', '0:v' , '-map' , '1:a' , '-c' , 'copy' , '-y', video.title + '.webm']
	sp = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	ret_value = sp.wait()
	out, err = sp.communicate()

	with open('log.txt', 'w+') as fp:
		fp.write(out.decode('utf-8'))
		fp.write(err.decode('utf-8'))
	if ret_value:
		print("Error in merging audio video files")
		os.remove('/tmp/audio.webm')
		os.remove('/tmp/video.webm')
		exit();
	cwd = os.getcwd()
	filename = video.title + '.webm' 
	old_path = '/tmp/' + filename
	new_path = cwd + '/' + filename
	# shutil.move(old_path, new_path)
	# os.remove(old_path)
	os.remove('/tmp/audio.webm')
	os.remove('/tmp/video.webm')


if __name__ == '__main__':
	global audio
	getInput();
	audio = tt.getbestaudio(preftype='webm') 
	audio.download(filepath='/tmp', quiet=False)
	if choice == 0:
		handleAudioFile(audio)
	elif choice == 1:
		handleVideoFile()
		mergeFiles()


#ffmpeg -i 1.webm -i 2.webm -map 0:v -map 1:a -c copy -y result.webm
#pip install --upgrade youtube-dl

