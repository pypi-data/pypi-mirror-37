# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 09:14:05 2018

@author: yifal
"""

#%matplotlib notebook
from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.utils.data
from torch.autograd import Variable
import skimage
import skimage.io
import skimage.transform
import numpy as np
import time 
from PSMNet2.models import stackhourglass
from PSMNet2.utils import preprocess
import cv2

processed = preprocess.get_transform(augment=False)

MAXDISP = 192
torch.cuda.manual_seed(10)
model = stackhourglass(MAXDISP)

model = nn.DataParallel(model, device_ids=[0])
model.cuda()


def load_model(model_file):
    state_dict = torch.load(model_file)
    model.load_state_dict(state_dict['state_dict'])
    print('Number of model parameters: {}'.format(sum([p.data.nelement() for p in model.parameters()])))


def test(imgL,imgR):
    model.eval()

    imgL = torch.FloatTensor(imgL).cuda()
    imgR = torch.FloatTensor(imgR).cuda()     

    imgL, imgR= Variable(imgL), Variable(imgR)

    with torch.no_grad():
        output = model(imgL,imgR)
    output = torch.squeeze(output)
    pred_disp = output.data.cpu().numpy()

    return pred_disp


def calculate_disparity(imgL,imgR):
    load_model('pretrained_model_KITTI2015.tar')
    imgL_o = (skimage.io.imread(imgL).astype('float32'))
    imgR_o = (skimage.io.imread(imgR).astype('float32'))
    
    imgL = processed(imgL_o).numpy()
    imgR = processed(imgR_o).numpy()
    imgL = np.reshape(imgL,[1,3,imgL.shape[1],imgL.shape[2]])
    imgR = np.reshape(imgR,[1,3,imgR.shape[1],imgR.shape[2]])
    
    pad_row = imgL_o.shape[0] + 32 - (imgL_o.shape[0] % 32)
    pad_col = imgL_o.shape[1] + 32 - (imgL_o.shape[1] % 32) 
    
    top_pad = pad_row-imgL.shape[2]
    left_pad = pad_col-imgL.shape[3]
    imgL = np.lib.pad(imgL,((0,0),(0,0),(top_pad,0),(0,left_pad)),mode='constant',constant_values=0)
    imgR = np.lib.pad(imgR,((0,0),(0,0),(top_pad,0),(0,left_pad)),mode='constant',constant_values=0)

    start_time = time.time()
    pred_disp = test(imgL,imgR)
    print('time = %.2f' %(time.time() - start_time))
    
    top_pad   = pad_row-imgL_o.shape[0]
    left_pad  = pad_col-imgL_o.shape[1]
    img = pred_disp[top_pad:,:-left_pad]
    
    return img

def correct_img(imgR,disparity_img):
    imgR_o = (skimage.io.imread(imgR).astype('float32'))
    
    y,x = np.mgrid[0:imgR_o.shape[0],0:imgR_o.shape[1]]
    map_y = y.astype(np.float32)
    map_x = np.array(x - disparity_img,dtype=np.float32)
    corrected_imgR = cv2.remap(imgR_o,map_x,map_y,cv2.INTER_LINEAR)
    
    return corrected_imgR
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    