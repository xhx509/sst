# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 09:02:18 2014

@author: hxu

it plots surface sea temp and drifter data in one picture, the time of temp showed in picture is starting time.
modify code of input value below before using it.


"""

import datetime as dt
import sys
import os
import pytz, pylab
import numpy as np
import matplotlib.pyplot as plt
from hx import getobs_drift_byrange,getobs_drift_byidrange,colors,getobs_drift_byid,plot_getsst
ops=os.defpath
pydir='../'
sys.path.append(pydir)
sys.path.append('/net/home3/ocn/jmanning/py/mygit/modules/')
from basemap import basemap_region
utc = pytz.timezone('UTC')
#################Input values#############################################
input_time=[dt.datetime(2012,1,30,0,0,0,0,pytz.UTC),dt.datetime(2012,9,1,0,0,0,0,pytz.UTC)] # start time and end time
gbox=[-68.0,-72.0,45.0,38.0] #  maxlon, minlon,maxlat,minlat
id=[] # id list, if you are not clear dedicated id, let id=[]
#'125450842''125450841'
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#

#fig = plt.figure()
#ax = fig.add_subplot(111)  
ask_input=input_time[0]
plot_getsst(ask_input,utc,sorted(gbox))    # get sst data and polt it

if id==[]:
    
    time,ids,lats,lons=getobs_drift_byrange(gbox,input_time)
    id=list(set(ids))
    rgbcolors=colors(len(id))   # set different colors to different drifter
    for k in range(len(id)):
        time,ids,lat_d,lon_d=getobs_drift_byidrange(id[k],gbox,input_time)   #get drifters' data
        plt.plot(lon_d[0],lat_d[0],'.',markersize=30,color=rgbcolors[k+1],label=str(id[k]))
        plt.plot(np.reshape(lon_d,np.size(lon_d)),np.reshape(lat_d,np.size(lat_d)),color=rgbcolors[k+1]) #plot
else:
    lats,lons=[],[]
    rgbcolors=colors(len(id))  # set different colors to different drifter
    for m in range(len(id)):
        time,ids,lat_d,lon_d=getobs_drift_byid(id[m],input_time)  #get drifters' data by id
        plt.plot(lon_d[0],lat_d[0],'.',markersize=30,color=rgbcolors[m+1],label=str(id[m]))
        plt.plot(np.reshape(lon_d,np.size(lon_d)),np.reshape(lat_d,np.size(lat_d)),color=rgbcolors[m+1])
        for n in range(len(lat_d)):  
            lats.append(lat_d[n])
            lons.append(lon_d[n])
    
plt.title(str(time[0].strftime("%d-%b-%Y %H"))+'h') 
pylab.ylim([sorted(gbox)[2]+0.01,sorted(gbox)[3]-0.01])  # set range area .
pylab.xlim([sorted(gbox)[0]+0.01,sorted(gbox)[1]-0.01])    
#pylab.ylim([min(lats)-(max(lats)-min(lats))/6.0,max(lats)+(max(lats)-min(lats))/6.0])
#pylab.xlim([min(lons)-(max(lons)-min(lons))/6.0,max(lons)+(max(lons)-min(lons))/6.0])

#ax.patch.set_facecolor('lightblue')   #set background color
bathy=True
region='wv' # set basemap 
basemap_region(region)
plt.legend( numpoints=1,loc=2)  
plt.savefig('./'+str(time[0].strftime("%d-%b-%Y %H"))+'h' + '.png')
 
#datetime_wanted=date2num(num2date(datetime_wanted)+datetime.timedelta( 0,step_size*60*60 ))
plt.show()
