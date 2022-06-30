import json


def create(file_name):
    datas = json.load(open("data/json/"+file_name+".json", "r", encoding='utf-8'))
    text_no_format = open("data/templates/index.html", "r").read()
    text_f_no_format = open("data/templates/one_frame.html", "r").read()
    list_frame_id = datas["frames"].keys()
    text_f_format = ""
    for ii in list_frame_id:
        res_info=""
        for dd in datas["frames"][ii].keys():
            if dd == "file":
                pass
            else:
                res_add = dd + " : " +str(round(datas["frames"][ii][dd]*100, 2))+"<br>"
                res_info += res_add
        text_add = text_f_no_format.format(
            file_name=datas["frames"][ii]["file"],
            info_res=res_info
        )
        text_f_format += text_add
    text_format = text_no_format.format(
        file_name=file_name,
        resolution=str(round(datas["height"]))+"x"+str(round(datas["width"])),
        duration=str(round(datas["duration"], 2))+" s.",
        file_vid="vids/"+file_name,
        frame_info=text_f_format
    )
    open("data/"+file_name+".html", "w").write(text_format)