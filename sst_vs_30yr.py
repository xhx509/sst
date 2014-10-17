# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:10:22 2014

@author: Huanxin
"""
"""
It compares model of 30yr and real observed sea surface temperature data. Before you running this program, please 
open and modify control file "ctrl_temsalmod.csv" in same directory. After running, a drawing will be plotted.
If you find problem in drawing of color bar , please modify color bar parameter setting.

"""
import sys
sys.path.append('/home/hxu/epd73/basemap-1.0.7/lib/mpl_toolkits')
from pylab import *
import matplotlib.tri as Tri
from mpl_toolkits.basemap import Basemap
from hx import plot_getsst
import pytz
import datetime as dt
import netCDF4
import sys
import numpy as np
from datetime import timedelta

urlname=open("ctrl_temsalmod.csv", "r").readlines()[0][27:-1]
depth=int(open("ctrl_temsalmod.csv", "r").readlines()[1][22:-1])
TIME=open("ctrl_temsalmod.csv", "r").readlines()[2][31:-1]
utc = pytz.timezone('UTC')
if urlname=="30yr":
    
    stime=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
    timesnum=stime.year-1981
    standardtime=dt.datetime.strptime(str(stime.year)+'-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
    timedeltaprocess=(stime-standardtime).days
    startrecord=26340+35112*(timesnum/4)+8772*(timesnum%4)+1+timedeltaprocess*24     
    url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3?temp,lon,lat,lonc,latc,time,nv,h,siglay,salinity'
else:
    TIME=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S") 
    now=dt.datetime.now()
    if TIME>now:
         diff=(TIME-now).days
    else:
         diff=(now-TIME).days
    if diff>3:
        print "please check your input start time,within 3 days both side form now on"
        sys.exit(0)
    timeperiod=(TIME)-(now-timedelta(days=3))
    startrecord=(timeperiod.seconds)/60/60
    url="http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_FVCOM_OCEAN_MASSBAY_FORECAST.nc?temp,lon,lat,lonc,latc,time,nv,h,siglay,salinity"
    
nc = netCDF4.Dataset(url)
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
latc = nc.variables['latc'][:]
lonc = nc.variables['lonc'][:]
temp=nc.variables['temp']
sali=nc.variables["salinity"]
siglay=nc.variables['siglay']
h = nc.variables['h'][:]
# read connectivity array
nv = nc.variables['nv'][:].T - 1
time_var = nc.variables['time']

# create a triangulation object, specifying the triangle connectivity array
tri = Tri.Triangulation(lon,lat, triangles=nv)
# plot depth using tricontourf
depthtotal=siglay[:,0]*h[0]
layer=np.argmin(abs(depthtotal+depth))
print layer
salinity=[]
temperature=temp[startrecord][layer]
'''
for i in range(len(lon)):
    depthtotal=siglay[:,i]*h[i]
    layer=np.argmin(abs(depthtotal+depth))
    #print i,layer,temp[startrecord,layer,i]
    temperature.append(temp[startrecord,layer,i])
    #salinity.append(sali[startrecord,layer,i])
'''    
#temperature=np.array(temperature)
#salinity=np.array(salinity)

latsize=[min(lat)-1,max(lat)+1]
lonsize=[min(lon)-1,max(lon)+1]
gbox=[lonsize[0],lonsize[1],latsize[0],latsize[1]]
datetime_wanted=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
fig=figure(figsize=(6,8))
ax=fig.add_subplot(211)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
#m.fillcontinents(color='grey')
m.drawmapboundary()
tricontourf(tri,temperature,np.arange(12,32,3))
colorbar(format='%1.0f'+'C')
ax.text(0.95, 0.1,'FVCOM MODEL',fontsize=19, horizontalalignment='right',verticalalignment='bottom',transform=ax.transAxes)
plt.title(' Time:'+str(TIME)[0:-3]) 
ax1=fig.add_subplot(212)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
#m.fillcontinents(color='grey')
m.drawmapboundary()
ask_input=datetime_wanted
plot_getsst(ask_input,utc,gbox)
#colorbar()
ax1.text(0.95, 0.1,'OBSERVED',fontsize=19, horizontalalignment='right',verticalalignment='bottom',transform=ax1.transAxes)
#plt.title(urlname+' real sea surface temp data:'+' Time:'+str(TIME)[0:-9]) 
plt.show()
plt.savefig(urlname+'30yr_sst.png')