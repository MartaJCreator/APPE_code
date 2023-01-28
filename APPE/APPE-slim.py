#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:43:27 2020

@author: MartaJRoss

This is a slim version of OperationDataAnalysisPart1b

"""

import os

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import scipy

from scipy import sparse

from scipy.sparse.linalg import spsolve

from scipy.signal import find_peaks

from scipy.signal import chirp, find_peaks, peak_widths

import pickle


class Format_Fetcher(object):

    def __init__(self):
        print("initialising Format_Fetcher")

        pass

    def read_files(self, file_location):

        if os.path.isdir(file_location):
            print("found file location")

        else:
            print("not a directory")

        self.location_o_files = file_location

        self.list_o_files = []

        for roots, dirs, files in os.walk(file_location):
            # print(roots, dirs, files)

            self.list_o_files = files
            break

            """
            This assumes directory only contains files and no
            other directories

            """

        pass

    def get_list_o_files(self):

        return self.list_o_files

    def get_location_o_files(self):

        return self.location_o_files


class Process_Manager(object):

    """
    Process_Manager collects the output from the other objects to compile and
    analyse - this then is given to CentralDataHolder

    """

    def __init__(self):

        """
        When Process_Manager is created, they create a version of Helper to analyse
        data
        """
        print("Process_Manager here")
        self.Helper = Helper()
        pass

    def collect_files(self, Format_Fetcher):

        self.list_o_files = Format_Fetcher.get_list_o_files()
        self.location_o_files = Format_Fetcher.get_location_o_files()
        pass

    def opener_o_files(self, a_CentralDataHolder):

        """
        This loops through the list of files, picks one at a time, opens it
        and gives it to Helper

        The files are then passed to CentralDataHolder
        """

        for file_name in self.list_o_files:

            if ".xye" in file_name:
                # print(file_name)
                # self.give_data_to_Helper(file_name)
                # self.Helper.data_analysis(self.give_data_to_Helper(file_name))
                self.Helper.create_data_array(self.give_data_to_Helper(file_name),
                                            file_name)

                self.Helper.process_peaks()

                a_CentralDataHolder.set_data_array(self.Helper.Return_data_array())
                a_CentralDataHolder.set_peaklist_40(self.Helper.Return_peaklist_40())
                a_CentralDataHolder.set_data_array40theta(self.Helper.Return_data_array40theta())
                a_CentralDataHolder.set_resolution_list(self.Helper.Return_resolution_list())
                a_CentralDataHolder.set_peaklist_40_SX(self.Helper.Return_peaklist_40_SX())
                a_CentralDataHolder.set_resolution_SX_list(self.Helper.Return_resolution_SX_list())

                a_CentralDataHolder.set_resolution_SX(self.Helper.Return_resolution_SX())
                a_CentralDataHolder.set_name(file_name)
                print("creating DataHolder for ", file_name)
                a_CentralDataHolder.create_new_DataHolder()


                # self.Helper.peak_analysis(self.give_data_to_Helper())
            else:
                pass

        pass

    def give_data_to_Helper (self, file_name):

       file_name = self.location_o_files + "/" + file_name

       print(file_name)


       with open (file_name, "r") as filereader:
           temp_bucket = filereader.readlines()
       return temp_bucket

    # def flatten_data (self, file_name):
       # self.baseline_correct()


    def output (self):
        pass

class Helper(object):

    """
    This is Bell Burnell's helper

    Contains all the knowhow for how to analyse the datasets, these different
    results become a property of Helper so that everytime Helper is called, they
    have these properties - helps with getting data between objects
    """

    def __init__(self):
        print("Helper here")

        self.data_array = "not set"

        self.file_name = "not set"

        self.data_array_40theta = "not set"

        self.resolution_list = "not set"

        self.type_of_dataset = "not set"

        self.peaklist = "not set"

        self.resolution = "not set"

        self.peaklist_40 = "not set"

        self.peaklist_40_SX = "not set"

        self.resolution_SX = "not set"

        self.resolution_SX_list = "not set"

        pass

    def Return_data_array(self):

        return self.data_array

    def Return_data_array40theta (self):

        return self.data_array_40theta

    def Return_peaklist_40 (self):

        return self.peaklist_40

    def Return_resolution_list (self):

        return self.resolution_list

    def Return_peaklist_40_SX (self):

        return self.peaklist_40_SX

    def Return_resolution_SX (self):

        return self.resolution_SX

    def Return_resolution_SX_list (self):

        return self.resolution_SX_list


    def create_data_array (self, raw_data, name_o_file):

        """
        This function reads the data loaded and splits the data into
        lists of x values and y values (2theta and intensity)

        data_array is the full data set

        data_array_40_thetha is the dataset upt to 40 degrees


        raw data is provided by outer function - this should be refactored into
        this class

        """

        self.raw_data = raw_data

        self.file_name = name_o_file

        temp_xvalues = []

        temp_yvalues = []

        for numbers in self.raw_data[1:]:

            temp_bucket = []

            split_rows = numbers.strip("\n").split()

            for number in split_rows:

                if "******" in numbers:
                    pass
                else:
                    temp_bucket.append(float(number))

            split_rows = temp_bucket

            if "******" in numbers:
                break

            else:
                temp_xvalues.append(split_rows[0])

                temp_yvalues.append(split_rows[1])

        data_array = np.array([temp_xvalues, temp_yvalues])

        self.data_array = data_array

        counter = 0

        for number in data_array [0] :

            if number > 40 :

                break

            else:
                counter = counter + 1

        self.data_array_40theta = self.data_array[0:counter, 0:counter]

        pass


    def finding_reference (self):

        if "_reference_" in self.file_name:
            self.type_of_dataset = "reference"

            """
            Change to REF
            """

        else:
            self.type_of_dataset = "SX"

        pass



    def process_peaks (self):

        # self.plot_data()
        self.finding_reference()

        if self.type_of_dataset == 'reference':

            self.Scale_reference()
            self.peak_possitions_ref()
            self.find_resolution_ref()

        else:
            self.peak_possitions_SX()
            self.find_resolution_SX()

        pass

        # # self.Helper.plot_data()
        # self.Helper.Scale_reference()
        # self.Helper.peak_possitions_ref()
        # self.Helper.peak_possitions_SX()
        # # self.Helper.peak_resolution()
        # self.Helper.find_resolution_SX()


    def plot_data (self):

        """
        This is a function to plot data
        """

        plt.plot(self.data_array[0], self.data_array[1])
        plt.show()

        pass

    def peak_possitions (self, data_array, input_prominence = 0.1,
                         title = None):
        """
        """

        peaks_y, properties = find_peaks(data_array[1],
                                         prominence=(input_prominence, None))

        # peaks_y, properties = find_peaks(self.data_array_40theta[1],
                                         # prominence=(1, None))

        peak_xvals = []

        peak_yvals = []

        for value in peaks_y:
            two_theta = data_array[0][value]
            peak_xvals.append(two_theta)
            peak_intensity = data_array[1][value]
            peak_yvals.append(peak_intensity)
            # print(peak_xvals)
            # print(peak_intensity)

        peaklist = np.array([peak_xvals, peak_yvals])

        print(len(peak_xvals), len(peak_yvals))

        plt.scatter(peak_xvals, peak_yvals)
        plt.plot(data_array[0], data_array[1])
        if title is not None:
            plt.title(title)
        plt.show()

        return peaklist

    def find_resolution(self, data_array, input_prominence = 100,
                        title = None):
        """
        Dont change prominence value here, its choose in seperate funcations
        """

        conversion_factor = data_array[0,1] - data_array[0,0]
        print("resolution data array", self.data_array.shape)
        peaks, _ = find_peaks(data_array[1], prominence = (input_prominence,
                              None))
        # print("peaks in resolution data", peaks)
        # peaks, _ = find_peaks(self.data_array[1], prominence = (500, None))

        results_half = peak_widths(data_array[1], peaks, rel_height=0.5)
        results_half[0]  # widths

        results_full = peak_widths(data_array[1], peaks, rel_height=1)
        results_full[0]

        plt.plot(data_array[1])
        plt.plot(peaks, data_array[1][peaks], "x")
        plt.hlines(*results_half[1:], color="C2")
        plt.hlines(*results_full[1:], color="C3")
        if title is not None:
            plt.title(title)
        plt.show()

        resolution_in_2theta = results_half[0] * conversion_factor

        resolution = resolution_in_2theta

        x_coordinate = []

        for value in peaks:

            two_theta = data_array[0][value]
            x_coordinate.append(two_theta)

        resolution_list = np.array([x_coordinate, resolution])

#        print("resolution list", resolution_list)

        return (resolution_list, resolution)

    def peak_possitions_SX (self):

        """
        This is a function that is set to pick up the most prominant peaks
        in the SX data set - set to pick up peaks with a prominence of between
        1 and 0.

        The function currently picks up peaks up to 40 degrees and this is set
        elsewhere.


        IMPORTANT PART - for finding SX peaks

        """

#        peaks_y, properties = find_peaks(self.data_array_40theta[1],
#                                         prominence=(0.1, None))
#
#        # peaks_y, properties = find_peaks(self.data_array_40theta[1],
#                                         # prominence=(1, None))
#
#        peak_xvals_SX = []
#
#        peak_yvals_SX = []
#
#        for value in peaks_y:
#            two_theta = self.data_array[0][value]
#            peak_xvals_SX.append(two_theta)
#            peak_intensity = self.data_array[1][value]
#            peak_yvals_SX.append(peak_intensity)
#            # print(peak_xvals)
#            # print(peak_intensity)
#
#        peaklist_40_SX = np.array([peak_xvals_SX, peak_yvals_SX])
#
#        print(len(peak_xvals_SX), len(peak_yvals_SX))
#
#        plt.scatter(peak_xvals_SX, peak_yvals_SX)
#        plt.plot(self.data_array_40theta[0], self.data_array_40theta[1])
#        plt.show()

#        self.peaklist_40_SX = peaklist_40_SX
#        test

        """
        peak resolution is here here
        """

        self.peaklist_40_SX = self.peak_possitions(self.data_array_40theta,
                                                   0.5, "Single Peak")

        self.peaklist_40 = self.peaklist_40_SX
        pass


    def find_resolution_SX (self):

        """
        This function finds the resolution of the peaks for the SX datasets,
        prominence is set between 1 and 0. Resolution is given in terms of
        FWHM, or results_half. Base peak width is given as results_full.

        data is plotted

        a conversion factor is found to convert the x values to 2theta terms

        a data array is then created of the 2theta values and resolution values
        in terms of 2theta
        """

#        conversion_factor = self.data_array[0,1] - self.data_array[0,0]
#
#        # peaks, _ = find_peaks(self.data_array[1], prominence = (0.1, None))
#
#        peaks, _ = find_peaks(self.data_array[1], prominence = (0.1, None))
#
#
#        results_half = peak_widths(self.data_array[1], peaks, rel_height=0.5)
#        results_half[0]  # widths
#
#        results_full = peak_widths(self.data_array[1], peaks, rel_height=1)
#        results_full[0]
#
#        plt.plot(self.data_array[1])
#        plt.plot(peaks, self.data_array[1][peaks], "x")
#        plt.hlines(*results_half[1:], color="C2")
#        plt.hlines(*results_full[1:], color="C3")
#        plt.show()

#        resolution_in_2theta = results_half[0] * conversion_factor
#
#        self.resolution_SX = resolution_in_2theta
#
#        x_coordinate = []
#
#        for value in peaks:
#
#            two_theta = self.data_array[0][value]
#            x_coordinate.append(two_theta)
#
#        # print("gary", x_coordinate, len(x_coordinate), len(self.resolution_SX))
#
#        resolution_SX_list = np.array([x_coordinate, self.resolution_SX])
#
#        self.resolution_SX_list = resolution_SX_list
#
#        print("MrCrabs", resolution_SX_list)
#        pass

        """
        set the rest here
        """

        resolution_data = self.find_resolution(self.data_array, 0.5,
                                               "Single Res")
        self.resolution_SX_list = resolution_data[0]
        self.resolution_SX = resolution_data[1]
        print(type(self.resolution_SX))

        """
        This has been added as the for the labo5 dataset
        @todo find the source of this bu
        """

        self.resolution_list = resolution_data[0]

    def Scale_reference (self):
        """
        doc needed
        """

        print ("Scale_reference check", type(self.data_array))

        self.highest_val = 0
        for number in self.data_array[1]:
            # print(number)
            if number > self.highest_val:
                self.highest_val = number
            else:
                pass

        scalar = 10000.0/self.highest_val
        print(scalar)
        # print(self.intensity[:5])
        self.scaled_int = []


        for y_value in self.data_array[1]:

            new_y_value = y_value*scalar

            # print(new_y_value)
            self.scaled_int.append(new_y_value)

        self.ref_data_array = np.array([self.data_array[0], self.scaled_int])
        self.data_array = self.ref_data_array


    def peak_possitions_ref (self):

        """
        Looks through data_array and finds most prominent peaks
        gives those peak heights and their respective 2 theta values
        Currently set for finding peaks in a reference data set as the
        prominence value is set between 10,000 and None

        The for loop then puts the x and y values into lists and these
        are combined at the end to give the peaks in a numpy array

        Works best for reference data!!!


        this was altered for chlorzoxazne max ref height 10,000

        THIS IS IMPORTANT!!!

        """


        # peaks_y, properties = find_peaks(self.data_array[1], height = 10000)
#        peaks_y, properties = find_peaks(self.data_array_40theta[1],
#                                         prominence=(100, None))
#        peak_xvals = []
#
#        peak_yvals = []
#
#        for value in peaks_y:
#            two_theta = self.data_array[0][value]
#            peak_xvals.append(two_theta)
#            peak_intensity = self.data_array[1][value]
#            peak_yvals.append(peak_intensity)
#
#        peaklist_40 = np.array([peak_xvals, peak_yvals])
#
#        plt.scatter(peak_xvals, peak_yvals)
#        plt.plot(self.data_array_40theta[0], self.data_array_40theta[1])
#        plt.title("reference")
#        plt.show()

#        self.peaklist_40 = peaklist_40

#        for element in peaklist_40:
#            print(element)
#            for line in element:
#                print(line)


        """
       Here you set the resolution, (as in you change the value from 100)
       
       @ 20-9-22 I think this comment can be reomved

        """

        self.peaklist_40 = self.peak_possitions(self.data_array_40theta,
                                                   0.5, "reference")

        # this is needed for the reffeence in the output
        self.peaklist_40_SX = self.peaklist_40


    def find_resolution_ref (self):

        """
        This function finds the resolution of the peaks in data_array, in terms
        of FWHM. The base width is given in results_full.

        This is plotted below

        The 2theta values and the resolution values are then placed into lists
        in the for loop and combined to give a data array


        works best for the reference data (high peak intensity values)
        """
#        conversion_factor = self.data_array[0,1] - self.data_array[0,0]
#        print(self.data_array.shape)
#        peaks, _ = find_peaks(self.data_array[1], prominence = (100, None))
#
#        print(peaks)
#
#        # peaks, _ = find_peaks(self.data_array[1], prominence = (500, None))
#
#        results_half = peak_widths(self.data_array[1], peaks, rel_height=0.5)
#        results_half[0]  # widths
#
#        results_full = peak_widths(self.data_array[1], peaks, rel_height=1)
#        results_full[0]
#
#        plt.plot(self.data_array[1])
#        plt.plot(peaks, self.data_array[1][peaks], "x")
#        plt.hlines(*results_half[1:], color="C2")
#        plt.hlines(*results_full[1:], color="C3")
#        plt.show()
#
#        resolution_in_2theta = results_half[0] * conversion_factor
#
#        self.resolution = resolution_in_2theta
#
#        FWHM_value = []
#        x_coordinate = []
#
#        for value in peaks:
#
#            print("spongebob ", value, self.data_array[0])
#
#            two_theta = self.data_array[0][value]
#            x_coordinate.append(two_theta)
#
#            # resolution_output = results_half[0][value]
#            # FWHM_value.append(resolution_output)
#
#        resolution_list = np.array([x_coordinate, self.resolution])


#        self.resolution_list = resolution_list
#        self.resolution_SX = self.resolution
#        self.resolution_SX_list = self.resolution_list

        """
        Here you set the resolution for the ref its the 100 value you change
        """

        resolution_list = self.find_resolution(self.data_array, 0.5)

        self.resolution_list = resolution_list[0]
        self.resolution = resolution_list[1]

        self.resolution_SX = self.resolution
        self.resolution_SX_list = self.resolution_list




#        resolution_data = self.find_resolution(self.data_array, 100)

#        self.resolution = resolution_data[1]
#        self.resolution_list = resolution_data[0]

#        self.resolution_SX = self.resolution
#        self.resolution_SX_list = self.resolution_list



#        self.resolution_list = self.find_resolution(self.data_array, 100)

        # # print(FWHM_value)
        # # print(x_coordinate)

        # height_o_peaks = self.peaklist_40[1]

        # half_height_o_peaks = (self.peaklist_40[1]) / 2

        # print("hello height of peaks: ", height_o_peaks)

        # # print("hi there", half_height_o_peaks)

        # pass



    def baseline_correct(self, y_values, lam, p, niter=100):

        """
        This function finds the baseline (however this distorts the data
        so needs to be redone maybe)
        """

        L = len(y_values)
        D = sparse.csc_matrix(np.diff(np.eye(L), 2))
        w = np.ones(L)
        for i in range(niter):
               W = sparse.spdiags(w, 0, L, L)
               Z = W + lam * D.dot(D.transpose())
               z = spsolve(Z, w * y_values)
               w = p * (y_values > z) + (1 - p) * (y_values < z)
        return z

        pass

class CentralDataHolder (object):

    """
    CentralDataHolder is an object that can exist outside of the program that keeps
    all the data in binary form so that another program created does
    not have to conver the data into a readable form again
    """

    def __init__ (self):

        self.collection_o_datasets = []
        self.OutputDelegate = OutputDelegate()
        self.selection = False
        self.selection_mask = "not set"

        pass

    def create_new_DataHolder (self):

        self.collection_o_datasets.append(
             DataHolder(self.file_name, self.Return_data_array,
                    self.Return_data_array40theta,
                  self.Return_peaklist_40, self.Return_peaklist_40_SX,
                  self.Return_resolution_list, self.Return_resolution_SX,
                  self.Return_resolution_SX_list))

        pass

    def peak_selection(self, selection_mask):
        """
        """
        assert type(selection_mask) == list

        self.selection = True
        self.selection_mask = selection_mask



    def output_DataHolder (self):

        for DataHolder in self.collection_o_datasets :
            self.OutputDelegate.output(DataHolder)
            self.OutputDelegate.combine_lists(DataHolder)

    def ouput_align_peaks (self):

        reference_DataHolder = "not set"

        list_o_SX_DataHolder = []

        print ("ouput_align_check")

        for DataHolder in self.collection_o_datasets:

            print(DataHolder.type_of_data)

            if DataHolder.type_of_data == "reference":

                """
                Change to REF
                """

                reference_DataHolder = DataHolder

            else:
                list_o_SX_DataHolder.append(DataHolder)


        for DataHolder in list_o_SX_DataHolder:

            DataHolder.peak_match(reference_DataHolder.peaklist_40)


            pass

    """
    def output_DataHolder_summary_table2(self):

        list_of_pds = []
        for DataHolder in self.collection_o_datasets:
            # DataHolder_other_ds = DataHolder.resolution_SX
            # print("here_1", DataHolder.resolution_SX)
            # pd_df = pd.DataFrame(data=DataHolder_other_ds, index=None,
                                   # columns=[DataHolder.file_name])

            file_name1 = DataHolder.file_name + "_peak_poss"
            file_name2 = DataHolder.file_name + "_peak_res"

            # print("here_1", DataHolder.resolution_SX_list)
            # print("here_2", DataHolder.resolution_SX_list[0,:])
            # print("here_3", DataHolder.resolution_SX_list[1,:])
            # print(DataHolder.reference_list, len(DataHolder.reference_list))

    """

    """


            # pd_df_pos = pd.DataFrame(data=DataHolder.reference_list[0,:],
                                      # index=None, columns=[file_name1])

            # print(DataHolder.filtered_SX_peaklist_40, "here")

            if DataHolder.filtered_SX_peaklist_40 == "not set":
                # print(DataHolder.file_name)
                pd_df_pos = pd.DataFrame(data=DataHolder.peaklist_40[0,:],
                                   index=None, columns=[file_name1])
                list_of_pds.append(pd_df_pos)
                pass
            else:

                pd_df_pos_1 = pd.DataFrame(data=DataHolder.filtered_SX_peaklist_40[0,:],
                                           index=None, columns=[file_name1])

                # pd_df_res = pd.DataFrame(data=DataHolder.resolution_SX_list[1,:],
                                          # index=None, columns=[file_name2])

                # list_of_pds.append(pd_df_pos)
                list_of_pds.append(pd_df_pos_1)
                # list_of_pds.append(pd_df_res)

        result = pd.concat(list_of_pds, axis=1, sort=False)

        result.to_excel('summary_dataset_experiment.xlsx', sheet_name='Sheet1')

        result_diff = self.difference_dataframe(result)

        result_diff.to_excel(
            'summary_dataset_experiment_diff.xlsx', sheet_name='Sheet2')

    """


    def resolution_dataset_output (self):


        list_of_pds = []
        for DataHolder in self.collection_o_datasets:
            # DataHolder_other_ds = DataHolder.resolution_SX
            # print("here_1", DataHolder.resolution_SX)
            # pd_df = pd.DataFrame(data=DataHolder_other_ds, index=None,
                                   # columns=[DataHolder.file_name])

            file_name1 = DataHolder.file_name + "_peak_poss"
            file_name2 = DataHolder.file_name + "_peak_res"

            # print("here_1", DataHolder.resolution_SX_list)
            # print("here_2", DataHolder.resolution_SX_list[0,:])
            # print("here_3", DataHolder.resolution_SX_list[1,:])
            # print(DataHolder.reference_list, len(DataHolder.reference_list))

            """

            """


            # pd_df_pos = pd.DataFrame(data=DataHolder.reference_list[0,:],
                                      # index=None, columns=[file_name1])

            # print(DataHolder.filtered_SX_peaklist_40, "here")

            if DataHolder.filtered_SX_peaklist_40 == "not set":
                # print(DataHolder.file_name)
                pd_df_pos = pd.DataFrame(data=DataHolder.peaklist_40[0,:],
                                   index=None, columns=[file_name1])
                list_of_pds.append(pd_df_pos)
                pass
            else:

                # pd_df_pos_1 = pd.DataFrame(data=DataHolder.filtered_SX_peaklist_40[0,:],
                                           # index=None, columns=[file_name1])

                pd_df_res = pd.DataFrame(data=DataHolder.filtered_SX_resolution_40[1,:],
                                          index=None, columns=[file_name2])

                # list_of_pds.append(pd_df_pos)
                # list_of_pds.append(pd_df_pos_1)
                list_of_pds.append(pd_df_res)

        result = pd.concat(list_of_pds, axis=1, sort=False)

        result.to_excel('summary_dataset_experiment_resolution.xlsx', sheet_name='Sheet1')

        # result_res = self.resolution_dataframe(result)

        # result_diff.to_excel(
            # 'summary_dataset_experiment_diff.xlsx', sheet_name='Sheet2')

        self.resolution_dataframe(result)
        
        
        

    def resolution_dataframe (self, dataframe):
        """
        """

        if self.selection == True:
            resolution_row_dataframe = dataframe.loc[self.selection_mask, :]
        else:
            resolution_row_dataframe = dataframe


#        orginal_line
#        resolution_row_dataframe = dataframe.loc[[0, 1, 2, 3, 5, 13], :]

        """
        # This is where specific peaks are chosen for analysis - but this should
        # be flexible to the user

        """

        average_res_dataframe = pd.DataFrame(resolution_row_dataframe.mean())


        result_res_total = pd.concat([dataframe , average_res_dataframe])

        """
        # if wanting to place the averages underneath the relavent columns then
        # replace average_dataframe with average_dataframe.T

        """

    """
        result_res_total.to_excel(
            'summary_dataset_experiment_average_1.xlsx', sheet_name='Sheet2')
        print(result_res_total.describe(), "result_res_total check ")


    """

    """
    THIS FUNCTION HAS BEEN BLOCKED OUT TO SIMPLIFY OUTPUT


    def difference_dataframe (self, dataframe):


        list_o_column = dataframe.columns

        # print(list_o_column)

        temp_bucket = [dataframe[list_o_column[0]]]

        temp_bucket_list_o_names = [list_o_column[0]]

        # print (temp_bucket_list_o_names, "look here please")
        for name in list_o_column[1:] :

            print(name)
            difference_df = dataframe[
                list_o_column[0]] - dataframe[name]

            difference_df = difference_df.abs()

            temp_bucket_list_o_names.append( name + "_difference")


            temp_bucket.append(difference_df)



        result_diff = pd.concat(temp_bucket, axis = 1, join = 'inner')

        result_diff.columns = temp_bucket_list_o_names

        if self.selection == True:
            sum_dataframe = result_diff.loc[self.selection_mask, :]
        else:
            sum_dataframe = result_diff
#        Orginal_line
#        sum_dataframe = result_diff.loc[[0, 1, 2, 3, 5, 13], :]


        """
        # This is where specific peaks are chosen for analysis - but this should
        # be flexible to the user

    """

        average_dataframe = pd.DataFrame(sum_dataframe.mean())


        result_diff_total = pd.concat([result_diff , average_dataframe])

        """
        # if wanting to place the averages underneath the relavent columns then
        # replace average_dataframe with average_dataframe.T

    """

        result_diff_total.to_excel(
            'summary_dataset_experiment_average.xlsx', sheet_name='Sheet2')
        # print(sum_dataframe.describe(), "wagwan piffting ")


        return result_diff

    """

    def output_DataHolder_summary_table(self):

        list_of_pds = []
        for DataHolder in self.collection_o_datasets:
            # DataHolder_other_ds = DataHolder.resolution_SX
            # print("here_1", DataHolder.resolution_SX)
            # pd_df = pd.DataFrame(data=DataHolder_other_ds, index=None,
                                   # columns=[DataHolder.file_name])

            file_name1 = DataHolder.file_name + "_peak_poss"
            file_name2 = DataHolder.file_name + "_peak_res"

            print("here_1", DataHolder.resolution_SX_list)
            # print("here_2", DataHolder.resolution_SX_list[0,:])
            # print("here_3", DataHolder.resolution_SX_list[1,:])

            pd_df_pos = pd.DataFrame(data=DataHolder.resolution_SX_list[0,:],
                                      index=None, columns=[file_name1])

            pd_df_res = pd.DataFrame(data=DataHolder.resolution_SX_list[1,:],
                                      index=None, columns=[file_name2])

            list_of_pds.append(pd_df_pos)
            list_of_pds.append(pd_df_res)

        result = pd.concat(list_of_pds, axis=1, sort=False)

        result.to_excel('summary_dataset.xlsx', sheet_name='Sheet1')

        print(result)

    def set_name (self, file_name):

        self.file_name = file_name

        pass

    def set_data_array (self, Return_data_array):

        self.Return_data_array = Return_data_array

        pass

    def set_data_array40theta (self, Return_data_array40theta):

        self.Return_data_array40theta =  Return_data_array40theta

        pass

    def set_peaklist_40 (self, Return_peaklist_40):

        self.Return_peaklist_40 = Return_peaklist_40

        pass

    def set_peaklist_40_SX (self, Return_peaklist_40_SX):

        self.Return_peaklist_40_SX = Return_peaklist_40_SX

        pass


    def set_resolution_list (self, Return_resolution_list):

        self.Return_resolution_list = Return_resolution_list

        pass

    def set_resolution_SX (self, Return_resolution_SX) :

        self.Return_resolution_SX = Return_resolution_SX

        pass

    def set_resolution_SX_list (self, Return_resolution_SX_list):

        self.Return_resolution_SX_list = Return_resolution_SX_list

        pass


class OutputDelegate (object):
    """
    OutputDelegate outputs the data to a file format to open i.e. the data
    into an excel spreadsheet

    Does this by collecting the information from CentralDataHolder and the DataHolders
    """
    def __init__(self):

        pass

    def combine_lists (self, a_DataHolder):

        """
        Need to make a data array of 2 theta, peaks possition (2 theta),
        peak intensity (counts), peak possition ratio, peak intensity ratio,
        S2N (background) stuff

        .T means transpose

        """

        list_o_output  = a_DataHolder.peaklist_40_SX.T.tolist()

        # print ("list of_data", list_o_output)

        return list_o_output

    def output (self, a_DataHolder):

        """
        Converts information to output files , creates an output file
        directory only if one does not already exist
        """

        output_array = []

        original_data = a_DataHolder.data_array.T.tolist()

        peak_coordinates = a_DataHolder.peaklist_40_SX.T.tolist()

        resolution_coordinates = a_DataHolder.resolution_SX.T.tolist()

        def adding_data_into_out_array(array):
            for line in array:
                if type(line) == list:
                    new_string = ""
                    for element in line:
                        new_string = new_string + " " + str(element)
                    output_array.append(new_string)
                    output_array.append("\n")

                else:
                    output_array.append(str(line))
                    output_array.append("\n")

        output_array.append("res data\n")
        adding_data_into_out_array(resolution_coordinates)

        output_array.append("peak data\n")
        adding_data_into_out_array(peak_coordinates)

        output_array.append("Org data\n")
        adding_data_into_out_array(original_data)


        for element in range(len(output_array)):
            if type(output_array[element]) == list:
                # print(output_array[element], element)
                pass

        # output_array = original_data + peak_coordinates + resolution_coordinates
        # print(original_data[:10], "\n")
        # print(peak_coordinates[:10], "\n")
        # print(resolution_coordinates[:10], "\n")

        file = a_DataHolder.file_name

        individual_folder_o_files = file + "_processed_data"

        output_directory_location = "processed_data_files"

        file = file.replace(".xye", "_processed.txt")

        output_file_location = output_directory_location + "/" + file

        print (output_file_location)

        if os.path.isdir(output_directory_location):
            pass

        else:
            os.mkdir(output_directory_location)
            pass
        print(output_file_location)


        if os.path.isfile(output_file_location):
            print("Caution folder contains file with same name", file)

        # elif os.path.isfile(output_file_location_csv):
            # print("Caution folder contains file with same name", file_csv)

        else:
            print("here", output_file_location)

            with open(output_file_location, "w") as fileoutput:
                 fileoutput.writelines(output_array)

            # with open(output_file_location_csv, "w") as fileoutput:
                 # fileoutput.writelines()
        pass

class DataHolder (object):

    """
    DataHolder is an object that holds data for CentralDataHolder

    """

    def __init__ (self, file_name, Return_data_array, Return_data_array40theta,
                  Return_peaklist_40, Return_peaklist_40_SX,
                  Return_resolution_list, Return_resolution_SX,
                  Return_resolution_SX_list):

        self.file_name = file_name
        self.data_array = Return_data_array
        self.data_array_40theta = Return_data_array40theta
        self.peaklist_40 = Return_peaklist_40
        self.peaklist_40_SX = Return_peaklist_40_SX
        self.resolution_list = Return_resolution_list
        self.resolution_SX_list = Return_resolution_SX_list

        self.resolution_SX = Return_resolution_SX

        """
        check is this is correct, some Signle XRD values dont need to be set
        i.e. you end up setting them all in Helpere anyhow
        """
        assert type(file_name) == str
        print(type(Return_data_array))
        assert type(Return_data_array) == np.ndarray
        assert type(Return_data_array40theta) == np.ndarray
        assert type(Return_peaklist_40) == np.ndarray
        assert type(Return_peaklist_40_SX) == np.ndarray
        print(type(Return_resolution_list))
        assert type(Return_resolution_list) == np.ndarray
        assert type(Return_resolution_SX_list) == np.ndarray

        assert type(Return_resolution_SX) == np.ndarray


        print("DataHolder created")
        self.type_of_data = "not set"
        self.process_inputs()

        self.reference_list = "not set"
        self.filtered_SX_peaklist_40 = "not set"
        self.filtered_SX_resolution_40 = "not set"
        pass

    def process_inputs (self):

        if "_reference_" in self.file_name:
            self.type_of_data = "reference"

            """
            Change to REF

            """

        else:
            self.type_of_data = "SX"

        pass

    def peak_match (self, reference_list):

        self.reference_list = reference_list

        self.filtered_SX_peaklist_40 = []

#        print(reference_list, len(reference_list), "look here")

        peak_found = False

        for peak in self.reference_list[0] :

#            print("peak", peak)

            for SX_peak in self.peaklist_40_SX.T:

                if SX_peak[0] < (peak + 0.3) and SX_peak[0] > (peak - 0.3):

                    self.filtered_SX_peaklist_40.append(SX_peak)

                    peak_found = True

            if peak_found == False :

                self.filtered_SX_peaklist_40.append(np.array([0, 0]))

            else :

                peak_found = False

        print(len(self.filtered_SX_peaklist_40), "length of filtered_SX_peaklist 40")
        self.filtered_SX_peaklist_40 = np.vstack(
            self.filtered_SX_peaklist_40).T

        peak_possition_diff_ave = []
        resolution_ave = []
        self.filtered_SX_resolution_40 = []

        for peak in self.filtered_SX_peaklist_40.T :
#            print("start", peak[0], "end" )

            if peak[0] == 0.0:
                self.filtered_SX_resolution_40.append(np.array([0, 0]))
            else:
                for res_peak in self.resolution_SX_list.T :
                    if res_peak[0] == peak[0] :
                        self.filtered_SX_resolution_40.append(res_peak)
            pass

        self.filtered_SX_resolution_40 = np.vstack(
            self.filtered_SX_resolution_40).T

        print(self.filtered_SX_resolution_40, "filtered_SX_resolution check" )


#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("echo")
#args = parser.parse_args()
#print(args.echo)


if __name__ == "__main__":


    screen_splash = """
░█████╗░██████╗░██████╗░███████╗██████╗░░█████╗░████████╗██╗░█████╗░███╗░░██╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║
██║░░██║██████╔╝██████╔╝█████╗░░██████╔╝███████║░░░██║░░░██║██║░░██║██╔██╗██║
██║░░██║██╔═══╝░██╔═══╝░██╔══╝░░██╔══██╗██╔══██║░░░██║░░░██║██║░░██║██║╚████║
╚█████╔╝██║░░░░░██║░░░░░███████╗██║░░██║██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║
░╚════╝░╚═╝░░░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝

██████╗░░█████╗░████████╗░█████╗░
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
██║░░██║███████║░░░██║░░░███████║
██║░░██║██╔══██║░░░██║░░░██╔══██║
██████╔╝██║░░██║░░░██║░░░██║░░██║
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝

░█████╗░███╗░░██╗░█████╗░██╗░░░░░██╗░░░██╗░██████╗██╗░██████╗
██╔══██╗████╗░██║██╔══██╗██║░░░░░╚██╗░██╔╝██╔════╝██║██╔════╝
███████║██╔██╗██║███████║██║░░░░░░╚████╔╝░╚█████╗░██║╚█████╗░
██╔══██║██║╚████║██╔══██║██║░░░░░░░╚██╔╝░░░╚═══██╗██║░╚═══██╗
██║░░██║██║░╚███║██║░░██║███████╗░░░██║░░░██████╔╝██║██████╔╝
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚═════╝░╚═╝╚═════╝░
"""

    print(screen_splash)
#    intput_variables = input("please enter important information")



    """
    a_Format_Fetcher.read_files() is where the folder of data is given, by changing
    this the program will open up a different folder of datafiles
    """


    a_CentralDataHolder = CentralDataHolder()

    a_CentralDataHolder.testname = "test"

    a_Format_Fetcher = Format_Fetcher()
    a_Format_Fetcher.read_files("test-data")

    # a_Format_Fetcher.read_files("background-removed_sep20data")

    a_Process_Manager = Process_Manager()

    a_Process_Manager.collect_files(a_Format_Fetcher)

    a_Process_Manager.opener_o_files(a_CentralDataHolder)

    a_CentralDataHolder.ouput_align_peaks()

  
    peak_mask = [0, 1, 2, 3, 5, 13]

    a_CentralDataHolder.peak_selection([0, 1, 2, 3, 5, 13])


    a_CentralDataHolder.output_DataHolder()

    # a_CentralDataHolder.output_DataHolder_summary_table2()

    a_CentralDataHolder.resolution_dataset_output()

    # a_CentralDataHolder.output_DataHolder_summary_table()




######

    # with open("Test-pickle", "wb") as file1:
        # pickle.dump(a_CentralDataHolder, file1)

    # with open("Test-pickle", "rb") as file1:
        # unpickle_CentralDataHolder = pickle.load(file1)
