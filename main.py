import os
import glob
import csv
import subprocess
import json
from alive_progress import alive_bar

# Function to fetch the codec and duration of a video file
# duration is represented in seconds
def get_video_data(filepath):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                 'format=filename,duration:stream=codec_name', '-of', 'json', filepath],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration = data['format']['duration']
            codec_name = data['streams'][0]['codec_name']
            return codec_name, duration, ""
        else:
            print("Error running ffprobe", result.stderr)
    except Exception as e:
        print("An error occurred", e)
    return "Error Detected", "1", e


# Function to create an entry to be written to a csv
def build_entry(filename):
    currentItem[0] = os.path.basename(os.path.normpath(filename))
    currentItem[1] = round(os.path.getsize(filename) / (1024 ** 3), 3)
    currentItem[2], currentItem[3], currentItem[6] = get_video_data(filename)
    currentItem[4] = ((float(currentItem[1])*(1024 ** 2)) / float(currentItem[3]))
    currentItem[3] = round(float(currentItem[3]) / 60, 2)
    currentItem[5] = filename
    return currentItem


def scan(fileExtension):
    print("STARTING INITIAL " + fileExtension + " SCAN...")
    count = 0
    for f in glob.glob(BASE_DIR + '/**/*.' + fileExtension, recursive=True):
        count += 1
    print("FOUND " + str(count) + " " + fileExtension + "s")
    with alive_bar(count, force_tty=True) as bar:
        for filename in glob.glob(BASE_DIR + '/**/*.' + fileExtension, recursive=True):
            build_entry(filename)
            writer.writerow(currentItem)
            bar()
    print(fileExtension + " SCAN COMPLETE\n\n")


# Set this to be the directory to scan
BASE_DIR = 'N:\\Plex\\Films'
OUTPUT = "Scan new"
# Set this to be the video formats to consider
formatSearch = ['mkv', 'mp4', 'avi', 'm4a', 'mov', 'wmv', 'm4v']

header = ['Filename', 'Filesize', 'Codec', 'Length', 'Rate (Kbps)', 'Directory', 'Error']
currentItem = ['', '', '', '', '', '', '']

with open(OUTPUT+'.csv', 'w', newline='') as out:
    writer = csv.writer(out)
    writer.writerow(header)

    for ext in formatSearch:
        scan(ext)
