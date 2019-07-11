# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:18:44 2019

@author: 张鹏举

import os
print os.path.dirname(os.path.realpath(__file__))


os.path.realpath

os.path.abspath    两者之间的区别

os.path.abspath()返回绝对路径，但不处理符号链接(注意linux中的符号链接不同于windows中的快捷方式)

os.path.realpath()先处理路径中的符号链接，再返回绝对路径
"""
import croe.trait
import re
import glob
import os
import sys
import importlib

path = os.path.dirname(os.path.realpath(__file__))+'\\trait\\'

class TraitAPI:

    def trait_info(self): #返回所有特征函数的{文件绝对路径：特征类， 。。。。。。}
        
        file_list = glob.glob(path + '*.py')
        
        file_list.remove(path + '__init__.py')
        
        file_list.remove(path + 'spider.py')

        info_dict = {}

        for i in file_list:

            regex = 'class (.*?):'

            with open(i, encoding = 'utf-8') as f:

                content = f.read()

                class_name = re.findall(regex, content)[0]

            info_dict[i] = class_name


        return info_dict

    def trait_obj(self):#返回所有特征函数的{网站域名：特征类， 。。。。。}

        trait_dict = {}
       
        trait_info = self.trait_info()

        for i in trait_info:

            module_name = os.path.split(i)[1].replace('.py', '')

            module = importlib.import_module(module_name)

            module_class = getattr(module, trait_info[i])

            trait_dict[module_class.domain] = module_class

        return trait_dict
            

            

        


    
if __name__ == '__main__':


    x = TraitAPI()
    info = x.trait_info()


    
    
    
    
        
        
        
        
    
    
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
