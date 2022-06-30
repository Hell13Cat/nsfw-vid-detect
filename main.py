import PIL.Image as Image
from nsfw_detector import predict
import cv2
import os
import json
import html_create

def save_frame(screen_folder, secs, vid):
    save_name = screen_folder + "/" + str(secs) + ".jpg"
    fps = vid.get(cv2.CAP_PROP_FPS)
    vid.set(cv2.CAP_PROP_POS_FRAMES, fps*secs)
    ret, frame = vid.read()
    cv2.imwrite(save_name, frame)
    return save_name

model = predict.load_model('./data/model/nsfw_mobilenet2.224x224.h5')
file_path = "./data/vids/example.mp4"
vid = cv2.VideoCapture( file_path )
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH) 
fps = vid.get(cv2.CAP_PROP_FPS)
totalNoFrames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
durationInSeconds = float(totalNoFrames) / float(fps)
datas = {"height":height, "width":width, "duration":durationInSeconds}
print(height, width, durationInSeconds)
screen_folder = "data/screen/" + file_path.split("/")[-1]
try:
    if not os.path.exists(screen_folder):
        os.makedirs(screen_folder)
except OSError:
    print('Error: Creating directory of data')
save_frame(screen_folder, 1, vid)
current_sec = 1
datas_frames = {}
while True:
    if current_sec < durationInSeconds:  
        file_name = save_frame(screen_folder, current_sec, vid)
        image = Image.open(file_name)
        data_res = predict.classify(model, file_name)
        data_one = data_res[list(data_res.keys())[0]]
        data_one["file"] = file_name.replace("data/", "", 1)
        datas_frames[str(current_sec)] = data_one
    else:
        break
    current_sec += 5
datas["frames"] = datas_frames
json.dump(datas, open("data/json/"+file_path.split("/")[-1]+".json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
html_create.create(file_path.split("/")[-1])