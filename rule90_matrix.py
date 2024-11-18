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

##Set row 0, the INITIAL STATE row. The first row, is randomly generated.

cs=[] #current state list
pd={} #provisional dictionary to store the cell state at the specified position
bd={} #BIG DICTIONARY to store EVERYTHING so the LEDs are not turned off at each row change. In fact they are switched off, but they are switched on again, as previous rows are stored in bd
with canvas(virtual) as draw:
    for column in range(8):    
        cell_state=r.randrange(2) #Randomly determine if cells are alive (1) or dead (0)
        draw.point((column,0), fill=cell_state) #for each column from row=0
        bd[column, 0]=cell_state #BIG DICTIONARY
        print("This is bd\n",bd,"\nIts length is",len(bd),"\n")  
        pd[column]=cell_state 
        cs.append(pd)
        pd={} #reset pd
t.sleep(2)
print("This is the current state (cs)",cs,"\n")

###Develop the INITIAL STATE on the subsequent rows, following XOR (the output is True only if the two inputs are different)

for row in range(1,8): #row 0 is were the INITIAL STATE is placed, so we must start at row=1 here
    dcs=[] #developing current state list
    with canvas(virtual) as draw:
        for column in range(8):
            if column==0 or column==7: #Columns on the extremes only have one neighbour, so they require special rules. I decided they should change they status at every row
                if cs[column][column]==0:
                    cell_state=1
                else:
                    cell_state=0
            else:
                #print("This is row",row,"This is column",column,", this is cs[column-1][column-1]",cs[column-1][column-1],", this is cs[column+1][column+1]",cs[column+1][column+1])
                if cs[column-1][column-1]!=cs[column+1][column+1]: #If the two neighbours of the current cell are different, this cell will be alive in the next generation.                
                    cell_state=1
                else:
                    cell_state=0
            bd[column, row]=cell_state #BIG DICTIONARY  
            pd[column]=cell_state 
            dcs.append(pd)
            pd={} #reset pd        
    cs=dcs #the developing current state becomes the current state
    print("This is bd\n",bd,"\nIts length is",len(bd),"\n")
    with canvas(virtual) as draw:
        for turn_on_row in range(row+1): #THE BIG DICTIONARY IN ACTION. +1 is to include the row just developed above
            for turn_on_column in range(8):
                draw.point((turn_on_column, turn_on_row), fill=bd[turn_on_column, turn_on_row]) #for each position use the BIG DICTIONRY to know if it should be on or off
                print("turn_on_column=",turn_on_column,"turn_on_row=",turn_on_row,"bd[turn_on_column, turn_on_row]",bd[turn_on_column, turn_on_row])
    t.sleep(2)

t.sleep(10)




