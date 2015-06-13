import os
import shutil

def organize_music(path, separator = " - "):
    '''Puts all the songs into folders separated by artists'''
    songs = get_songs(path)
    songsOrganized = 0
    failedSongs = []
    for song in songs:
        song = song.strip()
        if song.rfind(separator) == -1:
            failedSongs.append(song)
            continue
        artist, songName = song.split(separator, maxsplit=1)
        artistFolder = os.path.join(path, artist).strip()
        if not os.path.exists(artistFolder):
            os.mkdir(artistFolder)
        songSrc = os.path.join(path, song)
        songDst = os.path.join(artistFolder, song)
        try:
            os.rename(songSrc, songDst)
        except FileNotFoundError:
            failedSongs.append(song)
        else:
            songsOrganized += 1
        
    print("%d songs moved successfully. %d failed."
          % (songsOrganized, len(failedSongs)))
    print("The following songs failed: ", failedSongs)
    
def get_songs(path):
    '''Gets all songs in folder given a path'''
    return [file for file in os.listdir(path)
             if os.path.isfile(os.path.join(path, file)) and file[-3:] == 'mp3']

if __name__ == '__main__':
    path = input("What folder do you want to search?")
    separator = input("Insert a separator for the artist name and song name: ")
    organize_music(path, separator)
