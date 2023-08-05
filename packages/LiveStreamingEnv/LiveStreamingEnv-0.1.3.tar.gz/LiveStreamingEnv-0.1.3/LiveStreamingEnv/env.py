import numpy as np
import random
import datetime

MILLISECONDS_IN_SECOND = 1000.0
B_IN_MB = 1000000.0
BITS_IN_BYTE = 8.0
RANDOM_SEED = 42
VIDEO_CHUNCK_LEN = 2000.0  # millisec, every time add this amount to buffer
THROUGHT_LEN = 2000.0  # millisec, every time add this amount to buffer
BITRATE_LEVELS = 2
BUFFER_LEVELS = 2
CHUNK_TIME_LEN = 2
TOTAL_VIDEO_CHUNCK = 1000
BUFFER_THRESH = 60.0 * MILLISECONDS_IN_SECOND  # millisec, max buffer limit
DRAIN_BUFFER_SLEEP_TIME = 500.0  # millisec
PACKET_PAYLOAD_PORTION = 0.95
LINK_RTT = 80  # millisec
PACKET_SIZE = 1500  # bytes
NOISE_LOW = 0.9
NOISE_HIGH = 1.1
lamda = 1
default_quality = 0
latency_threshold = 7
skip_add_frame = 100
Debug = True
class Environment:
    def __init__(self, all_cooked_time, all_cooked_bw, all_cooked_rtt, random_seed=RANDOM_SEED, logfile_path='./', VIDEO_SIZE_FILE ='./video_size_'):
        assert len(all_cooked_time) == len(all_cooked_bw)
        assert len(all_cooked_time) == len(all_cooked_rtt)
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        self.log_file = open(logfile_path +"log." +current_time, "w")

        self.video_size_file = VIDEO_SIZE_FILE
        np.random.seed(random_seed)

        self.all_cooked_time = all_cooked_time
        self.all_cooked_bw = all_cooked_bw
        self.all_cooked_rtt = all_cooked_rtt
        self.time = 0
        self.play_time = 0
        self.play_time_counter = 0

        self.video_chunk_counter = 0
        self.buffer_size = 0

        self.gop_start_flag = 1
        # pick a random trace file
        self.trace_idx = np.random.randint(len(self.all_cooked_time))
        self.cooked_time = self.all_cooked_time[self.trace_idx]
        self.cooked_bw = self.all_cooked_bw[self.trace_idx]
        self.cooked_rtt = self.all_cooked_rtt[self.trace_idx]
        # randomize the start point of the trace
        # note: trace file starts with time 0
        #self.mahimahi_ptr = np.random.randint(1, len(self.cooked_bw))
        #self.mahimahi_ptr = 1
        self.decision = False
        self.buffer_status = True
        self.skip_flag = False
        self.skip_time = 100000
        
        #self.last_mahimahi_time = self.cooked_time[self.mahimahi_ptr - 1]
        self.video_size = {}  # in bytes
        self.cdn_arrive_time = {}
        self.gop_time_len = {}
        self.gop_flag = {}
        f = open("./time_variance")
        time_lines = f.readlines() 
        f.close()
        random_id = random.randint(0,1000)
        for bitrate in xrange(BITRATE_LEVELS):
            self.video_size[bitrate] = []
            self.cdn_arrive_time[bitrate] = []
            self.gop_time_len[bitrate] = []
            self.gop_flag[bitrate] = []
            cnt = 0
            with open(self.video_size_file + str(bitrate)) as f:
                for line in f:
                    #print(line.split(), bitrate)
                    self.video_size[bitrate].append(int(float(line.split()[0])))
                    self.gop_time_len[bitrate].append(0.04)
                    self.gop_flag[bitrate].append(int(float(line.split()[1])))
                    if cnt == 0:
                        self.cdn_arrive_time[bitrate].append(0)
                    else:
                        #self.cdn_arrive_time[bitrate].append(sum(self.gop_time_len[bitrate]) + self.gop_time_len[bitrate][cnt-1] + float(time_lines[(random_id + cnt) % 1000 ]))
                        self.cdn_arrive_time[bitrate].append(self.cdn_arrive_time[bitrate][cnt-1] + self.gop_time_len[bitrate][cnt-1])
                    cnt += 1
        random_id = random.randint(0,1000)
        for idx in range(len(self.cdn_arrive_time[0])):
            random_loss = float(time_lines[(random_id + idx) % 1000 ])
            for bitrate in range(BITRATE_LEVELS):
                 self.cdn_arrive_time[bitrate][idx] += random_loss
        self.gop_remain = self.video_size[default_quality][0]
        self.latency = self.gop_time_len[0][0] 

       
    def get_video_frame(self, quality, target_buffer):

        assert quality >= 0
        assert quality < BITRATE_LEVELS

        # Initial the Settings
        self.decision = False                                                 # GOP_flag
        video_frame_size = self.video_size[quality][self.video_chunk_counter] # Data_size
        cdn_rebuf_time = 0                                                    # CDN_rebuf_time
        rebuf = 0                                                             # rebuf_time
        CHUNK_TIME_LEN = 0.04                                                 # frame time len
        end_of_video = False                                                  # is trace time end
        duration = 0                                                          # this loop 's time len
        rtt = 0                                                               # this loop 's  rtt
 
        if target_buffer == 2:
            quick_play_bound = 2.5
            slow_play_bound = 1.0
        else:
            quick_play_bound = 4
            slow_play_bound = 1.5
        # This code is check the quick play or slow play
        # output is the play_weight
        if self.buffer_size > quick_play_bound :
            #quick play
            play_duration_weight = 1.05
            #if Debug:
                #print("kuaibo\n") 
            #elif self.buffer_size < slow_play_bound:
        elif  self.buffer_size < slow_play_bound :
            #slow play
            play_duration_weight = 0.95
            #if Debug:
                #print("manbo\n")
        else:
            play_duration_weight = 1
        
        # This code is check Is the cdn has the frame in this time
        # self.time means the real time
        # self.cdn_arrive_time means the time the frame came
        if self.time < self.cdn_arrive_time[quality][self.video_chunk_counter] and not end_of_video: # CDN can't get the frame
            cdn_rebuf_time = self.cdn_arrive_time[quality][self.video_chunk_counter] - self.time
            # if the client means the buffering
            if not self.buffer_status:
                # not buffering ,you can't get the frame ,but you must play the frame

                # the buffer is enough
                if self.buffer_size > cdn_rebuf_time * play_duration_weight:
                    self.buffer_size -= cdn_rebuf_time * play_duration_weight
                    self.play_time += cdn_rebuf_time * play_duration_weight
                    rebuf = 0
                # not enough .let the client buffering
                else:
                    self.buffer_size = 0
                    self.play_time += self.buffer_size
                    rebuf = cdn_rebuf_time  - (self.buffer_size / play_duration_weight)
                    self.buffer_status = True
            # calculate the play time , the real time ,the latency
                # the normal play the frame
                if self.skip_flag and self.play_time_counter >= self.skip_time:
                    self.play_time_counter += skip_add_frame
                    self.play_time = self.play_time_counter * CHUNK_TIME_LEN
                    self.skip_flag = False
                    #print("---------------caolelelele--------------------------")
                else:
                    self.play_time_counter = int(self.play_time/CHUNK_TIME_LEN)

                self.latency = self.time - self.cdn_arrive_time[quality][self.play_time_counter]
                self.time = self.cdn_arrive_time[quality][self.video_chunk_counter]
                # Debug info 
                #print("%.4f"%self.time ,"  cdn", "%4f"%cdn_rebuf_time, "~rebuf~~", "%.3f"%rebuf,"~dur~~","%.4f"%duration,"~delay~","%.4f"%(cdn_rebuf_time),"~id!", self.video_chunk_counter,  "---buffer--- ", "%4f"%self.buffer_size, "%.4f--play"%self.play_time ,self.play_time_counter,"%4f--latency--"%self.latency,"000")
                if Debug:
                    self.log_file.write(  "time %.4f\t"%self.time +  
                                      "cdn %.4f\t"%cdn_rebuf_time + 
                                      "rebuf %.3f\t"%rebuf  + 
                                      "dur %.4f\t"%duration + 
                                      "delay %.4f\t"%cdn_rebuf_time +
                                      "id %d\t"%self.video_chunk_counter + 
                                      "buffer %.4f\t"%self.buffer_size  +
                                      "play_time %.4f\t"%self.play_time + 
                                      "play_id %.4f\t"%self.play_time_counter + 
                                      "latency %.4f\t"%self.latency + "000\n")
                # Return the loop
                return  duration, video_frame_size, CHUNK_TIME_LEN, rebuf, self.buffer_size, rtt, self.latency ,self.decision, self.buffer_status, end_of_video
            else:
                self.time = self.cdn_arrive_time[quality][self.video_chunk_counter]
       
        # If the CDN can get the frame:
        if int(self.time / 0.5) >= len(self.cooked_bw):
            end_of_video = True
        else:
            throughput = self.cooked_bw[int(self.time / 0.5)]  * B_IN_MB
            rtt        = self.cooked_rtt[int(self.time / 0.5)]
            duration = float(video_frame_size / throughput)

        # If the the frame is the Gop end ,next will be the next I frame
        if self.gop_flag[quality][self.video_chunk_counter] == 1:
            self.decision = True 
        # If the buffering
        if self.buffer_status and not end_of_video:
            # let the buffer_size to expand to the target_buffer
            if self.buffer_size < target_buffer:
                rebuf = duration
                self.buffer_size += self.gop_time_len[quality][self.video_chunk_counter]
                self.video_chunk_counter += 1 
                self.time += duration
            # if the buffer is enough
            else:
                self.buffer_status = False
            # calculate the play time , the real time ,the latency
            self.play_time_counter = int(self.play_time/CHUNK_TIME_LEN) 
            self.latency = self.time - self.cdn_arrive_time[quality][self.play_time_counter]
            # Debug Info
            if self.latency > latency_threshold and not self.skip_flag:
                self.skip_flag = True
                self.skip_time = self.video_chunk_counter
                self.video_chunk_counter += skip_add_frame
                #print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww1", self.skip_time)
            else:
                self.video_chunk_counter += 1
            #print("%.4f"%self.time ,"  cdn", "%4f"%cdn_rebuf_time, "~rebuf~~", "%.3f"%rebuf,"~dur~~","%.4f"%duration,"~delay~","%.4f"%(duration),"~id!", self.video_chunk_counter,  "---buffer--- ", "%4f"%self.buffer_size,  "%.4f--play"%self.play_time ,self.play_time_counter ,"%4f--latency--"%self.latency,"111")
            
            if Debug:
                 self.log_file.write(  "time %.4f\t"%self.time +  
                                      "cdn %.4f\t"%cdn_rebuf_time + 
                                      "rebuf %.3f\t"%rebuf  + 
                                      "dur %.4f\t"%duration + 
                                      "delay %.4f\t"%cdn_rebuf_time +
                                      "id %d\t"%self.video_chunk_counter + 
                                      "buffer %.4f\t"%self.buffer_size  +
                                      "play_time %.4f\t"%self.play_time + 
                                      "play_id %.4f\t"%self.play_time_counter + 
                                      "latency %.4f\t"%self.latency + "111\n")
            # Return the loop
            return  duration, video_frame_size, CHUNK_TIME_LEN, rebuf, self.buffer_size, rtt, self.latency ,self.decision, self.buffer_status, end_of_video
        # If not buffering
        elif not end_of_video: 
            # the normal loop
            # the buffer is enough
            if self.buffer_size > duration * play_duration_weight:
                self.buffer_size -= duration * play_duration_weight
                self.play_time += duration * play_duration_weight 
                rebuf = 0
            # the buffer not enough
            else:
                self.buffer_size = 0
                self.play_time += self.buffer_size
                rebuf = duration  - (self.buffer_size / play_duration_weight)
                self.buffer_status = True
            # the normal play the frame
            if self.skip_flag and self.play_time_counter >= self.skip_time:
                self.play_time_counter += skip_add_frame
                self.play_time = self.play_time_counter * CHUNK_TIME_LEN
                self.skip_flag = False
                #print("----------------------------------------kale lalla---------------------------------------")
            else:
                self.play_time_counter = int(self.play_time/CHUNK_TIME_LEN) 
            self.latency = self.time - self.cdn_arrive_time[quality][self.play_time_counter]
            #print("%.4f"%self.time ,"  cdn", "%4f"%cdn_rebuf_time, "~rebuf~~", "%.3f"%rebuf,"~dur~~","%.4f"%duration,"~delay~","%.4f"%(duration * play_duration_weight),"~id!", self.video_chunk_counter,  "---buffer--- ", "%4f"%self.buffer_size, "%.4f--play--"%self.play_time ,self.play_time_counter,"%4f--latency--"%self.latency,"2222")
            if Debug:
                 self.log_file.write(  "time %.4f\t"%self.time +  
                                      "cdn %.4f\t"%cdn_rebuf_time + 
                                      "rebuf %.3f\t"%rebuf  + 
                                      "dur %.4f\t"%duration + 
                                      "delay %.4f\t"%cdn_rebuf_time +
                                      "id %d\t"%self.video_chunk_counter + 
                                      "buffer %.4f\t"%self.buffer_size  +
                                      "play_time %.4f\t"%self.play_time + 
                                      "play_id %.4f\t"%self.play_time_counter + 
                                      "latency %.4f\t"%self.latency + "222\n")
            #play add the time
            self.buffer_size += self.gop_time_len[quality][self.video_chunk_counter]
            self.time += duration
            if self.latency > latency_threshold and not self.skip_flag:
                self.skip_flag = True
                self.skip_time = self.video_chunk_counter
                self.video_chunk_counter += skip_add_frame
                #print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww2", self.skip_time)
            else:
                self.video_chunk_counter += 1
            #return loop
            return  duration, video_frame_size, CHUNK_TIME_LEN, rebuf, self.buffer_size, rtt, self.latency ,self.decision, False, end_of_video
        # if the video is end
        if self.video_chunk_counter >= TOTAL_VIDEO_CHUNCK or end_of_video:
            self.time = 0
            self.play_time = 0
            self.play_time_counter = 0

            self.video_chunk_counter = 0
            self.buffer_size = 0

            # pick a random trace file
            self.trace_idx = np.random.randint(len(self.all_cooked_time))
            self.cooked_time = self.all_cooked_time[self.trace_idx]
            self.cooked_bw = self.all_cooked_bw[self.trace_idx]
            self.cooked_rtt = self.all_cooked_rtt[self.trace_idx]
       
            self.decision = False
            self.buffer_status = True
            self.skip_flag = False
            self.skip_time = 100000

            self.video_size = {}  # in bytes
            self.cdn_arrive_time = {}
            self.gop_time_len = {}
            self.gop_flag = {}
            f = open("./time_variance")
            time_lines = f.readlines()
            f.close()
            random_id = random.randint(0,1000)
            for bitrate in xrange(BITRATE_LEVELS):
                self.video_size[bitrate] = []
                self.cdn_arrive_time[bitrate] = []
                self.gop_time_len[bitrate] = []
                self.gop_flag[bitrate] = []
                cnt = 0
                with open(self.video_size_file + str(bitrate)) as f:
                    for line in f:
                    #print(line.split(), bitrate)
                        self.video_size[bitrate].append(int(float(line.split()[0])))
                        self.gop_time_len[bitrate].append(0.04)
                        self.gop_flag[bitrate].append(int(float(line.split()[1])))
                        if cnt == 0:
                            self.cdn_arrive_time[bitrate].append(0)
                        else:
                        #self.cdn_arrive_time[bitrate].append(sum(self.gop_time_len[bitrate]) + self.gop_time_len[bitrate][cnt-1] + float(time_lines[(random_id + cnt) % 1000 ]))
                            self.cdn_arrive_time[bitrate].append(self.cdn_arrive_time[bitrate][cnt-1] + self.gop_time_len[bitrate][cnt-1])
                        cnt += 1
            random_id = random.randint(0,1000)
            for idx in range(len(self.cdn_arrive_time[0])):
                random_loss = float(time_lines[(random_id + idx) % 1000 ])
                for bitrate in range(BITRATE_LEVELS):
                    self.cdn_arrive_time[bitrate][idx] += random_loss
            self.gop_remain = self.video_size[default_quality][0]
            self.latency = self.gop_time_len[0][0] 
            return  duration, video_frame_size, CHUNK_TIME_LEN, rebuf, self.buffer_size, rtt, self.latency ,self.decision, self.buffer_status, end_of_video
