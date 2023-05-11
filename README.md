# X-ray-course-scripts
Scripts for CHEM-L2300 - X-ray Scattering Methods for Structural Analysis of Bio-based Materials.

## `waxs_fwhm.py` - Determining the FWHM for the WAXS scattering peak of gold nanoparticles

### Data input
The data files are named *WAXS_AuNP.txt* and *WAXS_AuNP_background.txt*, for the sample and backgound respectively. The script reads the *q* and *I* values from tab separated, UFT-8 .txt data files (first rows are regarded as names). It records them in the `data` and `data_bg` variables (numpy arrays), which are indexed as `Q` and `I` for the scattering and intensity.

The background is then subtracted and the normalized scatterng data overwrites the `Q` in `data`.

### Finding the peak
For the peak fitting, the `signal.savgol_filter()` function is used to obtain a smoothened function, to reduce noise on the peak. This helps in getting a single value in the next step, where the `signal.find_peaks()` is used, to determine the position of the peak. Since we are searching for just the highest peak, the height cutoff can be set to 0.9 times the intensity maximum.

### Determining the FWHM
Next, `signal.peak_widths()` is used to determine the full width at half maximum (FWHM), by setting the `rel_height` parameter to 0.5. The returned indicies are rounded and used to obtain the values of *q* at half maximum.

## Output
The position and FWHM are output on the console.

## Graphs
Matplotlib is used for plotting. The background-subtracted scattering data is plotted in black. The Peak is marked with the red cross. The position of the FWHM is indicated by the red line, and its value is drawn in red text.

The graph is exported to *AuNP_graph.png*.
