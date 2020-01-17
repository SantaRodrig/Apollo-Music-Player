import musicpd

client = musicpd.MPDClient()       # create client object
client.connect()
# print(client.mpd_version)
client.command_list_ok_begin()       # start a command list
results = client.command_list_end()
client.update()

# client.status()
# client.stats()

'''
def return_all_songs_as_list():
	listOfSongs = []
	for song in client.listall():
		for x in song:
			if song[x][-1] == '3':
				listOfSongs.append(song[x])
	return listOfSongs
'''


def return_all_songs_as_list():
	listOfSongs = []
	for path in client.listall():
		for x in song:
			if path[x].endswith('.mp3'):
				listOfSongs.append([x])
	return listOfSongs


# adds the song given in 'filename' to the current playlist/queue
# prints an error message if the song could not be found in the files and returns 1
"""def add_song_to_playlist(filename):
	song_in_files = False
	# check each song in the library to see if the filename matches any known paths
	listOfSongs = return_all_songs_as_list()
	for song in listOfSongs:
		if filename == song:
			song_in_files = True
			break
	# if it found the song, add it
	if song_in_files:
		client.add(filename)
		return 0
	# if not, tell us we failed
	else:
		print("Could not find song: " + filename + " in files")
		return 1"""


def add_song_to_queue(filename):
	try:
		client.add(filename)
	except:
		print("Could not find the file: " + filename)


def return_playList_songs_as_list():  # Returns a list of the playlist
	playListOfSongsList = []
	for song in client.playlist():
		if song.endswith('.mp3'):
			playListOfSongsList.append(song[6:])

	return playListOfSongsList


def remove_song_from_queue(fileName):  # get back to this
        song_in_playlist = False
        # check each song in the playlist to see if the filename matches what is in playlist
        # playlistSongs = return_playList_songs_as_list()
        # should it go with append or with the remove function because of the UI element
        playListOfSongs = return_playList_songs_as_list()
        pos = 0
        for song in playListOfSongs:
            print(pos)
            print(fileName)
            print(song)
            if fileName == song:
                song_in_playlist = True
                break
            pos = pos + 1
                
        if song_in_playlist:
            try:
                client.delete(pos)
            except:
                print("something went horribly wrong with the remove function")

def play_pause():
	if client.status()['state'] != 'play': 
		client.play()
	else:
		client.pause(1)
		
def list_all_songs():
	for song in client.listall():
		for x in song:
			if song[x][-1] == '3':		
				print(song[x])

def list_songs(): #lists songs in the playlist
	for song in client.playlistinfo():
		temp_string = (song["file"]) 
		temp_string = song_stripper(temp_string)
		print(temp_string)				
				
def song_stripper(s):  #test code -- might have bugs
	# finds last slash in filename to remove directories
	index_of_slash = s.rfind('/') 
	if index_of_slash != -1:
		temp_string = s[index_of_slash + 1:]
	else:
		temp_string = s

	# finds '.' at the end of file names to remove filetypes
	neg_size = len(temp_string) * -1
	for e in range(-1,-5,-1): 
		if e < neg_size:
			break
		elif temp_string[e] == '.':
			temp_string = temp_string[0:e]
			break

	# finds the first letter in the file name to remove track numbers
	# can mess up file names of songs that start with a number or character
	size = len(temp_string) - 1
	for e in range(6): 
		if e == size:  #TEST
			break		
		elif temp_string[e].isalpha():
			temp_string = temp_string[e:]
			break

	return temp_string

client.clear()

# list_all_songs()

x = input('select option: ' )

while x != 'stop':
        if x == 'play':
               # client.play()
                play_pause()
        elif x == 'pause':
                # client.pause()
               play_pause()
        elif x == 'next':
                # client.next()
                next_song()
        elif x == 'back':
               prev_song()
        elif x == 'add':
                list_all_songs()
                y = input('add song to playlist: ' )
                add_song_to_queue(y)
        elif x == 'playlist':
                list_songs()
        elif x == 'remove':
                list_all_songs()
                y = input('what song would you like to remove: ' )
                remove_song_from_queue(y)
        elif x.startswith('savePlaylist'):
            y = x[13:]
            client.save(y)
        elif x.startswith('addToPlaylist'):
            client.listplaylists()
            y = input('playlist name to add to: ')
            list_all_songs()
            z = input('choose song to add: ')
            client.playlistadd(y, z)
        else:
                print('not a command')
        x = input('select option: ' )

# client.play()
# play_pause()
# print(results)

client.disconnect()
