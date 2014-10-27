sst
===

Sea surface temperature 

This program gets observed  and  model sea surface data. After running this program, a contour plot will be generated at
the end.
Remember to modify the hard code before you running a process.

Some functions are saved in 'sst_function.py'


Reference:  http://tds.maracoos.org/thredds/SST.html .

List of programs:


2models_vs_obs.py         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        compare models of FVCOM , roms and real observed sea surface temperature data

get_drifter_erddap_sst.py    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     plot sst and erddap drifter data in one picture

getsst_drifter_raw.py plot   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     plot sst and raw drifter data in one picture

getsst.py             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            plot sst data

roms_model.py          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;           original roms' plotting, could plot layers' data

roms_sur.py              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         plot surface data of roms

sst_vs_30yr.py              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      plot both sst data and model FVCOM data 


There are flowcharts in this peckage to explain programs :

<a href="https://github.com/xhx509/sst/blob/master/getsst_flowchart.png">getsst</a>

<a href="https://github.com/xhx509/sst/blob/master/get_drifter_erddap_sst_flowchart.png">get_drifter_erddap_sst</a>

<a href="https://github.com/xhx509/sst/blob/master/sst_30yr_flowchart.png">sst_vs_30yr</a>
