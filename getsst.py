# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 10:33:04 2014

@author: hxu
"""
####################################################################
#from control file to get latmax,latmin,lonmax,lonmin,time,number, interval,arrow_percent
#this program use for plotting  sea surface temperature 
#it gets input value from './getcodar_byrange_ctl.txt',
#according to datetime and area range, we get data
#It doesn't work sometimes ,then you should check and modify url in function "getsst" in 'hx.py'
#Input values:datetime_wanted,filename
#output values:gbox,sst_data
#function uses:getcodar_ctl_file_edge,getcodar_ctl_lalo,getcodar_ctl_id,getcodar_edge, plot_getsst
####################################################################
from pylab import *
import pylab
import sys
import datetime as dt
import matplotlib.pyplot as plt
sys.path.append("/usr/local/lib/python2.7/dist-packages/Pydap-3.0.1-py2.7.egg")
from hx import  plot_getsst
import pytz
sys.path.append('/net/home3/ocn/jmanning/py/mygit/modules/')
from basemap import basemap_standard
from mpl_toolkits.basemap import Basemap
import numpy as np

utc = pytz.timezone('UTC')
png_num=0 # for saving picture  
#datetime_wanted,url,model_option,lat_max,lon_max,lat_min,lon_min,num,interval_dtime,arrow_percent=getcodar_ctl_file_edge(inputfilename)  #get data from ctl file
#gbox=[lon_min, lon_max, lat_min, lat_max]# , get edge box for sst
datetime_wanted=dt.datetime(2010,9,2,0,0,0,0,pytz.UTC)
gbox=[-76.0,-60.0,35.0,47.0]  #lon_min, lon_max, lat_min, lat_max
     

    #basemap_standard(lon_vel[idg[0]],lat_vel[idg[0]],0.5)
    #bm.basemap_usgs([min(np.reshape(lon_vel,np.size(lon_vel))[idg],max(np.reshape(lon_vel,np.size(lon_vel))[idg]))],[min(np.reshape(lat_vel,np.size(lat_vel))[idg],max(np.reshape(lat_vel,np.size(lat_vel))[idg]))],True)
latsize=[gbox[2]-1,gbox[3]+1]
lonsize=[gbox[0]-1,gbox[1]+1]
fig=figure(figsize=(6,8))
ax=fig.add_subplot(211)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
#m.fillcontinents(color='grey')
m.drawmapboundary()
ask_input=datetime_wanted
plot_getsst(ask_input,utc,gbox)
#pylab.ylim([gbox[2]+0.01,gbox[3]-0.01])
#pylab.xlim([gbox[0]+0.01,gbox[1]-0.01])
bathy=True
#region='wv'
#basemap_standard(region)
#basemap_standard([40.1,42.1],[-72.1,-70.1],[0.1])
plt.title(str(datetime_wanted.strftime("%d-%b-%Y %H"))+'h')
    #plt.savefig('/net/home3/ocn/jmanning/py/huanxin/work/hx/'+str(datetime_wanted)+ '.png')
#plt.savefig(str('%03d' % png_num) + '.png')
plt.savefig(str(datetime_wanted.strftime("%d-%b-%Y %H"))+'.png')
#datetime_wanted=date2num(num2date(datetime_wanted)+interval_dtime) # add interval_dtime for another forloop
plt.show()
    #plt.close()