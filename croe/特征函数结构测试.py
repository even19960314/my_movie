# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:28:58 2019

@author: 一文 --最远的你们是我最近的爱
"""
import unittest

from bj import Filmbj

import types

class TestFilmTrait(unittest.TestCase):
    
        
    trait_obj = Filmbj()#要测试的类实例请自行修改
    
    show_page_list = trait_obj.get_all_show_page_url()[:20]
    
    host = trait_obj.domain
    
    def test_func_name(self):#检查类中的的名称是否安要求写
        
        func_name = dir(self.trait_obj)
        
        self.assertTrue('get_film_info' in func_name)       
        self.assertTrue('film_search' in func_name)
        self.assertTrue('get_show_page_info' in func_name)
        self.assertTrue('get_all_show_page_url' in func_name)
        self.assertTrue('get_all_show_page_url_yield' in func_name)
        
        
        

    def test_get_all_show_page(self):#测试获取网站所有show_page页面的链接
        
        self.assertTrue(isinstance(self.show_page_list, list))#函数返回值为list
        self.assertTrue(bool(self.show_page_list))#返回值不能为空
        self.assertTrue(self.host in self.show_page_list[0])#必须是全链接
        self.assertTrue(isinstance(self.show_page_list[0], str))#返回值的元素要为str
        
    def test_get_all_show_page_url_yield(self):#
        
        yield_show_page = self.trait_obj.get_all_show_page_url_yield()
        
        self.assertTrue(isinstance(yield_show_page, types.GeneratorType))
        
        self.assertEqual(next(yield_show_page), self.show_page_list[0])
        
        self.assertEqual(next(yield_show_page), self.show_page_list[1])
        
        self.assertEqual(next(yield_show_page), self.show_page_list[2])
        
        
        
    def test_film_search(self):#网站搜索函数测试
        
        obj = self.trait_obj.film_search('筑梦情缘')
        
        search_list = obj['search_list'] #返回值要有‘search_list’键
        
        self.assertTrue(isinstance(obj, dict))#返回值要是一个字典
        
        self.assertTrue(obj['search_word'] == '筑梦情缘')#返回值要有‘search_word’键
        
        self.assertTrue('search_list' in obj)#返回值要有‘search_list’键
        
#        self.assertTrue('search_word' in obj)
        
        self.assertTrue(obj['host'] == self.host)#返回值要有‘'host'’键
        
        
        self.assertTrue(isinstance(search_list,list))##返回值‘search_list’键的值变列表
        
        if search_list:#如果有搜索结果
        
            self.assertTrue(isinstance(search_list[0], dict))#search_list的元素要为字典
            
            self.assertTrue(self.host in search_list[0]['url'])#每个搜索结果要有url键
            
            self.assertTrue(bool(search_list[0]['name']))#每个搜索结果要有name键
            
            self.assertTrue(bool(search_list[0]['types']))#每个搜索结果要有types键
            
            self.assertTrue(bool(search_list[0]['update_time']))#每个搜索结果要有update_time键
            
    
        

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
    
    
