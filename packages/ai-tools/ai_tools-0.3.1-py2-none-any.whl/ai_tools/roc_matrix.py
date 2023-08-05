#encoding=UTF-8
import os
import cv2
import xml.etree.ElementTree as ET
import shutil
import pdb
from zprint import *
#解析XML文件
def parse_rec_xml(filename_path):
    
    tree = ET.parse(filename_path)
    xml_info = {}
    xml_info['img_name'] = tree.find('filename').text
    xml_info['size'] = {}
    xml_info['size']['width'] = tree.find('size').find('width').text
    xml_info['size']['height'] = tree.find('size').find('height').text
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['R_L'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    xml_info['bbox_info'] = objects
    #return xml_info
    bbox_infos =  xml_info['bbox_info']
    return bbox_infos

#解析TXT文件
def parse_rec_txt(filename_path):
    
    f = open(filename_path)
    txt_info_list = f.readlines()
    f.close()
    txt_info = {}
    for txt_line in txt_info_list:
        txt_line_info = txt_line.strip('\n').split('\t')
        txt_line_value = txt_line_info[2].split(' ')
        txt_info['img_name'] = txt_line_info[0]
        txt_info['rec_num'] = txt_line_info[1]
        objects = []
        for i in range(int(txt_line_info[1])):
            rec_struct = {}
            rec_struct['rank'] = str(i)
            coor_1 = 5 * i
            rec_struct['bbox'] = [float(txt_line_value[coor_1+0]),
                                  float(txt_line_value[coor_1+1]),
                                  float(txt_line_value[coor_1+2]),
                                  float(txt_line_value[coor_1+3])]
            rec_struct['score'] = float(txt_line_value[coor_1+4])
            objects.append(rec_struct)
        txt_info['bbox_info'] = objects
    #return txt_info
    txt_infos = txt_info['bbox_info']
    return txt_infos

#求取重叠率。
def hasOverlap(groud_bbox, pre_bbox):
    if len(pre_bbox) == 0:
        return 0
    else:
        ixmin = max(groud_bbox[0], pre_bbox[0])
        iymin = max(groud_bbox[1], pre_bbox[1])
        ixmax = min(groud_bbox[2], pre_bbox[2])
        iymax = min(groud_bbox[3], pre_bbox[3])
        iw = max(ixmax - ixmin + 1., 0.)    #与0做比较
        ih = max(iymax - iymin + 1., 0.)
        inters = iw * ih                           #重叠面积
        # union  并集
        union = ((pre_bbox[2] - pre_bbox[0] + 1.) * (pre_bbox[3] - pre_bbox[1] + 1.) +
               (groud_bbox[2] - groud_bbox[0] + 1.) *
               (groud_bbox[3] - groud_bbox[1] + 1.) - inters)
        overlaps = inters / union
    return overlaps

def get_goal_name(goal_path):
    name_list = []
    for goal_name in os.listdir(goal_path):
        name = goal_name.split('.')[0] + '.' + goal_name.split('.')[1]
        name_list.append(name)
    return name_list

def get_rect(dir_path, file_name, file_type):
    if file_type ==1:
       file_path = os.path.join(dir_path, file_name + '.xml')
       if os.path.isfile(file_path):
          rect_info = parse_rec_xml(file_path)                # parse xml
       else:
          rect_info = []
    else:
       file_path = os.path.join(dir_path, file_name + '.txt')
       if os.path.isfile(file_path):
          rect_info = parse_rec_txt(file_path)                # parse txt
       else:
          rect_info = []
    return rect_info
        
def match_pre_gt(Prect, gt_rect):
    iou_v = 0
    k = 0
    for i in range(len(gt_rect)):
        iou = hasOverlap(gt_rect[i - k]['bbox'], Prect['bbox'])
        if iou > 0.5:
           del gt_rect[i - k]
           k = k +1 
           iou_v = iou
    return iou_v , gt_rect 
           
def judge_pre_gt(gt_rect, pre_rect, pos, roc_matrix):
    pos = pos + len(gt_rect)
    for Prect in pre_rect:
        iou_v, gt_rect = match_pre_gt(Prect, gt_rect)
        if iou_v > 0.5:
           roc_matrix.append([1, 0, Prect['score']])
        else:
           roc_matrix.append([0, 1, Prect['score']])
    return pos, roc_matrix
    
def get_RocMatrix_and_PosNum(gt_file_path, pre_file_path, gt_type, pre_type):
    gt_name_list = get_goal_name(gt_file_path)      
    pre_name_list = get_goal_name(pre_file_path)    
    gt_name_set = set(gt_name_list)
    pre_name_set = set(pre_name_list)
    gt_pre_name_set = gt_name_set | pre_name_set
    gt_pre_name_list = list(gt_pre_name_set)         
    pos = 0
    roc_matrix = []
    for i in range(len(gt_pre_name_list)):
        gt_rect = get_rect(gt_file_path, gt_pre_name_list[i], gt_type)
        pre_rect = get_rect(pre_file_path, gt_pre_name_list[i], pre_type)
        pos, roc_matrix = judge_pre_gt(gt_rect, pre_rect, pos, roc_matrix)
    return roc_matrix,pos

def get_roc_matrix(gt_path,pre_path):
    
    return get_RocMatrix_and_PosNum(gt_path, pre_path, 1, 0)


if __name__=="__main__":
    path = '/data1/llz/work/hand_llz/'
    gt_merge_path = os.path.join(path, '101968001_gt/')
    pre_merge_path = os.path.join(path, '101968001_pre/')
    
    roc_m,pos_num = get_RocMatrix_and_PosNum(gt_merge_path, pre_merge_path, 1, 0)
    
    zprint("%r,%r"%(pos_num, roc_m)) 
    zprint("%r,%r"%(pos_num, len(roc_m)))
