# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
from mapping import mapping
from communicate_with_arduino import arduino_communication

class communication():
   def create_walls_info(filename, wall_dimension, wall_thick, port, data_rate):  
       N,W,E,S = [], [], [], []
       im = Image.open(filename, 'r')
       _, pix_val = mapping.arrange_pixcels(im)
       cell_nr = (len(pix_val[0])-2*wall_thick)/wall_dimension
       dimension = str(int(cell_nr))+'x'+str(int(cell_nr))
       for j in range(1, int(cell_nr)+1 ):
           for i in range (1, int(cell_nr)+1):
                if pix_val [wall_thick+wall_dimension*j-1-int(wall_dimension/2)][wall_thick+wall_dimension*i-1] == (0,0,0):
                    E.append(1)
                else:
                    E.append(0)
                if pix_val [wall_thick+wall_dimension*j-1][wall_thick+wall_dimension*i-1-int(wall_dimension/2)] == (0,0,0):
                    N.append(1)
                else:
                    N.append(0)
                if pix_val [wall_thick+wall_dimension*(j-1)-1][wall_thick+wall_dimension*(i-1)-1-int(wall_dimension/2)] == (0,0,0):
                    S.append(1)
                else:
                    S.append(0)
                if pix_val [wall_thick+wall_dimension*(j-1)-1-int(wall_dimension/2)][wall_thick+wall_dimension*(i-1)-1] == (0,0,0):
                    W.append(1)
                else:
                    W.append(0)

       tables = [W,S,N,E]
       arduino_communication.connect(port, data_rate, tables, dimension)
       
   def reverse_table(table, cell_nr):
        for count, element in enumerate(table,0):
            if count % cell_nr == cell_nr -1 and element == 0:
                table[count] = 1
        return table
        
                

