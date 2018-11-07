# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 13:22:11 2018

@author: ELBELHADJI
"""

from bouygues_pysms import BouyguesClient

b = BouyguesClient(lastname='EL BELHADJI', user="elbelhadji.abdelmoghith@bbox.fr", passwd="azerty" )
b.login()

#test1
#b.send('Hello World')

#test2
#b.send('Hello World ' * 15)

#test3
#b.send('Hello World ' * 15, '0679750844')

#test4
#b.send('Hello World ' * 15,  ["0679750844", "0679750844", "0679750844"])

#b.send('Hello World ' * 15, ["0679750844", "0679750844"])

