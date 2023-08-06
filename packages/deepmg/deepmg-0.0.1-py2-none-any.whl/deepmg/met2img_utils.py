"""
======================================================================================
UTILS functions: support for module of models
======================================================================================
Author: Team Integromics, ICAN, Paris, France'
date: 20/12/2017 (updated to 26/10/2018, stable version)'
'this module includes:
'1. load data: 'load_img_util'
'2. convert data to colors: 'convert_color_real_img', 'convert_bin'
'3. embedding data to images (fill up and others): 'fillup_image', 'embed_image' 
'4. naming logs: 'name_log_final
'5. set up parameters from command line: 'para_cmd'
'6. Find files based on patterns of file: find_files 
"""

#from scipy.misc import imread
import numpy as np
import os, fnmatch
import math
from optparse import OptionParser
import ConfigParser


from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input as pre_resnet50
from keras.applications.vgg16 import preprocess_input as pre_vgg16
from keras.applications.vgg19 import preprocess_input as pre_vgg19
from keras.applications.inception_v3 import  preprocess_input as pre_incep

import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt


def find_files(pattern, path):
    """ find files in path based on pattern
    Args:
        pattern (string): pattern of file
        path (string): path to look for the files
    Return 
        list of names found
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def load_img_util (num_sample,path_write,dim_img,preprocess_img,channel,mode_pre_img, pattern_img='train'):
    """ load and reading images save to data array 
    Args:
        data_dir (array): folder contains images
        pattern_img (int): the pattern names of images (eg. 'img_1.png, img_2.png,...' so pattern='img') 
        num_sample (int) : the number of images read
        dim_img: dimension of images
        preprocess_img: preprocessing images, support: vgg16, vgg19, resnet50, incep
        path_write: path to save images

    Returns:
        array
    """
    temp = []
    for i in range(0,num_sample): #load samples for learning
        image_path = os.path.join(path_write, str(pattern_img) +str("_") + str(i) +".png")               
        if dim_img==-1: #if use real img
            if channel == 4:
                #img = imread(image_path)
                #img = img.astype('float32')
                print 'waiting for fixing issues from from scipy.misc import imread'
                exit()
            elif channel == 1:
                img = image.load_img(image_path,grayscale=True)
            else:   
                img = image.load_img(image_path)
        else: #if select dimension
           
            if channel == 1:
                img = image.load_img(image_path,grayscale=True, target_size=(dim_img, dim_img))
            
            else:
                img = image.load_img(image_path,target_size=(dim_img, dim_img))

        x = image.img_to_array(img)         
        # x = preprocess_input(x)
        if preprocess_img=='vgg16':
            x = pre_vgg16(x, mode= mode_pre_img)
        elif preprocess_img=='resnet50':
            x = pre_resnet50(x, mode= mode_pre_img)
        elif preprocess_img=='vgg19':
            x = pre_vgg19(x, mode= mode_pre_img)
        elif preprocess_img=='incep':
            x = pre_incep(x)
    
        temp.append(x)      

    return np.stack(temp)
               
def convert_color_real_img(value, debug=0, type='ab', num_bin=10 ):
    """ load and reading images save to data array  (use for abundance data) to create color images
    Args:
        value (float): orginial value
        debug (int): mode of debug
        type (string): ab (abundance) or pr (presence): custom color with hex ONLY for 10 bins
    Returns:
        value of color (hex)
    """
    color_v=0   
    
    #array of 10 colors: index 0 - 10, 0: black, 10: white
    color_arry = ['#000000', '#8B0000','#FF0000','#EE4000', '#FFA500', '#FFFF00','#00CD00', '#0000FF','#00BFFF','#ADD8E6','#FFFFFF'] 
    #break = [1e-07,4e-07,1.6e-06,6.4e-06,2.56e-05,0.0001024,0.0004096,0.0016384,0.0065536]
    if type=='ab':
        if value >= 0.0065536:
            color_v='#000000'
        elif value >= 0.0016384:
            color_v='#8B0000'
        elif value >= 0.0004096:
            color_v='#FF0000'
        elif value >= 0.0001024:
            color_v='#EE4000'
        elif value >= 2.56e-05:
            color_v= '#FFA500'
        elif value >= 6.4e-06:
            color_v= '#FFFF00'
        elif value >= 1.6e-06:
            color_v= '#00CD00'
        elif value >= 4e-07:
            color_v= '#0000FF'
        elif value >= 1e-07:
            color_v= '#00BFFF'        
        elif value > 0:
            color_v=  '#ADD8E6'
        else:
            color_v= 'w'
    elif type=='pr':
        if value >0:
            color_v='black'
        else:
            color_v='w'
   
    else:
        print 'this type ' +str(type) + ' is not supported!!!'
        exit()
        
    if debug==1:
        print(value,color_v)
  #  print(value,color_v)
   # print color_arry[1]
    return color_v

def convert_bin(value, debug=0, type='ab', 
    num_bin=10, max_v=0.0065536, min_v= 1e-07, multi_coef=4, color_img=False ):
    """ load and reading images save to data array  (use for abundance data) to create images
    **notes: ONLY apply to data range 0-1
    Args:
        value (float): orginial value
        debug (int): mode of debug
        type: 'ab' (ONLY support for 10 bins) or 'pr' (2 bins- binary bins) or eqw (Equal Width Binning)
            if 'eqw' : Equal Width Binning with thresold min_v,max_v
                max_v
                min_v
        num_bin : number of bins
        min_v,max_v: range to bin
        multi_coef: use for predefinded bin ('ab')
        color_img : return hex if num_bin=10 and use color images 
    
    Return:
        float if color_img=False, hex if color_img=True
    """
    color_v=0   
    #color_arry_num = [1,0.9,0.8,0.7,0.6, 0.5,0.4,0.3, 0.2,0.1]
    color_arry = ['#000000', '#8B0000','#FF0000','#EE4000', '#FFA500', '#FFFF00','#00CD00', '#0000FF','#00BFFF','#ADD8E6','#FFFFFF'] 
   # if debug==1:        
    #    print str(value) + '_'+ str(max_v)+'_' +str(min_v)
   
    if type == 'ab':
        if value >= (min_v * math.pow(multi_coef, 8)):            
            color_v=1.0
        elif value >= (min_v * math.pow(multi_coef, 7)):
            color_v=0.9
        elif value >= (min_v * math.pow(multi_coef, 6)):
            color_v=0.8
        elif value >= (min_v * math.pow(multi_coef, 5)):
            color_v=0.7
        elif value >= (min_v * math.pow(multi_coef, 4)):
            color_v=0.6
        elif value >= (min_v * math.pow(multi_coef, 3)):
            color_v=0.5
        elif value >= (min_v * math.pow(multi_coef, 2)):
            color_v=0.4
        elif value >= (min_v * math.pow(multi_coef, 1)):
            color_v=0.3
        elif value >= min_v:
            color_v=0.2        
        elif value > 0:
            color_v=0.1
        else:
            color_v= 0
   
    elif type=='pr':
        if value>0:
            color_v=1.0
        else:
            color_v=0
   
    elif type=='eqw':    #Equal Width Binning with a thresold max_v, return color_v is the id of binbin
        #in gray scale in python: 1: white, 0: black --> near 0: dark, near 1: white
        dis_max_min = max_v - min_v     #eg. dis_max_min=0.6
        v_bin = float(dis_max_min / num_bin) #distince between 2 bins, eg. 0.06 if num_bin = 10
        
        if value >= max_v: # old: 'if value > max_v': fixed from 15h30, 7/3
            color_v = num_bin
        elif value <= min_v: # old: 'elif value < min_v or value <= 0': fixed from 15h30, 7/3
            color_v = 0       
        else:
            #dis_min = value - min_v
            #print 'dis_min=' + str(dis_min)
            color_v = math.ceil ((value - min_v)/v_bin) 

        #scale color_v to 0-1, a greater real value will have a bigger color_v
        #print'value' + str(value) + '=min_v=' + str(min_v) + '=max_v=' + str(max_v) + '=v_bin=' + str(v_bin) + '==float((value-min_v)/v_bin)==' + str(math.ceil (float((value-min_v)/v_bin))) + '===color_v===' + str(color_v)
        #print '===color_v===' + str(color_v)        
        #print color_v
        if color_img and num_bin==10: #if use 10 distinct color, return #hex
            color_v = color_arry [ int(num_bin - color_v)]
        else: #if use gray, return real value
            color_v =  float(color_v / num_bin)
            
    else:
        print 'this type '+ str(type) + ' is not supported!!'

    if debug==1:
        print 'min_v=' +str(min_v) + 'max_v' + str(max_v)
        print(value,color_v)

    return color_v    
  
def embed_image(X_embedded, X, name_file, size_p=1, fig_size=4, type_data='ab', 
        marker='ro', num_bin=10, margin = 0, alpha_v=0.5, 
        setcolor ='color', max_v=0.0065536, min_v= 1e-07, dpi_v = 75, colormap='', 
        cmap_vmin=0.0, cmap_vmax =1.0):
    
    """ create an image using manifolds #https://matplotlib.org/api/markers_api.html
    Args:
        X_embedded (array): coordinates of points after manifold
        X (array) : value of data point 
        color_arr (array): array of colors of points
        name_file (string): name image output
        size_p (int): point size
        fig_size=4 (int) : figure size (usually, 1: gives imgages of 84x84, 2: 162x162,...)
        type_data: type of data: ab/pr/eqw
        marker (string): shape of point (refer:https://matplotlib.org/api/markers_api.html), should use 'o' (for large img and if density not high) and ',': pixels (for small images)
        alpha_v (float): mode of transparent 0-1
        num_bin (int): number of bins
        margin (float): margin of image (white border)
        setcolor: color/gray
        [min_v, max_v]: the range to set bins
        dpi_v : dpi of images
        colormap : colormap used to set colors for the image (if ''-->custom set)
        [cmap_vmin, cmap_vmax]: the range to set colors using colormap provided by Python
    Returns:
        an image
    """

    #binning 
    if setcolor=="gray":
        color_arr = [convert_bin(y, debug=0, type=type_data, min_v = min_v, max_v = max_v, num_bin = num_bin) for y in X ]   
    else:
        if colormap=='':
            if type_data=="eqw" and num_bin==10: #if forget to set auto_v = 1, then generating black/white/gray images
                color_arr = [convert_bin(y, debug=0, type=type_data, min_v = min_v, max_v = max_v, num_bin = num_bin, color_img =True) for y in X ]  
            else:
                color_arr = [convert_color_real_img(y, debug=0, type=type_data) for y in  X ]   
        else:
            color_arr = [convert_bin(y, debug=0, type=type_data, min_v = min_v, max_v = max_v, num_bin = num_bin) for y in X ]           
    
    #set options to remove padding/white border
    mpl.rcParams['savefig.pad_inches'] = 0   
    fig, ax = plt.subplots(figsize=(fig_size*1.0/dpi_v,fig_size*1.0/dpi_v), dpi=dpi_v, facecolor='w')   
    ax.set_axis_bgcolor('w')
    ax.axis('off') #if do not have this, images will appear " strange black point"!!
    ax = plt.axes([0,0,1,1], frameon=False) #refer https://gist.github.com/kylemcdonald/bedcc053db0e7843ef95c531957cb90f
    # Then we disable our xaxis and yaxis completely. If we just say plt.axis('off'),
    # they are still used in the computation of the image padding.
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Even though our axes (plot region) are set to cover the whole image with [0,0,1,1],
    # by default they leave padding between the plotted data and the frame. We use tigher=True
    # to make sure the data gets scaled to the full extents of the axes.
    plt.autoscale(tight=True) 
    #print fig.get_dpi() #default
    #embbed points
    
    #set lim_max,min in x-axis and y-axis
    x_max = np.max(X_embedded[:,0])
    x_min = np.min(X_embedded[:,0])
    y_max = np.max(X_embedded[:,1])
    y_min = np.min(X_embedded[:,1])

    #variable containing data point <> 0 or not avaiable
    new_color_array = []
    new_X_embedded = []
    
    #if importances_feature <> 'none':
    #    print 'use important feature'
    #     for i in range(0,len(importances_feature)):
    #         print X_embedded[importances_feature [i] ]
    #         print color_arr [importances_feature [i] ]

    #skip white points (which have no information)
    if setcolor=="gray":   
        color_1 =  np.ones(len(color_arr)) - color_arr
        color_1 = [str(i) for i in color_1]
        #print color_1
        for i in range(0,int(len(X_embedded))) :
            if color_1[i] <> '1.0': #in grayscale, '1': white
                new_color_array.append(color_1[i]) #convert to string and scale of gray
                new_X_embedded.append(X_embedded[i])    
    else: #if use color images
        if colormap =='':
            for i in range(0,int(len(X_embedded))) :
                if color_arr[i] <> 'w':
                    new_color_array.append(color_arr [i])
                    new_X_embedded.append(X_embedded[i])   
        else:
            color_1 =  np.ones(len(color_arr)) - color_arr           
            for i in range(0,int(len(X_embedded))) :
                if color_1[i] <> 1.0: #in grayscale, 1: white
                    new_color_array.append(color_1[i]) #convert to string and scale of gray
                    new_X_embedded.append(X_embedded[i]) 
            

    new_X_embedded= np.stack(new_X_embedded)
    #print 'len(new_X_embedded)=' + str(len(new_X_embedded))
    #print 'len(new_color_array)=' + str(len(new_color_array))
    #print new_color_array
    #print len(new_X_embedded)
    if colormap=='': #if use predefined color or grayscale
        ax.scatter(new_X_embedded[:,0],new_X_embedded[:,1], s=size_p, marker = marker,color=new_color_array, edgecolors='none', alpha = alpha_v)          
    else:       
        if not(colormap in ['viridis','rainbow','gist_rainbow','jet','nipy_spectral','Paired','Reds','YlGnBu',
                        'viridis_r','rainbow_r','gist_rainbow_r','jet_r','nipy_spectral_r','Paired_r','Reds_r','YlGnBu_r']):             
            print 'colormap ' +str(colormap) + ' is not supported!!'
            exit()            
        #ax.scatter(new_X_embedded[:,0],new_X_embedded[:,1], s=size_p, marker = marker,c=new_color_array, edgecolors='none', alpha = alpha_v, cmap=cmap)        
        #ax.scatter(new_X_embedded[:,0],new_X_embedded[:,1], s=size_p, marker = marker,c=new_color_array, edgecolors='none', alpha = alpha_v, cmap=plt.get_cmap(colormap))        
        if cmap_vmax == cmap_vmin:
             ax.scatter(new_X_embedded[:,0],new_X_embedded[:,1], s=size_p, marker = marker,c=new_color_array, edgecolors='none', alpha = alpha_v, cmap=plt.get_cmap(colormap),vmin=cmap_vmax/num_bin,vmax=cmap_vmax)      
        else:
            ax.scatter(new_X_embedded[:,0],new_X_embedded[:,1], s=size_p, marker = marker,c=new_color_array, edgecolors='none', alpha = alpha_v, cmap=plt.get_cmap(colormap),vmin=cmap_vmin,vmax=cmap_vmax)      
  
    #fixing the same positions for all images  
    plt.xlim([x_min - margin, x_max + margin])
    plt.ylim([y_min - margin, y_max + margin])
    fig.savefig(name_file+'.png') ##True to see "not available area (unused area)"    
    plt.close('all')
  
def fillup_image(X, name_file, fig_size, size_p=1, cor_x=0,cor_y=0, marker_p='ro', type_data='ab', setcolor="color", 
        max_v=0.0065536, min_v= 1e-07, num_bin = 10, dpi_v = 75, alpha_v=0.5, colormap='',cmap_vmin=0.0, cmap_vmax=1.0):
    """ create an image using fillup 
    Args:       
        X (array): value of data point    
        name_file (string): name image output
        fig_size=4 (int) : figure size (usually, 1: gives imgages of 84x84, 2: 162x162,...), 
            to compute/convert inches-pixel look at http://auctionrepair.com/pixels.html, 
                Pixels / DPI = Inches
                Inches * DPI = Pixels
        size_p (int): point size
        type_data (string): type of data (abundance: ab or presence: pr)
        setcolor: color/gray
        cor_x (float): coordinates of x
        cor_y (float): coordinates of y
        marker_p (string): shape of point (refer to :https://matplotlib.org/api/markers_api.html), should use 'o' (for large img and if density not high) and ',': pixels (for small images)
        [min_v, max_v]: the range to set bins
        dpi_v (int): dpi of images
        colormap : colormap used to set colors for the image (if ''-->custom set)
            colormap for color images (refer to https://matplotlib.org/examples/color/colormaps_reference.html)
        [cmap_vmin, cmap_vmax]: the range to set colors using colormap provided by Python
        
    Returns:
        an image
    """
    #get bins for features
    if setcolor=="gray":
        colors = [convert_bin(y, debug=0, type=type_data, min_v = min_v, max_v = max_v, num_bin = num_bin) for y in X ]   
        #print 'use gray'
        #print X.shape
    else:
        if colormap == '':
            if (type_data=="eqw" and num_bin == 10):  #if use color, eqw: 10 distinct color
                colors = [convert_bin(y, debug=0, type=type_data, min_v = min_v, max_v = max_v, num_bin = num_bin, color_img =True) for y in X ]  
            else:
                colors = [convert_color_real_img(y, debug=0, type=type_data) for y in  X ]
        else:
            #print 'use colormap'
            #colors = [convert_bin(y, debug=0, type=type_data, min_v = min_v, max_v = max_v, num_bin = num_bin) for y in X ]   
            colors = [convert_bin(y, debug=0, type=type_data, min_v = min_v, max_v = max_v, num_bin = num_bin) for y in X ] 
            #print   colors
            #print X.shape
            #print '#use colormap'
    #fig, ax = plt.subplots(figsize=(fig_size,fig_size), facecolor='w')
    
    #set the size of images
    mpl.rcParams['savefig.pad_inches'] = 0   
    fig, ax = plt.subplots(figsize=(fig_size*1.0/dpi_v,fig_size*1.0/dpi_v), dpi=dpi_v, facecolor='w')   
    ax.set_axis_bgcolor('w')

    #eliminate border/padding
    ax.axis('off') #if do not have this, images will appear " strange black point"!!
    ax = plt.axes([0,0,1,1], frameon=False) #refer https://gist.github.com/kylemcdonald/bedcc053db0e7843ef95c531957cb90f
    # Then we disable our xaxis and yaxis completely. If we just say plt.axis('off'),
    # they are still used in the computation of the image padding.
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Even though our axes (plot region) are set to cover the whole image with [0,0,1,1],
    # by default they leave padding between the plotted data and the frame. We use tigher=True
    # to make sure the data gets scaled to the full extents of the axes.
    plt.autoscale(tight=True) 
    #print fig.get_dpi() #default
    
    
    #size_fig: eg. t2d: 23.9165214862 -> matrix 24x24
    #draw images
    if setcolor=="gray":                     
        #ax.scatter(cor_x,cor_y, marker = marker_p, color=str( 1 - colors))
        color_1 =  np.ones(len(colors)) - colors
        color_1 = [str(i) for i in color_1]
        #print colors
        #print np.max(colors)
        #print color_1
        ax.scatter(cor_x,cor_y, s=size_p, marker = marker_p,color=color_1, edgecolors='none', alpha = alpha_v)

        #ax.plot(cor_x,cor_y, marker_p, color=str( 1 - colors), markersize=size_p)
    else:           
        #print colors
        # refer to https://pythonspot.com/matplotlib-scatterplot/
        if colormap=='': #if use predefined color
            ax.scatter(cor_x,cor_y, s=size_p, marker = marker_p,color=colors, edgecolors='none', alpha = alpha_v)
        else: 
           
            if not(colormap in ['viridis','rainbow','gist_rainbow','jet','nipy_spectral','Paired','Reds','YlGnBu',
                        'viridis_r','rainbow_r','gist_rainbow_r','jet_r','nipy_spectral_r','Paired_r','Reds_r','YlGnBu_r']):             
                print 'colormap ' +str(colormap) + ' is not supported!!'
                exit()
            
            #print 'colormap ' +str(colormap) + ' selected!'
            #colors = np.stack(colors)
            #print colors
            #color_1 =  np.ones(len(colors)) - colors
            
            #set lim_max,min in x-axis and y-axis
            x_max = np.max(cor_x)
            x_min = np.min(cor_x)
            y_max = np.max(cor_y)
            y_min = np.min(cor_y)

            cor_x_new =[]
            cor_y_new =[]
            color_new = []
            #skip value = 0
            for i in range(0,int(len(colors))) : #remove point with value = 0
                if colors[i] <> 0.0: #in grayscale, 1: white
                    color_new.append(1-colors[i]) #convert to string and scale of gray
                    cor_x_new.append(cor_x[i]) 
                    cor_y_new.append(cor_y[i]) 
            #color_1 = [str(i) for i in color_1]
           # ax.scatter(cor_x_new,cor_y_new, s=size_p, marker = marker_p,c=color_new, edgecolors='none', alpha = alpha_v,cmap=cmap)
            #ax.scatter(cor_x_new,cor_y_new, s=size_p, marker = marker_p,c=color_new, edgecolors='none', alpha = alpha_v,cmap=plt.get_cmap(colormap))
            #ax.scatter(cor_x_new,cor_y_new, s=size_p, marker = marker_p,c=color_new, edgecolors='none', alpha = alpha_v,cmap=plt.get_cmap(colormap),vmin=1.0/num_bin,vmax=1)
            if cmap_vmax == cmap_vmin:
                ax.scatter(cor_x_new,cor_y_new, s=size_p, marker = marker_p,c=color_new, edgecolors='none', alpha = alpha_v,cmap=plt.get_cmap(colormap),vmin=cmap_vmax/num_bin,vmax=cmap_vmax)
            else:              
                ax.scatter(cor_x_new,cor_y_new, s=size_p, marker = marker_p,c=color_new, edgecolors='none', alpha = alpha_v,cmap=plt.get_cmap(colormap),vmin=cmap_vmin,vmax=cmap_vmax)
          
          
            #this code to keep the same positions for all images belongging to a dataset
            plt.xlim([x_min, x_max])
            plt.ylim([y_min, y_max])
    
    #create image
    fig.savefig(name_file+'.png')#, transparent=False) ##True to see "not available area (unused area)"    
    plt.close('all')

def name_log_final(arg, n_time_text):
    """ naming for log file
    Args:
        arg (array): arguments input from keybroad
        n_time_text (string) : beginning time
    Returns:
        a string (name of log)
    """
    prefix=''

    mid="o"+str(arg.num_classes)+arg.optimizer+"_lr"+str(arg.learning_rate)+'de'+str(arg.learning_rate_decay)+"e"+str(arg.epoch)+"_"+str(n_time_text) + 'c' +str(arg.coeff) + 'di' + str(arg.dim_img) + 'ch' + str(arg.channel) #+  'bi' + str(arg.num_bin)+'_'+str(arg.min_v) + '_'+str(arg.max_v)
    
    #check which model will be used
    if arg.model=="model_cnn" : #Convolution 2D
        if arg.padding == '0': #does not use padding
            prefix='cnn_' + mid + "l"+str(arg.numlayercnn_per_maxpool)+"p"+str(arg.nummaxpool)+"f"+str(arg.numfilters)+"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc) + "nopad"
        elif arg.padding == '1': #use padding
            prefix='cnn_' + mid + "l"+str(arg.numlayercnn_per_maxpool)+"p"+str(arg.nummaxpool)+"f"+str(arg.numfilters)+"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc) + "pad"
    elif arg.model=="model_mlp": #Multi-Layer Perception
        prefix='mlp_' + mid + "l"+str(arg.numfilters)+"n"+str(arg.numlayercnn_per_maxpool)+"d"+str(arg.dropout_fc)
    elif arg.model=="model_lstm": #Long Short Term Memory networks
        prefix='lstm_' + mid + str(arg.numfilters)+"n"+str(arg.numlayercnn_per_maxpool)+"d"+str(arg.dropout_fc)
    elif arg.model=="model_vgglike": #Model VGG-like
        if arg.padding == '0':
            prefix='vgg_' + mid +"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc)+ "nopad"
        elif arg.padding == '1':
            prefix='vgg_' + mid +"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc)+ "pad"
       
    
    elif arg.model=="model_cnn1d": #Convolution 1D
        prefix = 'cn1d_' + mid + "l"+str(arg.numlayercnn_per_maxpool)+"p"+str(arg.nummaxpool)+"f"+str(arg.numfilters)+"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc)
    elif arg.model=="fc_model": #FC model 
        prefix='fc_' + mid + "dr" +str(arg.dropout_fc) 
    elif arg.model=="svm_model": #SVM model 
        prefix='svm_' + str(arg.svm_kernel)+str(arg.svm_c)+'_' + mid 
    elif arg.model=="rf_model": #Random forest model 
        prefix='rf_' +  str(arg.rf_n_estimators) + '_'+mid 
    else:
        prefix = arg.model +'_'+ mid + "l"+str(arg.numlayercnn_per_maxpool)+"p"+str(arg.nummaxpool)+"f"+str(arg.numfilters)+"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc)
    
    #use consec or estop
    if arg.e_stop_consec=="consec":
            prefix = 'estopc' + str(arg.e_stop) + '_' + prefix
    else:
        prefix = 'estop' + str(arg.e_stop) + '_' + prefix
    
    #if use <>'bin' or 'raw' --> images, so specify name of preprocessing images
    if arg.type_emb <> 'bin' and arg.type_emb <> 'raw':
        prefix = str(arg.preprocess_img) + str(arg.mode_pre_img)+'_' + prefix
    
    if arg.n_folds <> 10:
        prefix = 'k'+str(arg.n_folds)+'_' + prefix

    if arg.time_run <> 10:
        prefix = 'a'+str(arg.time_run)+'_' + prefix
    
    if arg.save_w==1: #if save weights of the network
        prefix = prefix + "weight"

     
    #if arg.cudaid > -1:   
    #    prefix = prefix + "gpu" + str(arg.cudaid)
        
    return prefix


def para_cmd ():
    '''
    READ parameters provided from the command lines
    '''
    parser = OptionParser()

    #available symbols: (0: not available)
    # a0   b  c0   d0   e0   f0   g0   h    i0  j  k0  l0    m0  n0   o0   p0   q0  r0   s0   t0   v0   x0   y0  z0

    ## set up to run experiment, INPUT ===============================================================================================
    ## ===============================================================================================================================
    parser.add_option("-a", "--time_run", type="int", default=10, help="give the #runs (default:10)") 
    parser.add_option("--config_file", type="string", default='', help="specify config file if reading parameters from files") 
    parser.add_option("--seed_value_begin", type="int", default=1, help="set the beginning seed for different runs (default:1)")
    parser.add_option("--channel", type="int", default=3, help="channel of images, 1: gray, 2: color (default:3)") 
    parser.add_option("-m", "--dim_img", type="int", default=-1, help="width or height (square) of images, -1: get real size of original images (default:-1)") 
    parser.add_option("-k", "--n_folds", type="int", default=10, help="number of k folds (default:10)") 
    parser.add_option("--test_exte", type="int", default=0, help="if==1, using external validation sets (default:0)")
        #training (*_x.csv) and test on test set (*_y.csv), then selecting the best model to evaluate on val set (*_zx.csv) and (*_zy.csv)
    
    ## folders/paths    
    parser.add_option("--parent_folder_img", type="string", default='images', help="name of parent folder containing images (default:images)") 
    #parser.add_option("--pattern_img", type="string", default='0',help="pattern of images")   
    parser.add_option("-r","--original_data_folder", type="string", default='data', help="parent folder containing data (default:data)")
    parser.add_option("-i", "--data_dir_img", type="string", default='wt2dphy', help="name of dataset (default:wt2phy)") 
    parser.add_option('--search_already', type="int", default=1, help="if >0: search existed experiments before running-->if existed, stopping the experiment (default:1)")   
        #--search_already helps to avoid repeating an experiment which executed.
  
      
    ## set enviroments to run
    parser.add_option("--cudaid", type="int", default=-1, help="id cuda to use (if <0: use CPU), (default:-1)") 
    #parser.add_option("--nthread", type="int", default=0, help="specify number of threads")    
   
    ## pre-processing images
    parser.add_option("--preprocess_img", type='choice', choices=['resnet50','vgg16','vgg16','incep','vgg19','none'], default='none', help="support resnet50/vgg16/vgg19, none: no use (default:none) ") 
    parser.add_option("--mode_pre_img", type='choice', choices=['caffe','tf'], default='caffe', help="support caffe/tf (default:caffe)") 
        #https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet50/preprocess_input
        
    ## log, OUTPUT ==========================================================================================================================
    ## ===============================================================================================================================
    parser.add_option("--parent_folder_results", type="string", default='results', help="parent folder containing results (default:results)")        
    parser.add_option('-x',"--save_optional", type='choice', choices=['0','1','2','3','4','5','6','7'], default=4, 
        help="mode of saving log, see func para_cmd for use (default:4)")
        #we have optional results such loss in file2, detail (of each epoch, models with 3 varible of binary)
        # loss/details/model
        # eg. 000: none of them will be saved, 111=7: save all, binary(001)=1: save model, 010=2: details, 100=4: loss, 
        # decimal: 0:none;7:all; model: 1 (only),3,5,7; detail: 2 (only),3,6,7; loss: 4 (only),5,6,7        
    parser.add_option("--debug", type="int", default=0, help="show DEBUG if >0 (default:0)")
    parser.add_option('-v',"--visualize_model", type="int", default=0, help="visualize the model if > 0 (default:0)")     
    parser.add_option('--save_w', type="int", default=0, help="save weight mode, default:0; 1:save (default:0)")   
    parser.add_option('--suff_fini', type="string", default='ok', help="append suffix when finishing (default:ok)")     
    parser.add_option('--save_rf', type="int", default=0, help="save important features and scores for Random Forests")     
   
    
    ## reduce dimension ==========================================================================================================================
    ## ===============================================================================================================================
    parser.add_option('--algo_redu', type="string", default="", help="algorithm of dimension reduction (rd_pro/pca/fa),  if emtpy so do not use (default:'')")     
    parser.add_option('--rd_pr_seed', type="string", default="None", help="seed for random projection (default:None)")     
    parser.add_option('--new_dim', type="int", default=676, help="new dimension after reduction (default:676)")     
    parser.add_option('--reduc_perle', type="int", default=10, help="perlexity for tsne (default:10)")     
    parser.add_option('--reduc_ini', type="string", default='pca', help="ini for reduction (default:pca)")     
    
   
    ## EMBBEDING type options ===================================================================================================================
    ## ===============================================================================================================================
    parser.add_option("--rnd_seed", type="string", default='none', help="shuffle order of feature: if none, use original order of data (only use for fillup) (default:none)") 
    parser.add_option('-t',"--type_emb", type="choice", default="raw",  
        choices=['raw','bin','fill','fills','tsne','megaman','lle','isomap','mds','se','pca','rd_pro','lda','nmf'], help="type of the embedding (default:raw)")       
    parser.add_option("--imp_fea", type="choice", default="none",  
        choices=['none','rf'], help="use sorting important feature supported 'rf' for many overlapped figures (default:none)")    
    parser.add_option('-g',"--label_emb", type=int, default=-1,  
        help="taxa level of labels provided in supervised embeddings 'kingdom=1','phylum=2','class=3','order=4','family=5','genus=6' (default:0)") 
        #ONLY for: Linear Discriminant Analysis (LDA)    
    parser.add_option("--emb_data", type="choice", default="",  
        choices=['','o'], help="data embbed: '': transformed data; o: original data (default:'')") 
        #data used in embeddings
    parser.add_option('-y',"--type_data", type='choice', choices=['ab','pr','eqw'], default="ab", help="type of binnings: species-bins with log4(ab)/eqw/presence(pr) (default:ab)") 
        #type binning data
    #parser.add_option("--min_value", type='float', default="1e-7", help="the minimun value begin break, if set 0 use minimun of train set") 
    
    ## manifold learning parameters
    parser.add_option('-p',"--perlexity_neighbor", type="int", default=5, help="perlexity for tsne/#neighbors for others (default:5)") 
    parser.add_option("--lr_tsne", type="float", default=100.0, help="learning rate for tsne (default:100.0)") 
        #create images#### read at http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
    parser.add_option("--label_tsne", type="string", default="", help="use label when using t-SNE,'': does not use (default:'')") 
    parser.add_option("--iter_tsne", type="int", default=300, help="#iteration for run tsne, should be at least 250, but do not set so high (default:300)") 
    parser.add_option("--ini_tsne", type="string", default="pca", help="Initialization of embedding: pca/random/ or an array for tsne (default:pca)") 
    parser.add_option("--n_components_emb", type="int", default=2, help="ouput dim after embedding (default:2)") 
    parser.add_option("--method_lle", type="string", default='standard', help="method for lle embedding: standard/ltsa/hessian/modified (default:standard)") 
    parser.add_option("--eigen_solver", type="string", default='auto', help="method for others (except for tsne) (default:auto)")         
    
    ## create images ===================================================================================================================
    ## ===============================================================================================================================
    parser.add_option('-s',"--shape_drawn", type='choice', choices=[',', 'o', 'ro'], default=',', 
        help="shape of point to illustrate data: ,(pixel)/ro/o(circle) (default:,)") 
        #from 23h30, 1/3, begin to use "pixel" for fig_size instead of "in inches"
    parser.add_option("--fig_size", type="int", default=24, help="size of one dimension in pixels (if <=0: use the smallest which fit data, ONLY for fillup) (default:24)") 
    parser.add_option("--point_size", type="float", default=1, help="point size for img (default:1)") 
        #'point_size' should be 1 which aims to avoid overlapping
    parser.add_option("--setcolor", type="string", default="color", help="mode color for images (gray/color) (default:color)") 
    parser.add_option("--colormap", type="string", default="", help="colormap for color images (diviris/gist_rainbow/rainbow/nipy_spectral/jet/Paired/Reds/YlGnBu) (default:'')") 
    parser.add_option("--cmap_vmin", type="float", default=0, help="vmin for cmap (default:0)") 
    parser.add_option("--cmap_vmax", type="float", default=1, help="vmax for cmap (default:1)")     
    parser.add_option("--margin", type="float", default=0, help="margin to images (default:0)")
    parser.add_option("--alpha_v", type="float", default=1, help="The alpha blending value, between 0 (transparent) and 1 (opaque) (default:1)") 
    parser.add_option("--recreate_img", type="int", default=0, help="if >0 rerun to create images even though they are existing (default:0)") 

    ## binning and scaling ===================================================================================================================
    ## ===============================================================================================================================
    parser.add_option("--scale_mode", type='choice', choices=['minmaxscaler','mms','none','quantiletransformer','qtf'], default='none', help="scaler mode for input (default:none)")
    parser.add_option('--n_quantile', type="int", default=1000, help="n_quantile in quantiletransformer (default:1000)")      
    parser.add_option('--min_scale', type="float", default=0, help="minimum value for scaling (only for minmaxscaler) (default:0) use if --auto_v=0") 
    parser.add_option('--max_scale', type="float", default=1, help="maximum value for scaling (only for minmaxscaler) (default:1) use if --auto_v=0")     
    parser.add_option("--min_v", type="float", default=1e-7, help="limit min for Equal Width Binning (default:1e-7)") 
    parser.add_option("--max_v", type="float", default=0.0065536, help="limit min for Equal Width Binning (default:0.0065536)") 
    parser.add_option("--num_bin", type="int", default=10, help="the number of bins (default:10)")
    parser.add_option("--auto_v", type="int", default=0, help="if > 0, auto adjust min_v and max_v (default:0)")       
        
    ## Architecture for training ======================================================================================== 
    ## ===============================================================================================================================  
    parser.add_option("-f", "--numfilters", type="int", default=64, help="#filters/neurons for each cnn/neural layer (default:64)") 
    parser.add_option("-n", "--numlayercnn_per_maxpool", type="int", default=1, help="#cnnlayer before each max pooling (default:1)") 
    parser.add_option("--nummaxpool", type="int", default=1, help="#maxpooling_layer (default:1)") 
    parser.add_option("--dropout_cnn", type="float", default=0, help="dropout rate for CNN layer(s) (default:0)") 
    parser.add_option("-d", "--dropout_fc", type="float", default=0, help="dropout rate for FC layer(s) (default:0)") 
 
    parser.add_option("--padding", type='choice', choices=['1', '0'], default='1', help="='1' uses pad, others: does not use (default:1)") 
    parser.add_option("--filtersize", type="int", default=3, help="the filter size (default:3)") 
    parser.add_option("--poolsize", type="int", default=2, help="the pooling size (default:2)") 
    parser.add_option("--model", type="string", default = 'fc_model', 
        help="type of model (fc_model/model_cnn1d/model_cnn/model_vgglike/model_lstm/resnet50/rf_model/svm_model/none) (none: only visualization not learning)")   
    
    
    ## learning parameters ==========================================================================================================
    ## ===============================================================================================================================   
    parser.add_option("-c", "--num_classes", type="int", default=1 ,help="the output of the network (default:1)")    
    parser.add_option("-e", "--epoch", type="int", default=500 ,help="the epoch used for training (default:500)")   
    parser.add_option("--learning_rate", type="float", default=-1, help="learning rate, if -1 use default value of the optimizer (default:-1)")   
    parser.add_option("--batch_size", type="int", default=16, help="batch size (default:16)")
    parser.add_option("--learning_rate_decay", type="float", default=0,  help="learning rate decay (default:0)")
    parser.add_option("--momentum", type="float", default=0.1 ,  help="momentum (default:0)")
    parser.add_option("-o","--optimizer", type="string", default="adam", help="support sgd/adam/Adamax/RMSprop/Adagrad/Adadelta/Nadam (default:adam)") 
    parser.add_option("-l","--loss_func", type="string", default="binary_crossentropy", help="support binary_crossentropy/mae/squared_hinge (default:binary_crossentropy)") 
    parser.add_option("-q","--e_stop", type="int", default=5, help="#epochs with no improvement after which training will be stopped (default:5)") 
    parser.add_option("--e_stop_consec", type="string", default="consec", help="option to choose consective (self defined: consec) or not (default:consec)") 
    parser.add_option("--svm_c", type="float", default = 1.0, 
        help="Penalty parameter C of the error term for SVM (default:1.0)")
        #parameters for SVM
    parser.add_option("--svm_kernel", type="string", default = "linear", 
        help="the kernel type used in the algorithm (linear, poly, rbf, sigmoid, precomputed) (default:linear)")
        #parameters for SVM
    parser.add_option("--rf_n_estimators", type="int", default = 500, 
        help="The number of trees in the forest (default:500)")
        #parameters for Random Forest

    #grid search for coef ========================================================================================
    ## ===============================================================================================================================   
    parser.add_option('-z',"--coeff", type="float", default=1, help="coeffiency (divided) for input (should use 255 for images) (default:1)")
    parser.add_option("--grid_coef_time", type="int", default=10, help="choose the best coef from #coef default for tuning coeficiency (default:5)")
    parser.add_option("--cv_coef_time", type="int", default=4, help="k-cross validation for each coef for tuning coeficiency (default:4)")
    parser.add_option("--coef_ini", type="float", default=255, help="initilized coefficient for tuning coeficiency (default:255)")
    parser.add_option("--metric_selection", type="string", default="roc_auc", help="roc_auc/accuracy/neg_log_loss/grid_search_mmc for tuning coeficiency (default:roc_auc)")

    (options, args) = parser.parse_args()
    return (options, args)


def para_config_file (options):
    '''
    READ parameters provided from a configuration file
    these parameters in the configuration file are fixed, 
    modify these parameters from cmd will not work, only can modify in the configuration file
    '''

    config = ConfigParser.ConfigParser()

    #read config file
    config.read (options.config_file)
 
    #set parameters for embedding type
    options.type_emb =  config.get("embeddings" ,"type_emb")
    options.type_data =  config.get("embeddings" ,"type_data")
    if config.has_option("embeddings","scale_mode"):
        options.scale_mode  =  config.get("embeddings" ,"scale_mode")
    if config.has_option("embeddings","auto_v"):
        options.auto_v  =  config.get("embeddings" ,"auto_v")
    if config.has_option("embeddings","num_bin"):
        options.num_bin  =  config.get("embeddings" ,"num_bin")

    #set parameters to generate images
    options.fig_size  = int( config.get("images" ,"fig_size"))
    if config.has_option("images","setcolor"):
        options.setcolor  =  config.get("images" ,"setcolor")
    if config.has_option("images","channel"):
        options.channel  = int(  config.get("images" ,"channel"))
    if config.has_option("images","alpha_v"):
        options.alpha_v  =  config.get("images" ,"alpha_v")
    
    #set parameters for learning
    options.coeff = float( config.get("learnings" ,"coeff") )
    options.model =  config.get("learnings" ,"model")
    if config.has_option("learnings","numlayercnn_per_maxpool"):
        options.numlayercnn_per_maxpool = int( config.get("learnings" ,"numlayercnn_per_maxpool"))
    if config.has_option("learnings","numfilters"):
        options.numfilters = int(  config.get("learnings" ,"numfilters"))
