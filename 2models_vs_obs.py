# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 15:04:31 2014

@author: hxu
"""


"""
It compares models of 30yr and roms and real observed sea surface temperature data. Before you running this program, please 
open and modify control file "ctrl_temsalmod.csv" in same directory. After running, a drawing will be plotted.
If you find problem in drawing of color bar , please modify color bar parameter setting.

"""
pydir='/hxu/anaconda/lib/python2.7/site-packages'
import sys
sys.path.append('/home/hxu/epd73/basemap-1.0.7/lib/mpl_toolkits')
sys.path.append(pydir)
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
def get_roms_id(url,datetime_wanted): #accroding time you input,get a index of time
    
        database= netCDF4.Dataset(url+'?ocean_time')
        time=database.variables['ocean_time'] 

        ddd=[]
        for i in time[0:].tolist():

            i=round(i,7)
            ddd.append(i)
        f = lambda a,l:min(l,key=lambda x:abs(x-a)) #match datetime_wanted
        datetime_wanted=f(datetime_wanted, ddd)
        id=[i for i,x in enumerate(ddd) if x == datetime_wanted]       

        for i in id:
          id=str(i) 
        return id
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


latsize=[min(lat)-1,max(lat)+1]
lonsize=[min(lon)-1,max(lon)+1]
gbox=[lonsize[0],lonsize[1],latsize[0],latsize[1]]
datetime_wanted=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
fig=figure(figsize=(6,8))
ax=fig.add_subplot(311)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
m.drawmapboundary()
tricontourf(tri,temperature,np.arange(6,26,3))
#colorbar(format='%1.0f'+'C')
ax.text(0.95, 0.1,'FVCOM',fontsize=17, horizontalalignment='right',verticalalignment='bottom',transform=ax.transAxes)
plt.title(' SST'+str(TIME)[0:-3]) 
layer=35
def getroms(TIME,layer):
  datetime_wanted=dt.datetime.strptime(TIME, "%Y-%m-%d %H:%M:%S")
  T=(date2num(datetime_wanted)-732312)*86400
  url='http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2009_da/his?'
  id= get_roms_id(url,T)
  #url1='http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2009_da/his?lon_rho,lat_rho,temp'
  database=netCDF4.Dataset(url)
  lat=database.variables['lat_rho'][:]
  lon=database.variables['lon_rho'][:]
  temp=database.variables['temp'][int(id):(int(id)+1)]
  temp=temp[0][layer]
  return lat,lon,temp
lat_r,lon_r,temp=getroms(TIME,layer)  
ax1=fig.add_subplot(312)
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
m.drawmapboundary()
CS = plt.contourf(lon_r,lat_r,temp,np.arange(6,26,3.0))
plt.colorbar(CS,format='%1.0f'+'C')
#tricontourf(tri,temperature,np.arange(12,32,3))
#colorbar(format='%1.0f'+'C')
ax1.text(0.95, 0.1,'ROM',fontsize=17, horizontalalignment='right',verticalalignment='bottom',transform=ax1.transAxes)
ax2=fig.add_subplot(313)
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
ax2.text(0.95, 0.1,'OBSERVED',fontsize=17, horizontalalignment='right',verticalalignment='bottom',transform=ax2.transAxes)
#plt.title(urlname+' real sea surface temp data:'+' Time:'+str(TIME)[0:-9]) 
plt.show()
plt.savefig('sst'+TIME[0:-4]+'.png')