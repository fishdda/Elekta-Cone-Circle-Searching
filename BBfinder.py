import os
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import pydicom as dicom

def read_file():
    '''
       You need to put the pic files into the fixed file path, now 
       only two file formats could be supported(.his file and .dcm file)
       Input: path storing files
       Output: image file array(n,row,colum) 
    '''
    path = os.getcwd()
    list_file = os.listdir(os.path.join(path,'Cone'))   
    flag = list_file[0].split('.')   
    
    if flag[1].lower() == 'dcm':        
        img_data = []
        for item in list_file:
            img = dicom.read_file(os.path.join(path,'Cone',item),force=True)
            img_data.append(img)
        img_data = np.stack([s.pixel_array for s in img_data])

        for i in range(len(list_file)):
            min_ = np.min(img_data[i,])
            max_ = np.max(img_data[i,])
            img_data[i,] = (img_data[i,]-min_)/(max_-min_)*255
        img_data = img_data.astype('uint8') ## To make sure the pic is 8 bit to avoid the error in circles
        
        return img_data
            
    elif flag[1].lower() == 'his':
        img_data = np.ones([len(list_file),1024,1024])
        for i in range(len(list_file)):
            pic = open(os.path.join(path,'Cone',list_file[i]),'rb')
            line = pic.readlines()
            raw_data = b''
            for item in line:raw_data+=item
            data = np.fromstring(raw_data, dtype='uint16')
            img_data[i] = data[50:].reshape((1024,1024))
    
        for i in range(len(list_file)):
            min_ = np.min(img_data[i,])
            max_ = np.max(img_data[i,])
            img_data[i,] = (img_data[i,]-min_)/(max_-min_)*255
        img_data = img_data.astype('uint8') ## To make sure the pic is 8 bit to avoid the error in circles
        
        return img_data


def Enter_Inf():
    '''
       Please enter the necessary information of Cone and BB ball.
    '''
    # Direction = input('Please enter the order of Gantry Angles:\n')
    # Ball_Size = input('Please enter the BB Ball Size(mm):\n')
    # Cone_Size = input('Please enter the Cone Size(mm):\n')
    Ball_Size = 4
    Cone_Size = 10
    
    print('Ball Radius: {} mm; Cone Radius: {} mm'.format(float(Ball_Size)/2.0,
          float(Cone_Size)/2.0))
    print('Pixel_Size:{}'.format(round(260.0/1024.0,4)))
    
    Pixel_Size = round(260.0/1024.0,4)    
    max_in_radius = math.ceil(round(float(Ball_Size)/2.0/Pixel_Size,2)+2)
    max_out_radius = math.ceil(round(float(Cone_Size)/2.0/Pixel_Size,2)+10)
    
    print('Ball Size Pixels:{}; Cone Size Pixels:{}'.format(max_in_radius,
                                                            max_out_radius))
    
    return Pixel_Size,max_in_radius,max_out_radius

def Find_Circles(img,IR,OR,RS):
    '''
       HoughTransformation Algorithm to find the circles.
    '''
    p2_in = 10
    p2_out = 20
    p1_in = range(p2_in,p2_in+20,2)
    p1_out = range(p2_in,p2_in+30,3)
    cir_in,cir_out,cir_in_,cir_out_ = {},{},{},{}
    cir_error = []
    for j in range(img.shape[0]):
        cir_in[j],cir_out[j] = [],[]
        ## Finding Circles ##
        for ii in p1_in:
            in_ = cv2.HoughCircles(img[j],cv2.HOUGH_GRADIENT,1,minDist = 0.000001,
        param1=ii,param2=p2_in,minRadius=IR-5,maxRadius=IR+5)
            if in_ is None:
                print ('The Threshold is a mistake!!')
                in_ = np.array([[[0.0,0.0,0.0]]])
            else:
                print('The {}th in_cirlces:{}'.format(j,in_))

            cir_in[j].append(in_)

        for i in p1_out:
            out_ = cv2.HoughCircles(img[j],cv2.HOUGH_GRADIENT,1,minDist = 100000,
        param1=i,param2=p2_out,minRadius=OR-10,maxRadius=OR+10)
            if out_ is None:
                print ('The Threshold is a mistake!!')
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

    for i in range(img.shape[0]):
            cv2.circle(img[i],(cir_in_[i][0][0],cir_in_[i][0][1]),
                       cir_in_[i][0][2],(0,255,255),1)
            cv2.circle(img[i],(cir_out_[i][0][0],cir_out_[i][0][1]),
                       cir_out_[i][0][2],(0,0,255),1)
            cv2.circle(img[i],(cir_out_[i][0][0],cir_out_[i][0][1]),
                       2,(0,255,0),1)

    for i,j in zip(cir_in_,cir_out_):
            cir_error.append((RS*(float(cir_in_[i][0][0])-float(cir_out_[j][0][0])),
                              RS*(float(cir_in_[i][0][1])-float(cir_out_[j][0][1]))))

    
    return img,cir_in_,cir_out_,cir_error


def Plot_IMG(test_img,cir_error,D,SD):
    '''
       To plot the image.
    '''
    path = os.getcwd()
    set_x,set_y = 480-50,550+50
    gantry = [180,-90,0,90]
    plt.figure(figsize=(15,10))
    for i in range(test_img.shape[0]):
        plt.subplot(241+i)
        plt.imshow(test_img[i,set_x:set_y,set_x:set_y])
        plt.xlabel('{}th Horizontal:{} mm\nVertical:{} mm \n Gantry Angle:{}'.format(i+1,
                    cir_error[i][0],cir_error[i][1],gantry[i]))
    plt.annotate("DX:{}mm,DY:{}mm,DZ:{}mm\n SDX:{}mm,SDY:{}mm,SDZ:{}mm\n".format(D[0],
                        D[1],D[2],SD[0],SD[1],SD[2]), (65,20))
    plt.savefig(os.path.join(path,'results.png'))
    plt.show()

def Modify_Cal(cir_error):
    Y_err,X_err,Z_err = [],[],[]

    Gantry = [180,-90,0,90]
    cir_err = []
    for i in range(len(cir_error)):
        cir_err.append((Gantry[i],cir_error[i]))
        
    for item in cir_err:
        Y_err.append(-item[1][1])
        if item[0] == 180:
            X_err.append(-item[1][0])
        if item[0] == 0:
            X_err.append(item[1][0])
        if item[0] == -90:
            Z_err.append(-item[1][0])
        if item[0] == 90:
            Z_err.append(item[1][0])
    
    D_Y = round(np.mean(np.array(Y_err)),2)
    D_X = round(np.mean(np.array(X_err)),2)
    D_Z = round(np.mean(np.array(Z_err)),2)
    SD_Y = round(np.std(np.array(Y_err)),2)
    SD_X = round(np.std(np.array(X_err)),2)
    SD_Z = round(np.std(np.array(Z_err)),2)
    
    print ('Dx:{}mm, Dy:{}mm, Dz:{}mm \n'.format(D_X,D_Y,D_Z))
    print ('SDx:{}mm, SDy:{}mm, SDz:{}mm \n'.format(SD_X,SD_Y,SD_Z))

    return (D_X,D_Y,D_Z),(SD_X,SD_Y,SD_Z)


def main():

    ## Load image file ##    

    img = read_file()
    
    ## Enter information ##
    RS,IR,OR = Enter_Inf()
    
    ## Finding the IsoCenter ##
    test_img,cir_in,cir_out,cir_error = Find_Circles(img,IR,OR,RS)
    
    ## Calculation of Modification ##
    D,SD = Modify_Cal(cir_error)
    
    ## Plot the results ##
    Plot_IMG(test_img,cir_error,D,SD)

if __name__ == '__main__':
    main()



        



