import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
def plot_IONEXmap_at_T(TEC_map, lonarray, latarray, times, label):
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
    from matplotlib import ticker
    lonLabels = np.arange(-180, 180, 60)
    latLabels = np.arange(-90, 90, 30)

    if len(times) == 1:
        fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'projection': ccrs.PlateCarree()})
        axs = [ax]
    else:
        num_times = len(times)
        num_rows = (num_times + 2) // 3  # Adjust number of rows based on the number of times
        num_cols = 2 if num_times <= 4 else 3  # Set number of columns based on the number of times
        Npanel = num_cols*num_rows
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(8, 2*num_rows), subplot_kw={'projection': ccrs.PlateCarree()}, sharex=True, sharey=True)
        axs = axs.flatten()

    cbar_width = 0.03
    cbar_pad = 0.03

    cbar_ax = fig.add_axes([1.01, 0.15, cbar_width, 0.7])  # position of the colorbar axes

    for idx, time in enumerate(times):
        if len(times) == 1:
            ax = axs[0]
        else:
            if idx >= len(axs):  # Check if we have more times than subplots
                break
            ax = axs[idx]

        TEC_at_T = TEC_map.loc[time]

        ax.coastlines()
        ax.set_global()

        lon, lat = np.meshgrid(lonarray, latarray)
        # Create the plot
        im = ax.pcolormesh(lon, lat, TEC_at_T, shading='auto', transform=ccrs.PlateCarree())
        # Maps the gridlines to the variable gl
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
        # Adds two attributes to gl, which are xlocator and ylocator
        gl.xlocator = ticker.FixedLocator(lonLabels)
        gl.ylocator = ticker.FixedLocator(latLabels)
        # Changes labels to show degrees North/South and East/West
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        # Removed labels from top and right side
        gl.xlabels_top = False
        gl.ylabels_right = False
        if len(times) != 1 and Npanel-idx > num_cols :
          gl.xlabels_bottom = False
        gl.ylabels_left = True if idx%num_cols == 0 else False
        formatted_time = f'{time:02d}:00'  # Assuming time is in hours, add :00 for minutes
        ax.set_title(f'TEC at Time: {formatted_time}')

    # Ensure that all subplots share the same x and y axes
    for ax in axs:
        ax.set_aspect('auto')  # Setting aspect to auto ensures that the map projection is not distorted

    # Add colorbar
    cbar = plt.colorbar(im, cax=cbar_ax, orientation='vertical', pad=cbar_pad, shrink=0.1)
    cbar.set_label(label)  # Add label to the colorbar

    plt.tight_layout(pad=0.1,w_pad=0.0)
    plt.show()
