"""
Example of usage of the AVB framework to infer a single exponential decay
model.

This uses the Python classes directly to infer the parameters for a single
instance of noisy data constructed as a Numpy array.
"""
import sys
import logging

import numpy as np

from avb import Avb
import svb

# This starts the random number generator off with the same seed value
# each time, so the results are repeatable. However it is worth changing
# the seed (or simply removing this line) to see how different data samples
# affect the results
np.random.seed(0)

# Ground truth parameters
PARAMS_TRUTH = [42, 0.5, 10, 5.0]
NOISE_PREC_TRUTH = 0.1
NOISE_VAR_TRUTH = 1/NOISE_PREC_TRUTH
NOISE_STD_TRUTH = np.sqrt(NOISE_VAR_TRUTH)

# Create single exponential model
model = svb.get_model_class("biexp")(None)

# Observed data samples are generated by Numpy from the ground truth
# Gaussian distribution. Reducing the number of samples should make
# the inference less 'confident' - i.e. the output variances for
# MU and BETA will increase
N = 100
DT = 0.02
t = np.array([float(t)*DT for t in range(N)])
DATA_CLEAN = model.ievaluate(PARAMS_TRUTH, t)
DATA_NOISY = DATA_CLEAN + np.random.normal(0, NOISE_STD_TRUTH, [N])
print("Data samples are:")
print(t)
print(DATA_CLEAN)
print(DATA_NOISY)

# Run Fabber as a comparison if desired
#import os
#import nibabel as nib
#niidata = DATA_NOISY.reshape((1, 1, 1, N))
#nii = nib.Nifti1Image(niidata, np.identity(4))
#nii.to_filename("data_noisy.nii.gz")
#os.system("fabber_exp --data=data_noisy --print-free-energy --output=fabberout --dt=%.3f --model=exp --num-exps=1 --method=vb --noise=white --overwrite --debug" % DT)

# Log to stdout
logging.getLogger().setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(levelname)s : %(message)s'))
logging.getLogger().addHandler(handler)

# Run AVB inference
avb = Avb(t, svb.DataModel(DATA_NOISY), model, debug="--debug" in sys.argv, max_iterations=5000)
#avb = Avb(t, svb.DataModel(DATA_NOISY), model, debug="--debug" in sys.argv, max_iterations=1)
avb.run(use_adam=True)