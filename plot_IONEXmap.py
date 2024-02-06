import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
def plot_IONEXmap_at_T(TEC_map, lonarray, latarray, time):
  from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
  from matplotlib import ticker

  TEC_at_T = TEC_map.loc[time]

  fig = plt.figure(figsize=[6,10])
  to_proj = ccrs.PlateCarree()
  from_proj = ccrs.PlateCarree()

  lonLabels = np.arange(-180, 180, 60)
  latLabels = np.arange(-90, 90, 30)

  ax = plt.subplot(projection=to_proj)
  ax.coastlines()
  ax.set_global()

  lon, lat = np.meshgrid(lonarray, latarray)
  # Create the plot
  plt.pcolormesh(lon, lat, TEC_at_T, shading='auto')
  # 1. Maps the gridlines to the variable gl
  gl = ax.gridlines(crs=to_proj, draw_labels=True)
  # 2. Adds two attributes to gl, which are xlocator and ylocator
  gl.xlocator = ticker.FixedLocator(lonLabels)
  gl.ylocator = ticker.FixedLocator(latLabels)

  # 3. Changes labels to show degrees North/South and East/West
  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER

  # 4. Removed labels from top and right side
  gl.xlabels_top = False
  gl.ylabels_right = False
  plt.colorbar(label='TEC [TECu]')
  plt.show()
