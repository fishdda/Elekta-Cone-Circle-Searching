import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import cv2
import math


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
            if data[50:].shape != (1048576,):
                x= data[181:]
                print(x.shape)
            else:
                x = data[50:]
                pass
            img_data[i] = x.reshape((1024,1024))
    
        for i in range(len(filename)):
            min_ = np.min(img_data[i,])
            max_ = np.max(img_data[i,])
            img_data[i,] = (img_data[i,]-min_)/(max_-min_)*255
        img_data = img_data.astype('uint8') ## To make sure the pic is 8 bit to avoid the error in circles
        
        return img_data

def Enter_Inf(Ball_Size,Cone_Size):
    '''
       Please enter the necessary information of Cone and BB ball.
    '''
    # Ball_Size = 8
    # Cone_Size = 50
    
    print('Ball Radius: {} mm; Cone Radius: {} mm'.format(float(Ball_Size)/2.0,
          float(Cone_Size)/2.0))
    print('Pixel_Size:{}'.format(round(260.0/1024.0,4)))
    
    Pixel_Size = round(260.0/1024.0,12)    
    max_in_radius = math.ceil(round(float(Ball_Size)/2.0/Pixel_Size,2))
    max_out_radius = math.ceil(round(float(Cone_Size)/2.0/Pixel_Size,2))
    
    print('Ball Size Pixels:{}; Cone Size Pixels:{}'.format(max_in_radius,
                                                            max_out_radius))
    
    return Pixel_Size,max_in_radius,max_out_radius


def Find_Circles(img,IR,OR,RS):
    '''
       HoughTransformation Algorithm to find the circles.
    '''
    p2_in,p2_out = 10,5
    p1_in = range(p2_in,p2_in+20,5)
    p1_out = range(p2_in,p2_in+15,5)
    cir_in,cir_out,cir_in_,cir_out_ = {},{},{},{}
    cir_error = []
    for j in range(img.shape[0]):
        cir_in[j],cir_out[j] = [],[]

        ## Finding Circles ##
        for ii in p1_in:
            in_ = cv2.HoughCircles(img[j],cv2.HOUGH_GRADIENT,1.123,minDist = 0.000001,
        param1=ii,param2=p2_in,minRadius=IR-5,maxRadius=IR)
            if in_ is None:
                #print ('The Threshold is a mistake!!')
                in_ = np.array([[[0.0,0.0,0.0]]])
            else:
                print('The {}th in_cirlces:{}'.format(j,in_))
                # pass

            cir_in[j].append(in_)

        for i in p1_out:
            out_ = cv2.HoughCircles(img[j],cv2.HOUGH_GRADIENT,1.12,minDist = 100000,
        param1=i,param2=p2_out,minRadius=OR-5,maxRadius=OR+3)
            if out_ is None:
                #print ('The Threshold is a mistake!!')
                out_ = np.array([[[0.0,0.0,0.0]]])
            else:
                print('The {}th out_cirlces:{}'.format(j,out_))
                # pass

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
                cir_in[j][item[0]] = (cir_in[j][item[0]][0][0][0],
                                      cir_in[j][item[0]][0][0][1],
                                      cir_in[j][item[0]][0][0][2])

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


def Plot(test_img,cir_in,cir_out,cir_error,name):
    from matplotlib.patches import Circle
    s = []
    x_axis = 380
    y_axis = 650
    for item in name:
        ss = item.split('/')
        kk = ss[-1].split('.')
        n = kk[0].split('_')
        s.append(n)
    f = plt.figure(figsize=(20,15))
    f.dpi = 100
    for i in range(test_img.shape[0]):  
        ax = f.add_subplot(241+i)
        # Show the image
        ax.imshow(test_img[i,x_axis:y_axis,x_axis:y_axis],'gray')
#         ax.set_axis_off()
        # Add the circle
        ax.scatter(cir_in[i][0][0]-x_axis,cir_in[i][0][1]-x_axis, c="r",marker = '*', s=4)
        ax.scatter(cir_out[i][0][0]-x_axis,cir_out[i][0][1]-x_axis, c="g",marker = '*', s=4)
        circ1 = Circle((cir_in[i][0][0]-x_axis,cir_in[i][0][1]-x_axis),
                      cir_in[i][0][2],color='r', linewidth=1, fill=False)
        ax.add_patch(circ1)
        circ2 = Circle((cir_out[i][0][0]-x_axis,cir_out[i][0][1]-x_axis),
                      cir_out[i][0][2],color='g', linewidth=1, fill=False)
        ax.add_patch(circ2)
        ax.set_xlabel('Horizontal(X):{} mm\n,Vertical(Y):{} mm \n '.format(cir_error[i][0],cir_error[i][1]))
        ax.set_title(s[i][0]+s[i][1],fontsize = 10)
        
#         plt.axis('off')
#     plt.savefig(os.path.join(os.getcwd(),'results.png'))

#     return f


def Axis_Proj(x1,y1,x2,y2,x3,y3,Y1,Y1_,Y2,Y2_,Y3,Y3_):
    plt.figure(figsize=(12,15))
    plt.subplot(311)
    plt.scatter(x1,y1,marker='*',color='red')
    plt.ylim(0,0.5)
    plt.xticks([-1, -0.5, 0, 0.5, 1])
    plt.vlines(Y1_, 0, 0.5, colors = "k", linestyles = "solid",linewidth=5)
    plt.vlines(Y1, 0, 0.5, colors = "g", linestyles = "dashed",linewidth=5)
    plt.vlines(0.0, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(0.5, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(-0.5, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(1, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(-1, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.xlabel('mm')
    plt.title("projection onto X axis")

    plt.subplot(312)
    plt.scatter(x2,y2,marker='*',color='red')
    plt.ylim(0,0.5)
    plt.xticks([-1, -0.5, 0, 0.5, 1])
    plt.vlines(Y2_, 0, 0.5, colors = "k", linestyles = "solid",linewidth=5)
    plt.vlines(Y2, 0, 0.5, colors = "g", linestyles = "dashed",linewidth=5)
    plt.vlines(0.0, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(0.5, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(-0.5, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(1, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(-1, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.xlabel('mm')
    plt.title("projection onto Y axis")

    plt.subplot(313)
    plt.scatter(x3,y3,marker='*',color='red')
    plt.ylim(0,0.5)
    plt.xticks([-1, -0.5, 0, 0.5, 1])
    plt.vlines(Y3_, 0, 0.5, colors = "k", linestyles = "solid",linewidth=5)
    plt.vlines(Y3, 0, 0.5, colors = "g", linestyles = "dashed",linewidth=5)
    plt.vlines(0.0, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(0.5, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(-0.5, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(1, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.vlines(-1, 0, 0.5, colors = "c", linestyles = "dashed")
    plt.xlabel('mm')
    plt.title("projection onto Z axis")


def Beam_Deviation(x,y1,y2,y3):

    z1 = np.polyfit(x, y1, 4)#用4次多项式拟合
    z2 = np.polyfit(x, y2, 4)#用4次多项式拟合
    z3 = np.polyfit(x, y3, 4)#用4次多项式拟合
    p1 = np.poly1d(z1)
    p2 = np.poly1d(z2)
    p3 = np.poly1d(z3)
    print(p1,p2,p3) #在屏幕上打印拟合多项式
    x2 = np.arange(-190, 190, 5)
    yvals1=p1(x2)#也可以使用yvals=np.polyval(z1,x)
    yvals2=p2(x2)#也可以使用yvals=np.polyval(z1,x)
    yvals3=p3(x2)#也可以使用yvals=np.polyval(z1,x)

    plt.figure(figsize=(10,8))
    plt.scatter(x,y1,marker = "o",color = 'r')
    plt.scatter(x,y2,marker = "o",color = 'g')
    plt.scatter(x,y3,marker = "o",color = 'b')
    plt.legend(['GT Deviation','AB Deviation','Total(R) Deviation'])
    plt.plot(x2,yvals1,'r')
    plt.plot(x2,yvals2,'g')
    plt.plot(x2,yvals3,'b')
    plt.grid()
    plt.xlabel('Angle')
    plt.ylabel('mm')

def table_output(file_name,cir_error):

    if len(file_name) == 8:

        Circle_Error = {i:j for i,j in zip([i.split('.')[0] for i in file_name],cir_error)}    
        Gantry_Couch = {'Gantry':[-180,-90,0,90,0,0,0,0],'Couch':[0,0,0,0,90,45,-45,-90]}
        df = pd.DataFrame(Gantry_Couch) 
        df['Vertical(mm)'] = 0
        df['Horizontal(mm)'] = 0
        mapping = {item:(item.split('_')[0].split('G')[1],item.split('_')[1].split('T')[1]) for item in Circle_Error.keys()}
        Cir_Errors = {mapping[item]:Circle_Error[item] for item in Circle_Error.keys()}
        for k,(i,j) in enumerate(zip(df['Gantry'],df['Couch'])):
            df.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][1],2), round(Cir_Errors[(str(i),str(j))][0],2)]


        
        df2 = df.copy()
        del df2['Vertical(mm)']
        del df2['Horizontal(mm)'] 
        df2['X-Proj(mm)'] = 0
        df2['Y-Proj(mm)'] = 0
        df2['Z-Proj(mm)'] = 0
        df2['GT(mm)'] = 0
        df2['AB(mm)'] = 0
        df2['R(mm)'] = 0

        for k,(i,j) in enumerate(zip(df2['Gantry'],df['Couch'])):
            if (i,j) == (-180,0):
                df2.iloc[k] = [i,j,round(-Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                               +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]
            elif (i,j) == (-90,0):
                df2.iloc[k] = [i,j,'No Projection',round(-Cir_Errors[(str(i),str(j))][1],2),round(-Cir_Errors[(str(i),str(j))][0],2),
                               round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]
            elif (i,j) == (0,0):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]  
            elif (i,j) == (90,0):
                df2.iloc[k] = [i,j,'No Projection',round(-Cir_Errors[(str(i),str(j))][1],2), round(Cir_Errors[(str(i),str(j))][0],2),
                               round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]  
            elif (i,j) == (0,90):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]    
            elif (i,j) == (0,45):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)] 
            elif (i,j) == (0,-45):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)] 
            elif (i,j) == (0,-90):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)] 

        X = np.array([item for item in df2['X-Proj(mm)'] if item != 'No Projection'])
        Y = np.array([item for item in df2['Y-Proj(mm)'] if item != 'No Projection'])
        Z = np.array([item for item in df2['Z-Proj(mm)'] if item != 'No Projection'])
        R = math.sqrt(round(np.mean(X),2)*round(np.mean(X),2)+round(np.mean(Y),2)*round(np.mean(Y),2)+round(np.mean(Z),2)*round(np.mean(Z),2))

        df3 = {'Coordinate System':['dX(mm)','dY(mm)','dZ(mm)','3D Displacement(mm)','Tolerance(mm)','Pass-Fall','SDx(mm)','SDy(mm)','SDz(mm)'],
               'Elekta Bipolar':[round(np.mean(X),2),round(np.mean(Y),2),round(np.mean(Z),2),round(R,2),1,'Pass' if round(R,2) < 1 else "Fall",
                                 round(np.std(X),2),round(np.std(Y),2),round(np.std(Z),2)]}

        df3 = pd.DataFrame(df3)

    elif len(file_name) == 4:

        Circle_Error = {i:j for i,j in zip([i.split('.')[0] for i in file_name],cir_error)}    
        Gantry_Couch = {'Gantry':[-180,-90,0,90],'Couch':[0,0,0,0]}
        df = pd.DataFrame(Gantry_Couch) 
        df['Vertical(mm)'] = 0
        df['Horizontal(mm)'] = 0
        mapping = {item:(item.split('_')[0].split('G')[1],item.split('_')[1].split('T')[1]) for item in Circle_Error.keys()}
        Cir_Errors = {mapping[item]:Circle_Error[item] for item in Circle_Error.keys()}
        for k,(i,j) in enumerate(zip(df['Gantry'],df['Couch'])):
            df.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][1],2), round(Cir_Errors[(str(i),str(j))][0],2)]


        
        df2 = df.copy()
        del df2['Vertical(mm)']
        del df2['Horizontal(mm)'] 
        df2['X-Proj(mm)'] = 0
        df2['Y-Proj(mm)'] = 0
        df2['Z-Proj(mm)'] = 0
        df2['GT(mm)'] = 0
        df2['AB(mm)'] = 0
        df2['R(mm)'] = 0

        for k,(i,j) in enumerate(zip(df2['Gantry'],df['Couch'])):
            if (i,j) == (-180,0):
                df2.iloc[k] = [i,j,round(-Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                               +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]
            elif (i,j) == (-90,0):
                df2.iloc[k] = [i,j,'No Projection',round(-Cir_Errors[(str(i),str(j))][1],2),round(-Cir_Errors[(str(i),str(j))][0],2),
                               round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]
            elif (i,j) == (0,0):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]  
            elif (i,j) == (90,0):
                df2.iloc[k] = [i,j,'No Projection',round(-Cir_Errors[(str(i),str(j))][1],2), round(Cir_Errors[(str(i),str(j))][0],2),
                               round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]  
            elif (i,j) == (0,90):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)]    
            elif (i,j) == (0,45):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)] 
            elif (i,j) == (0,-45):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)] 
            elif (i,j) == (0,-90):
                df2.iloc[k] = [i,j,round(Cir_Errors[(str(i),str(j))][0],2), round(-Cir_Errors[(str(i),str(j))][1],2),
                               'No Projection',round(Cir_Errors[(str(i),str(j))][1],2),round(Cir_Errors[(str(i),str(j))][0],2),
                              round(math.sqrt(round(Cir_Errors[(str(i),str(j))][1],2)*round(Cir_Errors[(str(i),str(j))][1],2)
                                        +round(Cir_Errors[(str(i),str(j))][0],2)*round(Cir_Errors[(str(i),str(j))][0],2)),2)] 

        X = np.array([item for item in df2['X-Proj(mm)'] if item != 'No Projection'])
        Y = np.array([item for item in df2['Y-Proj(mm)'] if item != 'No Projection'])
        Z = np.array([item for item in df2['Z-Proj(mm)'] if item != 'No Projection'])
        R = math.sqrt(round(np.mean(X),2)*round(np.mean(X),2)+round(np.mean(Y),2)*round(np.mean(Y),2)+round(np.mean(Z),2)*round(np.mean(Z),2))

        df3 = {'Coordinate System':['dX(mm)','dY(mm)','dZ(mm)','3D Displacement(mm)','Tolerance(mm)','Pass-Fall','SDx(mm)','SDy(mm)','SDz(mm)'],
               'Elekta Bipolar':[round(np.mean(X),2),round(np.mean(Y),2),round(np.mean(Z),2),round(R,2),1,'Pass' if round(R,2) < 1 else "Fall",
                                 round(np.std(X),2),round(np.std(Y),2),round(np.std(Z),2)]}

        df3 = pd.DataFrame(df3)
       

    return df,df2,df3