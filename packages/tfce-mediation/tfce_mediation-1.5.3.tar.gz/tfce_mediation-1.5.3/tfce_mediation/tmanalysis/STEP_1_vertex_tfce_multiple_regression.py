#!/usr/bin/env python

#    Multiple regression with TFCE
#    Copyright (C) 2016  Tristram Lett

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import numpy as np
import nibabel as nib
import argparse as ap

from tfce_mediation.cynumstats import resid_covars, tval_int
from tfce_mediation.tfce import CreateAdjSet
from tfce_mediation.pyfunc import write_vertStat_img, create_adjac_vertex, convert_fslabel, image_regression, image_reg_VIF

DESCRIPTION = "Vertex-wise multiple regression with TFCE."

def getArgumentParser(ap = ap.ArgumentParser(description = DESCRIPTION)):

	group = ap.add_mutually_exclusive_group(required=True)
	group.add_argument("-i", "--input", 
		nargs=2, 
		help="[Predictor(s)] [Covariate(s)] (recommended)", 
		metavar=('*.csv', '*.csv'))
	group.add_argument("-r", "--regressors", 
		nargs=1, help="Single step regression", 
		metavar=('*.csv'))

	ap.add_argument("-s", "--surface",  
		nargs=1, 
		metavar=('area or thickness'), 
		required=True)
	ap.add_argument("-f", "--fwhm", 
		help="Specific all surface file with different smoothing. Default is 03B (recommended)" , 
		nargs=1, 
		default=['03B'], 
		metavar=('??B'))

	mask = ap.add_mutually_exclusive_group(required=False)
	mask.add_argument("--fmri", 
		help="Masking threshold for fMRI surfaces. Default is 0.1 (i.e., mask regions with values less than -0.1 and greater than 0.1)",
		const=0.1, 
		type=float, 
		nargs='?')
	mask.add_argument("-m","--fsmask", 
		help="Create masking array based on fsaverage label. Default is cortex", 
		const='cortex', 
		nargs='?')
	mask.add_argument("-l","--label", 
		help="Load label as masking array for lh and rh, respectively.", 
		nargs=2, 
		metavar=('lh.*.label','rh.*.label'))
	mask.add_argument("-b","--binmask", 
		help="Load binary mask surface for lh and rh, respectively.", 
		nargs=2, 
		metavar=('lh.*.mgh','rh.*.mgh'))

	adjac = ap.add_mutually_exclusive_group(required=False)
	adjac.add_argument("-d", "--dist", 
		help="Load supplied adjacency sets geodesic distance in mm. Default is 3 (recommended).", 
		choices = [1,2,3], 
		type=int,  
		nargs=1, 
		default=[3])
	adjac.add_argument("-a", "--adjfiles", help="Load custom adjacency set for each hemisphere.", 
		nargs=2, 
		metavar=('*.npy', '*.npy'))
	adjac.add_argument("-t", "--triangularmesh", 
		help="Create adjacency based on triangular mesh without specifying distance.",
		action='store_true')
	ap.add_argument("--inputsurfs", 
		help="Load surfaces for triangular mesh tfce. --triangularmesh option must be used.",
		nargs=2,
		metavar=('lh.*.srf', 'rh.*.srf'))
	ap.add_argument("--tfce", 
		help="TFCE settings. H (i.e., height raised to power H), E (i.e., extent raised to power E). Default: %(default)s). H=2, E=2/3 is the point at which the cummulative density function is approximately Gaussian distributed.", 
		nargs=2, 
		default=[2,0.67], 
		metavar=('H', 'E'))
	ap.add_argument("--noweight", 
		help="Do not weight each vertex for density of vertices within the specified geodesic distance.", 
		action="store_true")
	ap.add_argument("-v", "--vertexregressor", 
		nargs=2,
		help="Add a vertex-wise independent regressor (beta feature). A variance inflation factor (VIF) image will also be produced to check for multicollinearity (generally, VIF > 5 suggest problematic collinearity.)", 
		metavar=('mgh', 'mgh'))

	return ap

def run(opts):

	scriptwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	surface = opts.surface[0]
	FWHM = opts.fwhm[0]

	#load surface data
	img_data_lh = nib.freesurfer.mghformat.load("lh.all.%s.%s.mgh" % (surface,FWHM))
	data_full_lh = img_data_lh.get_data()
	data_lh = np.squeeze(data_full_lh)
	affine_mask_lh = img_data_lh.get_affine()
	n = data_lh.shape[1] # num_subjects
	outdata_mask_lh = np.zeros_like(data_full_lh[:,:,:,1])
	img_data_rh = nib.freesurfer.mghformat.load("rh.all.%s.%s.mgh" % (surface,FWHM))
	data_full_rh = img_data_rh.get_data()
	data_rh = np.squeeze(data_full_rh)
	affine_mask_rh = img_data_rh.get_affine()
	outdata_mask_rh = np.zeros_like(data_full_rh[:,:,:,1])
	if not os.path.exists("lh.mean.%s.%s.mgh" % (surface,FWHM)):
		mean_lh = np.sum(data_lh,axis=1)/data_lh.shape[1]
		outmean_lh = np.zeros_like(data_full_lh[:,:,:,1])
		outmean_lh[:,0,0] = mean_lh
		nib.save(nib.freesurfer.mghformat.MGHImage(outmean_lh,affine_mask_lh),"lh.mean.%s.%s.mgh" % (surface,FWHM))
		mean_rh = np.sum(data_rh,axis=1)/data_rh.shape[1]
		outmean_rh = np.zeros_like(data_full_rh[:,:,:,1])
		outmean_rh[:,0,0] = mean_rh
		nib.save(nib.freesurfer.mghformat.MGHImage(outmean_rh,affine_mask_rh),"rh.mean.%s.%s.mgh" % (surface,FWHM))
	else:
		img_mean_lh = nib.freesurfer.mghformat.load("lh.mean.%s.%s.mgh" % (surface,FWHM))
		mean_full_lh = img_mean_lh.get_data()
		mean_lh = np.squeeze(mean_full_lh)
		img_mean_rh = nib.freesurfer.mghformat.load("rh.mean.%s.%s.mgh" % (surface,FWHM))
		mean_full_rh = img_mean_rh.get_data()
		mean_rh = np.squeeze(mean_full_rh)

	#TFCE
	if opts.triangularmesh:
		print("Creating adjacency set")
		if opts.inputsurfs:
			# 3 Neighbour vertex connectity
			v_lh, faces_lh = nib.freesurfer.read_geometry(opts.inputsurfs[0])
			v_rh, faces_rh = nib.freesurfer.read_geometry(opts.inputsurfs[1])
		else:
			v_lh, faces_lh = nib.freesurfer.read_geometry("%s/fsaverage/surf/lh.sphere" % os.environ["SUBJECTS_DIR"])
			v_rh, faces_rh = nib.freesurfer.read_geometry("%s/fsaverage/surf/rh.sphere" % os.environ["SUBJECTS_DIR"])
		adjac_lh = create_adjac_vertex(v_lh,faces_lh)
		adjac_rh = create_adjac_vertex(v_rh,faces_rh)
	elif opts.adjfiles:
		print("Loading prior adjacency set")
		arg_adjac_lh = opts.adjfiles[0]
		arg_adjac_rh = opts.adjfiles[1]
		adjac_lh = np.load(arg_adjac_lh)
		adjac_rh = np.load(arg_adjac_rh)
	elif opts.dist:
		print("Loading prior adjacency set for %s mm" % opts.dist[0])
		adjac_lh = np.load("%s/adjacency_sets/lh_adjacency_dist_%s.0_mm.npy" % (scriptwd,str(opts.dist[0])))
		adjac_rh = np.load("%s/adjacency_sets/rh_adjacency_dist_%s.0_mm.npy" % (scriptwd,str(opts.dist[0])))
	else:
		print("Error")
	if opts.noweight or opts.triangularmesh:
		vdensity_lh = 1
		vdensity_rh = 1
	else:
		# correction for vertex density
		vdensity_lh = np.zeros((adjac_lh.shape[0]))
		vdensity_rh = np.zeros((adjac_rh.shape[0]))
		for i in range(adjac_lh.shape[0]):
			vdensity_lh[i] = len(adjac_lh[i])
		for j in range(adjac_rh.shape[0]): 
			vdensity_rh[j] = len(adjac_rh[j])
		vdensity_lh = np.array((1 - (vdensity_lh/vdensity_lh.max()) + (vdensity_lh.mean()/vdensity_lh.max())), dtype=np.float32)
		vdensity_rh = np.array((1 - (vdensity_rh/vdensity_rh.max()) + (vdensity_rh.mean()/vdensity_rh.max())), dtype=np.float32)
	calcTFCE_lh = CreateAdjSet(float(opts.tfce[0]), float(opts.tfce[1]), adjac_lh)
	calcTFCE_rh = CreateAdjSet(float(opts.tfce[0]), float(opts.tfce[1]), adjac_rh)
	
	#create masks
	if opts.fmri:
		maskthresh = opts.fmri
		print(("fMRI threshold mask = %2.2f" % maskthresh))
		bin_mask_lh = np.logical_or(mean_lh > maskthresh, mean_lh < (-1*maskthresh))
		bin_mask_rh = np.logical_or(mean_rh > maskthresh, mean_rh < (-1*maskthresh))

	elif opts.fsmask:
		label = opts.fsmask
		print(("Loading fsaverage ?l.%s.label" % label))

		index_lh, _, _ = convert_fslabel("%s/fsaverage/label/lh.%s.label" % (os.environ["SUBJECTS_DIR"],label))
		index_rh, _, _ = convert_fslabel("%s/fsaverage/label/rh.%s.label" % (os.environ["SUBJECTS_DIR"],label))

		bin_mask_lh = np.zeros_like(mean_lh)
		bin_mask_lh[index_lh]=1
		bin_mask_lh = bin_mask_lh.astype(bool)

		bin_mask_rh = np.zeros_like(mean_rh)
		bin_mask_rh[index_rh]=1
		bin_mask_rh = bin_mask_rh.astype(bool)

	elif opts.label:
		label_lh = opts.label[0]
		label_rh = opts.label[1]

		index_lh, _, _ = convert_fslabel(label_lh)
		index_rh, _, _ = convert_fslabel(label_rh)

		bin_mask_lh = np.zeros_like(mean_lh)
		bin_mask_lh[index_lh]=1
		bin_mask_lh = bin_mask_lh.astype(bool)

		bin_mask_rh = np.zeros_like(mean_rh)
		bin_mask_rh[index_rh]=1
		bin_mask_rh = bin_mask_rh.astype(bool)
	elif opts.binmask:
		print("Loading masks")
		binmgh_lh = np.squeeze(nib.freesurfer.mghformat.load(opts.binmask[0]).get_data())
		binmgh_rh = np.squeeze(nib.freesurfer.mghformat.load(opts.binmask[1]).get_data())
		bin_mask_lh = binmgh_lh>.99
		bin_mask_rh = binmgh_rh>.99
	else:
		bin_mask_lh = mean_lh != 0
		bin_mask_rh = mean_rh != 0
	data_lh = data_lh[bin_mask_lh]
	num_vertex_lh = data_lh.shape[0]
	data_rh = data_rh[bin_mask_rh]
	num_vertex_rh = data_rh.shape[0]
	num_vertex = num_vertex_lh + num_vertex_rh
	all_vertex = data_full_lh.shape[0]

	if opts.input: 
	#load variables
		arg_predictor = opts.input[0]
		arg_covars = opts.input[1]
		pred_x = np.genfromtxt(arg_predictor, delimiter=',')
		covars = np.genfromtxt(arg_covars, delimiter=',')
	#step1
		x_covars = np.column_stack([np.ones(n),covars])
		y_lh = resid_covars(x_covars,data_lh)
		y_rh = resid_covars(x_covars,data_rh)
		merge_y=np.hstack((y_lh,y_rh))
		del y_lh
		del y_rh
	if opts.regressors:
		arg_predictor = opts.regressors[0]
		pred_x = np.genfromtxt(arg_predictor, delimiter=',')
		merge_y=np.hstack((data_lh.T,data_rh.T))

	#save variables
	if not os.path.exists("python_temp_%s" % (surface)):
		os.mkdir("python_temp_%s" % (surface))

	np.save("python_temp_%s/pred_x" % (surface),pred_x)
	np.save("python_temp_%s/num_subjects" % (surface),n)
	np.save("python_temp_%s/all_vertex" % (surface),all_vertex)
	np.save("python_temp_%s/num_vertex" % (surface),num_vertex)
	np.save("python_temp_%s/num_vertex_lh" % (surface),num_vertex_lh)
	np.save("python_temp_%s/num_vertex_rh" % (surface),num_vertex_rh)
	np.save("python_temp_%s/bin_mask_lh" % (surface),bin_mask_lh)
	np.save("python_temp_%s/bin_mask_rh" % (surface),bin_mask_rh)
	np.save("python_temp_%s/affine_mask_lh" % (surface),affine_mask_lh)
	np.save("python_temp_%s/affine_mask_rh" % (surface),affine_mask_rh)
	np.save("python_temp_%s/adjac_lh" % (surface),adjac_lh)
	np.save("python_temp_%s/adjac_rh" % (surface),adjac_rh)
	np.save("python_temp_%s/merge_y" % (surface),merge_y.astype(np.float32, order = "C"))
	np.save('python_temp_%s/optstfce'% (surface), opts.tfce)
	np.save('python_temp_%s/vdensity_lh'% (surface), vdensity_lh)
	np.save('python_temp_%s/vdensity_rh'% (surface), vdensity_rh)

	#write TFCE images
	if not os.path.exists("output_%s" % (surface)):
		os.mkdir("output_%s" % (surface))
	os.chdir("output_%s" % (surface))

	#step2
	X = np.column_stack([np.ones(n),pred_x])
	k = len(X.T)
	if opts.vertexregressor:
		img_x_lh = np.squeeze(nib.freesurfer.mghformat.load("../%s" % opts.vertexregressor[0]).get_data())
		img_x_rh = np.squeeze(nib.freesurfer.mghformat.load("../%s" % opts.vertexregressor[1]).get_data())
		img_x_lh = img_x_lh[bin_mask_lh]
		img_x_rh = img_x_rh[bin_mask_rh]
		img_x = np.hstack((img_x_lh.T,img_x_rh.T))
		img_x_lh = img_x_rh = None
		merge_y = np.hstack((data_lh.T,data_rh.T))
		tvals, timage = image_regression(merge_y.T.astype(np.float32),
			img_x.T.astype(np.float32),
			pred_x,
			covars)
		VIF = image_reg_VIF(merge_y, np.column_stack((pred_x, covars)))

		tvals = tvals.T
		timage = timage.T
		write_vertStat_img('tstat_imgcovar', 
			timage[:num_vertex_lh],
			outdata_mask_lh,
			affine_mask_lh,
			surface, 'lh',
			bin_mask_lh,
			calcTFCE_lh,
			bin_mask_lh.shape[0],
			vdensity_lh)
		write_vertStat_img('tstat_imgcovar', 
			timage[num_vertex_lh:],
			outdata_mask_rh,
			affine_mask_rh,
			surface,
			'rh',
			bin_mask_rh,
			calcTFCE_rh,
			bin_mask_rh.shape[0],
			vdensity_rh)
		write_vertStat_img('negtstat_imgcovar', 
			-timage[:num_vertex_lh],
			outdata_mask_lh,
			affine_mask_lh,
			surface, 'lh',
			bin_mask_lh,
			calcTFCE_lh,
			bin_mask_lh.shape[0],
			vdensity_lh)
		write_vertStat_img('negtstat_imgcovar', 
			-timage[num_vertex_lh:],
			outdata_mask_rh,
			affine_mask_rh,
			surface,
			'rh',
			bin_mask_rh,
			calcTFCE_rh,
			bin_mask_rh.shape[0],
			vdensity_rh)
		write_vertStat_img('VIF_imgcovar', 
			VIF[:num_vertex_lh],
			outdata_mask_lh,
			affine_mask_lh,
			surface, 'lh',
			bin_mask_lh,
			calcTFCE_lh,
			bin_mask_lh.shape[0],
			vdensity_lh, 
			TFCE = False)
		write_vertStat_img('VIF_imgcovar', 
			VIF[num_vertex_lh:],
			outdata_mask_rh,
			affine_mask_rh,
			surface,
			'rh',
			bin_mask_rh,
			calcTFCE_rh,
			bin_mask_rh.shape[0],
			vdensity_rh,
			TFCE =False)


	else:
		invXX = np.linalg.inv(np.dot(X.T, X))
		tvals = tval_int(X, invXX, merge_y, n, k, num_vertex)

	for j in range(k-1):
		tnum=j+1
		write_vertStat_img('tstat_con%d' % tnum, 
			tvals[tnum,:num_vertex_lh],
			outdata_mask_lh,
			affine_mask_lh,
			surface,
			'lh',
			bin_mask_lh,
			calcTFCE_lh,
			bin_mask_lh.shape[0],
			vdensity_lh)
		write_vertStat_img('tstat_con%d' % tnum,
			tvals[tnum,num_vertex_lh:],
			outdata_mask_rh,
			affine_mask_rh,
			surface,
			'rh',
			bin_mask_rh,
			calcTFCE_rh,
			bin_mask_rh.shape[0],
			vdensity_rh)
		write_vertStat_img('negtstat_con%d' % tnum,
			(tvals[tnum,:num_vertex_lh]*-1),
			outdata_mask_lh,
			affine_mask_lh,
			surface,
			'lh',
			bin_mask_lh,
			calcTFCE_lh,
			bin_mask_lh.shape[0],
			vdensity_lh)
		write_vertStat_img('negtstat_con%d' % tnum,
			(tvals[tnum,num_vertex_lh:]*-1),
			outdata_mask_rh,
			affine_mask_rh,
			surface,
			'rh',
			bin_mask_rh,
			calcTFCE_rh,
			bin_mask_rh.shape[0],
			vdensity_rh)

if __name__ == "__main__":
	parser = getArgumentParser()
	opts = parser.parse_args()
	run(opts)
