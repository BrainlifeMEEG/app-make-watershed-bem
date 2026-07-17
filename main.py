"""
Compute a watershed BEM surface from a FreeSurfer reconstruction.

This app copies a FreeSurfer subject reconstruction into out_dir, runs
MNE's watershed BEM algorithm on it, and generates a QC report.

Inputs:
    - output: Path to the FreeSurfer subject reconstruction directory

Outputs:
    - out_dir/: Copy of the subject reconstruction plus generated BEM surfaces
    - out_report/report.html: QC report with BEM/MRI visualization
    - product.json: Metadata about the BEM computation
"""

# Copyright (c) 2026 brainlife.io

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne

# Import shared utilities
from brainlife_utils import (
    load_config,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    require_config_keys
)

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_report')

# Load configuration
config = load_config()
require_config_keys(config, ['output'])

# subjects_dir: path to the directory containing the FreeSurfer subjects reconstructions (SUBJECTS_DIR)
subjects_dir = config['output']

# subject: Name of freesurfer subject folder
subject = 'output'

# copy folder subjects_dir to "out_dir"
os.system("cp -r " + subjects_dir + " out_dir")
subjects_dir = "out_dir"

# Start MNE-Report
report = mne.Report(title='Watershed BEM Report')

# Make Watershed BEM
mne.bem.make_watershed_bem(subject, subjects_dir=subjects_dir, overwrite=True)

# Add BEM to MNE-Report
report.add_bem(
    subject=subject,
    subjects_dir=subjects_dir,
    title="MRI & BEM",
    decim=40,
    width=256,
)

# == SAVE REPORT ==
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == CREATE PRODUCT.JSON ==
product_items = []
add_info_to_product(product_items, f'Computed watershed BEM surfaces for subject "{subject}"', 'success')
create_product_json(product_items)
