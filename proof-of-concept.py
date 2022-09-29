# USE AT YOUR OWN RISK!!!!
#
# Requires eyed3 and plexapi libraries, written & tested in python 3.9

from plexapi.myplex import MyPlexAccount
import eyed3

LIB = 'INSERT LIBRARY NAME'
# Counters
insync = 0
justsynced = 0
notag = 0
error = 0

account = MyPlexAccount('INSERT USERNAME', 'INSERT PASSWORD')
plex = account.resource(LIB).connect()

for album in plex.library.section(LIB).albums():
    for track in album.tracks():
        # Iterates across all tracks
        
        if isinstance(track.userRating, float): 
            # Checks to see if the Plex userRating exists, var type will be float if track is rated, it will be nonetype if not.
            
            print(track.title + ' is already rated in Plex, checking if export is needed...')
            audiofile = eyed3.load(track.locations[0])
            
            if isinstance(audiofile.tag.publisher,str):
                # Checks to see if ID3 tag exists and what it's value is to determine if it's already synced.
                
                rating = audiofile.tag.publisher
                try:
                    if float(rating) == track.userRating:
                        insync +=1
                        print('... Ratings are synchronized between Plex and local id3 tags.')
                except:
                    error +=1
                    print('… There is an issue with the local id3 tag aborting rating export') 
                    
            else:
                # This catches the case where ratings are to be exported from Plex -> ID3 Tag
                
                print('... Id3 tag does not exist, creating a new value from Plex: '+ str(track.userRating) )
                audiofile.tag.publisher = str(track.userRating)
                audiofile.tag.save(preserve_file_time=False,backup=False)
                justsynced +=1
                
        else:
            # This case is where Plex has no rating so it tries to fetch a value from the id3 tag
            
            print(track.title + ' has no rating in Plex, checking publisher id3 tag')
            try: 
                audiofile = eyed3.load(track.locations[0])
                if isinstance(audiofile.tag.publisher,str):
                    # this case is where Plex has no rating but the iD3 tag does so the next steps import the rating into Plex.
                
                    rating = audiofile.tag.publisher
                    track.rate(float(rating))
                    print('... ID3 tag rating value of ' + rating + ' found and saved to Plex userRating field.')
                    justsynced += 1 
                    
                else:
                    print('... failed to read id3 tag rating value for '+ track.title + ' due to incorrect Publisher tag')
                    error += 1
                    
            except:
                # This case is where eyeD3 raises an error due to issues with loading the tag
                
                print('... Error loading id3 tags')
                error += 1

# Stats Output                          
print(str(insync) + ' files alread in sync')
print(str(justsynced) + ' newly synced files')
print(str(notag) + ' files with no tags')
print(str(error) + ' files had errors')
