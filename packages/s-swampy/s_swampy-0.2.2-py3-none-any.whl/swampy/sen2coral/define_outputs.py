# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:35:53 2017

@author: PaulRyan/stevesagar
"""
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
#from itertools import combinations
#import os

from . import sambuca_outputs

#path must have trailing directory separator
def output_suite(result_recorder, image_info, coordinates, path='', filename=''):
    
    # read in subsection of image processed
    
    xs=coordinates[0]
    xe=coordinates[1]
    ys=coordinates[2]
    ye=coordinates[3]
    
    #define some output arrays from the results
    
    skip_mask = (result_recorder.success[xs:xe,ys:ye] < 1)
    chl = ma.masked_array(result_recorder.chl[xs:xe,ys:ye],mask=skip_mask)
    cdom = ma.masked_array(result_recorder.cdom[xs:xe,ys:ye],mask=skip_mask)
    nap = ma.masked_array(result_recorder.nap[xs:xe,ys:ye],mask=skip_mask)
    depth = ma.masked_array(result_recorder.depth[xs:xe,ys:ye],mask=skip_mask)
    nit = ma.masked_array(result_recorder.nit[xs:xe,ys:ye],mask=skip_mask)
    kd = ma.masked_array(result_recorder.kd[xs:xe,ys:ye],mask=skip_mask)
    sdi = ma.masked_array(result_recorder.sdi[xs:xe,ys:ye],mask=skip_mask)
    sub1_frac = ma.masked_array(result_recorder.sub1_frac[xs:xe,ys:ye],mask=skip_mask)
    sub2_frac = ma.masked_array(result_recorder.sub2_frac[xs:xe,ys:ye],mask=skip_mask)
    sub3_frac = ma.masked_array(result_recorder.sub3_frac[xs:xe,ys:ye],mask=skip_mask)
    error_f = ma.masked_array(result_recorder.error_f[xs:xe,ys:ye],mask=skip_mask)
    total_abun = sub1_frac+sub2_frac+sub3_frac
    sub1_norm = sub1_frac / total_abun
    sub2_norm = sub2_frac / total_abun
    sub3_norm = sub3_frac / total_abun
    
    # A scaled true colour image to look at closed rrs
    rgbimg=np.zeros(((xe-xs),(ye-ys),3), 'uint8')
    rgbimg[..., 0] = (result_recorder.closed_rrs[xs:xe,ys:ye,3])*1024
    rgbimg[..., 1] = (result_recorder.closed_rrs[xs:xe,ys:ye,2])*1024
    rgbimg[..., 2] = (result_recorder.closed_rrs[xs:xe,ys:ye,1])*1024
    
    fullname=path+filename
    
    sambuca_outputs.writeout(fullname+'1_depth.tif',depth,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'2_kd550.tif',kd,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'3_rgbimg.tif',rgbimg,image_info['affine'],image_info['crs'],transpose=[2,0,1])
    
    sambuca_outputs.writeout(fullname+'4_sdi.tif',sdi,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'5_sub1_frac.tif',sub1_frac,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'6_sub2_frac.tif',sub2_frac,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'7_sub3_frac.tif',sub3_frac,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'8_total_abun.tif',total_abun,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'9_error_f.tif',error_f,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'10_sub1_norm.tif',sub1_norm,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'11_sub2_norm.tif',sub2_norm,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'12_sub3_norm.tif',sub3_norm,image_info['affine'],image_info['crs'],np.float32)
    
    sambuca_outputs.writeout(fullname+'13_closedrrs.tif',result_recorder.closed_rrs[xs:xe,ys:ye,:],image_info['affine'],image_info['crs'],np.float32,transpose=[2,0,1])

    #img_path='C:\\Users\\PCUSER\\sambuca_project\\Swampy\\'
    plt.imshow(depth[xs:xe,ys:ye], interpolation='nearest');
    img = plt.colorbar()
    plt.title('depth')
    plt.savefig(fullname+"depth.png")
    plt.close()
        
    plt.imshow(sdi[xs:xe,ys:ye], interpolation='nearest');
    img = plt.colorbar()
    plt.title('sdi')
    plt.savefig(fullname+"sdi.png")
    plt.close()
    

 # single band - convert from float64 to float32
#    sambuca_outputs.writeout('1_rr_chl.tif',result_recorder.chl,src.affine,src.crs,np.float32)
#    
#    # write out masked array and convert type
#    sambuca_outputs.writeout('2_ma_chl.tif',chl,src.affine,src.crs,np.float32)
#    
#    # write out masked array, convert but use np.nan as the fill value
#    sambuca_outputs.writeout('3_ma_chl_nan.tif',chl,src.affine,src.crs,np.float32,fill=np.nan)
#    
#    # write out ndarray, but the band is not the first dimension so use transpose option
#    sambuca_outputs.writeout('4_rgbimg.tif',rgbimg,src.affine,src.crs,transpose=[2,0,1])
#    
#    # write out a single band from multi-band array
#    sambuca_outputs.writeout('7_rr_closedrrs_1band.tif',result_recorder.closed_rrs[:,:,0],src.affine,src.crs,dtype=np.float32)
    
    

