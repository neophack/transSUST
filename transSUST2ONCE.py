import json
import os
import tqdm

def trans(input, output):
    labeldir=os.path.join(input,"label")
    newannos={"meta_info": {
        "weather": "rainy",
        "period": "afternoon",
        "image_size": [
            1920,
            1020
        ],
        "point_feature_num": 4
    },
    "calib":{},"frames": []}
    sequence_id=os.path.basename(output)
    frames=[]
    if os.path.exists(labeldir):
        labels=os.listdir(labeldir)
        for i in tqdm.tqdm(range(len(labels))):
            labelfile=os.path.join(labeldir,labels[i])
            oldannos=json.load(open(labelfile, "r"))
            frame_id=labels[i].split(".")[0]
            boxes_3d=[]
            names=[]
            boxes_2d={}
            if len(oldannos)==0:
                continue
            for j in range(len(oldannos)):
                # print(oldannos[j])
                names.append(oldannos[j]["obj_type"])
                rotatez=oldannos[j]["psr"]["rotation"]["z"]
                boxes_3d.append([oldannos[j]["psr"]["position"]["x"],oldannos[j]["psr"]["position"]["y"],oldannos[j]["psr"]["position"]["z"],oldannos[j]["psr"]["scale"]["x"],oldannos[j]["psr"]["scale"]["y"],oldannos[j]["psr"]["scale"]["z"],roatez])
            frameannos={"sequence_id":sequence_id,"frame_id": frame_id, "annos":{"names":names,"boxes_3d": boxes_3d, "boxes_2d": boxes_2d},"pose":[0.,0.,0.,0.,0.,0.,0.]}
            frames.append(frameannos)
            # print(frameannos)
        newannos["frames"]=frames
        print(newannos)
    else:
        raise ValueError("Could not find label directory!")


if __name__ == "__main__":
    sequence_id=1
    input = "./data/test220126"
    output = "./data/%06d" % sequence_id
    trans(input, output)