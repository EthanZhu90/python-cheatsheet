import sys
import os
import cv2
from glob import glob 
from tqdm import tqdm 
from multiprocessing import Pool
import shutil

# root_dir = "datasets"
# vidList = glob(root_dir+ "/*/*.mp4")
# vidList = [os.path.relpath(i, root_dir) for i in vidList]
# print(len(vidList))

# res_stats = dict()
# def func(videoName):
#     vcap = cv2.VideoCapture(os.path.join(root_dir, videoName ))
#     if vcap.isOpened(): 
#         width  = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
#         height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#         return videoName, (width, height)
#     else:
#         return None, None 
#         #res_stats[videoName] = (width, height)
#         #print(res_stats)        
# pool = Pool(processes=12)
# for videoName, res in tqdm(pool.imap_unordered(func, vidList)):
#     if videoName is not None:
#         res_stats[videoName] = res
        
# pool.close()
# #print(res_stats)
# import pickle
# pickle.dump(res_stats, open("res_stats.pkl", "wb"))

import pickle
stats = pickle.load(open("res_stats.pkl", "rb"))
cnt = 1
vid2use = []
for key, values in stats.items():
    if values[0] >=480 and values[1] >=980:
        cnt +=1
        vid2use.append(key)
print(cnt)
# 31827

os.makedirs("datasets_480_980", exist_ok=True)
for vid in tqdm(vid2use):
    shutil.copy("datasets/" +vid, "datasets_480_980/"+vid.replace("/", "_"))

#hdfs dfs -put datasets_480_980.tar hdfs://harunava/home/byte_ailab_us_cvg/user/yizhe.zhu/old_picture
#hdfs dfs -get  hdfs://harunava/home/byte_ailab_us_cvg/user/yizhe.zhu/old_picture/datasets_480_980.tar
#########################
# scene split
##########################

# pip install scenedetect[opencv]
# Standard PySceneDetect imports:
from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect import video_splitter

# For content-aware scene detection:
from scenedetect.detectors import ContentDetector

def find_scenes(video_path, threshold=30.0):
    # Create our video & scene managers, then add the detector.
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))

    # Improve processing speed by downscaling before processing.
    video_manager.set_downscale_factor()

    # Start the video manager and perform the scene detection.
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    # Each returned scene is a tuple of the (start, end) timecode.
    return scene_manager.get_scene_list()


scenes = find_scenes('goldeneye.mp4')
#print(scenes)

video_splitter.split_video_mkvmerge(['goldeneye.mp4'], scenes, "$VIDEO_NAME-Scene$SCENE_NUMBER", "test_video_name")


