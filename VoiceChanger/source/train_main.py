#region need to train and inference
import os
import sys

now_dir = os.getcwd()
sys.path.append(now_dir)

import train_module as train
#endregion need to train and inference

#---------example train----------#

new_model_name = input("enter new models name: ")
total_epoch = 2 #at least 2
save_each_epoch = 2

train.vc_train(new_model_name, total_epoch, save_each_epoch)

input("\nany key to exit\n")