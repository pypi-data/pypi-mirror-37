"""
================================================================================
dev_met2img.py : Predicting diseases based on images (EMBEDDINGs) 
        with stratified cross-validation (including support building images and training)
================================================================================
Author: Team Integromic, ICAN, Paris, France' 
(**this version is still developping)
date: 25/12/2017' (updated to 30/10/2018)

function : run n times (cross validation) using embeddings 
    with fillup and manifold algorithms (t-SNE, LDA, isomap,...) 
    support color, gray images with manual bins or bins learned from training set
====================================================================================================================
Steps: 
1. set variables, naming logs and folder for outputs, inputs (images)
2. read original data from excel file including data (*_x.csv), labels (*_y.csv)
3. Plit data into stratified kfolds, then applying dimension reduction, transformation... 
4. load and call model
5. training and evaluate on validation set
6. summarize results, compute metric evaluation, average accuracy, auc each run, the experiment, and show on the screen, also save log.
====================================================================================================================
Input: 2 csv files, 1 for data (*_x.csv), 2 for labels (*_y.csv)
Output: 3 files (*.txt) of log on general information of the experiment in folder './results/' (default), 
    AND images (*.png) in folder './images/' (if not exist in advance)
    AND numerous files (*.txt) stored acc,loss at each epoch in folder results/<folder_of_dataset>/details
    AND numerous files (*.json) of models in folder results/<folder_of_dataset>/models

Metric evaluation: Accuracy, Area Under Curve (AUC), 
    Averaged True Negative (tn), Averaged False Negative (fn), Averaged True Negative (fp), Averaged True Positive (tp)	
    Precision (preci), Recall, F1-score	(f1), MCC
    Execution time, epoch stopped using Early Stopping

File 2,3 to take overview results after each k-fold-cv, file 1 for detail of each fold
'file 1: parameters; selected hyperparameters/labels/performance of each fold; 
    the final results of the experiment is at the last line
    the name of this file appended "ok" as finishes
'file 2: mean at the beginning and finished of acc, loss of train/val; the execution time; 
    the mean/sd of these at the last line
'file 3: mean at acc (computed based on averaged confusion matrix for cross-check)/auc/confusion matrix (tn,tp,fn,tn);
    tn: true negative, tp: true positive, fn: false negative, fp: false positive, and Matthews corrcoef (MMC)
    the mean/sd of these at the last line
====================================================================================================================
"""

#libraries ====================================================================
import os
#modules self-definition
#library for generating images and other ultis (find files,naming log, read parameters,...)
import utils
import vis_data

#get parameters from command line
options, args = utils.para_cmd()

#check if read parameters from configuration file
if options.config_file <> '':
    if os.path.isfile(options.config_file):
        utils.para_config_file(options)
        #print options
    else:
        print 'config file does not exist!!!'
        exit()

#check whether parameters all valid
utils.validation_para(options)
   

if options.cudaid > -1 and options.cudaid <= 10 : #if >10 get all gpus and memories
    #use gpu
    print 'gpu: ' + str(options.cudaid)    
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = str(options.cudaid)
elif  options.cudaid <= -1:
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np
import random as rn
import pandas as pd
import math
from time import gmtime, strftime
import time

from sklearn.metrics import roc_auc_score,accuracy_score,f1_score,precision_score,recall_score,matthews_corrcoef, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.manifold import TSNE, LocallyLinearEmbedding, SpectralEmbedding, MDS, Isomap
from sklearn.cluster import FeatureAgglomeration
from sklearn.decomposition import PCA, NMF
from sklearn.preprocessing import MinMaxScaler, QuantileTransformer
from sklearn import random_projection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier

if options.type_run not in ['vis','visual']:  
    import tensorflow as tf
    import models_def #models definitions
    import keras as kr
    from keras.applications.resnet50 import ResNet50
    from keras.applications.vgg16 import VGG16
    from keras.models import Model
    from keras.applications.resnet50 import preprocess_input
    from keras.utils import np_utils
    from keras import backend as optimizers
    from keras.models import Sequential
    from keras.layers import Activation, Dropout, Flatten, Dense, InputLayer, Conv2D, MaxPooling2D,Input

#declare varibables for measuring time
time_text = str(strftime("%Y%m%d_%H%M%S", gmtime()))
start_time = time.time() # check point the beginning
mid_time = [] # check point middle time to measure distance between runs

#transfer value from cmd line
input_shape = (options.dim_img, options.dim_img, options.channel)
num_classes = options.num_classes
batch_size = options.batch_size
epochs_num = options.epoch
number_filters = options.numfilters
dropout_rate_fc = options.dropout_fc
dropout_rate_cnn = options.dropout_cnn
filtersize = options.filtersize

data_dir_img = options.data_dir_img
numlayercnn_per_maxpool = options.numlayercnn_per_maxpool
nummaxpool = options.nummaxpool
poolsize = options.poolsize

if __name__ == "__main__":   
      
    # ===================== set folders and file pattern for outputs ===========================
    # ==========================================================================================
    
    dataset_name = options.data_dir_img

    #print 'path to read data' + options.original_data_folder[0]
    #path to read data and labels
    if options.original_data_folder[0] == "/": #use absolute path
        path_read =  options.original_data_folder 
    else: #relative path
        path_read = os.path.join('.', options.original_data_folder) 
    
    #pre_name: prefix name of folder       
    if options.algo_redu<>"":  #if use reducing dimension
        if options.algo_redu == 'rd_pro':
            if options.rd_pr_seed <> "None":
                pre_name = dataset_name + options.algo_redu + str(options.new_dim) + '_'+ str(options.reduc_perle)   + '_s' + str(options.rd_pr_seed)
            else:
                pre_name = dataset_name + options.algo_redu + str(options.new_dim) + '_'+ str(options.reduc_perle)  
        else:
            pre_name = dataset_name + options.algo_redu + str(options.new_dim) + '_'+ str(options.reduc_perle)   
    else:
        pre_name = dataset_name
    
    if options.del0  == 'y': #if remove columns which own all = 0
        pre_name = pre_name + '_del0'

    if options.rnd_seed <> "none": #set name for features ordered randomly
        if options.type_emb in ['raw','fill','fills']:
            pre_name = pre_name + 'rnd' + str(options.rnd_seed)
        else:
            print "use of features ordered randomly only supports on raw','fill','fills'"
            exit()

    if options.type_data == 'pr': #if select bin=binary black/white
        options.num_bin = 2

    if options.type_emb == 'raw':      #raw data  
        pre_name = pre_name + "_" + options.type_emb
   
    elif options.type_emb == 'bin': #bin: ab (manual bins), eqw (equal width bins), pr (binary: 2 bins)
        
        pre_name = pre_name + '_' + str(options.type_emb) + options.type_data 
        path_write = os.path.join('.', options.parent_folder_img, pre_name)
        pre_name =pre_name+'_nb'+str(options.num_bin) + '_au'+str(options.auto_v) + '_'+str(options.min_v) + '_'+str(options.max_v)+'_isc'+str(options.min_scale) + '_asc'+str(options.max_scale)
             
        if options.scale_mode in ['minmaxscaler','mms'] :
            pre_name = pre_name + 'mms' #add suffix 'mms' to refer minmaxscaler
        elif options.scale_mode in ['quantiletransformer','qtf']:            
            pre_name = pre_name + 'qtf' + str(options.n_quantile)  #add suffix 'qtf' to refer quantiletransformer
       
        if not os.path.exists(path_write):
            print path_write + ' does not exist, this folder will be created...' 
            os.makedirs(os.path.join(path_write)) 

    elif options.type_emb == 'fill': 
        #fill, create images only one time
        # set the names of folders for outputs    
        shape_draw=''  
        if options.shape_drawn == ',': #',' means pixel in the graph
            shape_draw='pix'
        pre_name = pre_name + '_' + str(options.type_emb) + '_' + shape_draw + '_r' + str(options.fig_size) + 'p'+ str(options.point_size) + options.type_data + "m" + str(options.margin) +'a'+str(options.alpha_v) + options.setcolor +options.colormap  + 'bi' + str(options.num_bin)+'_'+str(options.min_v) + '_'+str(options.max_v)
        if options.cmap_vmin <> 0 or options.cmap_vmax <> 1:
            pre_name = pre_name + 'cmv' + str(options.cmap_vmin) +'_' + str(options.cmap_vmax)
        path_write = os.path.join('.', options.parent_folder_img, pre_name)
        if not os.path.exists(path_write):
            print path_write + ' does not exist, this folder will be created...' 
            os.makedirs(os.path.join(path_write))     
 
    else: #if Fills (eqw) OR using other embeddings: tsne, LLE, isomap,..., set folder and variable, names
        #parameters for manifold: perplexsity in tsne is number of neigbors in others
        learning_rate_x = options.lr_tsne
        n_iter_x = options.iter_tsne
        perplexity_x = options.perlexity_neighbor  
        shape_draw=''  
        if options.shape_drawn == ',':
            shape_draw='pix'  #pixel

        #add pre_fix for image name
        if options.type_emb == 'fills':            
            pre_name = pre_name+'_'+str(options.type_emb)  + str(shape_draw) + '_r' + str(options.fig_size) + 'p'+ str(options.point_size) + options.type_data + "m" + str(options.margin) +'a'+str(options.alpha_v) + str(options.setcolor) + str(options.colormap)
        else: #others: tsne, lle,...
            
            if options.imp_fea in ['rf']:
                insert_named =  str(options.imp_fea)
            else:
                insert_named = ''

            if options.type_emb == 'lda':
                #if use supervised dimensional reduction, so determine which label used.
                pre_name = pre_name+'_'+str(options.type_emb)+ options.eigen_solver  + str(options.label_emb) +str(options.emb_data) + insert_named + '_p'+str(perplexity_x) + 'l'+str(learning_rate_x) + 'i'+str(n_iter_x) + shape_draw + '_r' + str(options.fig_size) + 'p'+ str(options.point_size) + options.type_data + "m" + str(options.margin) +'a'+str(options.alpha_v) + str(options.setcolor) + str(options.colormap)
       
            else:
                if options.label_tsne == "":
                    pre_name = pre_name+'_'+str(options.type_emb) +str(options.emb_data) + insert_named + '_p'+str(perplexity_x) + 'l'+str(learning_rate_x) + 'i'+str(n_iter_x) + shape_draw + '_r' + str(options.fig_size) + 'p'+ str(options.point_size) + options.type_data + "m" + str(options.margin) +'a'+str(options.alpha_v) + str(options.setcolor) + str(options.colormap)
                else: 
                    pre_name = pre_name+'_'+str(options.type_emb) +str(options.emb_data) + str(options.label_tsne)+ insert_named+ '_p'+str(perplexity_x) + 'l'+str(learning_rate_x) + 'i'+str(n_iter_x) + shape_draw + '_r' + str(options.fig_size) + 'p'+ str(options.point_size) + options.type_data + "m" + str(options.margin) +'a'+str(options.alpha_v) + str(options.setcolor)  + str(options.colormap)
            
        pre_name =pre_name+'_nb'+str(options.num_bin) + '_au'+str(options.auto_v) + '_'+str(options.min_v) + '_'+str(options.max_v)+'_isc'+str(options.min_scale) + '_asc'+str(options.max_scale)
        
        if options.cmap_vmin <> 0 or options.cmap_vmax <> 1:
            pre_name = pre_name + 'cmv' + str(options.cmap_vmin) +'_' + str(options.cmap_vmax)

        if options.type_emb == 'lle':
            pre_name = pre_name + str(options.method_lle)
             
        if options.scale_mode in ['minmaxscaler','mms'] :
            pre_name = pre_name + 'mms' #add suffix 'mms' to refer minmaxscaler
        elif options.scale_mode in ['quantiletransformer','qtf']:            
            pre_name = pre_name + 'qtf' + str(options.n_quantile)  #add suffix 'qtf' to refer quantiletransformer

        path_write_parentfolder_img = os.path.join('.', options.parent_folder_img, pre_name)
        #looks like: cir_p30l100i500/          
        if not os.path.exists(path_write_parentfolder_img):
            print path_write_parentfolder_img + ' does not exist, this folder will be created...' 
            os.makedirs(os.path.join(path_write_parentfolder_img))  

    
    #folder contains results
    res_dir = os.path.join(".", options.parent_folder_results, pre_name) 
    if options.debug == 'y':
        print res_dir 

    # check for existence to contain results, if not, then create
    if not os.path.exists(os.path.join(res_dir)):
        print res_dir + ' does not exist, this folder will be created to contain results...'
        os.makedirs(os.path.join(res_dir))
    if not os.path.exists(os.path.join(res_dir, 'details')):       
        os.makedirs(os.path.join(res_dir, 'details'))
    if not os.path.exists(os.path.join(res_dir, 'models')):
        os.makedirs(os.path.join(res_dir, 'models'))      
    
    #check whether this experiment had done before
    if options.search_already == 'y':
        prefix_search = utils.name_log_final(options, n_time_text= '*')        
        
        list_file = utils.find_files(prefix_search+'file*'+str(options.suff_fini)+'*',res_dir)
        
        if len(list_file)>0:
            print 'the result(s) existed at:'
            print list_file
            print 'If you would like to repeat this experiment, please set --search_already to n'
            exit()
        else:
            if options.cudaid > -1:
                list_file = utils.find_files(prefix_search+'gpu'+ str(options.cudaid)+'file*ok*',res_dir)
                if len(list_file)>0:
                    print 'the result(s) existed at:'
                    print list_file
                    print 'If you would like to repeat this experiment, please set --search_already to n'
                    exit()
    
    #get the pattern name for files log1,2,3
    prefix = utils.name_log_final(options, n_time_text= str(time_text))
    name2_para = utils.name_log_final(options, n_time_text= '')
    #print prefix    
    if options.debug == 'y':
        print prefix 
    #file1: contained general results, each fold; file2: accuracy,loss each run (finish a 10-cv), file3: Auc
    #folder details: acc,loss of each epoch, folder models: contain file of model (.json)
    
   
    prefix_file_log = res_dir + "/" + prefix + "file"
    prefix_details = res_dir + "/details/" + prefix+"acc_loss_"
    prefix_models = res_dir + "/models/" + prefix+"model_"

    # ===================== BEGIN: read orginal data from excel ===========================
    # ==============================================================================
     
    #read data and labels
    data = pd.read_csv(os.path.join(path_read, dataset_name + '_x.csv'))
    #print data.index
    #print list(data.index)
    data = data.set_index('Unnamed: 0') #rows: features, colulms: samples 
    
    # Delete column if it is All zeros (0)
   

    name_features =  list(data.index)
    #print name_features
    data = data.values      
    
   

    if options.rnd_seed <> "none": #set name for features ordered randomly
        if options.type_emb in ['raw','fill','fills']:
            np.random.seed(int(options.rnd_seed))
            np.random.shuffle(data) #shuffle features with another order using seed 'rnd_seed'
        else:
            print "use of features ordered randomly only supports on raw','fill','fills'"
            exit()
        
    data = np.transpose(data) #rows: samples, colulms: features
    data = np.stack(data)   
    print data.shape    

    if options.del0 == 'y':
        print data.shape
        print 'delete columns which have all = 0'
        #data[:, (data != 0).any(axis=0)]
        data = data[:, (data != 0).any(axis=0)]
        print data.shape

    labels = pd.read_csv(os.path.join(path_read, dataset_name + '_y.csv'))
    labels = labels.iloc[:,1] 
    
    if options.test_exte == 'y': #if use external validation set
        path_v_set_x = os.path.join(path_read, dataset_name + '_zx.csv')
        path_v_set_y = os.path.join(path_read, dataset_name + '_zy.csv')
        
        if not os.path.exists(path_v_set_x):
            print(path_v_set_x + ' does not exist!!')
            exit()   
        if not os.path.exists(path_v_set_y):
            print(path_v_set_y + ' does not exist!!')
            exit()   

        v_data_ori = pd.read_csv(path_v_set_x) #rows: features, colulms: samples 
        v_data_ori = v_data_ori.set_index('Unnamed: 0')
        v_data_ori = v_data_ori.values

        if options.rnd_seed <> "none": #set name for features ordered randomly
            if options.type_emb in ['raw','fill','fills']:
                np.random.seed(int(options.rnd_seed))
                np.random.shuffle(v_data_ori) #shuffle features with another order using seed 'rnd_seed'
            else:
                print "use of features ordered randomly only supports on raw','fill','fills'"
                exit()

        v_data_ori = np.transpose(v_data_ori) #rows: samples, colulms: features
        v_data_ori = np.stack(v_data_ori)  

        v_labels = pd.read_csv(path_v_set_y)
        v_labels = v_labels.iloc[:,1] 
            
    # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
    # <><><><><><><><><><><><><><> end of read orginal data from excel <><><><><><><>
   
    #building cordinates for fill-up 
    # (a square of len_square*len_square containing all values of data)
    if options.type_emb in [ 'fill','fills'] and options.algo_redu == "": #if use dimension reduction (algo_redu<>""), only applying after reducing
        cordi_x = []
        cordi_y = []
        len_data = data.shape[1]
        #build coordinates for fill-up with a square of len_square*len_square
        len_square = int(math.ceil(math.sqrt(len_data)))
        print 'square_fit_features=' + str(len_square) 
        k = 0
        for i in range(0,len_square):
            for j in range(0,len_square):                
                if k == (len_data):
                    break
                else:
                    cordi_x.append(j*(-1))
                    cordi_y.append(i*(-1))
                    k = k+1
            if k == (len_data):
                break
        print '#features=' +str(k)
    
    #create full set of images for fill-up using predefined-bins
    if options.type_emb == 'fill': 
        if options.fig_size <= 0: #if fig_size <=0, use the smallest size which fit the data, generating images of (len_square x len_square)
            options.fig_size = len_square
        #check whether images created completely or requirement for creating images from options; if not, then creating images
        if not os.path.exists(path_write+'/fill_' + str(len(labels)-1)+'.png') or options.recreate_img > 0 :
            labels.to_csv(path_write+'/y.csv', sep=',')
            mean_spe=(np.mean(data,axis=0))       
            vis_data.fillup_image(cor_x=cordi_x,cor_y=cordi_y, X = mean_spe, type_data=options.type_data,
                    name_file= path_write+"/global", fig_size = options.fig_size, 
                    min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin, alpha_v = options.alpha_v,
                    size_p =options.point_size, marker_p = options.shape_drawn, setcolor = options.setcolor, 
                    colormap = options.colormap, cmap_vmin = options.cmap_vmin,cmap_vmax = options.cmap_vmax)

            for i in range(0, len(labels)):
                print 'img fillup ' + str(i)            
                vis_data.fillup_image(cor_x=cordi_x,cor_y=cordi_y, X = data[i], type_data=options.type_data,
                    name_file= path_write+"/fill_"+str(i), fig_size = options.fig_size, 
                    min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin, alpha_v = options.alpha_v,
                    size_p =options.point_size, marker_p = options.shape_drawn, setcolor = options.setcolor, 
                    colormap = options.colormap,cmap_vmin = options.cmap_vmin,cmap_vmax = options.cmap_vmax)

        #reading images
        data = utils.load_img_util(num_sample = len(data), pattern_img='fill',
                    path_write = path_write , dim_img = options.dim_img, preprocess_img = options.preprocess_img, 
                    channel = options.channel,mode_pre_img = options.mode_pre_img)       
        print 'data=' + str(data.shape) #check dim of reading


        if options.test_exte == 'y': #if use external validation set
            
            #create images if does not exist
            if not os.path.exists(path_write+'/testval_' + str(len(v_labels)-1)+'.png') or options.recreate_img > 0 :
                labels.to_csv(path_write+'/y.csv', sep=',')
                mean_spe=(np.mean(v_data_ori,axis=0))       
                vis_data.fillup_image(cor_x=cordi_x,cor_y=cordi_y, X = mean_spe, type_data=options.type_data,
                        name_file= path_write+"/global_testval_", fig_size = options.fig_size, 
                        min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin, alpha_v = options.alpha_v,
                        size_p =options.point_size, marker_p = options.shape_drawn, setcolor = options.setcolor, 
                        colormap = options.colormap,cmap_vmin = options.cmap_vmin,cmap_vmax = options.cmap_vmax)

                for i in range(0, len(v_labels)):
                    print 'img fillup testval ' + str(i)            
                    vis_data.fillup_image(cor_x=cordi_x,cor_y=cordi_y, X = v_data_ori[i], type_data=options.type_data,
                        name_file= path_write+"/testval_"+str(i), fig_size = options.fig_size, 
                        min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin, alpha_v = options.alpha_v,
                        size_p =options.point_size, marker_p = options.shape_drawn, setcolor = options.setcolor, 
                        colormap = options.colormap,cmap_vmin = options.cmap_vmin,cmap_vmax = options.cmap_vmax)

            #reading images
            v_data_ori = utils.load_img_util(num_sample = len(v_data_ori), pattern_img='testval',
                        path_write = path_write , dim_img = options.dim_img, preprocess_img = options.preprocess_img, 
                        channel = options.channel,mode_pre_img = options.mode_pre_img)       
            print 'data testval=' + str(v_data_ori.shape) #check dim of reading

    # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
    # <><><><><><><><><><><><><><> end of set folders and file pattern for outputs <><><><><><><><><><><><><><>
   
    #if use external validations
    if options.test_exte == 'y':
        title_cols = np.array([["se","fold","model_ac",'model_au','model_mc',"acc","auc","mmc"]])  
        f=open(prefix_file_log+"4.txt",'a')
        np.savetxt(f,title_cols, fmt="%s",delimiter="\t")
        f.close()

    #save arg/options/configurations used in the experiment to LOG file1
    f = open(prefix_file_log+"1.txt",'a')
    np.savetxt(f,(options, args), fmt="%s", delimiter="\t")
    f.close()

    if options.save_para == 'y' : #save para to config file to rerun        
        if options. path_config_w == "":
            configfile_w = res_dir + "/" + pre_name + "_" + name2_para + ".cfg"
        else: #if user want to specify the path
            configfile_w = options. path_config_w + "/" + pre_name + "_" + name2_para + ".cfg"

        if os.path.isfile(configfile_w):
            print 'the config file exists!!! Please remove it, and try again!'
            exit()
        #print options
        else:
            utils.write_para(options,configfile_w)  
            print 'Config file was saved to ' + configfile_w      
            

    #save title (column name) for log2: acc,loss each run with mean(k-fold-cv)
    if options.save_optional in ['4','5','6','7']:
        title_cols = np.array([["seed","ep","tr_start","tr_fin","te_begin","te_fin","lo_tr_be","lo_tr_fi","lo_te_be","lo_te_fi""total_t","t_distant"]])  
    else:
        title_cols = np.array([["seed","ep","train_start","train_fin","test_start","test_fin","total_t","t_distant"]])  
    
    f=open(prefix_file_log+"2.txt",'a')
    np.savetxt(f,title_cols, fmt="%s",delimiter="\t")
    f.close()
    
    #save title (column name) for log3: acc,auc, confusion matrix each run with mean(k-fold-cv)
    title_cols = np.array([["se","ep","tr_tn","tr_fn","tr_fp","tr_tp","va_tn","va_fn","va_fp","va_tp","tr_acc",
        "va_acc","tr_auc","va_auc"]])  
    f=open(prefix_file_log+"3.txt",'a')
    np.savetxt(f,title_cols, fmt="%s",delimiter="\t")
    f.close()

    #initialize variables for global acc, auc
    temp_all_acc_loss=[]
    temp_all_auc_confusion_matrix=[]    

    train_acc_all =[] #stores the train accuracies of all folds, all runs
    train_auc_all =[] #stores the train auc of all folds, all runs
    #train_mmc_all =[] #stores the train auc of all folds, all runs
    val_mmc_all =[] #stores the validation accuracies of all folds, all runs
    val_acc_all =[] #stores the validation accuracies of all folds, all runs
    val_auc_all =[] #stores the validation auc of all folds, all runs
    
    best_mmc_allfolds_run = -1
    best_mmc_allfolds_run_get = -1
    best_acc_allfolds_run = 0
    best_auc_allfolds_run = 0

    # ===================== BEGIN: run each run ================================================
    # ==========================================================================================
    for seed_value in range(options.seed_value_begin,options.seed_value_begin+options.time_run) :
        print "We're on seed %d" % (seed_value)    
        np.random.seed(seed_value) # for reproducibility    
        if options.type_run not in ['vis','visual']:   
            tf.set_random_seed(seed_value)
        #rn.seed(seed_value)       

        #ini variables for scores in a seed
        #TRAIN: acc (at beginning + finish), auc, loss, tn, tp, fp, fn
        train_acc_1se=[]
        train_auc_1se=[]
        train_loss_1se=[]
        train_acc_1se_begin=[]
        train_loss_1se_begin=[]

        train_tn_1se=[]
        train_tp_1se=[]
        train_fp_1se=[]
        train_fn_1se=[]

        early_stop_1se=[]
       
        #VALIDATION: acc (at beginning + finish), auc, loss, tn, tp, fp, fn
        val_acc_1se=[]
        val_auc_1se=[]
        val_loss_1se=[]
        val_acc_1se_begin=[]
        val_loss_1se_begin=[]
        val_pre_1se=[]
        val_recall_1se=[]
        val_f1score_1se=[]
        val_mmc_1se=[]

        val_tn_1se=[]
        val_tp_1se=[]
        val_fp_1se=[]
        val_fn_1se=[]       

        #set the time distance between 2 runs, the time since the beginning
        distant_t=0
        total_t=0       


        #begin each fold
        skf=StratifiedKFold(n_splits=options.n_folds, random_state=seed_value, shuffle= True)
        for index, (train_indices,val_indices) in enumerate(skf.split(data, labels)):
            if options.type_run in ['vis','visual']:
                print "Creating images on  " + str(seed_value) + ' fold' + str(index+1) + "/"+str(options.n_folds)+"..."       
            else:
                print "Training on  " + str(seed_value) + ' fold' + str(index+1) + "/"+str(options.n_folds)+"..."       
            if options.debug == 'y':
                print(train_indices)
                print(val_indices)         

            #transfer data to train/val sets
            train_x = []
            train_y = []
            val_x = []
            val_y = []   
            train_x, val_x = data[train_indices], data[val_indices]
            train_y, val_y = labels[train_indices], labels[val_indices]
            if options.test_exte == 'y':  
                v_data =  v_data_ori
            print train_x.shape
            ##### reduce dimension 
            if options.algo_redu <> "": #if use reducing dimension
                if options.type_emb == 'fill':
                    print 'options.type_emb=fill is not supported!! for options.algo_redu=' +str(options.algo_redu) + '. Did you want to select fills?'
                    exit()

                print 'reducing dimension with ' + str(options.algo_redu)
                f=open(prefix_file_log+"1.txt",'a')          
                title_cols = np.array([["seed",seed_value," fold",index+1,"/",options.n_folds,"+++++++++++","seed",seed_value," fold",index+1,"/",options.n_folds,"+++++++++++","seed",seed_value," fold",index+1,"/",options.n_folds]])
                np.savetxt(f,title_cols, fmt="%s",delimiter="")             
                title_cols = np.array([["before reducing, tr_mi/me/ma="+ str(np.min(train_x)) + '/' + str(np.mean(train_x))+ '/'+ str(np.max(train_x))+", va_mi/me/ma="+ str(np.min(val_x)) + '/' + str(np.mean(val_x))+ '/'+str(np.max(val_x)) ]])           
                np.savetxt(f,title_cols, fmt="%s",delimiter="/")    

                t_re = time.time()
                f.close() 
                if options.algo_redu ==  "rd_pro": #if random projection
                    if options.rd_pr_seed == "None":
                        transformer = random_projection.GaussianRandomProjection(n_components=options.new_dim)
                    else:                        
                        transformer = random_projection.GaussianRandomProjection(n_components=options.new_dim, random_state = int(options.rd_pr_seed))
                    train_x = transformer.fit_transform(train_x)
                    #val_x = transformer.transform(val_x)
                elif options.algo_redu == "pca":
                    transformer = PCA(n_components=options.new_dim)
                    train_x = transformer.fit_transform(train_x)
                    #val_x = transformer.transform(val_x)
                
                elif options.algo_redu == 'fa': # FeatureAgglomeration
                    transformer = FeatureAgglomeration(n_clusters=options.new_dim)
                    train_x = transformer.fit_transform(train_x)
                    #val_x = transformer.transform(val_x)
                
                else:
                    print 'this algo_redu ' + str(options.algo_redu) + ' is not supported!'
                    exit()   

                #tranform validation and test set
                val_x = transformer.transform(val_x)
                if options.test_exte == 'y':  
                    v_data = transformer.transform(v_data)

                f=open(prefix_file_log+"1.txt",'a')    
                text_s = "after reducing, tr_mi/me/ma=" 
                text_s = text_s + str(np.min(train_x)) + '/' + str(np.mean(train_x))+ '/'+ str(np.max(train_x)) 
                text_s = text_s + ", va_mi/me/ma="+ str(np.min(val_x)) + '/' + str(np.mean(val_x))+ '/'+str(np.max(val_x)) 
                text_s = text_s + ', time_reduce=' +str(time.time()- t_re)
                title_cols = np.array([[text_s]])           
                np.savetxt(f,title_cols, fmt="%s",delimiter="/")            
                f.close()          

                #apply cordi to new size
                #when appyling to reduce dimension, no more data which still = 0, so should not use type_dat='pr'
                if options.type_emb in [ 'fills']:
                    cordi_x = []
                    cordi_y = []
                    len_square = int(math.ceil(math.sqrt(options.new_dim)))
                    print 'len_square=' + str(len_square) 
                    k = 0
                    for i in range(0,len_square):
                        for j in range(0,len_square):                            
                            if k == (options.new_dim):
                                break
                            else:
                                cordi_x.append(j*(-1))
                                cordi_y.append(i*(-1))
                                k = k+1
                        if k == (options.new_dim):
                            break
                                
                    print 'k====' +str(k)
           
            print(train_x.shape)
            print(val_x.shape)

            ##### scale mode, use for creating images/bins
            if options.scale_mode in ['minmaxscaler','quantiletransformer', 'mms','qtf'] :
                # 'fill' use orginal data with predefined bins, so do not need to use scaler because we cannot predict data distribution before scaling to set predefined bins
                if options.type_emb == 'fill':
                    print 'options.type_emb=fill is not supported!! for options.scale_mode=' +str(options.scale_mode) + '. Did you want to select fills?'
                    exit()              

                print 'before scale:' + str(np.max(train_x)) + '_' + str(np.min(train_x)) + '_' + str(np.max(val_x)) + '_'  + str(np.min(val_x))   
                if options.emb_data <> '': #if use original for embedding
                    train_x_original = train_x                
                 
                #select the algorithm for transformation
                if  options.scale_mode == 'minmaxscaler' or options.scale_mode =='mms' :       
                    scaler = MinMaxScaler(feature_range=(options.min_scale, options.max_scale)) #rescale value range [options.min_scale , options.max_scale ] 
                        #X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
                        #X_scaled = X_std * (max - min) + min
                elif options.scale_mode == 'quantiletransformer' or options.scale_mode =='qtf':  
                    scaler = QuantileTransformer(n_quantiles=options.n_quantile)                 

                #use training set to learn and apply to validation set 
                train_x = scaler.fit_transform(train_x)
                val_x = scaler.transform(val_x)       
                if options.test_exte == 'y':      
                    v_data = scaler.transform(v_data) 
               
                print 'after scale:' + str(np.max(train_x)) + '_'  + str(np.min(train_x)) + '_' + str(np.max(val_x)) + '_' + str(np.min(val_x))                   

                #get bins of training set  
                train_hist,train_bin_edges = np.histogram(train_x)
                val_hist0,val_bin_edges0 = np.histogram(val_x)
                val_hist1,val_bin_edges1 = np.histogram(val_x, bins = train_bin_edges)

                #save information on data transformed
                f=open(prefix_file_log+"1.txt",'a')          
                title_cols = np.array([["seed",seed_value," fold",index+1,"/",options.n_folds,"+++++++++++","seed",seed_value," fold",index+1,"/",options.n_folds,"+++++++++++","seed",seed_value," fold",index+1,"/",options.n_folds]])
                np.savetxt(f,title_cols, fmt="%s",delimiter="")             
                title_cols = np.array([["after scale, remained information="+ str(sum(val_hist1)) + '/' + str(sum(val_hist0))+'='+ str(float(sum(val_hist1))/sum(val_hist0))]])           
                np.savetxt(f,title_cols, fmt="%s",delimiter="/")
                title_cols = np.array([["max_train="+ str(np.max(train_x)),"min_train="+str(np.min(train_x)),"max_val="+str(np.max(val_x)),"min_val="+str(np.min(val_x))]])           
                np.savetxt(f,title_cols, fmt="%s",delimiter="/")
                np.savetxt(f,(np.histogram(val_x, bins = train_bin_edges), np.histogram(train_x, bins = train_bin_edges)), fmt="%s",delimiter="\n")
                
                f.close() 
                
                
            elif options.scale_mode == 'none':
                print 'do not use scaler'
            else:
                print 'this scaler (' + str(options.scale_mode) + ') is not supported now! Please try again!!'
                exit()

            #select type_emb in ['raw','bin','fills','tsne',...]
            if options.type_emb == "raw" or options.type_emb == "bin" : #reshape raw data into a sequence for ltsm model. 
                
                if options.type_emb == "bin" : 
                    if options.auto_v  == 'y': #if auto, adjust automatically min_v and max_v for binning
                        options.min_v = np.min(train_x)
                        options.max_v = np.max(train_x)
                    
                    temp_train_x=[]
                    temp_val_x=[]
                    temp_v_data=[]

                    for i in range(0, len(train_x)):   
                        temp_train_x.append( [vis_data.convert_bin(value=y,  type=options.type_data, min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin) for y in train_x[i] ])
                    for i in range(0, len(val_x)):   
                        temp_val_x.append( [vis_data.convert_bin(value=y,  type=options.type_data, min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin) for y in val_x[i] ])
                  
                    train_x = np.stack(temp_train_x)
                    val_x = np.stack(temp_val_x)

                    if options.test_exte == 'y':     
                        for i in range(0, len(v_data)):   
                            temp_v_data.append( [vis_data.convert_bin(value=y, type=options.type_data, min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin) for y in v_data[i] ])
                
                        v_data = np.stack(temp_v_data)

                print 'use data...' + str(options.type_emb )
                if options.model in ['model_con1d_baseline' , 'model_cnn1d']:
                    input_shape=((train_x.shape[1]),1)
                    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1],1))
                    val_x = np.reshape(val_x, (val_x.shape[0], val_x.shape[1],1))
                    if options.test_exte == 'y':     
                        v_data = np.reshape(v_data, (v_data.shape[0], v_data.shape[1],1))

                elif options.model in [ 'svm_model','rf_model']:
                    input_shape=((train_x.shape[1]))
                    train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1]))
                    val_x = np.reshape(val_x, (val_x.shape[0], val_x.shape[1]))
                    if options.test_exte == 'y':     
                        v_data = np.reshape(v_data, (v_data.shape[0], v_data.shape[1]))
                else:
                    input_shape=(1,(train_x.shape[1]))
                    train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
                    val_x = np.reshape(val_x, (val_x.shape[0], 1, val_x.shape[1]))      
                    if options.test_exte == 'y':     
                        v_data = np.reshape(v_data, (v_data.shape[0], 1, v_data.shape[1])) 
               
                print('input_shape='+str(input_shape))
                #print 'train_x:=' + str(train_x.shape)
                
               
                    
            elif options.type_emb <> "fill": #embedding type, new images after each k-fold

                #save information on bins
                f=open(prefix_file_log+"1.txt",'a')          
                if options.auto_v  == 'y': #if auto, adjust automatically min_v and max_v for binning
                    options.min_v = np.min(train_x)
                    options.max_v = np.max(train_x)
                
                title_cols = np.array([["bins for classification"]])           
                np.savetxt(f,title_cols, fmt="%s",delimiter="/")               
                #save information on histogram of bins
                w_interval = float(options.max_v - options.min_v) / options.num_bin
                binv0 = []
                for ik in range(0,options.num_bin+1):
                    binv0.append(options.min_v + w_interval*ik )

                np.savetxt(f,(np.histogram(val_x, bins = binv0), np.histogram(train_x, bins = binv0)), fmt="%s",delimiter="\n")
                f.close()

                t_img = time.time()
                # ++++++++++++ start embedding ++++++++++++

                # ++++++++++++ start to check folders where contain images ++++++++++++
                path_write= os.path.join(path_write_parentfolder_img,'s'+str(seed_value))
                print(path_write)
                #looks like: ./images/cir_p30l100i500/s1/        
                if not os.path.exists(path_write):
                    print(path_write + ' does not exist, this folder will be created...')
                    os.makedirs(os.path.join(path_write))    

                path_write= os.path.join(path_write_parentfolder_img,'s'+str(seed_value),"nfold"+str(options.n_folds))
                #looks like: ./images/cir_p30l100i500/s1/nfold10/   
                print(path_write)  
                if not os.path.exists(path_write):
                    print(path_write + ' does not exist, this folder will be created...')
                    os.makedirs(os.path.join(path_write))   
                
                path_write= os.path.join(path_write_parentfolder_img,'s'+str(seed_value),"nfold"+str(options.n_folds),"k"+str(index+1))   
                #looks like: ./images/cir_p30l100i500/s1/nfold10/k1    
                print(path_write)   
                if not os.path.exists(os.path.join(path_write)):
                    print(path_write + ' does not exist, this folder will be created...')
                    os.makedirs(os.path.join(path_write))    
                # <><><><><><> end to check folders where contain images <><><><><><>
                if options.type_emb == 'fills' and options.type_data <> 'pr': #fills: use fill-up with bins created from train-set with scale, should be used with type_data='eqw'
                    #run embbeding to create images if images do not exist     
                    if options.fig_size <= 0: #if fig_size <=0, use the smallest size which fit the data, generating images of (len_square x len_square)
                        options.fig_size = len_square
                    if (not os.path.exists(path_write+"/val_" + str(len(val_y)-1) + ".png")) or options.recreate_img > 0 :
                        #creating images if the sets of images are not completed OR requirement for creating from options.
                        for i in range(0, len(train_y)):
                            print 'img fillup train ' + str(i)            
                            vis_data.fillup_image(cor_x=cordi_x,cor_y=cordi_y,X = train_x[i], type_data=options.type_data,
                                name_file= path_write+"/train_"+str(i), fig_size = options.fig_size, 
                                min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin, alpha_v = options.alpha_v,
                                size_p =options.point_size, marker_p = options.shape_drawn, setcolor = options.setcolor , 
                                colormap = options.colormap,cmap_vmin = options.cmap_vmin,cmap_vmax = options.cmap_vmax)
                        
                        for i in range(0, len(val_y)):
                            print 'img fillup val ' + str(i)            
                            vis_data.fillup_image(cor_x=cordi_x,cor_y=cordi_y,X = val_x[i], type_data=options.type_data,
                                name_file= path_write+"/val_"+str(i), fig_size = options.fig_size, 
                                min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin, alpha_v = options.alpha_v,
                                size_p =options.point_size, marker_p = options.shape_drawn, setcolor = options.setcolor , 
                                colormap = options.colormap,cmap_vmin = options.cmap_vmin,cmap_vmax = options.cmap_vmax)      

                    
                    if options.test_exte == 'y':
                        if (not os.path.exists(path_write+"/testval_" + str(len(v_labels)-1) + ".png")) or options.recreate_img > 0 :
                            for i in range(0, len(v_labels)):
                                print 'img fillup testval ' + str(i)            
                                vis_data.fillup_image(cor_x=cordi_x,cor_y=cordi_y,X = v_data[i], type_data=options.type_data,
                                    name_file= path_write+"/testval_"+str(i), fig_size = options.fig_size, 
                                    min_v = options.min_v, max_v = options.max_v, num_bin = options.num_bin, alpha_v = options.alpha_v,
                                    size_p =options.point_size, marker_p = options.shape_drawn, setcolor = options.setcolor , 
                                    colormap = options.colormap,cmap_vmin = options.cmap_vmin,cmap_vmax = options.cmap_vmax)            

                               
                elif options.type_emb in  ['tsne','megaman','lle','isomap','mds','se','pca','rd_pro','lda','nmf'] : #if use other embeddings (not fill), then now embedding!
                         
                    # ++++++++++++ start to begin embedding ++++++++++++
                    # includes 2 steps: Step 1: embedding if does not exist, Step 2: read images

                    #run embbeding to create images if images do not exist               
                    if not os.path.exists(path_write+"/val_" + str(len(val_y)-1) + ".png") or options.recreate_img > 0 : 
                        #creating images if the sets of images are not completed OR requirement for creating from options.
                        print path_write + ' does not contain needed images, these images will be created...'
                        print 'Creating images based on ' + str(options.type_emb) + ' ... ============= '
                    
                        #compute cordinates of points in maps use either tsne/lle/isomap/mds/se
                        print 'building cordinates of points based on ' + str(options.type_emb)                   
                        if options.emb_data <> '': #if use original for embedding
                            input_x = np.transpose(train_x_original)
                        else:                                                        
                            input_x = np.transpose(train_x)                        

                        if options.type_emb =='tsne':

                            if  options.label_tsne<> "": #tsne according to label
                                if int(options.label_tsne) == 1 or int(options.label_tsne) ==0:                                
                                    input_x_filter = []
                                    #print train_y.shape
                                
                                    train_y1= train_y        
                                    #reset index to range into folds
                                    train_y1=train_y1.reset_index()     
                                    train_y1=train_y1.drop('index', 1)
                                    #print train_y1
                                    for i_tsne in range(0,len(train_y1)):
                                        #print str(i_tsne)+'_' + str(train_y1.x[i_tsne])
                                        if train_y1.x[i_tsne] == int(options.label_tsne):
                                            input_x_filter.append(train_x[i_tsne])
                                    input_x_filter = np.transpose(input_x_filter)
                                    X_embedded = TSNE (n_components=options.n_components_emb,perplexity=perplexity_x,n_iter=n_iter_x, init=options.ini_tsne,
                                        learning_rate=learning_rate_x).fit_transform( input_x_filter )  
                            else:
                                X_embedded = TSNE (n_components=options.n_components_emb,perplexity=perplexity_x,n_iter=n_iter_x, init=options.ini_tsne,
                                    learning_rate=learning_rate_x).fit_transform( input_x )  
                           
                        elif options.type_emb =='lle':   
                            X_embedded = LocallyLinearEmbedding(n_neighbors=perplexity_x, n_components=options.n_components_emb,
                                eigen_solver=options.eigen_solver, method=options.method_lle).fit_transform(input_x)
                        elif options.type_emb =='isomap': 
                            X_embedded = Isomap(n_neighbors=perplexity_x, n_components=options.n_components_emb, max_iter=n_iter_x, 
                                eigen_solver= options.eigen_solver).fit_transform(input_x)
                        elif options.type_emb =='nmf': 
                            X_embedded = NMF(n_components=options.n_components_emb, max_iter=n_iter_x).fit_transform(input_x)
                               
                        elif options.type_emb =='mds': 
                            X_embedded = MDS(n_components=options.n_components_emb, max_iter=n_iter_x,n_init=1).fit_transform(input_x)
                        elif options.type_emb =='se': 
                            if options.eigen_solver in ['none','None']:
                                X_embedded = SpectralEmbedding(n_components=options.n_components_emb,
                                    n_neighbors=perplexity_x).fit_transform(input_x)
                            else:
                                X_embedded = SpectralEmbedding(n_components=options.n_components_emb,
                                    n_neighbors=perplexity_x, eigen_solver= options.eigen_solver).fit_transform(input_x)
                        elif options.type_emb =='pca': 
                            X_embedded = PCA(n_components=options.n_components_emb).fit_transform(input_x)
                        elif options.type_emb =='rd_pro': 
                            X_embedded = random_projection.GaussianRandomProjection(n_components=options.n_components_emb).fit_transform(input_x)
                        elif options.type_emb =='lda': #supervised dimensional reductions using labels
                            print 'input_x'
                            print input_x.shape

                            phylum_inf = pd.read_csv(os.path.join(path_read, dataset_name + '_pl.csv'))
                            #print 'phylum_inf'
                            #print phylum_inf.shape
                            #print phylum_inf[:,1]
                            #phylum_inf = phylum_inf.iloc[:,1] 

                            #supported: 'svd' recommended for a large number of features;'eigen';'lsqr'
                            if options.eigen_solver in  ['eigen','lsqr']: 
                                lda = LinearDiscriminantAnalysis(n_components=2,solver=options.eigen_solver,shrinkage='auto')
                            else:
                                lda = LinearDiscriminantAnalysis(n_components=2,solver=options.eigen_solver)
                            #input_x = np.transpose(input_x)
                            #print phylum_inf.iloc[:,1] 
                            if options.label_emb <= -1:
                                print "please specify --label_emb for lda: 'kingdom=1','phylum=2','class=3','order=4','family=5','genus=6'"
                                exit
                            else:
                                phylum_inf = phylum_inf.iloc[:,options.label_emb ]                          

                            X_embedded = lda.fit(input_x, phylum_inf).transform(input_x)
                            #X_embedded = LinearDiscriminantAnalysis(
                             #    n_components=options.n_components_emb).fit_transform(np.transpose(input_x),train_y)                           
                            print X_embedded
                            #print X_embedded.shape
                     
                        else:
                            print options.type_emb + ' is not supported now!'
                            exit()
                
                        #+++++++++ CREATE IMAGE BASED ON EMBEDDING +++++++++                       
                        print 'creating global map, images for train/val sets and save coordinates....'
                        #global map
                        mean_spe=(np.mean(input_x,axis=1))    

                        if options.imp_fea in ['rf']: 
                            #print indices_imp
                            #print X_embedded [indices_imp]
                            #print mean_spe
                            #print mean_spe [indices_imp]
                            if options.imp_fea in ['rf']:
                                print 'find important features'
                            forest = RandomForestClassifier(n_estimators=500,max_depth=None,min_samples_split=2)
                            forest.fit(train_x, train_y)
                            importances = forest.feature_importances_
                            indices_imp = np.argsort(importances)
                            #indices_imp = np.argsort(importances)[::-1] #reserved order
                            f=open(path_write+'/imp.csv','a')
                            np.savetxt(f,np.c_[(indices_imp,importances)], fmt="%s",delimiter=",")
                            f.close()

                            vis_data.embed_image(X_embedded [indices_imp], X = mean_spe[indices_imp], name_file = path_write+"/global",
                                marker=options.shape_drawn,size_p= options.point_size, fig_size = options.fig_size, type_data= options.type_data,
                                margin = options.margin, alpha_v=options.alpha_v, setcolor = options.setcolor,  colormap = options.colormap,
                                min_v = options.min_v, max_v=options.max_v, num_bin = options.num_bin, 
                                cmap_vmin = options.cmap_vmin, cmap_vmax= options.cmap_vmax)
                            np.savetxt (path_write+'/coordinate.csv',X_embedded, delimiter=',')
                                            
                            #TRAIN: use X_embedded to create images; save labels
                            for i in range(0, len(train_x)):   
                                #print train_x 
                                #print train_x [i,indices_imp]                    
                                vis_data.embed_image(X_embedded [indices_imp], X = train_x [i,indices_imp],name_file =path_write+"/train_"+str(i),
                                    marker=options.shape_drawn,size_p= options.point_size, fig_size = options.fig_size, type_data= options.type_data,
                                    margin = options.margin, alpha_v=options.alpha_v, setcolor = options.setcolor, colormap = options.colormap,
                                    min_v = options.min_v, max_v=options.max_v, num_bin = options.num_bin,
                                    cmap_vmin = options.cmap_vmin, cmap_vmax= options.cmap_vmax)
                                print('created img '+"/train_"+str(i))             
                            train_y.to_csv(path_write+'/train_y.csv', sep=',')#, index=False)
                        
                            #TEST: use X_embedded to create images; save labels               
                            for i in range(0, len(val_x)):                
                                vis_data.embed_image(X_embedded [indices_imp],X = val_x [i,indices_imp],name_file = path_write+"/val_"+str(i),
                                    marker=options.shape_drawn, size_p= options.point_size, fig_size = options.fig_size, type_data= options.type_data,
                                    margin = options.margin, alpha_v=options.alpha_v, setcolor = options.setcolor, colormap = options.colormap,
                                    min_v = options.min_v, max_v=options.max_v, num_bin = options.num_bin, 
                                    cmap_vmin = options.cmap_vmin, cmap_vmax= options.cmap_vmax)
                                print('created img '+"/val_"+str(i))     
                            val_y.to_csv(path_write+'/val_y.csv', sep=',')#, index=False)   
                        else:
                            vis_data.embed_image(X_embedded, X = mean_spe, name_file = path_write+"/global",
                                marker=options.shape_drawn,size_p= options.point_size, fig_size = options.fig_size, type_data= options.type_data,
                                margin = options.margin, alpha_v=options.alpha_v, setcolor = options.setcolor,  colormap = options.colormap,
                                min_v = options.min_v, max_v=options.max_v, num_bin = options.num_bin, 
                                cmap_vmin = options.cmap_vmin, cmap_vmax= options.cmap_vmax)
                            np.savetxt (path_write+'/coordinate.csv',X_embedded, delimiter=',')
                                            
                            #TRAIN: use X_embedded to create images; save labels
                            for i in range(0, len(train_x)):                       
                                vis_data.embed_image(X_embedded, X = train_x [i,:],name_file =path_write+"/train_"+str(i),
                                    marker=options.shape_drawn,size_p= options.point_size, fig_size = options.fig_size, type_data= options.type_data,
                                    margin = options.margin, alpha_v=options.alpha_v, setcolor = options.setcolor, colormap = options.colormap,
                                    min_v = options.min_v, max_v=options.max_v, num_bin = options.num_bin,
                                    cmap_vmin = options.cmap_vmin, cmap_vmax= options.cmap_vmax)
                                print('created img '+"/train_"+str(i))             
                            train_y.to_csv(path_write+'/train_y.csv', sep=',')#, index=False)
                        
                            #TEST: use X_embedded to create images; save labels               
                            for i in range(0, len(val_x)):                
                                vis_data.embed_image(X_embedded,X = val_x [i,:],name_file = path_write+"/val_"+str(i),
                                    marker=options.shape_drawn, size_p= options.point_size, fig_size = options.fig_size, type_data= options.type_data,
                                    margin = options.margin, alpha_v=options.alpha_v, setcolor = options.setcolor, colormap = options.colormap,
                                    min_v = options.min_v, max_v=options.max_v, num_bin = options.num_bin, 
                                    cmap_vmin = options.cmap_vmin, cmap_vmax= options.cmap_vmax)
                                print('created img '+"/val_"+str(i))     
                            val_y.to_csv(path_write+'/val_y.csv', sep=',')#, index=False)                               

                    if options.test_exte == 'y':
                        if not os.path.exists(path_write+"/testval_" + str(len(v_labels)-1) + ".png") or options.recreate_img > 0 : 
                            for i in range(0, len(v_data)):
                                print 'created img testval ' + str(i)            
                                vis_data.embed_image(X_embedded,X = v_data [i,:],name_file = path_write+"/testval_"+str(i),
                                    marker=options.shape_drawn, size_p= options.point_size, fig_size = options.fig_size, type_data= options.type_data,
                                    margin = options.margin, alpha_v=options.alpha_v, setcolor = options.setcolor, colormap = options.colormap,
                                    min_v = options.min_v, max_v=options.max_v, num_bin = options.num_bin, cmap_vmin = options.cmap_vmin, cmap_vmax= options.cmap_vmax)
                        #<><><><><><> END of CREATE IMAGE BASED ON EMBEDDING <><><><><><>   
                else:
                    print  str(options.type_emb) + ' is not supported!!'
                    exit()    
                f=open(prefix_file_log+"1.txt",'a')
                title_cols = np.array([["time_read_or/and_create_img=" + str(time.time()- t_img)]])
                np.savetxt(f,title_cols, fmt="%s",delimiter="")
                f.close()   
                #+++++++++ read images for train/val sets +++++++++                
                train_x = utils.load_img_util(num_sample = len(train_y), pattern_img='train',
                    path_write = path_write , dim_img = options.dim_img, preprocess_img = options.preprocess_img, 
                    channel = options.channel,mode_pre_img = options.mode_pre_img)
                val_x = utils.load_img_util(num_sample = len(val_y), pattern_img='val',
                    path_write = path_write , dim_img = options.dim_img, preprocess_img = options.preprocess_img, 
                    channel = options.channel,mode_pre_img = options.mode_pre_img)
                if options.test_exte == 'y':
                    v_data = utils.load_img_util(num_sample = len(v_labels), pattern_img='testval',
                        path_write = path_write , dim_img = options.dim_img, preprocess_img = options.preprocess_img, 
                        channel = options.channel,mode_pre_img = options.mode_pre_img)
                #<><><><><><> END of read images for train/val sets <><><><><><>
                # <><><><><><> END of embedding <><><><><><>
               
            if options.debug == 'y':
                print(train_x.shape)
                print(val_x.shape)
                print(train_y)
                print(val_y)  
                print("size of data: whole data")
                print(data.shape)
                print("size of data: train_x")
                print(train_x.shape)
                print("size of data: val_x")
                print(val_x.shape)
                print("size of label: train_y")
                print(train_y.shape)
                print("size of label: val_y")
                print(val_y.shape)    

            #save lables of train/test set to log
            f=open(prefix_file_log+"1.txt",'a')
            title_cols = np.array([["seed",seed_value," fold",index+1,"/",options.n_folds,"###############","seed",seed_value," fold",index+1,"/",options.n_folds,"###############","seed",seed_value," fold",index+1,"/",options.n_folds]])
            np.savetxt(f,title_cols, fmt="%s",delimiter="")
            title_cols = np.array([["train_set"]])
            np.savetxt(f,title_cols, fmt="%s",delimiter="")        
            np.savetxt(f,[(train_y)], fmt="%s",delimiter=" ")
            title_cols = np.array([["validation_set"]])
            np.savetxt(f,title_cols, fmt="%s",delimiter="")    
            np.savetxt(f,[(val_y)], fmt="%s",delimiter=" ")
            f.close()   
                            
            if options.dim_img==-1 and options.type_emb <> 'raw' and options.type_emb <> 'bin': #if use real size of images
                input_shape = (train_x.shape[1],train_x.shape[2], options.channel)
            
            np.random.seed(seed_value) # for reproducibility   

            if options.type_run  in ['vis','visual']:  
                print 'mode: VISUALIZATIONS, CREATING IMAGES, NOT LEARNING'
            else:
                print 'mode: LEARNING'
                tf.set_random_seed(seed_value)     
                #rn.seed(seed_value) 
                      
                if options.e_stop==-1: #=-1 : do not use earlystopping
                    options.e_stop = epochs_num

                if options.e_stop_consec=='consec': #use sefl-defined func
                    early_stopping = models_def.EarlyStopping_consecutively(monitor='val_loss', 
                        patience=options.e_stop, verbose=1, mode='auto')
                else: #use keras func
                    early_stopping = kr.callbacks.EarlyStopping(monitor='val_loss', 
                        patience=options.e_stop, verbose=1, mode='auto')

                if options.coeff == 0: #run tuning for coef
                    print 'Error! options.coeff == 0 only use for tuning coef....'
                    exit()                                         
                        
                #+++++++++++ transform or rescale before fetch data into learning  +++++++++++
                if options.num_classes == 2:
                    train_y=kr.utils.np_utils.to_categorical(train_y)
                    val_y = kr.utils.np_utils.to_categorical(val_y)

                if options.debug == 'y':
                    print 'max_before coeff======='
                    print np.amax(train_x)
                train_x = train_x / float(options.coeff)
                val_x = val_x / float(options.coeff)   
                if options.test_exte == 'y':       
                    v_data = v_data/float(options.coeff)
                
                if options.debug == 'y':
                    print 'max_after coeff======='                 
                    print 'train='+str(np.amax(train_x))
                    if options.test_exte == 'y':       
                        print 'val_test='+str(np.amax(v_data))
                #<><><><><><> end of transform or rescale before fetch data into learning  <><><><><><>


                #++++++++++++   selecting MODELS AND TRAINING, TESTING ++++++++++++
               
                
                if options.model in  ['resnet50', 'vgg16']:
                    input_shape = Input(shape=(train_x.shape[1],train_x.shape[2], options.channel)) 
                
                model = models_def.call_model (type_model=options.model, 
                        m_input_shape= input_shape, m_num_classes= num_classes, m_optimizer = options.optimizer,
                        m_learning_rate=options.learning_rate, m_learning_decay=options.learning_rate_decay, m_loss_func=options.loss_func,
                        ml_number_filters=number_filters,ml_numlayercnn_per_maxpool=numlayercnn_per_maxpool, ml_dropout_rate_fc=dropout_rate_fc, 
                        mc_nummaxpool=nummaxpool, mc_poolsize= poolsize, mc_dropout_rate_cnn=dropout_rate_cnn, 
                        mc_filtersize=filtersize, mc_padding = options.padding,
                        svm_c=options.svm_c, svm_kernel=options.svm_kernel,rf_n_estimators=options.rf_n_estimators)
                        
                if options.visualize_model == 'y':  #visualize architecture of model  
                    from keras_sequential_ascii import sequential_model_to_ascii_printout
                    sequential_model_to_ascii_printout(model)                      

                np.random.seed(seed_value) # for reproducibility     
                tf.set_random_seed(seed_value)   
                #rn.seed(seed_value)                  
                        
                if options.model in ['svm_model', 'rf_model']:
                    print train_x.shape           
                    print 'run classic learning algorithms'  
                    model.fit(train_x, train_y)

                    if options.model in ['rf_model']: #save important and scores of features in Random Forests                    
                        if  options.save_rf == 'y':
                            importances = model.feature_importances_
                            #print importances
                            #indices_imp = np.argsort(importances)
                            #indices_imp = np.argsort(importances)[::-1] #reserved order
                            f=open(prefix_details+"s"+str(seed_value)+"k"+str(index+1)+"_importance_fea.csv",'a')
                            np.savetxt(f,np.c_[(name_features,importances)], fmt="%s",delimiter=",")
                            f.close()
                else:
                    print 'run deep learning algorithms'
                    history_callback=model.fit(train_x, train_y, 
                        epochs = epochs_num, 
                        batch_size=batch_size, verbose=1,
                        validation_data=(val_x, val_y), callbacks=[early_stopping],
                        shuffle=False)        # if shuffle=False could be reproducibility
                    print history_callback
            #<><><><><><> end of selecting MODELS AND TRAINING, TESTING  <><><><><><>

            #++++++++++++SAVE ACC, LOSS of each epoch++++++++++++     
            #               
            # print("memory=memory=memory=memory=memory=memory=memory=memory=")
            # mem_cons = process.memory_info().rss
            # mem_cons /= 1024
            # mem_cons /= 1024
            # print('Mb='+str(mem_cons))

            if options.type_run in ['vis','visual']: #only visual, not learning
                print 'mode: VISUALIZATIONS, CREATING IMAGES, NOT LEARNING, skip writing logs.... each fold'

            else: #learning
                train_acc =[]
                train_loss = []
                val_acc = []
                val_loss = []

                if options.model in ['svm_model', 'rf_model']:
            
                    ep_arr=range(1, 2, 1) #epoch         

                    train_acc.append ( -1)
                    train_loss.append ( -1)
                    val_acc .append (-1)
                    val_loss .append ( -1)
                    train_acc.append ( model.score(train_x,train_y))
                    train_loss.append ( -1)
                    val_acc .append ( model.score(val_x,val_y))
                    val_loss .append ( -1)

                else:
                    ep_arr=range(1, epochs_num+1, 1) #epoch
                    train_acc = history_callback.history['acc']  #acc
                    train_loss = history_callback.history['loss'] #loss
                    val_acc = history_callback.history['val_acc']  #acc
                    val_loss = history_callback.history['val_loss'] #loss

                #store for every epoch
                title_cols = np.array([["ep","train_loss","train_acc","val_loss","val_acc"]])  
                res=(ep_arr,train_loss,train_acc,val_loss,val_acc)
                res=np.transpose(res)
                combined_res=np.array(np.vstack((title_cols,res)))

                #save to file, a file contains acc,loss of all epoch of this fold
                print('prefix_details====')            
                print(prefix_details)   
                if options.save_optional in ['2','3','6','7'] :           
                    np.savetxt(prefix_details+"s"+str(seed_value)+"k"+str(index+1)+".txt", 
                        combined_res, fmt="%s",delimiter="\t")
                
                #<><><><><><> END of SAVE ACC, LOSS of each epoch <><><><><><>

                #++++++++++++ CONFUSION MATRIX and other scores ++++++++++++
                #train
                ep_stopped = len(train_acc)
                
                print 'epoch stopped= '+str(ep_stopped)
                early_stop_1se.append(ep_stopped)

                train_acc_1se.append (train_acc[ep_stopped-1])
                train_acc_1se_begin.append (train_acc[0] )
                train_loss_1se.append (train_loss[ep_stopped-1])
                train_loss_1se_begin.append (train_loss[0] )

                if options.model in ['svm_model', 'rf_model']:
                    Y_pred = model.predict_proba(train_x)#, verbose=2)
                    #Y_pred = model.predict(train_x) #will check auc later
                    if options.debug == 'y':
                        print Y_pred
                        print Y_pred[:,1]
                    #print Y_pred.loc[:,0].values
                    #print y_pred
                    train_auc_score=roc_auc_score(train_y, Y_pred[:,1])
                else:
                    Y_pred = model.predict(train_x, verbose=2)
                    train_auc_score=roc_auc_score(train_y, Y_pred)
                
                #store to var, global acc,auc  
                

                if num_classes==2:   
                    y_pred = np.argmax(Y_pred, axis=1)       
                    cm = confusion_matrix(np.argmax(train_y,axis=1),y_pred)
                    tn, fp, fn, tp = cm.ravel()                
                    print("confusion matrix")
                    print(cm.ravel())
                else:
                    if options.model in ['svm_model', 'rf_model']:
                        if options.debug == 'y':
                            print(Y_pred[:,1])
                        cm = confusion_matrix(train_y,Y_pred[:,1].round())
                        tn, fp, fn, tp = cm.ravel()
                    
                        print("confusion matrix")
                        print(cm.ravel())
                        
                    else:
                        if options.debug == 'y':
                            print(Y_pred.round())
                        cm = confusion_matrix(train_y,Y_pred.round())
                        tn, fp, fn, tp = cm.ravel()
                    
                        print("confusion matrix")
                        print(cm.ravel())
                
                train_tn_1se.append (tn)
                train_fp_1se.append (fp)
                train_fn_1se.append (fn) 
                train_tp_1se.append (tp)
                train_auc_1se.append (train_auc_score)

                #test
                val_acc_1se.append (val_acc[ep_stopped-1])
                val_acc_1se_begin.append (val_acc[0] )
                val_loss_1se.append (val_loss[ep_stopped-1])
                val_loss_1se_begin.append (val_loss[0] )

                if options.model in ['svm_model', 'rf_model']:
                    #Y_pred = model.predict(val_x)
                    Y_pred = model.predict_proba(val_x)#, verbose=2)
                    if options.debug == 'y':
                        print 'scores from svm/rf'
                        print Y_pred
                    val_auc_score=roc_auc_score(val_y, Y_pred[:,1])
                else:
                    Y_pred = model.predict(val_x, verbose=2)
                    if options.debug == 'y':
                        print 'scores from nn'
                        print Y_pred
                    val_auc_score=roc_auc_score(val_y, Y_pred)
                #print(Y_pred)
                print("score auc" +str(val_auc_score))          
                
                #store to var, global acc,auc  
            

                if num_classes==2:     
                    y_pred = np.argmax(Y_pred, axis=1)    
                    cm = confusion_matrix(np.argmax(val_y,axis=1),y_pred)
                    tn, fp, fn, tp = cm.ravel()
                    print("confusion matrix")
                    print(cm.ravel())
                else:
                    if options.model in ['svm_model', 'rf_model']:
                        if options.debug == 'y':
                            print(Y_pred[:,1])
                        cm = confusion_matrix(val_y,Y_pred[:,1].round())
                        tn, fp, fn, tp = cm.ravel()
                    
                        print("confusion matrix")
                        print(cm.ravel())
                    else:
                        if options.debug == 'y':
                            print(Y_pred.round())
                        cm = confusion_matrix(val_y,Y_pred.round())
                        tn, fp, fn, tp = cm.ravel()
                        print("confusion matrix")
                        print(cm.ravel())
                
                val_tn_1se.append (tn)
                val_fp_1se.append (fp)
                val_fn_1se.append (fn) 
                val_tp_1se.append (tp)
                val_auc_1se.append (val_auc_score)

                # Accuracy = TP+TN/TP+FP+FN+TN
                # Precision = TP/TP+FP
                # Recall = TP/TP+FN
                # F1 Score = 2 * (Recall * Precision) / (Recall + Precision)
                # TP*TN - FP*FN / sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

                if tp+fp == 0:
                    val_pre = 0
                else:
                    val_pre = np.around( tp/float(tp+fp),decimals=3)

                if tp+fn == 0:
                    val_recall=0
                else:
                    val_recall = np.around(tp/float(tp+fn),decimals=3)
                
                if val_recall+val_pre == 0:
                    val_f1score = 0
                else:
                    val_f1score = np.around(2 * (val_recall*val_pre)/ float(val_recall+val_pre),decimals=3)

                if math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)) == 0:
                    val_mmc = 0
                else:
                    val_mmc = np.around(float(tp*tn - fp*fn) / float(math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))),decimals=3)
                #<><><><><><> END of CONFUSION MATRIX and other scores  <><><><><><>

                val_pre_1se.append (val_pre)
                val_recall_1se.append (val_recall)
                val_f1score_1se.append (val_f1score)
                val_mmc_1se.append (val_mmc)

                f=open(prefix_file_log+"1.txt",'a')   
                t_checked=time.time()           
                # title_cols = np.array([["seed",seed_value," fold",index+1,"/",options.n_folds]])
                # np.savetxt(f,title_cols, fmt="%s",delimiter="")
                title_cols = np.array([["after training"]])           
                np.savetxt(f,title_cols, fmt="%s",delimiter="\t")
                title_cols = np.array([["t_acc","v_acc","t_auc","v_auc",'v_mmc',"t_los","v_los","time","ep_stopped"]])           
                np.savetxt(f,title_cols, fmt="%s",delimiter="--")
                np.savetxt(f,np.around(np.c_[(train_acc[ep_stopped-1],val_acc[ep_stopped-1] , train_auc_score,val_auc_score,
                    val_mmc,
                    train_loss[ep_stopped-1] , val_loss[ep_stopped-1],(t_checked - start_time),ep_stopped)], decimals=3), fmt="%s",delimiter="--")
                f.close() 

                train_acc_all.append(train_acc[ep_stopped-1])
                train_auc_all.append(train_auc_score)
                val_acc_all.append(val_acc[ep_stopped-1])
                val_auc_all.append(val_auc_score)
                val_mmc_all.append(val_mmc)
            
                #use external set
                if options.test_exte == 'y':                
                    Y_pred_v = model.predict(v_data)
                    print Y_pred_v
                    v_val_acc_score = accuracy_score(v_labels, Y_pred_v.round())
                    v_val_auc_score = roc_auc_score(v_labels, Y_pred_v)
                    v_val_mmc_score = matthews_corrcoef(v_labels, Y_pred_v.round())

                    f=open(prefix_file_log+"4.txt",'a')   
                    np.savetxt(f,np.c_[(seed_value,index+1,val_acc[ep_stopped-1],
                        val_auc_score,val_mmc, v_val_acc_score,v_val_auc_score,v_val_mmc_score)], fmt="%s",delimiter="\t")
                    f.close() 

                    if (best_mmc_allfolds_run < val_mmc) or (best_mmc_allfolds_run == val_mmc and v_val_auc_score > best_auc_allfolds_run) or (best_mmc_allfolds_run == val_mmc and v_val_auc_score == best_auc_allfolds_run and v_val_acc_score > best_acc_allfolds_run):
                        best_mmc_allfolds_run = val_mmc
                        best_mmc_allfolds_run_get = v_val_mmc_score
                        best_acc_allfolds_run = v_val_acc_score
                        best_auc_allfolds_run = v_val_auc_score

            
                #save model file         
                
                if options.save_w == 'y' : #save weights
                    options.save_optional = '7'
                    #if options.save_optional in [1,3,5,7] :
                        # serialize weights to HDF5, ***note: this might consume more memory and storage
                    model.save_weights(prefix_models+"s"+str(seed_value)+"k"+str(index+1)+".h5")
                    print("Saved model to disk")
                    #else:
                    #   print("Please set 'save_optional' in [1,3,5,7] to save the architecture of model")
                    #  exit()
                
                if options.save_optional in ['1','3','5','7'] :
                    model_json = model.to_json()
                    with open(prefix_models+"s"+str(seed_value)+"k"+str(index+1)+".json", "w") as json_file:
                        json_file.write(model_json)
        
            # <><><><><><><><><><><><><><><><><><> finish one fold  <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
            
        
        if options.type_run in ['vis','visual']: #only visual, not learning
            print 'mode: VISUALIZATIONS, CREATING IMAGES, NOT LEARNING, skip writing logs.... each run time'

        else: #learning    
            #check point after finishing one running time
            mid_time.append(time.time())   
            if seed_value == options.seed_value_begin:              
                total_t=mid_time[seed_value - options.seed_value_begin ]-start_time
                distant_t=total_t
            else:
                total_t=mid_time[seed_value- options.seed_value_begin ]-start_time
                distant_t=mid_time[seed_value - options.seed_value_begin]-mid_time[seed_value-options.seed_value_begin-1 ]           

            res=(seed_value,np.mean(early_stop_1se),
                np.mean(train_acc_1se_begin),np.mean(train_acc_1se),
                np.mean(val_acc_1se_begin),np.mean(val_acc_1se),
                np.mean(train_loss_1se_begin),np.mean(train_loss_1se),
                np.mean(val_loss_1se_begin),np.mean(val_loss_1se),
                total_t,distant_t)
            temp_all_acc_loss.append(res)       
        
            f=open(prefix_file_log+"2.txt",'a')        
            if options.save_optional in ['4','5','6','7'] :
                np.savetxt(f,np.c_[(seed_value,np.mean(early_stop_1se),
                    np.mean(train_acc_1se_begin),np.mean(train_acc_1se),
                    np.mean(val_acc_1se_begin),np.mean(val_acc_1se),
                    np.mean(train_loss_1se_begin),np.mean(train_loss_1se),
                    np.mean(val_loss_1se_begin),np.mean(val_loss_1se),
                    total_t,distant_t)], fmt="%s",delimiter="\t")
            else:
                np.savetxt(f,np.c_[(seed_value,np.mean(early_stop_1se),
                    np.mean(train_acc_1se_begin),np.mean(train_acc_1se),
                    np.mean(val_acc_1se_begin),np.mean(val_acc_1se),
                #  train_loss_1se_begin.mean(),train_loss_1se.mean(),
                #  val_loss_1se_begin.mean(),val_loss_1se.mean(),
                    total_t,distant_t)],fmt="%s",delimiter="\t")
            f.close()

            #confusion and auc
            res=(seed_value,np.mean(early_stop_1se),
                    np.mean(train_tn_1se),np.mean(train_fn_1se),
                    np.mean(train_fp_1se),np.mean(train_tp_1se),
                    np.mean(val_tn_1se),np.mean(val_fn_1se),
                    np.mean(val_fp_1se),np.mean(val_tp_1se),
                    (float((np.mean(train_tp_1se)+np.mean(train_tn_1se))/float(np.mean(train_tn_1se)+np.mean(train_fn_1se)+np.mean(train_fp_1se)+np.mean(train_tp_1se)))), #accuracy
                    (float((np.mean(val_tp_1se)+np.mean(val_tn_1se))/float(np.mean(val_tn_1se)+np.mean(val_fn_1se)+np.mean(val_fp_1se)+np.mean(val_tp_1se)))), 
                    float(np.mean(train_auc_1se)) , #auc
                    float(np.mean(val_auc_1se)) ,
                    float(np.mean(val_pre_1se)),
                    float(np.mean(val_recall_1se)),
                    float(np.mean(val_f1score_1se)),
                    float(np.mean(val_mmc_1se)))
            temp_all_auc_confusion_matrix.append(res)    

            f=open(prefix_file_log+"3.txt",'a')
            np.savetxt(f,np.c_[(seed_value,np.mean(early_stop_1se),
                    np.mean(train_tn_1se),np.mean(train_fn_1se),
                    np.mean(train_fp_1se),np.mean(train_tp_1se),
                    np.mean(val_tn_1se),np.mean(val_fn_1se),
                    np.mean(val_fp_1se),np.mean(val_tp_1se),
                    (float((np.mean(train_tp_1se)+np.mean(train_tn_1se))/float(np.mean(train_tn_1se)+np.mean(train_fn_1se)+np.mean(train_fp_1se)+np.mean(train_tp_1se)))), #accuracy
                    (float((np.mean(val_tp_1se)+np.mean(val_tn_1se))/float(np.mean(val_tn_1se)+np.mean(val_fn_1se)+np.mean(val_fp_1se)+np.mean(val_tp_1se)))), 
                    float(np.mean(train_auc_1se)) , #auc
                    float(np.mean(val_auc_1se)))],fmt="%s",delimiter="\t")
            f.close()
        # <><><><><><><><><><><><><><><><><><> END of all folds of a running time <><><><><><><><><><><><><><><><><><><><><><><><>
    
    
    if options.type_run in ['vis','visual']: #only visual, not learning
        print 'mode: VISUALIZATIONS, CREATING IMAGES, NOT LEARNING, skip writing logs.... skip collecting results'
        print 'images were created successfully at ' + path_write

    else: #learning  
        #update to the end of file the mean/sd of all results (acc,loss,...): file2
        f=open(prefix_file_log+"2.txt",'a')
        acc_loss_mean=np.around(np.mean(temp_all_acc_loss, axis=0),decimals=3)
        acc_loss_std=np.around(np.std(temp_all_acc_loss, axis=0),decimals=3)
        np.savetxt(f,acc_loss_mean, fmt="%s",newline="\t")
        np.savetxt(f,acc_loss_std, fmt="%s",newline="\t",header="\n")
        f.close() 
        f.close() 

        #update to the end of file the mean/sd of all results (auc, tn, tp,...): file3
        f=open(prefix_file_log+"3.txt",'a')
        auc_mean=np.around(np.mean(temp_all_auc_confusion_matrix, axis=0),decimals=3)
        auc_std=np.around(np.std(temp_all_auc_confusion_matrix, axis=0),decimals=3)
        np.savetxt(f,auc_mean, fmt="%s",newline="\t")
        np.savetxt(f,auc_std, fmt="%s",newline="\t",header="\n")
        f.close() 

        finish_time=time.time()
        #save final results to the end of file1
        
        
        f=open(prefix_file_log+"1.txt",'a')
        title_cols = np.array([['time','tr_ac',"va_ac","sd","va_au","sd","tn","fn","fp","tp","preci","sd","recall","sd","f1","sd","mmc","sd","epst"]])
        np.savetxt(f,title_cols, fmt="%s",delimiter="\t")   
        TN=auc_mean[6]
        FN=auc_mean[7]
        FP=auc_mean[8]
        TP=auc_mean[9]
        precision=auc_mean[14]
        recall=auc_mean[15]
        f1_score=auc_mean[16]
        mmc=auc_mean[17]

        np.savetxt(f,np.c_[ (np.around( finish_time-start_time,decimals=1),acc_loss_mean[3],acc_loss_mean[5],acc_loss_std[5],auc_mean[13],auc_std[13], 
            TN, FN, FP, TP,precision,auc_std[14],recall,auc_std[15],f1_score,auc_std[16],mmc,auc_std[17],auc_mean[1])],
            fmt="%s",delimiter="\t")
        

        #update name file to acknowledge the running done!
        print 'acc='+str(acc_loss_mean[5])
        
        #append "ok" as marked "done!"  
        if options.test_exte == 'y':
            
            title_cols = np.array([['tr_ac_a','sd_ac',"va_ac_a","sd_ac",'tr_au_a',
                'sd_au',"va_au_a","sd_au",'va_mc_a','sd_mc','mcc_best','auc_best','acc_best','mmc_valtest']])
            np.savetxt(f,title_cols, fmt="%s",delimiter="\t")   
            np.savetxt(f,np.c_[ (
                np.mean(train_acc_all, axis=0),
                np.std(train_acc_all, axis=0),
                np.mean(val_acc_all, axis=0),
                np.std(val_acc_all, axis=0),
                #len(train_acc_all), #in order to check #folds * #run
                #len(val_acc_all),
                np.mean(train_auc_all, axis=0),
                np.std(train_auc_all, axis=0),
                np.mean(val_auc_all, axis=0),
                np.std(val_auc_all, axis=0),
                np.mean(val_mmc_all, axis=0),
                np.std(val_mmc_all, axis=0),
                best_mmc_allfolds_run,
                best_auc_allfolds_run,
                best_acc_allfolds_run,
                best_mmc_allfolds_run_get
                #len(train_auc_all),
                #len(val_auc_all)
                )] , fmt="%s",delimiter="\t")
        else:
            title_cols = np.array([['tr_ac_a','sd_ac',"va_ac_a","sd_ac",'tr_au_a','sd_au',"va_au_a","sd_au",'va_mc_a','sd_mc']])
            np.savetxt(f,title_cols, fmt="%s",delimiter="\t")   
            np.savetxt(f,np.c_[ (
                np.mean(train_acc_all, axis=0),
                np.std(train_acc_all, axis=0),
                np.mean(val_acc_all, axis=0),
                np.std(val_acc_all, axis=0),
                #len(train_acc_all), #in order to check #folds * #run
                #len(val_acc_all),
                np.mean(train_auc_all, axis=0),
                np.std(train_auc_all, axis=0),
                np.mean(val_auc_all, axis=0),
                np.std(val_auc_all, axis=0),
                np.mean(val_mmc_all, axis=0),
                np.std(val_mmc_all, axis=0)
                #len(train_auc_all),
                #len(val_auc_all)
                )] , fmt="%s",delimiter="\t")
        
        f.close()   
        if options.cudaid > -1:    
            os.rename(res_dir + "/" + prefix+"file1.txt", res_dir + "/" + prefix+"gpu"+ str(options.cudaid) + "file1_"+str(options.suff_fini)+".txt")  
        else:
            os.rename(prefix_file_log+"1.txt", prefix_file_log+"1_"+str(options.suff_fini)+".txt")  
                    