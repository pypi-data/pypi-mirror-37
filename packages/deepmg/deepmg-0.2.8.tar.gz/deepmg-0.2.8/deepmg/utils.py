"""
======================================================================================
UTILS functions
======================================================================================
Author: Thanh Hai Nguyen
date: 20/12/2017 (updated to 31/10/2018, stable version)'
'this module includes:
'1. find_files: find files based on a given pattern, aiming to avoid repeating the experiments
'2. load_img_util: load images
'3. name_log_final: support to name log files
'4. para_cmd: get parameters from command line when running the package
'5. para_config_file: read parameters from a given config file
'6. write_para: write parameters of an experiment to a config file 
"""

#from scipy.misc import imread
import numpy as np
import os, fnmatch
import math
from optparse import OptionParser
import ConfigParser



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
        pattern_img (string): the pattern names of images (eg. 'img_1.png, img_2.png,...' so pattern='img') 
        num_sample (int) : the number of images read
        dim_img: dimension of images
        preprocess_img: preprocessing images, support: vgg16, vgg19, resnet50, incep
        path_write: path to save images

    Returns:
        array
    """
    from keras.preprocessing import image
    from keras.applications.resnet50 import preprocess_input as pre_resnet50
    from keras.applications.vgg16 import preprocess_input as pre_vgg16
    from keras.applications.vgg19 import preprocess_input as pre_vgg19
    from keras.applications.inception_v3 import  preprocess_input as pre_incep
    
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

def name_log_final(arg, n_time_text):
    """ naming for log file
    Args:
        arg (array): arguments input from keybroad
        n_time_text (string) : beginning time
    Returns:
        a string (use for either prefix or suffix for name of log)
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
    parser.add_option("-a", "--type_run", choices=['vis','visual','learn','train'], default='learn', help="select a mode to run") 
    parser.add_option("--time_run", type="int", default=10, help="give the #runs (default:10)") 
    parser.add_option("--config_file", type="string", default='', help="specify config file if reading parameters from files") 
    parser.add_option("--seed_value_begin", type="int", default=1, help="set the beginning seed for different runs (default:1)")
    parser.add_option("--channel", type="int", default=3, help="channel of images, 1: gray, 2: color (default:3)") 
    parser.add_option("-m", "--dim_img", type="int", default=-1, help="width or height (square) of images, -1: get real size of original images (default:-1)") 
    parser.add_option("-k", "--n_folds", type="int", default=10, help="number of k folds (default:10)") 
    parser.add_option("--test_exte", choices=['n','y'], default='n', help="if==y, using external validation sets (default:n)")
        #training (*_x.csv) and test on test set (*_y.csv), then selecting the best model to evaluate on val set (*_zx.csv) and (*_zy.csv)
    
    ## folders/paths    
    parser.add_option("--parent_folder_img", type="string", default='images', help="name of parent folder containing images (default:images)") 
    #parser.add_option("--pattern_img", type="string", default='0',help="pattern of images")   
    parser.add_option("-r","--original_data_folder", type="string", default='data', help="parent folder containing data (default:data)")
    parser.add_option("-i", "--data_dir_img", type="string", default='', help="name of dataset to run the experiment") 
    parser.add_option('--search_already', choices=['n','y'], default='y', help="earch existed experiments before running-->if existed, stopping the experiment (default:y)")   
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
    parser.add_option("--debug", choices=['n','y'], default='n', help="show DEBUG if y (default:n)")
    parser.add_option('-v',"--visualize_model", choices=['n','y'], default='n', help="visualize the model")     
    parser.add_option('--save_w', choices=['n','y'], default='n', help="save weight mode")   
    parser.add_option('--suff_fini', type="string", default='ok', help="append suffix when finishing (default:ok)")     
    parser.add_option('--save_rf', choices=['n','y'], default='n', help="save important features and scores for Random Forests")  
    parser.add_option('--save_para', choices=['n','y'], default='n', help="save parameters to files")  
    parser.add_option('--path_config_w', type="string", default='',help="if empty, save to the same folder of the results")              
   
    
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
    parser.add_option("--del0", choices=['n','y'], default='y', help="if yes, delete features have nothing") 
  
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
    parser.add_option("--point_size", type="float", default=1.0, help="point size for img (default:1)") 
        #'point_size' should be 1 which aims to avoid overlapping
    parser.add_option("--setcolor", type="string", default="color", help="mode color for images (gray/color) (default:color)") 
    parser.add_option("--colormap", type="string", default="", help="colormap for color images (diviris/gist_rainbow/rainbow/nipy_spectral/jet/Paired/Reds/YlGnBu) (default:'')") 
    parser.add_option("--cmap_vmin", type="float", default=0.0, help="vmin for cmap (default:0)") 
    parser.add_option("--cmap_vmax", type="float", default=1.0, help="vmax for cmap (default:1)")     
    parser.add_option("--margin", type="float", default=0.0, help="margin to images (default:0)")
    parser.add_option("--alpha_v", type="float", default=1.0, help="The alpha blending value, between 0 (transparent) and 1 (opaque) (default:1)") 
    parser.add_option("--recreate_img", type="int", default=0, help="if >0 rerun to create images even though they are existing (default:0)") 

    ## binning and scaling ===================================================================================================================
    ## ===============================================================================================================================
    parser.add_option("--scale_mode", type='choice', choices=['minmaxscaler','mms','none','quantiletransformer','qtf'], default='none', help="scaler mode for input (default:none)")
    parser.add_option('--n_quantile', type="int", default=1000, help="n_quantile in quantiletransformer (default:1000)")      
    parser.add_option('--min_scale', type="float", default=0.0, help="minimum value for scaling (only for minmaxscaler) (default:0) use if --auto_v=0") 
    parser.add_option('--max_scale', type="float", default=1.0, help="maximum value for scaling (only for minmaxscaler) (default:1) use if --auto_v=0")     
    parser.add_option("--min_v", type="float", default=1e-7, help="limit min for Equal Width Binning (default:1e-7)") 
    parser.add_option("--max_v", type="float", default=0.0065536, help="limit min for Equal Width Binning (default:0.0065536)") 
    parser.add_option("--num_bin", type="int", default=10, help="the number of bins (default:10)")
    parser.add_option("--auto_v", type="int", default=0, help="if > 0, auto adjust min_v and max_v (default:0)")       
        
    ## Architecture for training ======================================================================================== 
    ## ===============================================================================================================================  
    parser.add_option("-f", "--numfilters", type="int", default=64, help="#filters/neurons for each cnn/neural layer (default:64)") 
    parser.add_option("-n", "--numlayercnn_per_maxpool", type="int", default=1, help="#cnnlayer before each max pooling (default:1)") 
    parser.add_option("--nummaxpool", type="int", default=1, help="#maxpooling_layer (default:1)") 
    parser.add_option("--dropout_cnn", type="float", default=0.0, help="dropout rate for CNN layer(s) (default:0)") 
    parser.add_option("-d", "--dropout_fc", type="float", default=0.0, help="dropout rate for FC layer(s) (default:0)") 
 
    parser.add_option("--padding", type='choice', choices=['1', '0'], default='1', help="='1' uses pad, others: does not use (default:1)") 
    parser.add_option("--filtersize", type="int", default=3, help="the filter size (default:3)") 
    parser.add_option("--poolsize", type="int", default=2, help="the pooling size (default:2)") 
    parser.add_option("--model", type="string", default = 'fc_model', 
        help="type of model (fc_model/model_cnn1d/model_cnn/model_vgglike/model_lstm/resnet50/rf_model/svm_model/none) (none: only visualization not learning)")   
    
    
    ## learning parameters ==========================================================================================================
    ## ===============================================================================================================================   
    parser.add_option("-c", "--num_classes", type="int", default=1 ,help="the output of the network (default:1)")    
    parser.add_option("-e", "--epoch", type="int", default=500 ,help="the epoch used for training (default:500)")   
    parser.add_option("--learning_rate", type="float", default=-1.0, help="learning rate, if -1 use default value of the optimizer (default:-1)")   
    parser.add_option("--batch_size", type="int", default=16, help="batch size (default:16)")
    parser.add_option("--learning_rate_decay", type="float", default=0.0,  help="learning rate decay (default:0)")
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
    parser.add_option('-z',"--coeff", type="float", default=1.0, help="coeffiency (divided) for input (should use 255 for images) (default:1)")
    parser.add_option("--grid_coef_time", type="int", default=10, help="choose the best coef from #coef default for tuning coeficiency (default:5)")
    parser.add_option("--cv_coef_time", type="int", default=4, help="k-cross validation for each coef for tuning coeficiency (default:4)")
    parser.add_option("--coef_ini", type="float", default=255.0, help="initilized coefficient for tuning coeficiency (default:255)")
    parser.add_option("--metric_selection", type="string", default="roc_auc", help="roc_auc/accuracy/neg_log_loss/grid_search_mmc for tuning coeficiency (default:roc_auc)")

    (options, args) = parser.parse_args()
    return (options, args)

def para_config_file (options):
    '''
    READ parameters provided from a configuration file
    these parameters in the configuration file are fixed, 
    modify these parameters from cmd will not work, only can modify in the configuration file

    Args:
        options (array): array of parameters
    '''

    config = ConfigParser.ConfigParser()

    #read config file
    config.read (options.config_file)

    if config.has_option('experiment','type_run'):
        options.type_run=config.get('experiment','type_run')
    if config.has_option('experiment','time_run'):
        options.time_run=int(config.get('experiment','time_run'))
    #if config.has_option('experiment','config_file'):
    #    options.config_file=config.get('experiment','config_file')
    if config.has_option('experiment','seed_value_begin'):
        options.seed_value_begin=int(config.get('experiment','seed_value_begin'))
    if config.has_option('Visual','channel'):
        options.channel=int(config.get('Visual','channel'))
    if config.has_option('Visual','dim_img'):
        options.dim_img=int(config.get('Visual','dim_img'))
    if config.has_option('Learning','n_folds'):
        options.n_folds=int(config.get('Learning','n_folds'))
    if config.has_option('Learning','test_exte'):
        options.test_exte=config.get('Learning','test_exte')
    if config.has_option('In_out','parent_folder_img'):
        options.parent_folder_img=config.get('In_out','parent_folder_img')
    if config.has_option('In_out','original_data_folder'):
        options.original_data_folder=config.get('In_out','original_data_folder')
    if config.has_option('In_out','data_dir_img'):
        options.data_dir_img=config.get('In_out','data_dir_img')
    #if config.has_option('experiment','search_already'):
        #options.search_already=config.get('experiment','search_already')
    if config.has_option('experiment','cudaid'):
        options.cudaid=int(config.get('experiment','cudaid'))
    if config.has_option('Learning','preprocess_img'):
        options.preprocess_img=config.get('Learning','preprocess_img')
    if config.has_option('In_out','mode_pre_img'):
        options.mode_pre_img=config.get('In_out','mode_pre_img')
    if config.has_option('In_out','parent_folder_results'):
        options.parent_folder_results=config.get('In_out','parent_folder_results')
    if config.has_option('In_out','save_optional'):
        options.save_optional=config.get('In_out','save_optional')
    if config.has_option('In_out','debug'):
        options.debug=config.get('In_out','debug')
    if config.has_option('Visual','visualize_model'):
        options.visualize_model=config.get('Visual','visualize_model')
    if config.has_option('In_out','save_w'):
        options.save_w=config.get('In_out','save_w')
    if config.has_option('In_out','suff_fini'):
        options.suff_fini=config.get('In_out','suff_fini')
    if config.has_option('In_out','save_rf'):
        options.save_rf=config.get('In_out','save_rf')
    #if config.has_option('In_out','save_para'):
        #options.save_para=config.get('In_out','save_para')
    if config.has_option('In_out','path_config_w'):
        options.path_config_w=config.get('In_out','path_config_w')
    if config.has_option('Visual','algo_redu'):
        options.algo_redu=config.get('Visual','algo_redu')
    if config.has_option('experiment','rd_pr_seed'):
        options.rd_pr_seed=config.get('experiment','rd_pr_seed')
    if config.has_option('Vis_learn','new_dim'):
        options.new_dim=int(config.get('Vis_learn','new_dim'))
    if config.has_option('Visual','reduc_perle'):
        options.reduc_perle=int(config.get('Visual','reduc_perle'))
    if config.has_option('Visual','reduc_ini'):
        options.reduc_ini=config.get('Visual','reduc_ini')
    if config.has_option('experiment','rnd_seed'):
        options.rnd_seed=config.get('experiment','rnd_seed')
    if config.has_option('Visual','type_emb'):
        options.type_emb=config.get('Visual','type_emb')
    if config.has_option('Visual','imp_fea'):
        options.imp_fea=config.get('Visual','imp_fea')
    if config.has_option('Visual','label_emb'):
        options.label_emb=int(config.get('Visual','label_emb'))
    if config.has_option('Visual','emb_data'):
        options.emb_data=config.get('Visual','emb_data')
    if config.has_option('Visual','type_data'):
        options.type_data=config.get('Visual','type_data')
    if config.has_option('Vis_learn','del0'):
        options.del0=config.get('Vis_learn','del0')
    if config.has_option('Visual','perlexity_neighbor'):
        options.perlexity_neighbor=int(config.get('Visual','perlexity_neighbor'))
    if config.has_option('Vis_learn','lr_tsne'):
        options.lr_tsne=float(config.get('Vis_learn','lr_tsne'))
    if config.has_option('Vis_learn','label_tsne'):
        options.label_tsne=config.get('Vis_learn','label_tsne')
    if config.has_option('Vis_learn','iter_tsne'):
        options.iter_tsne=int(config.get('Vis_learn','iter_tsne'))
    if config.has_option('Vis_learn','ini_tsne'):
        options.ini_tsne=config.get('Vis_learn','ini_tsne')
    if config.has_option('Visual','n_components_emb'):
        options.n_components_emb=int(config.get('Visual','n_components_emb'))
    if config.has_option('Vis_learn','method_lle'):
        options.method_lle=config.get('Vis_learn','method_lle')
    if config.has_option('Vis_learn','eigen_solver'):
        options.eigen_solver=config.get('Vis_learn','eigen_solver')
    if config.has_option('Visual','shape_drawn'):
        options.shape_drawn=config.get('Visual','shape_drawn')
    if config.has_option('Visual','fig_size'):
        options.fig_size=int(config.get('Visual','fig_size'))
    if config.has_option('Visual','point_size'):
        options.point_size=float(config.get('Visual','point_size'))
    if config.has_option('Visual','setcolor'):
        options.setcolor=config.get('Visual','setcolor')
    if config.has_option('Visual','colormap'):
        options.colormap=config.get('Visual','colormap')
    if config.has_option('Vis_learn','cmap_vmin'):
        options.cmap_vmin=float(config.get('Vis_learn','cmap_vmin'))
    if config.has_option('Vis_learn','cmap_vmax'):
        options.cmap_vmax=float(config.get('Vis_learn','cmap_vmax'))
    if config.has_option('Visual','margin'):
        options.margin=float(config.get('Visual','margin'))
    if config.has_option('Visual','alpha_v'):
        options.alpha_v=float(config.get('Visual','alpha_v'))
    if config.has_option('Visual','recreate_img'):
        options.recreate_img=int(config.get('Visual','recreate_img'))
    if config.has_option('Vis_learn','scale_mode'):
        options.scale_mode=config.get('Vis_learn','scale_mode')
    if config.has_option('Vis_learn','n_quantile'):
        options.n_quantile=int(config.get('Vis_learn','n_quantile'))
    if config.has_option('Vis_learn','min_scale'):
        options.min_scale=float(config.get('Vis_learn','min_scale'))
    if config.has_option('Vis_learn','max_scale'):
        options.max_scale=float(config.get('Vis_learn','max_scale'))
    if config.has_option('Vis_learn','min_v'):
        options.min_v=float(config.get('Vis_learn','min_v'))
    if config.has_option('Vis_learn','max_v'):
        options.max_v=float(config.get('Vis_learn','max_v'))
    if config.has_option('Vis_learn','num_bin'):
        options.num_bin=int(config.get('Vis_learn','num_bin'))
    if config.has_option('Vis_learn','auto_v'):
        options.auto_v=config.get('Vis_learn','auto_v')
    if config.has_option('model','numfilters'):
        options.numfilters=int(config.get('model','numfilters'))
    if config.has_option('model','numlayercnn_per_maxpool'):
        options.numlayercnn_per_maxpool=int(config.get('model','numlayercnn_per_maxpool'))
    if config.has_option('model','nummaxpool'):
        options.nummaxpool=int(config.get('model','nummaxpool'))
    if config.has_option('model','dropout_cnn'):
        options.dropout_cnn=float(config.get('model','dropout_cnn'))
    if config.has_option('model','dropout_fc'):
        options.dropout_fc=float(config.get('model','dropout_fc'))
    if config.has_option('model','padding'):
        options.padding=int(config.get('model','padding'))
    if config.has_option('model','filtersize'):
        options.filtersize=int(config.get('model','filtersize'))
    if config.has_option('model','poolsize'):
        options.poolsize=int(config.get('model','poolsize'))
    if config.has_option('model','model'):
        options.model=config.get('model','model')
    if config.has_option('model','num_classes'):
        options.num_classes=int(config.get('model','num_classes'))
    if config.has_option('model','epoch'):
        options.epoch=int(config.get('model','epoch'))
    if config.has_option('model','learning_rate'):
        options.learning_rate=float(config.get('model','learning_rate'))
    if config.has_option('model','batch_size'):
        options.batch_size=int(config.get('model','batch_size'))
    if config.has_option('model','learning_rate_decay'):
        options.learning_rate_decay=float(config.get('model','learning_rate_decay'))
    if config.has_option('model','momentum'):
        options.momentum=float(config.get('model','momentum'))
    if config.has_option('model','optimizer'):
        options.optimizer=config.get('model','optimizer')
    if config.has_option('model','loss_func'):
        options.loss_func=config.get('model','loss_func')
    if config.has_option('model','e_stop'):
        options.e_stop=int(config.get('model','e_stop'))
    if config.has_option('model','e_stop_consec'):
        options.e_stop_consec=config.get('model','e_stop_consec')
    if config.has_option('model','svm_c'):
        options.svm_c=float(config.get('model','svm_c'))
    if config.has_option('model','svm_kernel'):
        options.svm_kernel=config.get('model','svm_kernel')
    if config.has_option('model','rf_n_estimators'):
        options.rf_n_estimators=int(config.get('model','rf_n_estimators'))
    if config.has_option('model','coeff'):
        options.coeff=float(config.get('model','coeff'))
    if config.has_option('grid_search','grid_coef_time'):
        options.grid_coef_time=int(config.get('grid_search','grid_coef_time'))
    if config.has_option('grid_search','cv_coef_time'):
        options.cv_coef_time=int(config.get('grid_search','cv_coef_time'))
    if config.has_option('grid_search','coef_ini'):
        options.coef_ini=float(config.get('grid_search','coef_ini'))
    if config.has_option('grid_search','metric_selection'):
        options.metric_selection=config.get('grid_search','metric_selection')
  
def write_para(options,configfile):
    '''
    WRITE parameters TO FILE configfile (included path)
    
    Args:
        options (array): array of parameters
        configfile (string): file to write
    '''
    Config = ConfigParser.ConfigParser()

    Config.add_section('experiment')
    Config.add_section('Visual')
    Config.add_section('Learning')
    Config.add_section('In_out')    
    Config.add_section('Vis_learn')
    Config.add_section('model')
    Config.add_section('grid_search')

    Config.set('experiment','type_run',options.type_run)
    Config.set('experiment','time_run',options.time_run)
    #Config.set('experiment','config_file',options.config_file)
    Config.set('experiment','seed_value_begin',options.seed_value_begin)
    Config.set('Visual','channel',options.channel)
    Config.set('Visual','dim_img',options.dim_img)
    Config.set('Learning','n_folds',options.n_folds)
    Config.set('Learning','test_exte',options.test_exte)
    Config.set('In_out','parent_folder_img',options.parent_folder_img)
    Config.set('In_out','original_data_folder',options.original_data_folder)
    Config.set('In_out','data_dir_img',options.data_dir_img)
    #Config.set('experiment','search_already',options.search_already)
    Config.set('experiment','cudaid',options.cudaid)
    Config.set('Learning','preprocess_img',options.preprocess_img)
    Config.set('In_out','mode_pre_img',options.mode_pre_img)
    Config.set('In_out','parent_folder_results',options.parent_folder_results)
    Config.set('In_out','save_optional',options.save_optional)
    Config.set('In_out','debug',options.debug)
    Config.set('Visual','visualize_model',options.visualize_model)
    Config.set('In_out','save_w',options.save_w)
    Config.set('In_out','suff_fini',options.suff_fini)
    Config.set('In_out','save_rf',options.save_rf)
    #Config.set('In_out','save_para',options.save_para)
    Config.set('In_out','path_config_w',options.path_config_w)
    Config.set('Visual','algo_redu',options.algo_redu)
    Config.set('experiment','rd_pr_seed',options.rd_pr_seed)
    Config.set('Vis_learn','new_dim',options.new_dim)
    Config.set('Visual','reduc_perle',options.reduc_perle)
    Config.set('Visual','reduc_ini',options.reduc_ini)
    Config.set('experiment','rnd_seed',options.rnd_seed)
    Config.set('Visual','type_emb',options.type_emb)
    Config.set('Visual','imp_fea',options.imp_fea)
    Config.set('Visual','label_emb',options.label_emb)
    Config.set('Visual','emb_data',options.emb_data)
    Config.set('Visual','type_data',options.type_data)
    Config.set('Vis_learn','del0',options.del0)
    Config.set('Visual','perlexity_neighbor',options.perlexity_neighbor)
    Config.set('Vis_learn','lr_tsne',options.lr_tsne)
    Config.set('Vis_learn','label_tsne',options.label_tsne)
    Config.set('Vis_learn','iter_tsne',options.iter_tsne)
    Config.set('Vis_learn','ini_tsne',options.ini_tsne)
    Config.set('Visual','n_components_emb',options.n_components_emb)
    Config.set('Vis_learn','method_lle',options.method_lle)
    Config.set('Vis_learn','eigen_solver',options.eigen_solver)
    Config.set('Visual','shape_drawn',options.shape_drawn)
    Config.set('Visual','fig_size',options.fig_size)
    Config.set('Visual','point_size',options.point_size)
    Config.set('Visual','setcolor',options.setcolor)
    Config.set('Visual','colormap',options.colormap)
    Config.set('Vis_learn','cmap_vmin',options.cmap_vmin)
    Config.set('Vis_learn','cmap_vmax',options.cmap_vmax)
    Config.set('Visual','margin',options.margin)
    Config.set('Visual','alpha_v',options.alpha_v)
    Config.set('Visual','recreate_img',options.recreate_img)
    Config.set('Vis_learn','scale_mode',options.scale_mode)
    Config.set('Vis_learn','n_quantile',options.n_quantile)
    Config.set('Vis_learn','min_scale',options.min_scale)
    Config.set('Vis_learn','max_scale',options.max_scale)
    Config.set('Vis_learn','min_v',options.min_v)
    Config.set('Vis_learn','max_v',options.max_v)
    Config.set('Vis_learn','num_bin',options.num_bin)
    Config.set('Vis_learn','auto_v',options.auto_v)
    Config.set('model','numfilters',options.numfilters)
    Config.set('model','numlayercnn_per_maxpool',options.numlayercnn_per_maxpool)
    Config.set('model','nummaxpool',options.nummaxpool)
    Config.set('model','dropout_cnn',options.dropout_cnn)
    Config.set('model','dropout_fc',options.dropout_fc)
    Config.set('model','padding',options.padding)
    Config.set('model','filtersize',options.filtersize)
    Config.set('model','poolsize',options.poolsize)
    Config.set('model','model',options.model)
    Config.set('model','num_classes',options.num_classes)
    Config.set('model','epoch',options.epoch)
    Config.set('model','learning_rate',options.learning_rate)
    Config.set('model','batch_size',options.batch_size)
    Config.set('model','learning_rate_decay',options.learning_rate_decay)
    Config.set('model','momentum',options.momentum)
    Config.set('model','optimizer',options.optimizer)
    Config.set('model','loss_func',options.loss_func)
    Config.set('model','e_stop',options.e_stop)
    Config.set('model','e_stop_consec',options.e_stop_consec)
    Config.set('model','svm_c',options.svm_c)
    Config.set('model','svm_kernel',options.svm_kernel)
    Config.set('model','rf_n_estimators',options.rf_n_estimators)
    Config.set('model','coeff',options.coeff)
    Config.set('grid_search','grid_coef_time',options.grid_coef_time)
    Config.set('grid_search','cv_coef_time',options.cv_coef_time)
    Config.set('grid_search','coef_ini',options.coef_ini)
    Config.set('grid_search','metric_selection',options.metric_selection)   
    #save configuration file
    with open(configfile, 'w') as f:
        Config.write(f)

def validation_para(options):
    '''
    check whether parameters are valid or not
    # refer https://stackoverflow.com/questions/287871/print-in-terminal-with-colors to find a color to display the error
    '''
    
    
    if options.data_dir_img == '':
        print   "Please specify the dataset " + '\x1b[1;33;41m' + '--data_dir_img' + '\x1b[0m'
        exit()

    if options.type_run in ['vis','visual'] and options.type_emb in ['raw','bin']:
        print "Visualization cannot be made with 1D! Please select " + '\x1b[1;33;41m' + '--type_emb' + '\x1b[0m'+ " with Fill-up or t-SNE or another manifold learning!"
        exit()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'