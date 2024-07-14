from PIL import Image, ImageDraw
import os

class mapping():
    def get_pixcels(filename, precsion, binary, positions, txt_filename):
        im = Image.open(filename, 'r')
        pix_data, pix_val_list = mapping.arrange_pixcels(im)
        values_to_insert, values_to_insert_pos = [], []
        for count_1, pix_1 in enumerate(pix_val_list, 1):
            values_to_insert_row, values_to_insert_row_pos = [], []
            if count_1 % int(precsion) == 0 and  binary == True:
                for count_2, pix_2 in enumerate(pix_1, 1):
                    if count_2 % int(precsion) == 0:
                        if pix_2 == (255, 255, 255):
                            value = 0
                        else:
                            value = 1
                        values_to_insert_row.append(value)
                values_to_insert.append(values_to_insert_row)
            if count_1 % int(precsion) == 0 and  positions == True:
                for count_2, pix_2 in enumerate(pix_1, 1):
                    if count_2 % int(precsion) == 0:
                        try:
                            values_to_insert_row_pos.append(pix_data[count_1][count_2])
                        except:
                            continue
                values_to_insert_pos.append(values_to_insert_row_pos)
        if binary:
            mapping.write_to_file(values_to_insert, txt_filename)
        if positions:
            mapping.write_to_file(values_to_insert_pos, txt_filename)
            
    def write_to_file (values, filename):
        filename = mapping.create_filename(filename)
        f = open(filename, "w")
        
        for row in values:
            string_row = ""
            for record in row:
                string_row += str(record) + " "
            f.write(string_row + '\n')
        f.close()
        
    def arrange_pixcels(im):
        width, height = im.size
        pix_val = list(im.getdata())
        #pix_val.reverse()
        pix_data, pix_val_list= [], []
        i = len(pix_val)-1
        for y in range(height): 
            row_pix_val, row_pix_data = [], []
            for x in range(width):
                if pix_val[i] == (0,0,0):
                    row_pix_data.append([x,y])
                row_pix_val.append(pix_val[i])
                i-=1
            pix_val_list.append(row_pix_val)
            pix_data.append(row_pix_data)
        if len(pix_data) == len(pix_val_list):
            return (pix_data, pix_val_list)
        else:
            raise ValueError('Blad danych')
       
        
    def create_filename(directory):
        name = "DANE.txt" 
        if os.path.isfile(name):
            n=0
            while os.path.isfile(name):
                n+=1 
                name = "DANE" + str(n)+'.txt' 
        filename = directory + '//'+ name
        return filename 
