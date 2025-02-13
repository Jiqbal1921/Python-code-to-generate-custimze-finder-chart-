# -*- coding: utf-8 -*-
"""Finder chart.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10FRHQwSgJu2iO8CoO15jNiDLluxVXe9S
"""

from astroquery.skyview import SkyView
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, Angle
import numpy as np

# Central coordinate between NGC 869 and NGC 884
coord_center = SkyCoord('02h20m30s +57d07m00s', frame='icrs')

# Set the field of view to 60 arcminutes (which is 2/3 degree)
fov = 45 * u.arcmin  # 60 arcminutes field of view

# Download the image using the DSS2 survey from SkyView
image_list = SkyView.get_images(position=coord_center, survey=['DSS2 Red'], width=fov, height=fov)

# Extract data from the returned image list
img_data = image_list[0][0].data

# Ensure image data is a float array for proper inversion
img_data = img_data.astype(float)

# Invert the image data
img_data_inverted = np.max(img_data) - img_data

# Calculate the figure size in inches for 870x570 pixels at 100 DPI
fig_width_inch = 870 / 100  # 8.7 inches
fig_height_inch = 570 / 100  # 5.7 inches

# Create the figure with the specified size
fig, ax = plt.subplots(figsize=(fig_width_inch, fig_height_inch))

# Show the inverted image data and set extent to match image dimensions
im = ax.imshow(
    img_data_inverted,
    cmap='gray',
    origin='lower',
    vmin=0,
    vmax=np.max(img_data_inverted),
    extent=[0, img_data.shape[1], 0, img_data.shape[0]]
)

# Generate ticks for RA and Dec
x_ticks = ax.get_xticks()
y_ticks = ax.get_yticks()

# Estimate RA/Dec ranges for display based on central coordinate and field of view
ra_center = coord_center.ra.deg
dec_center = coord_center.dec.deg

# Convert pixel coordinates to world coordinates assuming linear distribution
ra_values = ra_center + ((x_ticks - img_data.shape[1] / 2) * (fov.to(u.deg).value / img_data.shape[1]))
dec_values = dec_center + ((y_ticks - img_data.shape[0] / 2) * (fov.to(u.deg).value / img_data.shape[0]))

# Custom function to format RA and Dec labels
def format_ra_label(ra):
    angle = Angle(ra, unit='deg')
    h, m, s = angle.to_string(unit=u.hour, sep=':', precision=2).split(':')
    return f"{h}h {m}m"

def format_dec_label(dec):
    angle = Angle(dec, unit='deg')
    d, m, s = angle.to_string(unit=u.deg, sep=':', precision=2).split(':')
    return f"{d}° {m}'"

# Apply formatted RA and Dec labels
ra_labels = [format_ra_label(ra) for ra in ra_values]
dec_labels = [format_dec_label(dec) for dec in dec_values]

# Apply custom tick labels
ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)
ax.set_xticklabels(ra_labels)
ax.set_yticklabels(dec_labels)

plt.xlabel('RA (J2000)')
plt.ylabel('Dec (J2000)')
plt.title('NGC 884 and NGC 869')

# Adjust plot limits to fit the image perfectly
ax.set_xlim(0, img_data.shape[1])
ax.set_ylim(0, img_data.shape[0])

# Remove any extra space around the image
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Add North (N) and East (E) directional labels
ax.text(0.05, 0.94, 'N', color='black', fontsize=14, transform=ax.transAxes)
ax.text(0.1, 0.88, 'E', color='black', fontsize=14, transform=ax.transAxes)

# Add arrows for North and East directions
ax.arrow(0.05, 0.85, 0, 0.05, transform=ax.transAxes, color='black', head_width=0.02)
ax.arrow(0.05, 0.85, 0.05, 0, transform=ax.transAxes, color='black', head_width=0.02)

# Add FOV label on the right side of the image, opposite to the North-East labels
ax.text(0.95, 0.91, "(50' x 50')", color='black', fontsize=14, transform=ax.transAxes, ha='right')

# Save the figure with the desired resolution
plt.savefig('ngc_884_869_image.png', dpi=100, bbox_inches='tight', pad_inches=0)

plt.show()