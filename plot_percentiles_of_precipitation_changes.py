## IMPORTING:
import os
print("1")
from netCDF4 import Dataset as NetCDFFile
print("2")
import matplotlib.pyplot as plt
print(3)
import numpy as np
print(4)
##os.system("pip install -q condacolab")
#import condacolab
#condacolab.install()
#os.system("mamba install -q -c conda-forge cartopy")
import cartopy.crs as ccrs
print(5)
import cartopy.feature
print("6")
import pickle
import matplotlib as mpl
print("reading")
# functions :
########################################
#
#           READ NETCDF FILES
#
########################################

#RCM:
def read_nc(nc_file, var):
    nc = NetCDFFile(nc_file)
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]
    rlat = nc.variables['rlat'][:]
    rlon = nc.variables['rlon'][:]
    pr   = nc.variables[var][:]
    nc.close()
    return  rlat, rlon, pr

def plot_maps(name, val,cmap, minn, maxx, nn, rlat,rlon):
    '''
    minn : colorbar min value
    maxx : colorbar max value
    '''
    pol_lon=-105.36
    pol_lat=42.18

    fig = plt.figure('1')
    fig.set_size_inches(14, 10)
    pc = ccrs.PlateCarree()
    rp = ccrs.RotatedPole(pole_longitude= pol_lon,
                          pole_latitude= pol_lat,
                          globe=ccrs.Globe(semimajor_axis=6370000,
                                           semiminor_axis=6370000))
    ax = plt.axes(projection=rp)

    ax.coastlines('50m', linewidth=0.8)
    ax.add_feature(cartopy.feature.BORDERS)
    ax.add_feature(cartopy.feature.OCEAN,
                   edgecolor='black', zorder=0,
                   linewidth=0.8, alpha=.7)
    ax.add_feature(cartopy.feature.BORDERS,
                   edgecolor='black', zorder=0,
                   linewidth=0.8, alpha=.7)
    ax.add_feature(cartopy.feature.LAND, zorder=0,
                   linewidth=0.8, alpha=.7)

#    v = np.linspace(np.nanmin(added_value),np.nanmax(added_value) , 21, endpoint=True)
    v =  np.linspace(minn,maxx , nn, endpoint=True)
    #cmap = plt.cm.  # define the colormap
    cmap = cmap
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
#    # force the first color entry to be grey
#    cmaplist[0] = (.5, .5, .5, 1.0)

    # create the new map
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, cmap.N)

    norm = mpl.colors.BoundaryNorm(v, cmap.N)
    rlons, rlats = np.meshgrid(rlon, rlat)
    cs = plt.pcolor(rlons, rlats, val.squeeze(), cmap=cmap, zorder=1,norm=norm,linewidth=0,rasterized=True,shading="auto")
    ax.gridlines( draw_labels=True,linewidth=1, color='black', alpha=0.5, linestyle='--')
    #cs = plt.contourf(lons, lats, t, v, transform=ccrs.PlateCarree(), cmap=plt.cm.BuGn)
    cax = fig.add_axes([ax.get_position().x1+0.05,ax.get_position().y0,0.02,ax.get_position().height])
    cb = plt.colorbar(cs, cax=cax)
    #ax.gridlines( draw_labels=True,dms=True,linewidth=2, color='black', alpha=0.5, linestyle='--')
    #cb.set_label('total precip [mm/day]', fontsize=20)
    cb.ax.tick_params(labelsize=20)
    os.system('mkdir -p plots')
    #name = "./plots/added_value.pdf"
    #plt.savefig(name,bbox_inches='tight')
    plt.savefig(name, format='png', bbox_inches='tight')
    plt.close()




# read the percentiles & scenarios: 
dir_2_file = "/p/tmp/fallah/"

#for scen, scenname in [("sp010","ssp585"), ("sp016","ssp126"), ("sp012","ssp370")]:
#    for pctl in [99]: 
#        print("scenario is "+scenname)
#        print("pctl is     "+str(pctl))
#        print("---------------------------")  
#        rlat, rlon, data = read_nc(dir_2_file+scen+"_out03/TOT_PREC_changes_yearlymax_"+scen+"_"+str(pctl)+".nc", "TOT_PREC")
#        if pctl == 50:
#            plot_maps("./plots/pr_change_"+scenname+"_"+str(pctl)+".eps",data,plt.cm.PuOr,-5,5,11, rlat,rlon)
#        elif pctl == 100:
#            plot_maps("./plots/pr_change_"+scenname+"_"+str(pctl)+".eps",data,plt.cm.PuOr,-20,20,11,rlat,rlon)
#        else:
#            plot_maps("./plots/pr_change_"+scenname+"_"+str(pctl)+".eps",data,plt.cm.PuOr,-10,10,21,rlat,rlon)  

# ploting the results from intake stuff for the whole CMIP6 models: 

#intake_dir="/p/tmp/fallah/intake/remaped/"


#rlat, rlon, data = read_nc(intake_dir+"ssp585/ssp585_ensmean.nc", "pr")
#plot_maps("./plots/pr_change_ssp585_cmip6.eps",data,plt.cm.PuOr,-10,10,21,rlat,rlon)
#rlat, rlon, data = read_nc(intake_dir+"ssp370/ssp370_ensmean.nc", "pr")
#plot_maps("./plots/pr_change_ssp370_cmip6.eps",data,plt.cm.PuOr,-10,10,21,rlat,rlon)
#rlat, rlon, data = read_nc(intake_dir+"ssp126/ssp126_ensmean.nc", "pr")
#plot_maps("./plots/pr_change_ssp126_cmip6.eps",data,plt.cm.PuOr,-10,10,21,rlat,rlon)



#rlat, rlon, data = read_nc(intake_dir+"ssp585/ssp585_ensstd.nc", "pr")
#plot_maps("./plots/pr_change_ssp585_cmip6_ensstd.eps",data,plt.cm.binary,0,10,21,rlat,rlon)

#rlat, rlon, data = read_nc(intake_dir+"ssp370/ssp370_ensstd.nc", "pr")
#plot_maps("./plots/pr_change_ssp370_cmip6_ensstd.eps",data,plt.cm.binary,0,10,21,rlat,rlon)

#rlat, rlon, data = read_nc(intake_dir+"ssp126/ssp126_ensstd.nc", "pr")
#plot_maps("./plots/pr_change_ssp126_cmip6_ensstd.eps",data,plt.cm.binary,0,10,21,rlat,rlon)

print("test")

#dir="/home/fallah/scripts/added_value/bash/"
#############################import cmasher as cmr
#rlat, rlon, data = read_nc(dir+"diff_RMSE.nc", "tp")
#data[data<-3000] = np.nan
#cmaps = plt.cm.PiYG 
#plot_maps("./plots/RMSE_diffs_annuanl.png",data,cmaps,-5,5,11,rlat,rlon)#

##data[data<-3000] = np.nan
#rlat, rlon, data = read_nc(dir+"diff_RMSE_DJF.nc", "tp")
#data[data<-3000] = np.nan
#plot_maps("./plots/RMSE_diffs_DJF.png",data,cmaps,-5,5,21,rlat,rlon)

#rlat, rlon, data = read_nc(dir+"diff_RMSE_JJA.nc", "tp")
#data[data<-3000] = np.nan
#plot_maps("./plots/RMSE_diffs_JJA.png",data,cmaps,-5,5,21,rlat,rlon)


####################################################


#rlat, rlon, data = read_nc(dir+"RMSE_ERAInterim.nc", "tp")
#data[data<-3000] = np.nan
#cmaps = plt.cm.Reds
#plot_maps("./plots/RMSE_ERAInterim_annuanl.png",data,cmaps,0,20,11,rlat,rlon)

#rlat, rlon, data = read_nc(dir+"RMSE_ERAInterim_JJA.nc", "tp")
#data[data<-3000] = np.nan
#cmaps = plt.cm.Reds
#plot_maps("./plots/RMSE_ERAInterim_JJA.png",data,cmaps,0,20,11,rlat,rlon)#


#rlat, rlon, data = read_nc(dir+"RMSE_ERAInterim_DJF.nc", "tp")
#data[data<-3000] = np.nan
#cmaps = plt.cm.Reds
#plot_maps("./plots/RMSE_ERAInterim_DJF.png",data,cmaps,0,20,11,rlat,rlon)


#######################################################################

# plot the changes in number of  days with pr > 20mm prx20mm 
#for sp in ["sp016", "sp012", "sp010"]:

    

##sp="sp010" #ssp585
##sp="sp012" #ssp370
###sp="sp009" # historical
###sp="sp016" # ssp126
#    dir="/p/tmp/fallah/"+sp+"_out03/"
#    rlat, rlon, data = read_nc(dir+"TOT_PREC_changes_"+sp+"_eca_r20mm.nc", "very_heavy_precipitation_days_index_per_time_period")
#    cmaps = plt.cm.BrBG                                         
#    plot_maps("./plots/eca_rx20mm_"+sp+".png",data,cmaps,-100,100,21,rlat,rlon)
    

####################################################################
# CMIP6 




intake_dir="/p/tmp/fallah/intake/remaped/"   
rlat, rlon, data = read_nc(intake_dir+"ssp585/ssp585_ensmean_eca_20mm.nc", "very_heavy_precipitation_days_index_per_time_period") 
plot_maps("./plots/TOT_PREC_changes_ssp585_cmip6_ensmean.png",data,plt.cm.BrBG,-100,100,21,rlat,rlon)
rlat, rlon, data = read_nc(intake_dir+"ssp585/ssp585_ensstd_eca_20mm.nc", "very_heavy_precipitation_days_index_per_time_period")
plot_maps("./plots/TOT_PREC_changes_ssp585_cmip6_ensstd.png",data,plt.cm.binary,0,100,21,rlat,rlon)






rlat, rlon, data = read_nc(intake_dir+"ssp370/ssp370_ensmean_eca_20mm.nc", "very_heavy_precipitation_days_index_per_time_period")
plot_maps("./plots/TOT_PREC_changes_ssp370_cmip6_ensmean.png",data,plt.cm.BrBG,-100,100,21,rlat,rlon)
rlat, rlon, data = read_nc(intake_dir+"ssp370/ssp370_ensstd_eca_20mm.nc", "very_heavy_precipitation_days_index_per_time_period")
plot_maps("./plots/TOT_PREC_changes_ssp370_cmip6_ensstd.png",data,plt.cm.binary,0,100,21,rlat,rlon)

rlat, rlon, data = read_nc(intake_dir+"ssp126/ssp126_ensmean_eca_20mm.nc", "very_heavy_precipitation_days_index_per_time_period")
plot_maps("./plots/TOT_PREC_changes_ssp126_cmip6_ensmean.png",data,plt.cm.BrBG,-100,100,21,rlat,rlon)
rlat, rlon, data = read_nc(intake_dir+"ssp126/ssp126_ensstd_eca_20mm.nc", "very_heavy_precipitation_days_index_per_time_period")
plot_maps("./plots/TOT_PREC_changes_ssp126_cmip6_ensstd.png",data,plt.cm.binary,0,100,21,rlat,rlon)



#rlat, rlon, data = read_nc(intake_dir+"ssp370/ssp370_ensmean.nc", "pr")  
#plot_maps("./plots/pr_change_ssp370_cmip6.eps",data,plt.cm.PuOr,-10,10,21,rlat,rlon)
#rlat, rlon, data = read_nc(intake_dir+"ssp126/ssp126_ensmean.nc", "pr") 
#plot_maps("./plots/pr_change_ssp126_cmip6.eps",data,plt.cm.PuOr,-10,10,21,rlat,rlon)    
