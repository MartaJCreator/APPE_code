#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:56:40 2020

@author: martaross

step 1, read through folders to find specific file
step 2, read through specifc SX-PXRD "filename.xye" file
step 3, read through 2nd column (which should be the intensity values)
step 4, find highest value in 2nd column, call highest_val
step 5, divide value in 2nd column by highest_val
step 6, read through 2nd column
step 7, multiply new 2nd column number by new greatest intensity (chosen by user)
step 8, give new column name = called scaled_Y
step 9, take each value in scaled_Y and take to the power of 0.5
step 10, give answer as newerror
step 11, create new collumn of newerror
step 12, create new .xye file of 2theta, scaled_Y and newerror

"""

import os 

from decimal import Decimal


class File_Fetcher(object):
    """
    This is the file reader 
    """

    def __init__(self, a_location):
        self.location = a_location
        print (self.location)
        self.list_o_files = []
        self.reader()
        
    def reader(self):
        # print("reader is running", self.location)
        # print(os.path.isdir(self.location))
        for root, dirs, files in os.walk(self.location):
            print(root, dirs, files)
            self.list_o_files = files
        # print(self.list_o_files)
        
    def get_list_o_files(self):
        """
        This returns list_o_files

        """
        return(self.list_o_files, self.location)
    
    
class File_Editor(object):
    """
    This is the file editor 

    """
    
    def __init__(self):
        """
        This is to initialise and for File_Editor to make her own Helper

        """
        self.a_Helper = Helper()
        self.a_J_Ames = J_Ames()
        pass
    
    def processlist_o_data(self, data_from_File_Fetcher):
        print(data_from_File_Fetcher)
        list_o_files = data_from_File_Fetcher[0]
        location_of_files = data_from_File_Fetcher[1]
    
        for file in list_o_files:
            if ".xye" in file:
                total_file_name = location_of_files + "/" + file
                print(file)
                temp_list = self.open_file(total_file_name)             
                self.a_Helper.set_raw_data(temp_list)
                self.a_Helper.split_data()
                self.a_Helper.find_highest_y()
                self.a_Helper.scale_intensity()
                self.a_Helper.give_new_error()
                self.a_J_Ames.wallE(self.return_buckets())
                self.a_J_Ames.final_output(file)
                
            else:
                pass
            
    def open_file(self, file):
        with open(file, "r") as reader:
            list_o_data = reader.readlines()
        return(list_o_data)


    def return_buckets(self):
        return (self.a_Helper.xray_wavelength, self.a_Helper.TwoTheta, 
                self.a_Helper.scaled_int, self.a_Helper.new_error)
        
    def return_filename(self):
        
        return self.file
    
    

class Helper(object):
    """
    
    This is the raw data editor
    
    """
    
    def __init__(self):
        self.raw_data = "not set"
        self.xray_wavelength = "not set"
        
        pass
    
    def get_raw_data(self): 
        return(self.raw_data)
    
    def set_raw_data(self, raw_data):
        self.raw_data = raw_data
        # print("setting raw data to", self.raw_data)
    
    def split_data(self):
        self.split = []
        self.TwoTheta = []
        self.Intensity = []
        self.error = []
        self.xray_wavelength = self.raw_data[0]
        
        
        for line in self.raw_data[1:]:
            # print(line.strip("\n").split())
            # self.split.append(line.strip("\n").split())
            # print(self.split)
            temp_value = line.strip("\n").split()
            self.TwoTheta.append(temp_value[0])
            self.Intensity.append(float(temp_value[1]))
            self.error.append(temp_value[2])

        # print(self.TwoTheta[:3], self.Intensity[:3], self.error[:3])
            
            
    def find_highest_y(self):
        
        print(self.Intensity[:5])
        self.highest_val = 0
        for number in self.Intensity:
            # print(number)
            if number > self.highest_val:
                self.highest_val = number
            else:
                pass
            
        print(self.highest_val)
            
    
        pass
        
    def scale_intensity(self):
        
        scalar = 50000.0/self.highest_val
        print(scalar)
        # print(self.intensity[:5])
        self.scaled_int = []
        for y_value in self.Intensity:
            
            new_y_value = y_value*scalar
            
            # print(new_y_value)
            self.scaled_int.append(new_y_value)
        
        
            
        print(self.scaled_int[:5])
        
    def give_new_error(self):
        
        self.new_error = []
        for new_y_value in self.scaled_int:
            new_error = new_y_value**0.5
            self.new_error.append(new_error)
            
        print(self.new_error[:5])
              

class J_Ames(object):
    """
    This is the writer of the new file 

    Named after Jonathan Ames in the TV series, bored to death, about a 
    struggeling detective novelist who becomes a detective in order to 
    beat his writer block.
    """
    
    def __init__(self):
        pass

    def wallE(self, raw_data):
        """
        This is where the buckets are recombined from File_Editor
        
        Named after walle who does a good job at compiling things

        """
        self.raw_data = raw_data
        
        print(len(self.raw_data[2]))
        
        print(len(self.raw_data[1]))
        
        self.xray_wavelength = self.raw_data[0]
        self.TwoTheta = self.raw_data[1]
        self.scaled_int = self.raw_data[2]
        self.new_error = self.raw_data[3]
        
        self.weaved_values = [self.xray_wavelength]
        
        for number in range(len(self.TwoTheta)):
            # print(self.TwoTheta[number])
            # print(self.scaled_int[number])
            # print(self.new_error[number])
            
    
            new_string = self.Format_Helper(number)
           
            
            self.weaved_values.append(new_string)
            
        
        # print(self.weaved_values)
        for line in self.weaved_values[:5]:
            print(line)
        
        pass
    
    def final_output(self, file):
        
        output_directory_location = "OutputScaledData"
        
        file = file.replace(".xye", "_ScaledDATA.xye")
        
        file_csv = file.replace(".xye", ".csv")
        
        output_file_location = output_directory_location + "/" + file
       
        output_file_location_csv = output_directory_location + "/" + file_csv
        
        
        print(file)
        
        if os.path.isdir(output_directory_location):
            pass
            
        else:
            os.mkdir(output_file_location)
            pass
        print(output_file_location)
        
        
        if os.path.isfile(output_file_location):
            print("Caution folder contains file with same name", file)
        
        elif os.path.isfile(output_file_location_csv):
            print("Caution folder contains file with same name", file_csv)
            
        else:
            print("here", output_file_location)
            
            with open(output_file_location, "w") as fileoutput:
                fileoutput.writelines(self.weaved_values)
            
          
            with open(output_file_location_csv, "w") as fileoutput:
                fileoutput.writelines(self.weaved_values)
        
        
        pass
    
    def Format_Helper(self, number):
        
        """
        This is to make the number formatting consistent
        
        
        """
        
        self.scaled_int_decimal = round(Decimal(str(self.scaled_int[number])), 3)
        
        
        self.new_error_decimal = round(Decimal(str(self.new_error[number])), 3)
        
    
        return("{}      {}      {}\n".format(self.TwoTheta[number], 
                                       self.scaled_int_decimal, 
                                       self.new_error_decimal))
         
    





if __name__ == "__main__":
    print ("hello world ")
    a_File_Fetcher = File_Fetcher("test-dataSCALE")
    
    a_File_Editor = File_Editor()    
    
    a_File_Editor.processlist_o_data(a_File_Fetcher.get_list_o_files())
    
    # print(a_File_Editor.return_buckets())


    # a_J_Ames.wallE(a_File_Editor.return_buckets())
    
    


