#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re as r
import glob
import io
import numpy as np
import log

from math import cos
from datetime import datetime, time
import xml.parsers as pars
from xml.dom import minidom


__component_name__ = "metadata-extraction"  # Extract Metadata for Landsat Products (LS01 - LS08)
__author__ = "Sebastien Saunier"
__copyright__ = "Copyright 2017, TPZ"
__version__ = "0.1.0"
__status__ = "Production"  # "Prototype", "Development", or "Production"
description = __component_name__ + " version:" + __version__ + " (" + __status__ + ")"


# July, 13 Wednesday : S . Saunier
#   -- Cron Data Import --
#      - inspect if data in INPUT DATA
#      -Import data
#      -Applied pre processing
#      -



# 20/12/2016 - Re package for uk - Add Error Management
# For missing mtl, missing image file, empty test site
# 20/03/2017 - Modification add self.'isValid'
#            - Modification get_in_band_solar_irrandiance_value in order to Account
#              for Sensor = 'MSS' and not necessary 'MSS_X'
# 13/12/2017 - Add Sentinel 2 Class.


class LandsatMTL:
    # Object for methadata extraction

   def __init__(self, product_path):
        self.isValid = True
        print ' '
        log.info('Landsat MTL Class    : \n')
        log.info('- Product : ')
        log.info('            '+str(product_path))
        self.product_path = product_path
        re = 'L*_MTL.txt'
        md_list = glob.glob(os.path.join(self.product_path, re))

        if not os.path.exists((self.product_path)):
            log.err(' -- Input product does not exist')
            self.isValid = False
            return

        #check if MTL file is present
        if not md_list:
            log.err(' Warning - no MTL file found')
            log.err(' Procedure aborted')
            self.isValid = False
            return

        try:
            mtl_file_name = glob.glob(os.path.join(self.product_path, re))[0]
            self.mtl_file_name = mtl_file_name
            mtl_file = io.open(mtl_file_name, 'rU')
            mtl_text = mtl_file.read()
            mtl_file.close()
            f = mtl_file_name
            self.product_name = os.path.dirname(f).split('\\')[-1]  # PRODUCT_NAME
            regex = r.compile('LANDSAT_SCENE_ID =.*')
            res = regex.findall(mtl_text)
            if res:
                self.landsat_scene_id = (((res)[0].split('='))[1].replace('"', '')).replace(' ', '')
            else:
                self.landsat_scene_id = ((os.path.basename(mtl_file_name).split('_'))[0]).replace(' ', '')
            print ' -- Landsat_id : ' + self.landsat_scene_id + ' \n'
            string_to_search = 'FILE_DATE =.*'
            self.file_date = reg_exp(mtl_text, string_to_search)
            string_to_search = 'PROCESSING_SOFTWARE_VERSION =.*'
            self.processing_sw = reg_exp(mtl_text, string_to_search)
            string_to_search = 'SPACECRAFT_ID =.*'
            self.mission = reg_exp(mtl_text, string_to_search)
            string_to_search = 'SENSOR_ID =.*'
            self.sensor = reg_exp(mtl_text, string_to_search)
            string_to_search = 'DATA_TYPE =.*'
            self.data_type = reg_exp(mtl_text, string_to_search)
            data_type = self.data_type
            string_to_search = 'MODEL_FIT_TYPE =.*'
            #MODEL_FIT_TYPE = "L1T_SINGLESCENE_OPTIMAL"
            #MODEL_FIT_TYPE = "L1T_MULTISCENE_SUBOPTIMAL"
            #MODEL_FIT_TYPE = "L1G+_MULTISCENE_SUBOPTIMAL"            
            self.model_fit = reg_exp(mtl_text, string_to_search)

            if data_type == "L1T":
                string_to_search = 'ELEVATION_SOURCE =.*'
                self.elevation_source = reg_exp(mtl_text, string_to_search)				
            else:
                self.elevation_source = 'N/A'
            string_to_search = 'OUTPUT_FORMAT =.*'  # OUTPUT_FORMAT

            self.output_format = reg_exp(mtl_text, string_to_search)
            string_to_search = 'EPHEMERIS_TYPE =.*'
            self.ephemeris_type = reg_exp(mtl_text, string_to_search)
            string_to_search = 'SPACECRAFT_ID =.*'
            self.spacecraft_id = reg_exp(mtl_text, string_to_search)
            string_to_search = 'SENSOR_ID =.*'
            self.sensor_id = reg_exp(mtl_text, string_to_search)
            string_to_search = 'WRS_PATH =.*'
            self.path = reg_exp(mtl_text, string_to_search)
            string_to_search = 'WRS_ROW =.*'
            self.row = reg_exp(mtl_text, string_to_search)
            string_to_search = 'DATE_ACQUIRED =.*'
            self.observation_date = reg_exp(mtl_text, string_to_search)
            string_to_search = 'SCENE_CENTER_TIME =.*'
            self.scene_center_time = reg_exp(mtl_text, string_to_search)

            self.scene_boundary_lat = []
            string_to_search = 'CORNER_UL_LAT_PRODUCT =.*'
            self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))
            string_to_search = 'CORNER_UR_LAT_PRODUCT =.*'
            self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))
            string_to_search = 'CORNER_LR_LAT_PRODUCT =.*'
            self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))
            string_to_search = 'CORNER_LL_LAT_PRODUCT =.*'
            self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))

 			
            self.scene_boundary_lon = []
            string_to_search = 'CORNER_UL_LON_PRODUCT =.*'
            self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
            string_to_search = 'CORNER_UR_LON_PRODUCT =.*'
            self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
            string_to_search = 'CORNER_LR_LON_PRODUCT =.*'
            self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
            string_to_search = 'CORNER_LL_LON_PRODUCT =.*'
            self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
#INFORMATION ON GROUND CONTROL POINTS
            string_to_search = 'GROUND_CONTROL_POINT_FILE_NAME =.*'
            self.gcp_filename = reg_exp(mtl_text, string_to_search)

            if self.processing_sw == "SLAP_03.04":
                if self.data_type == "L1T":
                    print "GCP : ",self.gcp_filename
                    if self.gcp_filename != 'NotApplicable-geometricrefinementusingneighbouringscenes' :
			            self.model_fit =  "L1T_SINGLESCENE_OPTIMAL"
                    else :
                        self.model_fit =  "L1T_MULTISCENE_SUBOPTIMAL"
            string_to_search = 'GROUND_CONTROL_POINTS_MODEL =.*'
            self.gcp_nb = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GROUND_CONTROL_POINTS_DISCARDED =.*'
            self.gcp_nb_dis = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GEOMETRIC_RMSE_MODEL =.*'
            self.gcp_rms = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GEOMETRIC_RMSE_MODEL_Y =.*'
            self.gcp_rms_x = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GEOMETRIC_RMSE_MODEL_X =.*'
            self.gcp_rms_y = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GEOMETRIC_MAX_ERR =.*'
            self.gcp_max_err = reg_exp(mtl_text, string_to_search)

            string_to_search = 'GROUND_CONTROL_POINT_RESIDUALS_SKEW_X =.*'
            self.gcp_res_skew_x = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GROUND_CONTROL_POINT_RESIDUALS_SKEW_Y =.*'
            self.gcp_res_skew_y = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GROUND_CONTROL_POINT_RESIDUALS_KURTOSIS_X =.*'
            self.gcp_res_kurt_x = reg_exp(mtl_text, string_to_search)
            string_to_search = 'GROUND_CONTROL_POINT_RESIDUALS_KURTOSIS_Y =.*'
            self.gcp_res_kurt_y = reg_exp(mtl_text, string_to_search)
			
#QA INFORMATION
            if (
                    (self.mission == 'LANDSAT_1') or
                    (self.mission == 'LANDSAT_2') or
                    (self.mission == 'LANDSAT_3')
            ):
  
                string_to_search = 'IMAGE_QUALITY_BAND_4 =.*'
                iq_band_1 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'IMAGE_QUALITY_BAND_5 =.*'
                iq_band_2 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'IMAGE_QUALITY_BAND_6 =.*'
                iq_band_3 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'IMAGE_QUALITY_BAND_7 =.*'
                iq_band_4 = reg_exp(mtl_text, string_to_search)
				
                string_to_search = 'SLA_PIXELS_BAND_4 =.*'
                sla_band_1 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'SLA_PIXELS_BAND_5 =.*'
                sla_band_2 = reg_exp(mtl_text, string_to_search)				
                string_to_search = 'SLA_PIXELS_BAND_6 =.*'
                sla_band_3 = reg_exp(mtl_text, string_to_search)			
                string_to_search = 'SLA_PIXELS_BAND_7 =.*'
                sla_band_4 = reg_exp(mtl_text, string_to_search)			

            if (
                    (self.mission == 'LANDSAT_4') or
                    (self.mission == 'LANDSAT_5')
            ):
 
                string_to_search = 'IMAGE_QUALITY_BAND_1 =.*'
                iq_band_1 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'IMAGE_QUALITY_BAND_2 =.*'
                iq_band_2 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'IMAGE_QUALITY_BAND_3 =.*'
                iq_band_3 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'IMAGE_QUALITY_BAND_4 =.*'
                iq_band_4 = reg_exp(mtl_text, string_to_search)

                string_to_search = 'SLA_PIXELS_BAND_1 =.*'
                sla_band_1 = reg_exp(mtl_text, string_to_search)
                string_to_search = 'SLA_PIXELS_BAND_2 =.*'
                sla_band_2 = reg_exp(mtl_text, string_to_search)				
                string_to_search = 'SLA_PIXELS_BAND_3 =.*'
                sla_band_3 = reg_exp(mtl_text, string_to_search)			
                string_to_search = 'SLA_PIXELS_BAND_4 =.*'
                sla_band_4 = reg_exp(mtl_text, string_to_search)
                if ( iq_band_1 ) :
                    self.iq_band_1 = iq_band_1
                if ( iq_band_2 ) :
                    self.iq_band_2 = iq_band_2
                if ( iq_band_3 ) :
                    self.iq_band_3 = iq_band_3
                if ( iq_band_4 ) :
                    self.iq_band_4 = iq_band_4
                if ( sla_band_1 ) :
                    self.sla_band_1 = sla_band_1
                if ( sla_band_2 ) :
                    self.sla_band_2 = sla_band_2
                if ( sla_band_3 ) :
                    self.sla_band_3 = sla_band_3
                if ( sla_band_4 ) :
                    self.sla_band_4 = sla_band_4

			
			
#INFORMATION ON FILE NAMES
            string_to_search = 'METADATA_FILE_NAME =.*'
            self.md_filename = reg_exp(mtl_text, string_to_search)
            string_to_search = 'CPF_NAME =.*'
            self.cpf_filename = reg_exp(mtl_text, string_to_search)

            string_to_search = 'CLOUD_COVER =.*'
            self.cloud_cover = reg_exp(mtl_text, string_to_search)
            string_to_search = 'CLOUD_COVER_AUTOMATED_L1 =.*'
            self.cloud_cover_l1 = reg_exp(mtl_text, string_to_search)
            string_to_search = 'IMAGE_QUALITY =.*'
            self.image_quality = reg_exp(mtl_text, string_to_search)
            string_to_search = 'SUN_AZIMUTH =.*'
            self.sun_azimuth_angle = reg_exp(mtl_text, string_to_search)
            string_to_search = 'SUN_ELEVATION =.*'
            self.sun_zenith_angle = 90.0 - np.float(reg_exp(mtl_text, string_to_search))
            string_to_search = 'UMT_ZONE =.*'
            self.utm_zone = reg_exp(mtl_text, string_to_search)

            regex = r.compile('FILE_NAME_BAND_.* =.*')
            result = (regex.findall(mtl_text))
            image_file_name = []
            band_sequence = []
            for k in result:
                image_file_band_name = ((k.split('='))[1].replace(' ', '').replace('"', ''))
                image_file_name.append(image_file_band_name)
                band_id = str((image_file_band_name.split('.')[0]).split('B')[-1])
                if band_id != 'QA':
                    band_sequence.append(band_id)
            self.band_sequence = band_sequence

            regex = r.compile('RADIANCE_MAXIMUM_BAND_.* =.*')
            result = (regex.findall(mtl_text))
            radiance_maximum = []
            for k in result:
                v = np.float((k.split('='))[1].replace(' ', ''))
                radiance_maximum.append(v)
            self.radiance_maximum = radiance_maximum

            regex = r.compile('RADIANCE_MINIMUM_.* =.*')
            result = (regex.findall(mtl_text))
            radiance_minimum = []
            for k in result:
                v = np.float((k.split('='))[1].replace(' ', ''))
                radiance_minimum.append(v)
            self.radiance_minimum = radiance_minimum

            regex = r.compile('RADIANCE_MULT_BAND_.* =.*')
            result = (regex.findall(mtl_text))
            rescaling_gain = []
            for k in result:
                v = np.float((k.split('='))[1].replace(' ', ''))
                rescaling_gain.append(v)
            self.rescaling_gain = rescaling_gain

            regex = r.compile('RADIANCE_ADD_BAND_.* =.*')
            result = (regex.findall(mtl_text))

            rescaling_offset = []
            for k in result:
                v = np.float((k.split('='))[1].replace(' ', ''))
                rescaling_offset.append(v)
            self.rescaling_offset = rescaling_offset
            self.doy = int(self.landsat_scene_id[13:16])
            self.dE_S = compute_earth_solar_distance(self.doy)
            self.sun_earth_distance = compute_earth_solar_distance(self.doy)
            self.solar_irradiance = get_in_band_solar_irrandiance_value(self.mission, self.sensor)
            self.radiance_to_reflectance_coefficient = self.compute_radiance_to_reflectance_coefficient()
		   #  BQA List
            [self.bqa,self.bqa_filename] = self.get_qa_band()
           #  Image list
            self.dn_image_list = self.set_image_file_name('DN')
            self.radiance_image_list = self.set_image_file_name('RAD')
            self.rhotoa_image_list = self.set_image_file_name('RHO')
            self.surf_image_list = self.set_image_file_name('surf')
            # Check Image_file_name versus MTL information
            self.missing_image_in_list = 'FALSE'
            for ch in image_file_name:
               if (os.path.exists(os.path.join(self.product_path, ch)) is False):
                  self.missing_image_in_list = 'Missing_image'

            # Additionnal information - post computed - Test site
            self.test_site = ' '
            self.interest = ' '

        except IndexError:
        # if not md_list:
           print ' -- Warning - no MTL file found'
           print ' -- Procedure aborted'
           self.mtl_file_name = ''


   def display_mtl_info(self):
      print " "
      print "Product Metadata : \n"
      print " -- Mission : " + self.mission
      print " -- Sensor : " + self.sensor
      print " -- Data Type : " + self.data_type
      print " -- Observation Date : " + self.observation_date
      print " -- Observation Time : " + self.scene_center_time
      print " -- Product Path / Row : " + self.path + ' / ' + self.row
      for k, site_info in enumerate(self.test_site):
         print " -- Test site / Interest : " + site_info + ' / ' + self.interest[k]
        # return ch

      print " "
      print " -- Product_path : " + self.product_path
      print " -- Mtl File : " + self.mtl_file_name
      print " -- Observation Date : " + self.observation_date
      print " -- Day Of Year : " + str(self.doy)
      print ' '
      print " -- Band _id : " + str([v for v in self.band_sequence])
      print " -- Gain : " + str(self.rescaling_gain)
      print " -- Offset : " + str(self.rescaling_offset)
      print " -- Solar Irradiance : " + str(self.solar_irradiance)
      print " -- Radiance to Reflectance factor : " + str(self.radiance_to_reflectance_coefficient)
      print " "
      print " -- Earth Sun Distance  : " + str(self.dE_S)
      print " "
      print " "


   def get_scene_center_coordinates(self):
      lon = np.divide(np.sum(np.double(self.scene_boundary_lon)), 4)
      lat = np.divide(np.sum(np.double(self.scene_boundary_lat)), 4)
      return [lon, lat]

   def get_qa_band(self):
      try :
         bqa_filename = glob.glob(os.path.join(self.product_path,self.landsat_scene_id+'_BQA.TIF'))[0]
         bqa = True
      except IndexError:	 
         bqa_filename = ' ' 
         bqa = False 
      return bqa,bqa_filename
   
   
   def set_image_file_name(self, opt):
      product_path = self.product_path
      image_list = []

      if opt == 'DN':
        print ' -- DN configuration'
#        regex1 = os.path.join(product_path, 'L[O,M,T,C][1-8]*[0-9]_B?.TIF')
#        regex2 = os.path.join(product_path, 'L[O,M,T,C][1-8]*[0-9]_B?[0-3].TIF')
#        regex3 = os.path.join(product_path, 'L[O,M,T,C][1-8]*[0-9]_B?.TIFF')
		# Premier regex4 : [0-9,T] ne fonctionne pas
        #regex4 = os.path.join(product_path, 'L[O,M,T,C][0][1-8].*[_,_MTI_]B?.TIF')
        regex4 = 'L[O,M,T,C]0[1-8].*?_(RT|LT)(_MTI)?_B\d{1,2}.TIF'
        p = r.compile(regex4)
        image_list_g = glob.glob(regex4)
        first_list = glob.glob((os.path.join(product_path,'*.TIF')))
        image_list_g = [rec for rec in first_list if p.match(os.path.basename(rec)) ]		
#        for rec in first_list :
#            print (os.path.basename(rec))
#            print p.match(os.path.basename(rec))

#        print [p.search(rec) for rec in first_list]
#        regex4 = os.path.join(product_path, 'L[O,M,T,C][0][1-8]*[_,_MTI_]B?.TIF')
          
#        image_list_g = glob.glob(regex1) + glob.glob(regex2)  + glob.glob(regex3) + glob.glob(regex4)
#        image_list_g = glob.glob(regex4)
        if (len(image_list_g) == 0) :
            print product_path
            print "%%%%% [WARNING] - No Level 1 DN image file found "
            print "%%%%% [WARNING] - Check function  [set_image_file_name]"
        array = []
        for rec in image_list_g:
            filename = os.path.basename(rec)

            if (((filename.split('_')[1]).split('.')[0]).replace('B', '')) == 'L1TP' :
                # LT05_L1TP_198030_20111011_20161005_01_T1_B1.TIF
                # LC08_L1TP_199030_20170527_20170527_01_RT_B1.TIF
                print 'usgs collection product'
                band_id = int(((filename.split('B')[1]).split('.')[0]).replace('B', ''))
                rad = (filename.split('_B')[0])
            else :
                 #LM51990301985107ESA00_B1.TIF
                 band_id = int(((filename.split('_')[1]).split('.')[0]).replace('B', ''))
                 rad = filename.split('_')[0]

            print 'Radical ',rad
            array.append([band_id, rec])

        array_sort = sorted(array, key=lambda x: x[0])
        for rec in array_sort:
            image_list.append(rec[1])

      if opt == 'RAD':
        dn_image = self.dn_image_list
        print ' -- RADIANCE configuration'
        image_list = []
        for rec in dn_image:
            filename = os.path.basename(rec)
            if (((filename.split('_')[1]).split('.')[0]).replace('B', '')) == 'L1TP' :
                # LT05_L1TP_198030_20111011_20161005_01_T1_B1.TIF
                print 'usgs collection product'
                band_id = int(((filename.split('B')[1]).split('.')[0]).replace('B', ''))
                rad = (filename.split('_B')[0])
            else :
                 #LM51990301985107ESA00_B1.TIF
                 band_id = int(((filename.split('_')[1]).split('.')[0]).replace('B', ''))
                 rad = filename.split('_')[0]

            print os.path.join(product_path, ''.join([rad, '_RAD_', str(band_id)]))
            image_list.append(os.path.join(product_path, ''.join([rad, '_RAD_B', str(band_id),'.TIF'])))

      if opt == 'RHO':
        print ' -- TOA REFLECTANCE configuration'
        dn_image = self.dn_image_list
        regex = os.path.join(product_path, 'L[O,M,T,C][0][1-8]*RHO*.TIF') #RHO TOA Products
        image_list = glob.glob(regex)
        if (len(image_list) == 0) :
            print "%%%%% [WARNING] - No R TOA file found "
        else:
            print "%%%%% RHO TOA Reflectance files found : set "


        image_list = []

        for rec in dn_image:
            filename = os.path.basename(rec)
            product_path = os.path.dirname(rec)
            if (((filename.split('_')[1]).split('.')[0]).replace('B', '')) == 'L1TP' :
                # LT05_L1TP_198030_20111011_20161005_01_T1_B1.TIF
                print 'usgs collection product'
                band_id = int(((filename.split('B')[1]).split('.')[0]).replace('B', ''))
                rad = (filename.split('_B')[0])
            else :
                 #LM51990301985107ESA00_B1.TIF
                 band_id = int(((filename.split('_')[1]).split('.')[0]).replace('B', ''))
                 rad = filename.split('_')[0]

            image_list.append(os.path.join(self.product_path, ''.join([rad, '_RHO_B', str(band_id),'.TIF'])))

      if opt == 'surf':
        # Assume no additional transformation needed
        print ' -- SURFACE REFLECTANCE configuration'
        regex = os.path.join(product_path, 'L[O,M,T,C][0][1-8]*_sr_band?.tif') #SR Products
        image_list = glob.glob(regex)
        if (len(image_list) == 0) :
            print product_path
            print "%%%%% [WARNING] - No SR file found [set_image_file_name]"
        else:
            print "%%%%% !!!!!!!!! - Surface Reflectance file found, [self.surf_image_list] is set"


      return image_list


   def update_image_file_list(self):
    # Force to re order list - glob glob does not order according to band id
    # Process Radiance List
    radiance_image_list = [rec for rec in glob.glob(os.path.join(self.product_path, '*RAD*'))]
    array = []
    image_list = []
    print 'radiance list'

    for rec in radiance_image_list:
        print rec
        filename = os.path.basename(rec)
        rad = filename.split('_')[0]
        band_id = int(((filename.split('_')[2]).split('.')[0]).replace('B', ''))
        array.append([band_id, rec])
    array_sort = sorted(array, key=lambda x: x[0])
    print ' '
    for rec in array_sort:
        print rec
        image_list.append(rec[1])

    self.radiance_image_list = image_list

    # Process Reflectance List
    rhotoa_image_list = [rec for rec in glob.glob(os.path.join(self.product_path, '*RHO*TIF'))]
    array = []
    image_list = []
    for rec in rhotoa_image_list:
        filename = os.path.basename(rec)
        rad = filename.split('_')[0]
        band_id = int(((filename.split('_')[2]).split('.')[0]).replace('B', ''))
        array.append([band_id, rec])
    array_sort = sorted(array, key=lambda x: x[0])
    for rec in array_sort:
        image_list.append(rec[1])

    self.rhotoa_image_list = image_list


   def display_image_file_info(self):
    for image in self.dn_image_list:
        print image
    print ' '
    for image in self.radiance_image_list:
        print image
    print ' '
    for image in self.rhotoa_image_list:
        print image
    print ' '


   def compute_radiance_to_reflectance_coefficient(self):
   # Out coefficient for each band
   # Calculer uniqument pour les bandes specifie dans and_sequenc
    mission = self.mission
    len_tab = len(self.solar_irradiance)
    radianceToReflectance_coefficient = [0 for i in range(len_tab)]
    dE_S = self.dE_S
    sza = np.float(self.sun_zenith_angle)
    solar_irradiance = self.solar_irradiance
    for k, band_id in enumerate(self.band_sequence):
        if (
                        (self.mission == 'LANDSAT_1') or
                        (self.mission == 'LANDSAT_2') or
                    (self.mission == 'LANDSAT_3')
        ):
            band_num = np.int(band_id) - 4
        else:
            # print str(band_id)
            band_num = np.int(band_id) - 1

        esun = solar_irradiance[band_num]
        quotient = np.multiply(esun, np.cos(np.multiply(sza, np.divide(np.pi, 180))))
        if quotient != 0.00:
            factor = np.divide(
                np.multiply(np.pi, np.power((dE_S), 2)),
                quotient
            )
        else:
            factor = 1
            # En sortie du processeur radiance*10 et donc pour convertir en reflectance_data
            # Il faut multiplie par 0.1
        c = 1.0
        radianceToReflectance_coefficient[band_num] = c * factor

    # FORMULE
    # (radiance*pi*dE_S*dE_S)/(esun*cos((sza)*pi/180));

    return radianceToReflectance_coefficient


   def get_info(self):
   # Allow to expert elements of instance for direct insertion into CSV
    scene_id = self.landsat_scene_id
    obs_date = self.observation_date
    sc_time = self.scene_center_time
    doy = str(self.doy)
    sza = str(self.sun_zenith_angle)
    saa = str(self.sun_azimuth_angle)
    gain = ''
    offset = ''
    radiance_min = ''
    radiance_max = ''
    for rec, v in enumerate(self.rescaling_gain):
        gain += str(v) + ' '
        offset += str(self.rescaling_offset[rec]) + ' '
        radiance_min += str(self.radiance_minimum[rec]) + ' '
        radiance_max += str(self.radiance_maximum[rec]) + ' '
    ch = ' '.join([scene_id, obs_date, sc_time, doy,
                   sza, saa, gain, offset, radiance_min, radiance_max])
    return ch


   def get_band_info(self, band_id):
   # Allow to expert elements of instance for direct insertion into CSV
    scene_id = self.landsat_scene_id
    obs_date = self.observation_date
    sc_time = self.scene_center_time
    doy = str(self.doy)
    sza = str(self.sun_zenith_angle)
    saa = str(self.sun_azimuth_angle)
    gain = str(self.rescaling_gain[band_id - 1])
    offset = str(self.rescaling_offset[band_id - 1])
    radiance_min = str(self.radiance_minimum[band_id - 1])
    radiance_max = str(self.radiance_maximum[band_id - 1])
    ch = ' '.join([scene_id, str(band_id), obs_date, sc_time, doy,
                   sza, saa, gain, offset, radiance_min, radiance_max])
    return ch


   def add_roi_name_information(self, roi_name):
    self.test_site = self.test_site[0] + ':' + roi_name
    return self.test_site


   def set_test_site_information(self, desc_site_file):
   # desc site file - list test site file and properties
   # Objectif : Find a test site defined in desc site file for the product
   # by default no site recognize
   # Test site information => Site Name and Possible Assessment
    site_id_o = 'N/A'
    site_label_o = ''
    country_o = ''

    # Access to XML File 'desc_site_file' for each geo coordinates
    # Test if coordinates is within scene footprint
    # Build vector datatabase
    #         delta_lon : UR - UL (difference of longitude)
    #         delta_lat : LL - UL (difference of latitude)
    #
    # Relative position of input points - lat/lon (from desc File )
    #         lambdaLat = lat - UL (latitude)
    #         lambdaLon = lon - UL (longitude)
    #
    # Projection of the point in the databas
    #         beta 1 = lambdaLat / delta_lat
    #         beta 2 = lambdaLon / delta_lon
    #
    # if beta_1 and beta_2 are < 1.0 alors le point (site) appartient au vertex d entree (produit)


    delta_lon = np.double(self.scene_boundary_lon[1]) - np.double(self.scene_boundary_lon[0])
    delta_lat = np.double(self.scene_boundary_lat[0]) - np.double(self.scene_boundary_lat[3])

    xmldoc = minidom.parse(desc_site_file)
    sites = xmldoc.getElementsByTagName('site')  # get all the sites

    self.test_site = []
    self.interest = []

    record_number = -1
    cpt = 0
    for site in sites:
        site_id = site.getElementsByTagName('id')[0].childNodes[0].data
        site_label = site.getElementsByTagName('label')[0].childNodes[0].data
        country = site.getElementsByTagName('country')[0].childNodes[0].data
        latitude_ctr = site.getElementsByTagName('latCenter')[0].childNodes[0].data
        longitude_ctr = site.getElementsByTagName('lonCenter')[0].childNodes[0].data
        lamdaLat = -np.double(latitude_ctr) + np.double(self.scene_boundary_lat[0])
        lamdaLon = -np.double(longitude_ctr) + np.double(self.scene_boundary_lon[0])
        beta_longitude = np.divide(lamdaLon, delta_lon)
        beta_latitude = np.divide(lamdaLat, delta_lat)
        # print site_id
        # print str(beta_latitude)+' '+str(beta_longitude)
        ##Repere oriente avec le upper left d ou condition sur le if
        if ((0 < (beta_latitude) < 1) and (-1 < (beta_longitude) < 0)):
            site_id_o = site_id
            site_label_o = site_label
            country_o = country
            ch = ' '.join([country_o, site_id_o])
            record_number = cpt
            site = xmldoc.getElementsByTagName('site')[record_number]
            stabilityMonitoringFlag = site.getElementsByTagName('stabilityMonitoring')[0].childNodes[0].data
            directLocationFlag = site.getElementsByTagName('directLocation')[0].childNodes[0].data
            interbandRegistrationFlag = site.getElementsByTagName('interbandRegistration')[0].childNodes[0].data
            mtfFlag = site.getElementsByTagName('MTF')[0].childNodes[0].data

            interest_ch = ''
            if stabilityMonitoringFlag == 'Y':
                interest_ch += ' stabilityMonitoring'
            if directLocationFlag == 'Y':
                interest_ch += ' directLocation'
            if interbandRegistrationFlag == 'Y':
                interest_ch += ' interbandRegistration'
            if mtfFlag == 'Y':
                interest_ch += ' MTF'

            self.test_site.append(ch)
            self.interest.append(interest_ch)

        cpt += 1


   def get_test_site_information(self):
    # if no ROI DEFINED DO NOT CONSIDER test_site



    return self.test_site

#########################################################################
#                                                                       #
#              S2 MSI L1 / L2 Sentinel 2 Class                          #
#                                                                       #
#########################################################################

class Sentinel2MTL:
    # Object for methadata extraction

    def __init__(self, product_path):
        self.isValid = True
        print ' '
        log.info( 'Sentinel 2 MTL Class    : \n')
        log.info(' -- Product : ' + str(product_path))
        self.product_path = product_path
        if not os.path.exists((self.product_path)):
            log.err( 'input product does not exist')
            self.isValid = False
            return

        re = 'MTD*_MSI*.xml'
        radical = os.path.basename(product_path)
        search_path = os.path.join(self.product_path, radical+'.SAFE',re);
        md_list = glob.glob(os.path.join(self.product_path, radical+'.SAFE',re))
        if not md_list :
            log.err( 'no MTL File found')
            self.isValid = False
            return

        mtl_file_name = md_list[0]

        try :
            dom = minidom.parse(mtl_file_name)
        except pars.expat.ExpatError:
            log.err( ' -- Not well formed MTL file')
            self.isValid = False
            return
#Read XML Metadata
        try:
            #mini dom
            mtl_file_name = glob.glob(os.path.join(self.product_path, radical+'.SAFE', re))[0]
            self.mtl_file_name = mtl_file_name
            node = (dom.getElementsByTagName('PRODUCT_URI'))[0]
            self.product_name = ((node.childNodes)[0]).data
            self.scene_id = (self.product_name).replace('.SAFE','')

            #FILE_DATE = 2017 - 11 - 30T16:00:05Z %DEFINITION LANDSAT
            node_name = 'GENERATION_TIME'
            node = (dom.getElementsByTagName(node_name))[0]
            self.file_date = ((node.childNodes)[0]).data

            node_name = 'PROCESSING_BASELINE'
            node = (dom.getElementsByTagName(node_name))[0]
            self.processing_sw = ((node.childNodes)[0]).data

            node_name = 'SPACECRAFT_NAME'
            node = (dom.getElementsByTagName(node_name))[0]
            self.mission = ((node.childNodes)[0]).data
            self.sensor = 'MSI'

            node_name = 'PRODUCT_TYPE'
            node = (dom.getElementsByTagName(node_name))[0]
            self.data_type = ((node.childNodes)[0]).data

            # return
            #
            # string_to_search = 'MODEL_FIT_TYPE =.*'
            # self.model_fit = ''
            #
            # if data_type == "Level-1C":
            #     string_to_search = 'ELEVATION_SOURCE =.*'
            #     self.elevation_source = ''
            # else:
            #     self.elevation_source = 'N/A'
            # string_to_search = 'OUTPUT_FORMAT =.*'  # OUTPUT_FORMAT
            #
            # self.output_format = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'EPHEMERIS_TYPE =.*'
            # self.ephemeris_type = ''
            # string_to_search = 'SPACECRAFT_ID =.*'
            # self.spacecraft_id = self.mission
            # string_to_search = 'SENSOR_ID =.*'
            # self.sensor_id = self.sensor
            # string_to_search = 'WRS_PATH =.*'
            # self.path = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'WRS_ROW =.*'
            # self.row = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'DATE_ACQUIRED =.*'
            # self.observation_date = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'SCENE_CENTER_TIME =.*'
            # self.scene_center_time = reg_exp(mtl_text, string_to_search)
            #
            # self.scene_boundary_lat = []
            # string_to_search = 'CORNER_UL_LAT_PRODUCT =.*'
            # self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))
            # string_to_search = 'CORNER_UR_LAT_PRODUCT =.*'
            # self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))
            # string_to_search = 'CORNER_LR_LAT_PRODUCT =.*'
            # self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))
            # string_to_search = 'CORNER_LL_LAT_PRODUCT =.*'
            # self.scene_boundary_lat.append(reg_exp(mtl_text, string_to_search))
            #
            # self.scene_boundary_lon = []
            # string_to_search = 'CORNER_UL_LON_PRODUCT =.*'
            # self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
            # string_to_search = 'CORNER_UR_LON_PRODUCT =.*'
            # self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
            # string_to_search = 'CORNER_LR_LON_PRODUCT =.*'
            # self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
            # string_to_search = 'CORNER_LL_LON_PRODUCT =.*'
            # self.scene_boundary_lon.append(reg_exp(mtl_text, string_to_search))
            # # INFORMATION ON GROUND CONTROL POINTS
            # string_to_search = 'GROUND_CONTROL_POINT_FILE_NAME =.*'
            # self.gcp_filename = reg_exp(mtl_text, string_to_search)
            #
            # # QA INFORMATION
            # string_to_search = 'IMAGE_QUALITY_BAND_1 =.*'
            # iq_band_1 = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'IMAGE_QUALITY_BAND_2 =.*'
            # iq_band_2 = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'IMAGE_QUALITY_BAND_3 =.*'
            # iq_band_3 = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'IMAGE_QUALITY_BAND_4 =.*'
            # iq_band_4 = reg_exp(mtl_text, string_to_search)
            #
            # if (iq_band_1):
            #         self.iq_band_1 = iq_band_1
            # if (iq_band_2):
            #         self.iq_band_2 = iq_band_2
            # if (iq_band_3):
            #        self.iq_band_3 = iq_band_3
            # if (iq_band_4):
            #         self.iq_band_4 = iq_band_4
            #
            # # INFORMATION ON FILE NAMES
            # string_to_search = 'METADATA_FILE_NAME =.*'
            # self.md_filename = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'CPF_NAME =.*'
            # self.cpf_filename = reg_exp(mtl_text, string_to_search)
            #
            # string_to_search = 'CLOUD_COVER =.*'
            # self.cloud_cover = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'CLOUD_COVER_AUTOMATED_L1 =.*'
            # self.cloud_cover_l1 = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'IMAGE_QUALITY =.*'
            # self.image_quality = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'SUN_AZIMUTH =.*'
            # self.sun_azimuth_angle = reg_exp(mtl_text, string_to_search)
            # string_to_search = 'SUN_ELEVATION =.*'
            # self.sun_zenith_angle = 90.0 - np.float(reg_exp(mtl_text, string_to_search))
            # string_to_search = 'UMT_ZONE =.*'
            # self.utm_zone = reg_exp(mtl_text, string_to_search)
            #
            # regex = r.compile('FILE_NAME_BAND_.* =.*')
            # result = (regex.findall(mtl_text))
            # image_file_name = []
            # band_sequence = []
            # for k in result:
            #     image_file_band_name = ((k.split('='))[1].replace(' ', '').replace('"', ''))
            #     image_file_name.append(image_file_band_name)
            #     band_id = str((image_file_band_name.split('.')[0]).split('B')[-1])
            #     if band_id != 'QA':
            #         band_sequence.append(band_id)
            # self.band_sequence = band_sequence
            #
            # regex = r.compile('RADIANCE_MAXIMUM_BAND_.* =.*')
            # result = (regex.findall(mtl_text))
            # radiance_maximum = []
            # for k in result:
            #     v = np.float((k.split('='))[1].replace(' ', ''))
            #     radiance_maximum.append(v)
            # self.radiance_maximum = radiance_maximum
            #
            # regex = r.compile('RADIANCE_MINIMUM_.* =.*')
            # result = (regex.findall(mtl_text))
            # radiance_minimum = []
            # for k in result:
            #     v = np.float((k.split('='))[1].replace(' ', ''))
            #     radiance_minimum.append(v)
            # self.radiance_minimum = radiance_minimum
            #
            # regex = r.compile('RADIANCE_MULT_BAND_.* =.*')
            # result = (regex.findall(mtl_text))
            # rescaling_gain = []
            # for k in result:
            #     v = np.float((k.split('='))[1].replace(' ', ''))
            #     rescaling_gain.append(v)
            # self.rescaling_gain = rescaling_gain
            #
            # regex = r.compile('RADIANCE_ADD_BAND_.* =.*')
            # result = (regex.findall(mtl_text))
            #
            # rescaling_offset = []
            # for k in result:
            #     v = np.float((k.split('='))[1].replace(' ', ''))
            #     rescaling_offset.append(v)
            # self.rescaling_offset = rescaling_offset
            # self.doy = int(self.landsat_scene_id[13:16])
            # self.dE_S = compute_earth_solar_distance(self.doy)
            # self.sun_earth_distance = compute_earth_solar_distance(self.doy)
            # self.solar_irradiance = get_in_band_solar_irrandiance_value(self.mission, self.sensor)
            # self.radiance_to_reflectance_coefficient = self.compute_radiance_to_reflectance_coefficient()
            # #  BQA List
            # [self.bqa, self.bqa_filename] = self.get_qa_band()
            # #  Image list
            # self.dn_image_list = self.set_image_file_name('DN')
            # self.radiance_image_list = self.set_image_file_name('RAD')
            # self.rhotoa_image_list = self.set_image_file_name('RHO')
            # self.surf_image_list = self.set_image_file_name('surf')
            # # Check Image_file_name versus MTL information
            # self.missing_image_in_list = 'FALSE'
            # for ch in image_file_name:
            #     if (os.path.exists(os.path.join(self.product_path, ch)) is False):
            #         self.missing_image_in_list = 'Missing_image'
            #
            # # Additionnal information - post computed - Test site
            # self.test_site = ' '
            # self.interest = ' '

        except IndexError:
            # if not md_list:
            log.err( ' -- Warning - no MTL file found')
            log.err( ' -- Procedure aborted')
            self.mtl_file_name = ''

    def display_mtl_info(self):
        print " "
        print "Product Metadata : \n"
        print " -- Mission : " + self.mission
        print " -- Sensor : " + self.sensor
        print " -- Data Type : " + self.data_type
        print " -- Observation Date : " + self.observation_date
        print " -- Observation Time : " + self.scene_center_time
        print " -- Product Path / Row : " + self.path + ' / ' + self.row
        for k, site_info in enumerate(self.test_site):
            print " -- Test site / Interest : " + site_info + ' / ' + self.interest[k]
        # return ch

        print " "
        print " -- Product_path : " + self.product_path
        print " -- Mtl File : " + self.mtl_file_name
        print " -- Observation Date : " + self.observation_date
        print " -- Day Of Year : " + str(self.doy)
        print ' '
        print " -- Band _id : " + str([v for v in self.band_sequence])
        print " -- Gain : " + str(self.rescaling_gain)
        print " -- Offset : " + str(self.rescaling_offset)
        print " -- Solar Irradiance : " + str(self.solar_irradiance)
        print " -- Radiance to Reflectance factor : " + str(self.radiance_to_reflectance_coefficient)
        print " "
        print " -- Earth Sun Distance  : " + str(self.dE_S)
        print " "
        print " "

    def get_scene_center_coordinates(self):
        lon = np.divide(np.sum(np.double(self.scene_boundary_lon)), 4)
        lat = np.divide(np.sum(np.double(self.scene_boundary_lat)), 4)
        return [lon, lat]

    def get_qa_band(self):
        try:
            bqa_filename = glob.glob(os.path.join(self.product_path, self.landsat_scene_id + '_BQA.TIF'))[0]
            bqa = True
        except IndexError:
            bqa_filename = ' '
            bqa = False
        return bqa, bqa_filename

    def set_image_file_name(self, opt):
        product_path = self.product_path
        image_list = []

        if opt == 'DN':
            print ' -- DN configuration'
            regex1 = os.path.join(product_path, 'L[O,M,T,C][1-8]*[0-9]_B?.TIF')
            regex2 = os.path.join(product_path, 'L[O,M,T,C][1-8]*[0-9]_B?[0-3].TIF')
            regex3 = os.path.join(product_path, 'L[O,M,T,C][1-8]*[0-9]_B?.TIFF')
            regex4 = os.path.join(product_path, 'L[O,M,T,C][0][1-8]*[0-9,T][_,_MTI_]B?.TIF')

            image_list_g = glob.glob(regex1) + glob.glob(regex2) + glob.glob(regex3) + glob.glob(regex4)
            if (len(image_list_g) == 0):
                print product_path
                print "%%%%% [WARNING] - No Level 1 DN image file found "
                print "%%%%% [WARNING] - Check function  [set_image_file_name]"
            array = []
            for rec in image_list_g:
                filename = os.path.basename(rec)

                if (((filename.split('_')[1]).split('.')[0]).replace('B', '')) == 'L1TP':
                    # LT05_L1TP_198030_20111011_20161005_01_T1_B1.TIF
                    # LC08_L1TP_199030_20170527_20170527_01_RT_B1.TIF
                    print 'usgs collection product'
                    band_id = int(((filename.split('B')[1]).split('.')[0]).replace('B', ''))
                    rad = (filename.split('_B')[0])
                else:
                    # LM51990301985107ESA00_B1.TIF
                    band_id = int(((filename.split('_')[1]).split('.')[0]).replace('B', ''))
                    rad = filename.split('_')[0]

                print 'Radical ', rad
                array.append([band_id, rec])

            array_sort = sorted(array, key=lambda x: x[0])
            for rec in array_sort:
                image_list.append(rec[1])

        if opt == 'RAD':
            dn_image = self.dn_image_list
            print ' -- RADIANCE configuration'
            image_list = []
            for rec in dn_image:
                filename = os.path.basename(rec)
                if (((filename.split('_')[1]).split('.')[0]).replace('B', '')) == 'L1TP':
                    # LT05_L1TP_198030_20111011_20161005_01_T1_B1.TIF
                    print 'usgs collection product'
                    band_id = int(((filename.split('B')[1]).split('.')[0]).replace('B', ''))
                    rad = (filename.split('_B')[0])
                else:
                    # LM51990301985107ESA00_B1.TIF
                    band_id = int(((filename.split('_')[1]).split('.')[0]).replace('B', ''))
                    rad = filename.split('_')[0]

                print os.path.join(product_path, ''.join([rad, '_RAD_', str(band_id)]))
                image_list.append(os.path.join(product_path, ''.join([rad, '_RAD_B', str(band_id), '.TIF'])))

        if opt == 'RHO':
            print ' -- TOA REFLECTANCE configuration'
            dn_image = self.dn_image_list
            regex = os.path.join(product_path, 'L[O,M,T,C][0][1-8]*RHO*.TIF')  # RHO TOA Products
            image_list = glob.glob(regex)
            if (len(image_list) == 0):
                print "%%%%% [WARNING] - No R TOA file found "
            else:
                print "%%%%% RHO TOA Reflectance files found : set "

            image_list = []

            for rec in dn_image:
                filename = os.path.basename(rec)
                product_path = os.path.dirname(rec)
                if (((filename.split('_')[1]).split('.')[0]).replace('B', '')) == 'L1TP':
                    # LT05_L1TP_198030_20111011_20161005_01_T1_B1.TIF
                    print 'usgs collection product'
                    band_id = int(((filename.split('B')[1]).split('.')[0]).replace('B', ''))
                    rad = (filename.split('_B')[0])
                else:
                    # LM51990301985107ESA00_B1.TIF
                    band_id = int(((filename.split('_')[1]).split('.')[0]).replace('B', ''))
                    rad = filename.split('_')[0]

                image_list.append(os.path.join(self.product_path, ''.join([rad, '_RHO_B', str(band_id), '.TIF'])))

        if opt == 'surf':
            # Assume no additional transformation needed
            print ' -- SURFACE REFLECTANCE configuration'
            regex = os.path.join(product_path, 'L[O,M,T,C][0][1-8]*_sr_band?.tif')  # SR Products
            image_list = glob.glob(regex)
            if (len(image_list) == 0):
                print product_path
                print "%%%%% [WARNING] - No SR file found [set_image_file_name]"
            else:
                print "%%%%% !!!!!!!!! - Surface Reflectance file found, [self.surf_image_list] is set"

        return image_list

    def update_image_file_list(self):
        # Force to re order list - glob glob does not order according to band id
        # Process Radiance List
        radiance_image_list = [rec for rec in glob.glob(os.path.join(self.product_path, '*RAD*'))]
        array = []
        image_list = []
        print 'radiance list'

        for rec in radiance_image_list:
            print rec
            filename = os.path.basename(rec)
            rad = filename.split('_')[0]
            band_id = int(((filename.split('_')[2]).split('.')[0]).replace('B', ''))
            array.append([band_id, rec])
        array_sort = sorted(array, key=lambda x: x[0])
        print ' '
        for rec in array_sort:
            print rec
            image_list.append(rec[1])

        self.radiance_image_list = image_list

        # Process Reflectance List
        rhotoa_image_list = [rec for rec in glob.glob(os.path.join(self.product_path, '*RHO*TIF'))]
        array = []
        image_list = []
        for rec in rhotoa_image_list:
            filename = os.path.basename(rec)
            rad = filename.split('_')[0]
            band_id = int(((filename.split('_')[2]).split('.')[0]).replace('B', ''))
            array.append([band_id, rec])
        array_sort = sorted(array, key=lambda x: x[0])
        for rec in array_sort:
            image_list.append(rec[1])

        self.rhotoa_image_list = image_list

    def display_image_file_info(self):
        for image in self.dn_image_list:
            print image
        print ' '
        for image in self.radiance_image_list:
            print image
        print ' '
        for image in self.rhotoa_image_list:
            print image
        print ' '

    def compute_radiance_to_reflectance_coefficient(self):
        # Out coefficient for each band
        # Calculer uniqument pour les bandes specifie dans and_sequenc
        mission = self.mission
        len_tab = len(self.solar_irradiance)
        radianceToReflectance_coefficient = [0 for i in range(len_tab)]
        dE_S = self.dE_S
        sza = np.float(self.sun_zenith_angle)
        solar_irradiance = self.solar_irradiance
        for k, band_id in enumerate(self.band_sequence):
            if (
                    (self.mission == 'LANDSAT_1') or
                    (self.mission == 'LANDSAT_2') or
                    (self.mission == 'LANDSAT_3')
            ):
                band_num = np.int(band_id) - 4
            else:
                # print str(band_id)
                band_num = np.int(band_id) - 1

            esun = solar_irradiance[band_num]
            quotient = np.multiply(esun, np.cos(np.multiply(sza, np.divide(np.pi, 180))))
            if quotient != 0.00:
                factor = np.divide(
                    np.multiply(np.pi, np.power((dE_S), 2)),
                    quotient
                )
            else:
                factor = 1
                # En sortie du processeur radiance*10 et donc pour convertir en reflectance_data
                # Il faut multiplie par 0.1
            c = 1.0
            radianceToReflectance_coefficient[band_num] = c * factor

        # FORMULE
        # (radiance*pi*dE_S*dE_S)/(esun*cos((sza)*pi/180));

        return radianceToReflectance_coefficient

    def get_info(self):
        # Allow to expert elements of instance for direct insertion into CSV
        scene_id = self.landsat_scene_id
        obs_date = self.observation_date
        sc_time = self.scene_center_time
        doy = str(self.doy)
        sza = str(self.sun_zenith_angle)
        saa = str(self.sun_azimuth_angle)
        gain = ''
        offset = ''
        radiance_min = ''
        radiance_max = ''
        for rec, v in enumerate(self.rescaling_gain):
            gain += str(v) + ' '
            offset += str(self.rescaling_offset[rec]) + ' '
            radiance_min += str(self.radiance_minimum[rec]) + ' '
            radiance_max += str(self.radiance_maximum[rec]) + ' '
        ch = ' '.join([scene_id, obs_date, sc_time, doy,
                       sza, saa, gain, offset, radiance_min, radiance_max])
        return ch

    def get_band_info(self, band_id):
        # Allow to expert elements of instance for direct insertion into CSV
        scene_id = self.landsat_scene_id
        obs_date = self.observation_date
        sc_time = self.scene_center_time
        doy = str(self.doy)
        sza = str(self.sun_zenith_angle)
        saa = str(self.sun_azimuth_angle)
        gain = str(self.rescaling_gain[band_id - 1])
        offset = str(self.rescaling_offset[band_id - 1])
        radiance_min = str(self.radiance_minimum[band_id - 1])
        radiance_max = str(self.radiance_maximum[band_id - 1])
        ch = ' '.join([scene_id, str(band_id), obs_date, sc_time, doy,
                       sza, saa, gain, offset, radiance_min, radiance_max])
        return ch

    def add_roi_name_information(self, roi_name):
        self.test_site = self.test_site[0] + ':' + roi_name
        return self.test_site

    def set_test_site_information(self, desc_site_file):
        # desc site file - list test site file and properties
        # Objectif : Find a test site defined in desc site file for the product
        # by default no site recognize
        # Test site information => Site Name and Possible Assessment
        site_id_o = 'N/A'
        site_label_o = ''
        country_o = ''

        # Access to XML File 'desc_site_file' for each geo coordinates
        # Test if coordinates is within scene footprint
        # Build vector datatabase
        #         delta_lon : UR - UL (difference of longitude)
        #         delta_lat : LL - UL (difference of latitude)
        #
        # Relative position of input points - lat/lon (from desc File )
        #         lambdaLat = lat - UL (latitude)
        #         lambdaLon = lon - UL (longitude)
        #
        # Projection of the point in the databas
        #         beta 1 = lambdaLat / delta_lat
        #         beta 2 = lambdaLon / delta_lon
        #
        # if beta_1 and beta_2 are < 1.0 alors le point (site) appartient au vertex d entree (produit)

        delta_lon = np.double(self.scene_boundary_lon[1]) - np.double(self.scene_boundary_lon[0])
        delta_lat = np.double(self.scene_boundary_lat[0]) - np.double(self.scene_boundary_lat[3])

        xmldoc = minidom.parse(desc_site_file)
        sites = xmldoc.getElementsByTagName('site')  # get all the sites

        self.test_site = []
        self.interest = []

        record_number = -1
        cpt = 0
        for site in sites:
            site_id = site.getElementsByTagName('id')[0].childNodes[0].data
            site_label = site.getElementsByTagName('label')[0].childNodes[0].data
            country = site.getElementsByTagName('country')[0].childNodes[0].data
            latitude_ctr = site.getElementsByTagName('latCenter')[0].childNodes[0].data
            longitude_ctr = site.getElementsByTagName('lonCenter')[0].childNodes[0].data
            lamdaLat = -np.double(latitude_ctr) + np.double(self.scene_boundary_lat[0])
            lamdaLon = -np.double(longitude_ctr) + np.double(self.scene_boundary_lon[0])
            beta_longitude = np.divide(lamdaLon, delta_lon)
            beta_latitude = np.divide(lamdaLat, delta_lat)
            # print site_id
            # print str(beta_latitude)+' '+str(beta_longitude)
            ##Repere oriente avec le upper left d ou condition sur le if
            if ((0 < (beta_latitude) < 1) and (-1 < (beta_longitude) < 0)):
                site_id_o = site_id
                site_label_o = site_label
                country_o = country
                ch = ' '.join([country_o, site_id_o])
                record_number = cpt
                site = xmldoc.getElementsByTagName('site')[record_number]
                stabilityMonitoringFlag = site.getElementsByTagName('stabilityMonitoring')[0].childNodes[0].data
                directLocationFlag = site.getElementsByTagName('directLocation')[0].childNodes[0].data
                interbandRegistrationFlag = site.getElementsByTagName('interbandRegistration')[0].childNodes[0].data
                mtfFlag = site.getElementsByTagName('MTF')[0].childNodes[0].data

                interest_ch = ''
                if stabilityMonitoringFlag == 'Y':
                    interest_ch += ' stabilityMonitoring'
                if directLocationFlag == 'Y':
                    interest_ch += ' directLocation'
                if interbandRegistrationFlag == 'Y':
                    interest_ch += ' interbandRegistration'
                if mtfFlag == 'Y':
                    interest_ch += ' MTF'

                self.test_site.append(ch)
                self.interest.append(interest_ch)

            cpt += 1

    def get_test_site_information(self):
        # if no ROI DEFINED DO NOT CONSIDER test_site

        return self.test_site






#########################################################################
#                                                                       #
#              Functions                                                #
#                                                                       #
#########################################################################


def compute_earth_solar_distance(doy):
    dE_S = 1 - np.multiply(0.016729,
                           np.cos(0.9856 * (doy - 4) * np.divide(np.pi, 180)))
    return dE_S


def get_in_band_solar_irrandiance_value(mission, sensor):
    # In band Solar Irrandiance
    print mission
    print sensor
    if ((mission == 'LANDSAT_5') and (sensor == 'MSS')):
        solarIrradiance = [1848, 1588, 1235, 856.6]
    elif ((mission == 'LANDSAT_4') and (sensor == 'MSS_4' or sensor == 'MSS' )):  # Fraire regexp pour les autres Landsat mss
        solarIrradiance = [1848, 1588, 1235, 856.6]
    elif ((mission == 'LANDSAT_3') and (sensor == 'MSS_3' or sensor == 'MSS')):  # Fraire regexp pour les autres Landsat mss
        solarIrradiance = [1848, 1588, 1235, 856.6]
    elif ((mission == 'LANDSAT_2') and (sensor == 'MSS_2' or sensor == 'MSS')):  # Fraire regexp pour les autres Landsat mss
        solarIrradiance = [1848, 1588, 1235, 856.6]
    elif ((mission == 'LANDSAT_1') and (sensor == 'MSS_1' or sensor == 'MSS')):  # Fraire regexp pour les autres Landsat mss
        solarIrradiance = [1848, 1588, 1235, 856.6]


    elif ((mission == 'LANDSAT_5') and (sensor == 'TM')):
        solarIrradiance = [1983.0, 1796.0, 1536.0, 1031.0, 220.0, 0.0, 83.44];

    elif ((mission == 'LANDSAT_4') and (sensor == 'TM')):
        solarIrradiance = [1983.0, 1796.0, 1536.0, 1031.0, 220.0, 0.0, 83.44];

    elif ((mission == 'LANDSAT_7') and (sensor == 'ETM')):
        solarIrradiance = [1970, 1843, 1555, 1047, 227.1, 0, 80.53]

    elif ((mission == 'LANDSAT_8')
          and ((sensor == 'OLI') or
                   (sensor == 'OLI_TIRS') or
                   (sensor == 'TIRS'))):  # OR TIRS OR OLI_TIRS
        solarIrradiance = [2067, 2067, 1893, 1603, 972.6, 245, 79.72, 0, 399.7, 0, 0];

    elif ((mission == 'SENTINEL_2') and (sensor == 'OLCI')):  # SENTINEL2
        solarIrradiance = [1913.57, 1941.63, 1822.61, 1512.79,
                           1425.56, 1288.32, 1163.19, 1036.39,
                           955.19, 813.04, 367.15, 245.59, 85.25]
    else:
        solarIrradiance = 'SOLAR IRRADIANCE NOT_FOUND'
    return solarIrradiance


def getTimeZeroValue(mission):
    if (mission == 'LANDSAT_5'):  # Fraire regexp pour les autres Landsat mss
        timeZeroValue = 1984.207

    elif (mission == 'LANDSAT_7'):
        timeZeroValue = 1999.3

    elif (mission == 'LANDSAT_8'):
        timeZeroValue = 2015  # m(TBC)

    else:
        timeZeroValue = 'NOT_FOUND'
    return timeZeroValue


def reg_exp(mtl_text, stringToSearch):
    regex = r.compile(stringToSearch)
    result = (regex.findall(mtl_text))
    if result:
        subs = (result[0].split('='))[1].replace('"', '').replace(' ', '')
    else:
        subs = 'not found'
    return subs
