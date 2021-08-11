_ThisFile = 'bmp_class.py'
# ----- Date        : 5/08/2021
# ----- Author      : Simon Bird
# ----- Version
_version = '0v23'
# ----- IDE         : IDLE shell 3.9.6
# ----- Programmer  : DEFAULT
# ----- Total time 
totalTime = ['xx','xx']
dayMultiplier = 'xx'

#------------Current edit--------------#
# 11/08/2021
# Comments and Tidy, upload to github


class bmp_file():
    class_open=0
#containers , sizes and var
    file_header_data=[]
    fhd_elements=16
    read_data_header=[]
    read_bmp_rawdata=[]
    write_bmp_rawdata=[]
    fp_read  = None
    fp_write = None    

                # uint_16, uint_32 can be got from import ctypes    
#File_header    #BYTES WIDE - discription 
    file_type=b'BM'     #2b - fixed - check on open
    file_size=None      #4b - to be calculated in code
    reserved1=0         #2b - used by editor / display program
    reserved2=0         #2b - as above
    offset_data=54      #4b - start of pixel data
#Info_header
    info_size=40        #4b - size of this header
    bwidth=None         #4b - 2's compliment +- , positive bottom left first
    bheight=None        #4b - and +-
    planes=1            #2b
    bit_count=24        #2b - 8 * (rgb) but little end, so (bgr)
    compression=0       #4b
    size_image=0        #4b - 0 for uncompressed
    x_pixel_scaler=0    #4b
    x_pixel_scaler=0    #4b
    colours_used=0      #4b
    colours_important=0 #4b

#=====================#
    
    def __init__(self):
        self.class_open=1

    def error_function(self):
        return -1

#==========Memory================================#
    def check_mem(self , bytes_wide):
        mem_check=[]
        try:
            for b in range (bytes_wide):
                mem_check.append(b'\xFF')
            print("Memory Check is OK")
        except Exception:
            print("Not Enough Memory To Allocate")
            return False
        mem_check.clear()
        return True



#=========FILE ENCAPSULATION FUNCTIONS ============#

    def p_open(self , file_name_in):
        try:   self.fp_read = open(file_name_in , 'rb')
        except Exception:
            print( " Error Opening File -" , file_name_in ) ;                                   # print( Exception )
            return self.error_function()
        self.fp_read.seek(0,2);     size_of_file=self.fp_read.tell();     self.fp_read.seek(0,0)# end , read , reset
        return size_of_file

    def p_seek(self , pos):                                                                     # also add if pos > file size
        try:
            self.fp_read.seek(pos,0);
            return 1
        except Exception:
            print ( "Error Seeking to Position ");
            return self.error_function()


    def p_write(self , object_to_write):                                                        # protected write wrapper - try catch
        try:
            fp_write.write(object_to_write)
        except Exception:
            print("Error Writing to file")
            return self.error_function()
        return 1

    def p_read(self , byte_width):                                                              # protected read mask try catch
        try:   return (self.fp_read.read(byte_width))
        except Exception:
            print( " Error Reading Open File "  ) ;                                             # print( Exception )
            return self.error_function()
   
    def p_close(self , file_to_close):
        if(file_to_close == 'read'):  self.fp_read.close()
        if(file_to_close == 'write'): self.fp_write.close()

#====================================================#

    def set_dimentions( self , width_in , height_in ):
        self.bwidth = width_in
        self.bheight = height_in
        pixels = width_in * height_in
        raw_data = pixels * 3
        self.file_size =  raw_data + self.offset_data 

        self.prepare_header()           # not best placed here!!

        self.set_background()
        
    def convert_for_write ( self , size , data , sign=False ):
        return bytes(data.to_bytes(size, byteorder="little", signed=sign))

    def prepare_header (self):
        self.file_header_data.append(self.file_type)
        self.file_header_data.append(self.convert_for_write(4,self.file_size))
        self.file_header_data.append(self.convert_for_write(2,self.reserved1))
        self.file_header_data.append(self.convert_for_write(2,self.reserved2))
        self.file_header_data.append(self.convert_for_write(4,self.offset_data))
        self.file_header_data.append(self.convert_for_write(4,self.info_size))
        self.file_header_data.append(self.convert_for_write(4,self.bwidth,sign=True))
        self.file_header_data.append(self.convert_for_write(4,self.bheight,sign=True))
        self.file_header_data.append(self.convert_for_write(2,self.planes))
        self.file_header_data.append(self.convert_for_write(2,self.bit_count))
        self.file_header_data.append(self.convert_for_write(4,self.compression))
        self.file_header_data.append(self.convert_for_write(4,self.size_image))
        self.file_header_data.append(self.convert_for_write(4,self.x_pixel_scaler))
        self.file_header_data.append(self.convert_for_write(4,self.x_pixel_scaler))
        self.file_header_data.append(self.convert_for_write(4,self.colours_used))
        self.file_header_data.append(self.convert_for_write(4,self.colours_important))
        print(self.file_header_data)
        return 1

    def set_background(self):
        for g in range (self.bheight):
            self.prepare_pixel(255,0,255)
            for h in range(self.bwidth-1):
                self.prepare_pixel(0,255,0)
                
    def prepare_pixel(self , r , g , b ):
        self.write_bmp_rawdata.append(self.convert_for_write( 3,( b + (g<<8) + (r<<16))))

    def write_all(self , file_name_in):
        fp=open(file_name_in,'wb')
        for e in range(self.fhd_elements):
            fp.write(self.file_header_data[e])
        for p in range(self.bwidth*self.bheight):
            fp.write(self.write_bmp_rawdata[p])
        fp.close()

#==============================#  
    
    def read_all(self,file_name):
        fp=open(file_name,'rb')
        for x in range (self.file_size):
            print(fp.read(1))
        fp.close()

    def data_int_in(self , bytes_in , sign = False ):    return (int.from_bytes(bytes_in, byteorder = 'little' , signed = sign ))

    def read_bmp_header(self , file_name_in):
        self.p_open( file_name_in )
        if(self.read_file_header() == 40):
            self.read_info_header()
            return 1
        
    def read_file_header( self ):
        self.read_data_header.append(self.p_read(2))
        if((self.read_data_header[0] == b'BM')):
            print("Valid BMP Tag")                                              #read next data till offset - return and use offset to work out next header
            self.read_data_header.append(self.p_read(4));    self.file_size=self.data_int_in(self.read_data_header[1])
                                                                                #can check above file_size with seek(0,2) tell for actual size
            self.read_data_header.append(self.p_read(2));    self.reserved1=self.data_int_in(self.read_data_header[2])
            self.read_data_header.append(self.p_read(2));    self.reserved2=self.data_int_in(self.read_data_header[3])
            self.read_data_header.append(self.p_read(4));    self.off_set  =self.data_int_in(self.read_data_header[4])            
            return ( self.data_int_in ( self.read_data_header[4] ) - 14)        # 14 is this header
        else:    print("No Valid BMP Tag")

    def read_info_header(self):                                                 # has seperate function for colour pallet
                                                                                #- ie check offset against info_size pass to f()
        self.read_data_header.append(self.p_read(4));    self.info_size         =self.data_int_in(self.read_data_header[5])
        self.read_data_header.append(self.p_read(4));    self.bwidth            =self.data_int_in(self.read_data_header[6])
        self.read_data_header.append(self.p_read(4));    self.bheight           =self.data_int_in(self.read_data_header[7] , sign = True )
        self.read_data_header.append(self.p_read(2));    self.planes            =self.data_int_in(self.read_data_header[8] , sign = True )
        self.read_data_header.append(self.p_read(2));    self.bit_count         =self.data_int_in(self.read_data_header[9])
        self.read_data_header.append(self.p_read(4));    self.compression       =self.data_int_in(self.read_data_header[10])
        self.read_data_header.append(self.p_read(4));    self.size_image        =self.data_int_in(self.read_data_header[11])
        self.read_data_header.append(self.p_read(4));    self.x_pixel_scaler    =self.data_int_in(self.read_data_header[12])
        self.read_data_header.append(self.p_read(4));    self.y_pixel_scaler    =self.data_int_in(self.read_data_header[13])
        self.read_data_header.append(self.p_read(4));    self.colours_used      =self.data_int_in(self.read_data_header[14])
        self.read_data_header.append(self.p_read(4));    self.colours_important =self.data_int_in(self.read_data_header[15])
        print("width = ",self.bwidth)
#EDIT FOR FUTURE
        # self.info_size = FUNCTION ( byte_size , pos):
        # ??? - self.read_data_header.append(fp.read(4)); return (self.data_int_in(self.read_data_header[5]))

    def read_bmp_data(self):                   
        if(self.bit_count==24):     local_byte_width = 3                            # 3 bits read per time - read as bgr
                                                                                    # needs work ie if alpha then, else FUNCTION X
        if(self.check_mem( ( ( self.bwidth * self.bheight ) * local_byte_width ) ) ):
            self.p_seek( self.off_set  )                          
            for p in range ( ( self.bwidth * self.bheight ) ):
                self.read_bmp_rawdata.append( self.p_read( local_byte_width ));                        
                               
    def read_raw_pixel(self, pixel_no):                                             # make rgb from bgr
        return 1
      
#==================================# - use functions - ===============================================#

    def raw_copy(self , source_file , destination_file ):
        self.read_bmp_header(source_file)
        self.read_bmp_data()

        self.write_bmp_rawdata.clear()
        self.write_bmp_rawdata=rawdata=self.read_bmp_rawdata
        
        self.prepare_header()
        self.write_all(destination_file)
        return 1

    def find_pixel(self , x , y ):    return ((y*self.bwidth) + x)
    
    def modify_pixel(self , x , y , r , g , b ):
        new_pixel=(self.convert_for_write( 3,( b + (g<<8) + (r<<16))))      #bitshift and make bytes (width 3 )
        self.write_bmp_rawdata[self.find_pixel( x , y )]=new_pixel
        
    def change_pixels(self , source_file , destination_file ):
        self.read_bmp_header(source_file)
        self.read_bmp_data()

        self.write_bmp_rawdata.clear()
        self.write_bmp_rawdata=rawdata=self.read_bmp_rawdata
        
        for cp in range (4):                                                 # current_pixel
            self.modify_pixel( cp+1 , cp+1 , 0 , 0 , 0)                      # test put diagonal line across
        
        self.prepare_header()
        self.write_all(destination_file)

    def merge_bmps(self):
        return 1
        
def test_bed():
    my_bmpC=bmp_file()
    #print(my_bmpC.check_mem(800000))

    #my_bmpC.set_dimentions(100,100)
    #my_bmpC.write_all("t1_1.bmp")
    #my_bmpC.read_all("t1_1.bmp")

    #print(my_bmpC.read_bmp_header("t1_1.bmp"))
    #my_bmpC.read_bmp_data()
    #print(len(my_bmpC.read_bmp_rawdata))
    my_bmpC.change_pixels("t1_1.bmp","t1_1x.bmp")

#========================== MAIN ===========================#

def main_core():
    test_bed()

main_core()


#END
