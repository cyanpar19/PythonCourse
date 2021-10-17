# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 13:29:02 2021

@author: celal.yanpar
"""


def fib(n):
    fib = [1,1]
    while len(fib)< n:
        fib.append(fib[-1]+fib[-2])
    return fib
    
    