import os
import shutil
# The shutil module offers a number of high-level operations on files and
# collections of files. In particular, functions are provided which support
# file copying and removal. For operations on individual files,
# see also the os module.
# Only used once for shutil.move(file_path, dir)
import eyed3
eyed3.log.setLevel("ERROR")
# https://eyed3.readthedocs.io/en/latest/installation.html
# eyeD3 is a Python tool for working with audio files, specifically
# MP3 files containing ID3 metadata (i.e. song info).
# https://stackoverflow.com/questions/22403189/python-eyed3-warning
# GPL - https://simple.wikipedia.org/wiki/GNU_General_Public_License


# Get "working directory", aka the folder (and the ones its in) you're doing work in
project_wd = os.getcwd()
os.chdir(project_wd + "/BP_Test_Files")
cwd = os.getcwd()
# Take the working directory then add the name of the folder where you'll put everything
# Once you have the name of that full folder


track_details = []
allfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]

# CHECK FOR OTHER GARBAGE OTHER THAN MP3s
garbage_bin_list = []
for line in range(0,len(allfiles)):
    if allfiles[line].endswith(".mp3"):
        pass
    else:
        garbage_bin_list.append(line)
for index in range(0, len(garbage_bin_list)):
    del(allfiles[index])


# SPLIT UP TAGS
for line in range(0,len(allfiles)):
    BP_track_name = allfiles[line]
    BP_track_name_split = BP_track_name.split("_", 1)
    BP_track_number = BP_track_name_split[0]

    file = eyed3.load(allfiles[line])
    track_detail = [BP_track_number, file.tag.album, file.tag.artist, file.tag.title, BP_track_name]
    track_details.append(track_detail)


print("\nRaw list of files: ")
for line in range(0, len(track_details)):
    print(track_details[line])


print("\n***************************************************\n")



if len(track_details[line][0]) > 4:
    pass
else:
    print("This is an old track. You will need to follow up.")
    print(track_details[line])


def name_folder(folder_contents):
    artist_list = []
    artist_percent_list_1 = []
    artist_percent_list_2 = []

    if len(folder_contents) == 1:
        artist_name = folder_contents[0][2]
        track_name = folder_contents[0][3]
        folder_name = artist_name + " - " + track_name
        if folder_name.endswith(" (Original Mix)"):
            folder_name = folder_name[:-len(" (Original Mix)")]
    else:
        for file in range(0, len(folder_contents)):
            #print(folder_contents[line])
            album_name = folder_contents[file][1]
            artist_name = folder_contents[file][2]
            artist_list.append(artist_name)

        #print(artist_list)

        for artist_in_album in range(0,len(artist_list)):
            artist_percent = artist_list.count(artist_list[artist_in_album])/len(artist_list)
            #print(artist_percent)
            #artist_percent_list.insert(0, artist_list[artist_in_album])
            #artist_percent_list.insert(1, artist_percent)
            artist_and_percent = [artist_list[artist_in_album], artist_percent]
            artist_percent_list_1.append(artist_list[artist_in_album])
            artist_percent_list_2.append(artist_percent)

        #print(artist_percent_list_1)
        #print(artist_percent_list_2)
        current_max = 0
        for line in range(0,len(artist_percent_list_2)):
            if artist_percent_list_2[line] > current_max:
                current_max = artist_percent_list_2[line]
                current_max_index = line
        #print(current_max)
        max_artist_percent = current_max
        if max_artist_percent > 0.5:
            artist_name = artist_percent_list_1[current_max_index]
        elif max_artist_percent < 0.5:
            artist_name = "VA"
        elif max_artist_percent == 0.5:
            artist_percent_list_1_no_dupl = []
            artist_percent_list_2_no_dupl = []
            [artist_percent_list_1_no_dupl.append(x) for x in artist_percent_list_1 if x not in artist_percent_list_1_no_dupl]
            #print(artist_percent_list_1_no_dupl)
            [artist_percent_list_2_no_dupl.append(x) for x in artist_percent_list_2 if x not in artist_percent_list_2_no_dupl]
            #print(artist_percent_list_2_no_dupl)

            if len(artist_percent_list_2_no_dupl) == 1:
                artist_name = artist_percent_list_1_no_dupl[0] + ", " + artist_percent_list_1_no_dupl[1]
            else:
                #print(artist_percent_list_2)
                artist_name = artist_percent_list_1[artist_percent_list_2.index(0.5)]


        #print(artist_percent_list)

        folder_name = artist_name + " - " + album_name

    return folder_name


new_folder = []
new_folder_list = []
remaining_track_details = []

while track_details or remaining_track_details:
    compare_line = track_details[0]
    new_folder.append(track_details.pop(0))


    while track_details:
        #print(compare_line[0][0:4])
        #print(track_details[0][0][0:4])
        if compare_line[0][0:4] == track_details[0][0][0:4] \
        and compare_line[1] == track_details[0][1]:
            new_folder.append(track_details.pop(0))
        else:
            remaining_track_details.append(track_details.pop(0))

    folder_name = name_folder(new_folder)
    #print(folder_name)
    new_folder_list.append(new_folder)

    track_details = remaining_track_details
    remaining_track_details = []

    new_folder = []


for line in range(0, len(new_folder_list)):
    print(f"A new folder ({name_folder(new_folder_list[line])}) needs to be created with these files:")

    for subline in range(0, len(new_folder_list[line])):
        print(new_folder_list[line][subline][0] + " | " + \
                new_folder_list[line][subline][1] + " | " + \
                new_folder_list[line][subline][2] + " | " + \
                new_folder_list[line][subline][3])
        print(new_folder_list[line][subline][4])
    print("")


    dir = name_folder(new_folder_list[line])
    #print(dir)

    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except:
        "There was an error making a directory"
        print(dir)



    for subline in range(0, len(new_folder_list[line])):
        if os.path.exists(dir):
            file_path = cwd + "/" + new_folder_list[line][subline][4]
            dir_path = cwd + "/" + dir + "/" + new_folder_list[line][subline][4]
            #print(f'dir_path: {dir_path}')

            # move files into created directory
            shutil.move(file_path, dir)
