rm -rf ./ffmpeg_output
mkdir ffmpeg_output
ffmpeg -hide_banner -loglevel panic -i ./ZZXQF.mp4 -filter:v fps=fps=$1 ./ffmpeg_output/ZZXQF-%6d.jpg
echo "FFMPEG Extract #Frames "$(ls -l ./ffmpeg_output | grep "^-" | wc -l)