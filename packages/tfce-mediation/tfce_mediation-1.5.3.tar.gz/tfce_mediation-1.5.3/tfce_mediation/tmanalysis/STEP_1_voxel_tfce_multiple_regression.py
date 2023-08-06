#!/usr/bin/env python

#  Multiple regression with TFCE
#  Copyright (C) 2016	Tristram Lett

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.	If not, see <http://www.gnu.org/licenses/>.

import os
import numpy as np
import nibabel as nib

from scipy import stats
import argparse as ap

from tfce_mediation.cynumstats import resid_covars, tval_int, calcF
from tfce_mediation.tfce import CreateAdjSet
from tfce_mediation.pyfunc import write_voxelStat_img, create_adjac_voxel, image_regression, image_reg_VIF

DESCRIPTION = "Voxel-wise multiple regression with TFCE. "

def getArgumentParser(ap = ap.ArgumentParser(description = DESCRIPTION)):

	group = ap.add_mutually_exclusive_group(required=True)
	group.add_argument("-i", "--input", 
		nargs=2,
		help="[Predictor(s)] [Covariate(s)] (recommended)", 
		metavar=('*.csv', '*.csv'))
	group.add_argument("-r", "--regressors", 
		nargs=1, 
		help="Single step regression", 
		metavar=('*.csv'))
	group.add_argument("-m", "--onesample", 
		nargs=1, 
		help="One sample t-test. i.e., test sample mean or intercept.", 
		metavar=('*.csv or none'))
	ap.add_argument("-f", "--ftest", 
		help=	"""
				Perform mixed-effect model ANOVA on predictors (experimental).
				The square root of the f-statistic image undergoes TFCE.
				""", 
		action="store_true")
	ap.add_argument("-t", "--tfce", 
		help="TFCE settings. H (i.e., height raised to power H), E (i.e., extent raised to power E), Connectivity (either 26 or 6 directions). Default: %(default)s).", 
		nargs=3, 
		default=[2,1,26], 
		metavar=('H', 'E', '[6 or 26]'))
	ap.add_argument("-v", "--voxelregressor", 
		nargs=1,
		help="Add a voxel-wise independent regressor (beta feature). A variance inflation factor (VIF) image will also be produced to check for multicollinearity (generally, VIF > 5 suggest problematic collinearity.)", 
		metavar=('*.nii.gz'))
	return ap

def run(opts):
	if not os.path.exists("python_temp"):
		print("python_temp missing!")

	#load variables
	raw_nonzero = np.load('python_temp/raw_nonzero.npy')
	affine_mask = np.load('python_temp/affine_mask.npy')
	data_mask = np.load('python_temp/data_mask.npy')
	data_index = data_mask>0.99
	num_voxel = np.load('python_temp/num_voxel.npy')
	n = raw_nonzero.shape[1]

	imgext = '.nii.gz' #default save type is nii.gz 
#	if not os.path.isfile('python_temp/imgext.npy'): # to maintain compability
#		imgext = '.nii.gz'
#	else:
#		imgext = np.load('python_temp/imgext.npy')

	#step1
	if opts.input:
		pred_x = np.genfromtxt(opts.input[0], delimiter=',')
		covars = np.genfromtxt(opts.input[1], delimiter=',')
		x_covars = np.column_stack([np.ones(n),covars])
		y = resid_covars(x_covars,raw_nonzero)
		np.save('python_temp/covars',covars)
	if opts.regressors:
		pred_x = np.genfromtxt(opts.regressors[0], delimiter=',')
		y = raw_nonzero.T
	if opts.onesample:
		pred_x=np.ones(n)
		pred_x[:int(n/2)]=-1
		if opts.onesample[0] != 'none':
			covars = np.genfromtxt(opts.onesample[0], delimiter=',')
			x_covars = np.column_stack([np.ones(n),covars])
			y = resid_covars(x_covars,raw_nonzero)
			np.save('python_temp/covars',covars)
		else:
			y = raw_nonzero.T

	ancova=0
	if opts.ftest: 
		ancova=1

	#TFCE
	adjac = create_adjac_voxel(data_index,data_mask,num_voxel,dirtype=opts.tfce[2])
	calcTFCE = CreateAdjSet(float(opts.tfce[0]), float(opts.tfce[1]), adjac) # H=2, E=2, 26 neighbour connectivity

	#save
	np.save('python_temp/adjac',adjac)
	np.save('python_temp/pred_x',pred_x)
	np.save('python_temp/ancova', ancova)
	np.save('python_temp/optstfce', opts.tfce)
	np.save('python_temp/raw_nonzero_corr',y.T.astype(np.float32, order = "C"))

	if not os.path.exists('output'):
		os.mkdir('output')
	os.chdir('output')
	X = np.column_stack([np.ones(n),pred_x])
	k = len(X.T)

	if opts.onesample:
		if opts.onesample[0] == 'none':
			tvalues, _ = stats.ttest_1samp(raw_nonzero,0,axis=1)
			write_voxelStat_img('tstat_intercept',
				tvalues,
				data_mask,
				data_index,
				affine_mask,
				calcTFCE,
				imgext)
			write_voxelStat_img('negtstat_intercept',
				(tvalues*-1),
				data_mask,
				data_index,
				affine_mask,
				calcTFCE,
				imgext)
		else:
			tvalues=tval_int(x_covars, np.linalg.inv(np.dot(x_covars.T, x_covars)),raw_nonzero.T,n,len(x_covars.T),num_voxel)
			tvalues = tvalues[0]
			write_voxelStat_img('tstat_intercept',
				tvalues,
				data_mask,
				data_index,
				affine_mask,
				calcTFCE,
				imgext)
			write_voxelStat_img('negtstat_intercept',
				(tvalues*-1),
				data_mask,
				data_index,
				affine_mask,
				calcTFCE,
				imgext)
		exit()

	if ancova==0:

		if opts.voxelregressor:

			img_all_name = opts.voxelregressor[0]
			_, file_ext = os.path.splitext(img_all_name)
			if file_ext == '.gz':
				_, file_ext = os.path.splitext(img_all_name)
				if file_ext == '.mnc':
					imgext = '.mnc'
					image_x = nib.load('../%s' % img_all_name).get_data()[data_index].astype(np.float32)
				else:
					imgext = '.nii.gz'
					os.system("zcat ../%s > temp_4d.nii" % img_all_name)
					image_x = nib.load('temp_4d.nii').get_data()[data_index].astype(np.float32)
					os.system("rm temp_4d.nii")
			elif file_ext == '.nii':
				imgext = '.nii.gz' # default to zipped images
				image_x = nib.load('../%s' % img_all_name).get_data()[data_index].astype(np.float32)
			else:
				print('Error filetype for %s is not supported' % img_all_name)
				quit()

			tvalues, timage = image_regression(raw_nonzero.astype(np.float32), image_x, pred_x, covars)
			write_voxelStat_img('tstat_imgcovar', 
				timage,
				data_mask,
				data_index,
				affine_mask,
				calcTFCE,
				imgext)
			write_voxelStat_img('negtstat_imgcovar',
				-timage,
				data_mask,
				data_index,
				affine_mask,
				calcTFCE,
				imgext)
			tvalues = tvalues.T
			VIF = image_reg_VIF(image_x.T, np.column_stack((pred_x, covars)))
			write_voxelStat_img('VIF_imgcovar',
				VIF,
				data_mask,
				data_index,
				affine_mask,
				calcTFCE,
				imgext,
				TFCE = False)
		else:
			#multiple regression
			invXX = np.linalg.inv(np.dot(X.T, X))
			tvalues = tval_int(X, invXX, y, n, k, num_voxel)
		tvalues[np.isnan(tvalues)]=0 #only necessary for ANTS skeleton
		#write TFCE images
		for j in range(k-1):
			tnum=j+1
			write_voxelStat_img('tstat_con%d' % tnum, tvalues[tnum], data_mask, data_index, affine_mask, calcTFCE, imgext)
			write_voxelStat_img('negtstat_con%d' % tnum, (tvalues[tnum]*-1), data_mask, data_index, affine_mask, calcTFCE, imgext)
	elif ancova==1:
		#anova
		fvals = calcF(X, y, n, k) # sqrt to approximate the t-distribution
		fvals[fvals < 0] = 0
		write_voxelStat_img('fstat',
			np.sqrt(fvals),
			data_mask,
			data_index,
			affine_mask,
			calcTFCE,
			imgext)
	else:
		print("Error")
		exit()

if __name__ == "__main__":
	parser = getArgumentParser()
	opts = parser.parse_args()
	run(opts)
