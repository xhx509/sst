# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 14:11:23 2014

@author: hxu
"""
'''
this project only get roms data and plot them with basemap

'''

#get data from opendap
#deal with and plot
pydir='/hxu/anaconda/lib/python2.7/site-packages'
import sys
sys.path.append('/home/hxu/epd73/basemap-1.0.7/lib/mpl_toolkits')
sys.path.append(pydir)
from pylab import *
from mpl_toolkits.basemap import Basemap
import datetime as dt
import netCDF4
import numpy as np
from matplotlib.dates import date2num
def get_roms_id(url,datetime_wanted): #accroding time you input,get a index of that
    
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
urlname=open("ctrl_temsalmod.csv", "r").readlines()[0][27:-1]
depth=int(open("ctrl_temsalmod.csv", "r").readlines()[1][22:-1])
TIME=open("ctrl_temsalmod.csv", "r").readlines()[2][31:-1]
layer=36
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
lat,lon,temp=getroms(TIME,layer)  
fig=figure(figsize=(6,8))
ax=fig.add_subplot(111)
latsize=[np.min(lat),np.max(lat)]
lonsize=[np.min(lon),np.max(lon)]
m = Basemap(projection='cyl',llcrnrlat=min(latsize)-0.01,urcrnrlat=max(latsize)+0.01,\
            llcrnrlon=min(lonsize)-0.01,urcrnrlon=max(lonsize)+0.01,resolution='h')#,fix_aspect=False)
m.drawparallels(np.arange(int(min(latsize)),int(max(latsize))+1,3),labels=[1,0,0,0])
m.drawmeridians(np.arange(int(min(lonsize)),int(max(lonsize))+1,3),labels=[0,0,0,1])
m.drawcoastlines()
m.drawmapboundary()
CS = plt.contourf(lon,lat,temp,np.arange(6,26,3.0))
plt.colorbar(CS,format='%1.0f'+'C')
#tricontourf(tri,temperature,np.arange(12,32,3))
#colorbar(format='%1.0f'+'C')
ax.text(0.95, 0.1,'roms_surface',fontsize=19, horizontalalignment='right',verticalalignment='bottom',transform=ax.transAxes)
plt.title('roms_Time:'+str(TIME)[0:-3]) 
plt.show()
plt.savefig(urlname+'roms.png')