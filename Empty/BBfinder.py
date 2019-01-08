import os
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import pydicom as dicom
from matplotlib.patches import Circle
def Read_File(filename):

    flag = filename[0].split('.')   
    
    if flag[1].lower() == 'dcm':        
        img_data = []
        for item in filename:
            img = dicom.read_file(item,force=True)
            img_data.append(img)
        img_data = np.stack([s.pixel_array for s in img_data])

        for i in range(len(filename)):
            min_ = np.min(img_data[i,])
            max_ = np.max(img_data[i,])
            img_data[i,] = (img_data[i,]-min_)/(max_-min_)*255
        img_data = img_data.astype('uint8') ## To make sure the pic is 8 bit to avoid the error in circles
        
        return img_data
            
    elif flag[1].lower() == 'his':
        img_data = np.ones([len(filename),1024,1024])
        for i in range(len(filename)):
            pic = open(filename[i],'rb')
            line = pic.readlines()
            raw_data = b''
            for item in line:raw_data+=item
            data = np.fromstring(raw_data, dtype='uint16')
            img_data[i] = data[50:].reshape((1024,1024))
    
        for i in range(len(filename)):
            min_ = np.min(img_data[i,])
            max_ = np.max(img_data[i,])
            img_data[i,] = (img_data[i,]-min_)/(max_-min_)*255
        img_data = img_data.astype('uint8') ## To make sure the pic is 8 bit to avoid the error in circles
        
        return img_data


def Enter_Inf():
    '''
       Please enter the necessary information of Cone and BB ball.
    '''
    Ball_Size = 8
    Cone_Size = 15
    
    print('Ball Radius: {} mm; Cone Radius: {} mm'.format(float(Ball_Size)/2.0,
          float(Cone_Size)/2.0))
    print('Pixel_Size:{}'.format(round(260.0/1024.0,4)))
    
    Pixel_Size = round(260.0/1024.0,4)    
    max_in_radius = math.ceil(round(float(Ball_Size)/2.0/Pixel_Size,2))
    max_out_radius = math.ceil(round(float(Cone_Size)/2.0/Pixel_Size,2))
    
    print('Ball Size Pixels:{}; Cone Size Pixels:{}'.format(max_in_radius,
                                                            max_out_radius))
    
    return Pixel_Size,max_in_radius,max_out_radius


def Find_Circles(img,IR,OR,RS):
    '''
       HoughTransformation Algorithm to find the circles.
    '''
    p2_in,p2_out = 15,20
    p1_in = range(p2_in,p2_in+10,2)
    p1_out = range(p2_in,p2_in+20,2)
    cir_in,cir_out,cir_in_,cir_out_ = {},{},{},{}
    cir_error = []

    for j in range(img.shape[0]):
        cir_in[j],cir_out[j] = [],[]
        ## Finding Circles ##
        for ii in p1_in:
            in_ = cv2.HoughCircles(img[j],cv2.HOUGH_GRADIENT,1.15,minDist = 0.000001,
        param1=ii,param2=p2_in,minRadius=IR-5,maxRadius=IR)
            if in_ is None:
                #print ('The Threshold is a mistake!!')
                in_ = np.array([[[0.0,0.0,0.0]]])
            else:
                print('The {}th in_cirlces:{}'.format(j,in_))

            cir_in[j].append(in_)

        for i in p1_out:
            out_ = cv2.HoughCircles(img[j],cv2.HOUGH_GRADIENT,1,minDist = 100000,
        param1=i,param2=p2_out,minRadius=OR-5,maxRadius=OR+5)
            if out_ is None:
                #print ('The Threshold is a mistake!!')
                out_ = np.array([[[0.0,0.0,0.0]]])
            else:
                print('The {}th out_cirlces:{}'.format(j,out_))

            cir_out[j].append(out_)
            
        ## Cleaning the data ##
        for item in enumerate(cir_in[j]):
            if item[1].shape[1] == 1:
                # this means only one circle
                cir_in[j][item[0]] = (item[1][0][0][0],item[1][0][0][1],
                                      item[1][0][0][2])
            else:
                # this means more than one circles
                kk = np.abs(item[1] - np.array([0,0,IR]))
                flag = np.where(kk == np.min(kk))
                print(flag[1])
                cir_in[j][item[0]] = (cir_in[j][item[0]][0][flag[1][0]][0],
                                      cir_in[j][item[0]][0][flag[1][0]][1],
                                      cir_in[j][item[0]][0][flag[1][0]][2])

        for item in enumerate(cir_out[j]):
            if item[1].shape[1] == 1:
                # this means only one circle
                cir_out[j][item[0]] = (item[1][0][0][0],item[1][0][0][1],
                                      item[1][0][0][2])
            else:
                # this means more than one circles
                kk = np.abs(item[1] - np.array([0,0,OR]))
                flag = np.where(kk == np.min(kk))
                print(flag[1])
                cir_out[j][item[0]] = (cir_out[j][item[0]][0][flag[1][0]][0],
                                      cir_out[j][item[0]][0][flag[1][0]][1],
                                      cir_out[j][item[0]][0][flag[1][0]][2])

    for key in cir_in.keys():
             cir_in_[key] = list(set(cir_in[key]))
             cir_out_[key] = list(set(cir_out[key]))

    for key,value in cir_in_.items():
        
        if len(value) > 1:
            cir_in_[key] = [value[0]]
            cir_out_[key] = [cir_out_[key][0]]
        else:
            pass

    for i,j in zip(cir_in_,cir_out_):
            cir_error.append((round(RS*(float(cir_in_[i][0][0])-float(cir_out_[j][0][0])),4),
                              round(RS*(float(cir_in_[i][0][1])-float(cir_out_[j][0][1])),4)))


    for i,item in enumerate(cir_error):
        print('X{0},Y{1}:{2}'.format(i,i,item))
        
    return img,cir_in_,cir_out_,cir_error


def Modify_Cal(cir_error):
    Y_err,X_err,Z_err = [],[],[]

    Gantry = [180,-90,0,90]
    cir_err = []
    for i in range(len(cir_error)):
        cir_err.append((Gantry[i],cir_error[i]))
        
    for item in cir_err:
        Y_err.append(item[1][1])
        if item[0] == 180:
            X_err.append(item[1][0])
        if item[0] == 0:
            X_err.append(item[1][0])
        if item[0] == -90:
            Z_err.append(item[1][0])
        if item[0] == 90:
            Z_err.append(item[1][0])
    
    D_Y = -round(np.mean(np.array(Y_err)),2)
    D_X = round((X_err[0] - X_err[1])/2,2)
    D_Z = round((Z_err[1] - Z_err[0])/2,2)
    SD_Y = round(np.std(np.array(Y_err)),2)
    SD_X = round(np.std(np.array(X_err)),2)
    SD_Z = round(np.std(np.array(Z_err)),2)
    print ('X_err:{},Y_err:{},Z_err:{}'.format(X_err,Y_err,Z_err))
    print ('Dx:{}mm, Dy:{}mm, Dz:{}mm \n'.format(D_X,D_Y,D_Z))
    print ('SDx:{}mm, SDy:{}mm, SDz:{}mm \n'.format(SD_X,SD_Y,SD_Z))

    return (D_X,D_Y,D_Z),(SD_X,SD_Y,SD_Z)


def Plot(test_img,cir_in,cir_out,cir_error):

	gantry = [180,-90,0,90]
	f = plt.figure(figsize=(15,5))
	f.dpi = 100
	for i in range(test_img.shape[0]):  
		ax = f.add_subplot(241+i)
		# Show the image
		ax.imshow(test_img[i,400:630,400:630],'gray')
		# Add the circle
		ax.scatter(cir_in[i][0][0]-400,cir_in[i][0][1]-400, c="r",marker = '*', s=4)
		ax.scatter(cir_out[i][0][0]-400,cir_out[i][0][1]-400, c="g",marker = '*', s=4)
		circ1 = Circle((cir_in[i][0][0]-400,cir_in[i][0][1]-400),
		              cir_in[i][0][2],color='r', linewidth=1, fill=False)
		ax.add_patch(circ1)
		circ2 = Circle((cir_out[i][0][0]-400,cir_out[i][0][1]-400),
		              cir_out[i][0][2],color='g', linewidth=1, fill=False)
		ax.add_patch(circ2)
		ax.set_xlabel('{}th Horizontal(X):{} mm\nVertical(Y):{} mm \n '.format(i+1,cir_error[i][0],cir_error[i][1]))
		ax.set_title('Gantry Angle:{}'.format(gantry[i]),fontsize = 20)
	plt.savefig(os.path.join(os.getcwd(),'results.png'))

	return f


