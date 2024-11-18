#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.
#My modifications from the teacher-modified script

#Obscure
import keyboard
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport

#Understandable
import time as t
import random as r

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1 or 1, block_orientation=0, rotate= 0)
virtual = viewport(device, width=10, height=10)

#I can start playing

#Set the INITIAL STATE

cs=[] #current state list
pd={} #provisional dictionary to store the cell state at the specified position

with canvas(virtual) as draw:
    for row in range(8):
        for column in range(8):    
            cell_state=r.randrange(2)
            draw.point((column,row), fill=cell_state)            
            #print("This is column=",column,"and cell_state=",cell_state)
            pd[column, row]=cell_state 
            cs.append(pd)
            pd={} #reset pd
t.sleep(2)
print("This is the current state (cs)",cs,"\n")

#Develop SUBSEQUENT STATES from INITAL STATE

with canvas(virtual) as draw:
    for column in range(8):
        for row in range(8):
            if (column==0 or row==0) or (column==7 or row==7):
                print("Column and/or row should be 0 or 7. This is column",column,"and this is row",row)
                #draw.point((column,row), fill=1) Use this to turn on the margins of the matrix
            else:
                #print("cs[column-1,row-1]",cs[column-1,row-1])
                print("cs[1,1]",cs[1,1])
                #if cs[column-1,row-1]


t.sleep(2)

#[1,3][2,3][3,3]
#[1,4][2,4][3,4]
#[1,5][2,5][3,5]

#[column-1,row-1][column,row-1][column+1,row-1]
#[column-1,row][column,row][column+1,row]
#[column-1,row+1][column,row+1][column+1,row+1]


