Script to help gather useful information from video files.
Works by looking for different video files by recursively searching folders from a starting directory.
The useful data from each file is then compiled into a .csv file to be used later.

The reason for this project was to help identify which video files were taking up the most space for their length (i.e. the largest bitrate files). These files are often using less efficient video codecs and so can be transcoded into more efficient containers (h265).
FFmpeg Batch AV Converter is useful for this, especially with nvenc enabled.
