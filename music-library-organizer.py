import os
import shutil

def organize_music(path, separator = " - "):
    '''Puts all the songs into folders separated by artists'''
    songs = get_songs(path)
    songsOrganized = 0
    failedSongs = []
    for song in songs:
        song = song.strip()
        if song.find(separator) == -1:
            failedSongs.append(song)
            continue
        artist, songName = song.split(separator, maxsplit=1)
        artistFolder = os.path.abspath(os.path.join(path, artist).strip())
        if not os.path.exists(artistFolder):
            os.mkdir(artistFolder)
            
        songSrc = os.path.join(path, song)
        songDst = os.path.join(artistFolder, song)
        try:
            os.rename(songSrc, songDst)
        except FileNotFoundError as error:
            print(error)
            failedSongs.append(song)
        except FileExistsError as error:
            print(error)
            failedSongs.append(song)
        else:
            songsOrganized += 1
            
    return songsOrganized, failedSongs

def deorganize_music(path, separator):
    '''Undoes what organize_music does if given the same path and separator, use at your own risk'''
    folders = get_folders(path)
    failedSongs = []
    songsDeOrganized = 0
    for folder in folders:
        folderPath = os.path.join(path, folder)
        songs = get_songs(folderPath)
        for song in songs:
            if should_remove_from_folder(song, separator, folder):
                try:
                    os.rename(os.path.join(folderPath, song), os.path.join(path, song))
                except FileNotFoundError:
                    failedSongs.append(song)
                except FileExistsError:
                    failedSongs.append(song)
                else:
                    songsDeOrganized += 1

        if os.listdir(folderPath) == []:
            os.rmdir(folderPath)

    return songsDeOrganized, failedSongs

def should_remove_from_folder(song, separator, folder):
    return song.split(separator, maxsplit=1)[0].upper().strip('. ') == folder.upper()

def get_folders(path):
    '''Gets subfolders of a folder'''
    return [folder for folder in os.listdir(path)
            if os.path.isdir(os.path.join(path, folder))]
    
def get_songs(path):
    '''Gets all songs in folder given a path'''
    return [file for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file)) and file[-3:] == 'mp3']

if __name__ == '__main__':
    path = input("What folder do you want to search?").strip()
    separator = input("Insert a separator for the artist name and song name: ")
    succesful, fails = organize_music(path, separator)
    #succesful, fails = deorganize_music(path, separator)
    print("%d songs moved successfully. %d failed."
          % (succesful, len(fails)))
    if len(fails) > 0:
        print("The following songs failed: ", fails)
    
