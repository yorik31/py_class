#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re as r
import glob
import io
import numpy as np
#from math import cos
#from datetime import datetime, time


class LandsatMTL:
    # Object for methadata extraction

    def __init__(self, product_path):
        self.isValid = True
        print 'Landsat MTL Class    :'
        print 'Product : '+str(product_path)
        self.product_path = product_path
        re = 'L*_MTL.txt'
        md_list = glob.glob(os.path.join(self.product_path, re))
        print md_list
        #check if file is present
        if not md_list:
            print ' Warning - no MTL file found'
            print ' Procedure aborted'
            self.isValid = False
            return

        try :
            mtl_file_name = glob.glob(os.path.join(self.product_path, re))[0]

            self.mtl_file_name = mtl_file_name
			mtl_file = io.open(mtl_file_name, 'rU')
			mtl_text = mtl_file.read()
			mtl_file.close()    
			longueur = len(mtl_text)

			if longueur < 10 :
			  print ' Size of MTL too small'
			  print ' Procedure aborted'
			  self.isValid = False
			  return

			f = mtl_file_name
			self.product_name = os.path.dirname(f).split('/')[-1]  # PRODUCT_NAME
			regex = r.compile('LANDSAT_SCENE_ID =.*')
			res=regex.findall(mtl_text)
			if res :
			self.landsat_scene_id = ((res)[0].split('='))[1].replace('"', '')
			else:
			self.landsat_scene_id = (os.path.basename(mtl_file_name).split('_'))[0]
					
			print 'Landsat _id '+self.landsat_scene_id
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
			
			if data_type == "L1T":
			  string_to_search = 'ELEVATION_SOURCE =.*'
			  self.elevation_source = reg_exp(mtl_text, string_to_search)
			  string_to_search = 'GROUND_CONTROL_POINT_FILE_NAME =.*'
			  self.gcp_filename = reg_exp(mtl_text, string_to_search)
			  string_to_search = 'GROUND_CONTROL_POINTS_MODEL =.*'
			  self.gcp_nb = reg_exp(mtl_text, string_to_search)
			  string_to_search = 'GEOMETRIC_RMSE_MODEL =.*'
			  self.gcp_rms = reg_exp(mtl_text, string_to_search)
			  string_to_search = 'GEOMETRIC_RMSE_MODEL_Y =.*'
			  self.gcp_rms_x = reg_exp(mtl_text, string_to_search)
			  string_to_search = 'GEOMETRIC_RMSE_MODEL_X =.*'
			  self.gcp_rms_y = reg_exp(mtl_text, string_to_search)
			else:
			  self.elevation_source = 'N/A'
			  self.gcp_filename = 'N/A'
			  self.gcp_nb = 'N/A'
			  self.gcp_rms = 'N/A'
			  self.gcp_rms_x = 'N/A'
			  self.gcp_rms_y = 'N/A'
				 
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
					
			string_to_search = 'METADATA_FILE_NAME =.*'
			self.gcp_md_filename = reg_exp(mtl_text, string_to_search)
			string_to_search = 'CPF_NAME =.*'
			self.gcp_cpf_filename = reg_exp(mtl_text, string_to_search)
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
			if band_id != 'QA' :
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
			self.doy = int(self.landsat_scene_id[14:17])
			self.dE_S = compute_earth_solar_distance(self.doy)
			self.sun_earth_distance = compute_earth_solar_distance(self.doy)
			self.solar_irradiance = get_in_band_solar_irrandiance_value(self.mission, self.sensor)

			self.radiance_to_reflectance_coefficient = self.compute_radiance_to_reflectance_coefficient()

			# Image list
			self.dn_image_list = self.set_image_file_name('DN')
			self.radiance_image_list = self.set_image_file_name('RAD')
			self.rhotoa_image_list = self.set_image_file_name('RHO')
			self.surf_image_list = self.set_image_file_name('surf')

			#Check Image_file_name versus MTL information
			self.missing_image_in_list = 'FALSE'
			for ch in image_file_name :
				if (os.path.exists(os.path.join(self.product_path,ch)) is False ):
				  self.missing_image_in_list = 'Missing_image'


			# Additionnal information - post computed - Test site 
			self.test_site = ' '
			self.interest = ' '

		except IndexError:
        #if not md_list:
            print ' -- Warning - no MTL file found'
            print ' -- Procedure aborted'
			self.mtl_file_name = ''		
		
    def get_scene_center_coordinates(self):
        lon = np.divide(np.sum(np.double(self.scene_boundary_lon)),4)
        lat = np.divide(np.sum(np.double(self.scene_boundary_lat)),4)
        return [lon,lat]		
		
		
    def display_mtl_info(self):
        print " "
        print "Product Metadata : \n"
        print " -- Mission : " + self.mission
        print " -- Sensor : " + self.sensor
        print " -- Data Type : " + self.data_type
        print " -- Observation Date : " + self.observation_date
        print " -- Observation Time : " + self.scene_center_time
        print " -- Product Path / Row : " + self.path + ' / ' + self.row
        for k,site_info in enumerate(self.test_site):
           print " -- Test site / Interest : " + site_info + ' / ' + self.interest[k]
         #return ch

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

    def set_image_file_name(self,opt):

        product_path=self.product_path
        image_list=[]
 
        if opt == 'DN' :
            print ' -- DN configuration'
            regex1=os.path.join(product_path,'L[O,M,T,C][1-8]*[0-9]_B?.TIF')
            regex2=os.path.join(product_path,'L[O,M,T,C][1-8]*[0-9]_B?[0-3].TIF')
            image_list_g=glob.glob(regex1)+glob.glob(regex2)
            array=[]
            for rec in image_list_g:
               filename=os.path.basename(rec)
               rad=filename.split('_')[0]
               band_id=int(((filename.split('_')[1]).split('.')[0]).replace('B',''))
               array.append([band_id, rec])

            array_sort=sorted(array,key=lambda x : x[0])
            for rec in array_sort:
               image_list.append(rec[1])
               
        if opt == 'RAD' :
            dn_image = self.dn_image_list
            print ' -- RADIANCE configuration'
            image_list = []
            for rec in dn_image:
                filename=os.path.basename(rec)
                rad=filename.split('_')[0]
                band_id=filename.split('_')[1]
                image_list.append(os.path.join(product_path,''.join([rad,'_RAD_',band_id])))

        if opt == 'RHO' :
            dn_image = self.dn_image_list
            print ' -- REFLECTANCE configuration'
            image_list = []
            for rec in dn_image:
                filename=os.path.basename(rec)
                product_path=os.path.dirname(rec)
                rad=filename.split('_')[0]
                band_id=filename.split('_')[1]
                image_list.append(os.path.join(self.product_path,''.join([rad,'_RHO_',band_id])))
                
        if opt == 'surf' :
            #Assume no additional transformation needed
            print ' -- SURFACE REFLECTANCE configuration'
            image_list=glob.glob(os.path.join(self.product_path,'L[O,C]8*_sr_band*.tif'))

        return image_list

    def update_image_file_list(self):
        
        #Force to re order list - glob glob does not order according to band id
        #Process Radiance List
        radiance_image_list=[ rec for rec in glob.glob(os.path.join(self.product_path,'*RAD*'))]
        array=[]
        image_list=[]
        for rec in radiance_image_list:
           filename=os.path.basename(rec)
           rad=filename.split('_')[0]
           band_id=int(((filename.split('_')[2]).split('.')[0]).replace('B',''))
           array.append([band_id, rec])
        array_sort=sorted(array,key=lambda x : x[0])
        for rec in array_sort:
           image_list.append(rec[1])

        self.radiance_image_list=image_list

        #Process Reflectance List
        rhotoa_image_list=[ rec for rec in glob.glob(os.path.join(self.product_path,'*RHO*'))]
        array=[]
        image_list=[]
        for rec in rhotoa_image_list:
           filename=os.path.basename(rec)
           rad=filename.split('_')[0]
           band_id=int(((filename.split('_')[2]).split('.')[0]).replace('B',''))
           array.append([band_id, rec])
        array_sort=sorted(array,key=lambda x : x[0])
        for rec in array_sort:
              image_list.append(rec[1])

        self.rhotoa_image_list=image_list		
		
    def display_image_file_info(self):

        for image in self.input_image_list:
            print image
        print ' '
        for image in self.radiance_image_list:
            print image
        print ' '
        for image in self.rho_toa_image_list:
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
                print str(band_id)
                band_num = np.int(band_id) - 1

            esun = solar_irradiance[band_num]
            quotient = np.multiply(esun,np.cos(np.multiply(sza , np.divide(np.pi, 180))))
            if quotient != 0.00:
               factor = np.divide(
                   np.multiply(np.pi , np.power((dE_S), 2)),
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
        #Allow to expert elements of instance for direct insertion into CSV
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
        for rec,v in enumerate(self.rescaling_gain):
            gain += str(v)+' '
            offset += str(self.rescaling_offset[rec])+' '
            radiance_min += str(self.radiance_minimum[rec])+' '
            radiance_max += str(self.radiance_maximum[rec])+' '
        ch = ' '.join([scene_id, obs_date, sc_time, doy,
                      sza, saa, gain, offset, radiance_min, radiance_max])
        return ch
		
    def get_band_info(self,band_id):
        #Allow to expert elements of instance for direct insertion into CSV
        scene_id = self.landsat_scene_id
        obs_date = self.observation_date
        sc_time = self.scene_center_time
        doy = str(self.doy)
        sza = str(self.sun_zenith_angle)
        saa = str(self.sun_azimuth_angle)        
        gain = str(self.rescaling_gain[band_id - 1])
        offset = str(self.rescaling_offset[band_id - 1])
        radiance_min =str(self.radiance_minimum[band_id - 1])
        radiance_max = str(self.radiance_maximum[band_id - 1])
        ch = ' '.join([scene_id, str(band_id),obs_date, sc_time, doy,
                      sza, saa, gain, offset, radiance_min, radiance_max])
        return ch
		
	def add_roi_name_information(self, roi_name): 
       
       self.test_site = self.test_site[0]+':'+roi_name 
       return self.test_site

    def set_test_site_information(self, desc_site_file):      
         
         #desc site file - list test site file and properties
         #Objectif : Find a test site defined in desc site file for the product
         #by default no site recognize
         #Test site information => Site Name and Possible Assessment
         site_id_o='N/A'
         site_label_o=''
         country_o=''

         #Access to XML File 'desc_site_file' for each geo coordinates 
         #Test if coordinates is within scene footprint
         #Build vector datatabase 
         #         delta_lon : UR - UL (difference of longitude)
         #         delta_lat : LL - UL (difference of latitude)
         #
         #Relative position of input points - lat/lon (from desc File )
         #         lambdaLat = lat - UL (latitude)
         #         lambdaLon = lon - UL (longitude)
         #
         #Projection of the point in the databas
         #         beta 1 = lambdaLat / delta_lat
         #         beta 2 = lambdaLon / delta_lon
         #
         # if beta_1 and beta_2 are < 1.0 alors le point (site) appartient au vertex d entree (produit)
       

         delta_lon=np.double(self.scene_boundary_lon[1]) - np.double(self.scene_boundary_lon[0]) 
         delta_lat=np.double(self.scene_boundary_lat[0]) - np.double(self.scene_boundary_lat[3])


	 xmldoc = minidom.parse(desc_site_file)
         sites=xmldoc.getElementsByTagName('site') #get all the sites
                   
         self.test_site=[]
         self.interest=[]

         record_number=-1
         cpt=0 
         for site in sites:
            site_id=site.getElementsByTagName('id')[0].childNodes[0].data
            site_label=site.getElementsByTagName('label')[0].childNodes[0].data
            country=site.getElementsByTagName('country')[0].childNodes[0].data
            latitude_ctr=site.getElementsByTagName('latCenter')[0].childNodes[0].data
            longitude_ctr=site.getElementsByTagName('lonCenter')[0].childNodes[0].data
            lamdaLat=-np.double(latitude_ctr)+np.double(self.scene_boundary_lat[0])
            lamdaLon=-np.double(longitude_ctr)+np.double(self.scene_boundary_lon[0])
            beta_longitude=np.divide(lamdaLon,delta_lon)
            beta_latitude=np.divide(lamdaLat,delta_lat)
            #print site_id
            #print str(beta_latitude)+' '+str(beta_longitude)
            ##Repere oriente avec le upper left d ou condition sur le if
            if ((0 < (beta_latitude) < 1) and ( -1 < (beta_longitude) < 0)):
               site_id_o=site_id
               site_label_o=site_label
               country_o=country
               ch = ' '.join([country_o,site_id_o])
               record_number = cpt
               site=xmldoc.getElementsByTagName('site')[record_number]
               stabilityMonitoringFlag=site.getElementsByTagName('stabilityMonitoring')[0].childNodes[0].data
               directLocationFlag=site.getElementsByTagName('directLocation')[0].childNodes[0].data
               interbandRegistrationFlag=site.getElementsByTagName('interbandRegistration')[0].childNodes[0].data
               mtfFlag=site.getElementsByTagName('MTF')[0].childNodes[0].data
               
               interest_ch=''
               if stabilityMonitoringFlag == 'Y' :
                  interest_ch += ' stabilityMonitoring'
               if directLocationFlag == 'Y' :
                  interest_ch += ' directLocation'
               if interbandRegistrationFlag == 'Y' :
                  interest_ch += ' interbandRegistration'
               if mtfFlag == 'Y' :
                  interest_ch += ' MTF'
               
               self.test_site.append(ch)
               self.interest.append(interest_ch)     
              
            cpt += 1
         

    def get_test_site_information(self):
         # if no ROI DEFINED DO NOT CONSIDER test_site
         return self.test_site     
	   
	   
	def compute_earth_solar_distance(doy):

		dE_S = 1-np.multiply(0.016729,
                       np.cos(0.9856*(doy-4)*np.divide(np.pi,180)))
		return dE_S

		
		
		
		
	def get_in_band_solar_irrandiance_value(mission,sensor):

		#In band Solar Irrandiance
		if mission == 'LANDSAT_5' and sensor == 'MSS':
			solarIrradiance = [1848, 1588, 1235, 856.6]
		elif ((mission=='LANDSAT_4') and (sensor == 'MSS_4')): #Fraire regexp pour les autres Landsat mss
			solarIrradiance = [1848, 1588, 1235, 856.6]
		elif ((mission=='LANDSAT_3') and (sensor == 'MSS_3')): #Fraire regexp pour les autres Landsat mss
			solarIrradiance = [1848, 1588, 1235, 856.6]
		elif ((mission=='LANDSAT_2') and (sensor == 'MSS_2')): #Fraire regexp pour les autres Landsat mss
			solarIrradiance = [1848, 1588, 1235, 856.6]
		elif ((mission=='LANDSAT_1') and (sensor == 'MSS_1')): #Fraire regexp pour les autres Landsat mss
			solarIrradiance = [1848, 1588, 1235, 856.6]


		elif ((mission == 'LANDSAT_5') and (sensor == 'TM')):
			solarIrradiance = [1983.0, 1796.0, 1536.0, 1031.0, 220.0, 0.0, 83.44];

		elif ((mission == 'LANDSAT_7') and (sensor == 'ETM')):
			solarIrradiance = [1970,1843,1555,1047,227.1,0,80.53]

		elif ((mission == 'LANDSAT_8')
				and ((sensor == 'OLI') or
					(sensor == 'OLI_TIRS') or
					(sensor == 'TIRS'))): #OR TIRS OR OLI_TIRS
			solarIrradiance = [2067,2067,1893,1603,972.6,245,79.72,0,399.7,0,0];

		elif ((mission == 'SENTINEL_2') and (sensor == 'OLCI')): #SENTINEL2
			solarIrradiance = [1913.57,1941.63,1822.61,1512.79,
							   1425.56,1288.32,1163.19,1036.39,
							   955.19,813.04,367.15,245.59,85.25]
		else:
			solarIrradiance = 'NOT_FOUND'
		return solarIrradiance

	def getTimeZeroValue(mission):

		if (mission=='LANDSAT_5'): #Fraire regexp pour les autres Landsat mss
			timeZeroValue=1984.207

		elif (mission == 'LANDSAT_7'):
			 timeZeroValue=1999.3

		elif (mission == 'LANDSAT_8'):
			 timeZeroValue=2015 #m(TBC)

		else:
			timeZeroValue='NOT_FOUND'
		return timeZeroValue

def reg_exp(mtl_text, stringToSearch):
    regex = r.compile(stringToSearch)
    result = (regex.findall(mtl_text))
    if result:
        subs = (result[0].split('='))[1].replace('"', '').replace(' ', '')
    else:
        subs = 'not found'
    return subs
