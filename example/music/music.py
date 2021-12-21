from buzzer_music import music
from time import sleep
 
#Example songs
 
song = '0 A#4 1 1;2 F5 1 1;4 D#5 1 1;8 D5 1 1;11 D5 1 1;6 A#4 1 1;14 D#5 1 1;18 A#4 1 1;20 D#5 1 1;22 A#4 1 1;24 D5 1 1;27 D5 1 1;30 D#5 1 1;32 A#4 1 1;34 F5 1 1;36 D#5 1 1;38 A#4 1 1;40 D5 1 1;43 D5 1 1;46 D#5 1 1;50 A#4 1 1;52 D#5 1 1;54 G5 1 1;56 F5 1 1;59 D#5 1 1;62 F5 1 1;64 A#4 1 1;66 F5 1 1;68 D#5 1 1;70 A#4 1 1;72 D5 1 1;75 D5 1 1;78 D#5 1 1;82 A#4 1 1;84 D#5 1 1;86 A#4 1 1;88 D5 1 1;91 D5 1 1;94 D#5 1 1;96 A#4 1 1;100 D#5 1 1;102 A#4 1 1;104 D5 1 1;107 D5 1 1;110 D#5 1 1;114 A#4 1 1;116 D#5 1 1;118 G5 1 1;120 F5 1 1;123 D#5 1 1;126 F5 1 1;98 F5 1 1'
 
from machine import Pin
 
mySong = music(song, pins=[Pin(23)])

 
while True:
    print(mySong.tick())
    sleep(0.04)