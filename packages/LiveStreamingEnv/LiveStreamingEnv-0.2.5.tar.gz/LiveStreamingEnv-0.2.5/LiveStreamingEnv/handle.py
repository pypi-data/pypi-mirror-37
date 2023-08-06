import random

BITRATE_LEVELS = 2
video_size = {}  # in bytes
cdn_arrive_time = {}
gop_time_len = {}
gop_flag = {}
VIDEO_SIZE_FILE ='./video_trace/video_size_copy_'

f = open("./time_variance")
time_lines = f.readlines()
f.close()
random_id = random.randint(0,1000)
for bitrate in range(BITRATE_LEVELS):
    video_size[bitrate] = []
    cdn_arrive_time[bitrate] = []
    gop_time_len[bitrate] = []
    gop_flag[bitrate] = []
    cnt = 0
    with open(VIDEO_SIZE_FILE + str(bitrate)) as f:
         for line in f:
            #print(line.split(), bitrate)	    
            video_size[bitrate].append(int(float(line.split()[0])))
            gop_time_len[bitrate].append(0.04)
            gop_flag[bitrate].append(int(float(line.split()[1])))
            if cnt == 0:
                cdn_arrive_time[bitrate].append(0)
            else:
                #self.cdn_arrive_time[bitrate].append(sum(self.gop_time_len[bitrate]) + self.gop_time_len[bitrate][cnt-1] + float(time_lines[(random_id + cnt) % 1000 ]))
                cdn_arrive_time[bitrate].append(cdn_arrive_time[bitrate][cnt-1] + gop_time_len[bitrate][cnt-1])
            cnt += 1
random_id = random.randint(0,1000)
for idx in range(len(cdn_arrive_time[0])):
    random_loss = float(time_lines[(random_id + idx) % 1000 ])
    for bitrate in range(BITRATE_LEVELS):
          cdn_arrive_time[bitrate][idx] += random_loss
OUT_FILE = "video_size_"
for bitrate in range(BITRATE_LEVELS):
    f =  open(OUT_FILE + str(bitrate),"w")
    for idx in range(len(video_size[0])):
            #print(cdn_arrive_time[bitrate][idx], video_size[bitrate][idx], gop_flag[bitrate][idx])
        f.write(str(cdn_arrive_time[bitrate][idx]) + "\t" +
               str (video_size[bitrate][idx]) +  "\t" +
               str(gop_flag[bitrate][idx]) + "\n")
    f.close()
exit()
