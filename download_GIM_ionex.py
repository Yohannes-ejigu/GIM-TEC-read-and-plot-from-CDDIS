import sys
import wget
import subprocess
import os
import time as systime
import string
import numpy as np
import pandas as pd

import subprocess

def download_IONEX(yr, day, center, username, psw):
    "Before using this function, you need to have an account (user name and pasword from EARTHDATA LOGIN!"
    try:
        ionex_Zip_type2 = '{}g{:03}0.{:02}i.Z'.format(center.lower(), day, yr % 100)
        ionex_Zip_type3_options = [
            '{}0OPSFIN_{:04}{:03}0000_01D_01H_GIM.INX.gz'.format(center.upper(), yr, day),
            '{}0OPSRAP_{:04}{:03}0000_01D_01H_GIM.INX.gz'.format(center.upper(), yr, day),
            '{}0OPSULT_{:04}{:03}0000_01D_01H_GIM.INX.gz'.format(center.upper(), yr, day)
        ]

        # Try downloading and uncompressing type 2
        url_type2 = 'https://cddis.nasa.gov/archive/gps/products/ionex/{:04}/{:03}/{}'.format(yr, day, ionex_Zip_type2)
        subprocess.run(['wget', '--auth-no-challenge', '--user', username, '--password', psw, url_type2], check=True)
        print(f"Download successful. File saved as {ionex_Zip_type2}")
        subprocess.run(['uncompress', ionex_Zip_type2], check=True)
        return

    except subprocess.CalledProcessError as e_type2:
        print(f"Error downloading {ionex_Zip_type2}. Error: {e_type2}")

        # If type 2 download fails, try type 3 options
        for ionex_Zip_type3 in ionex_Zip_type3_options[1:]:
            try:
                url_type3 = 'https://cddis.nasa.gov/archive/gps/products/ionex/{:04}/{:03}/{}'.format(yr, day, ionex_Zip_type3)
                subprocess.run(['wget', '--auth-no-challenge', '--user', username, '--password', psw, url_type3], check=True)
                print(f"Download successful. File saved as {ionex_Zip_type3}")
                subprocess.run(['uncompress', ionex_Zip_type3], check=True)
                return
            except subprocess.CalledProcessError as e_type3:
                print(f"Error downloading {ionex_Zip_type3}. Error: {e_type3}")
        
        # If all options fail, try the default option
        try:
            url_type3_default = 'https://cddis.nasa.gov/archive/gps/products/ionex/{:04}/{:03}/{}'.format(yr, day, ionex_Zip_type3_options[0])
            subprocess.run(['wget', '--auth-no-challenge', '--user', username, '--password', psw, url_type3_default], check=True)
            print(f"Default Download successful. File saved as {ionex_Zip_type3_options[0]}")
            subprocess.run(['uncompress', ionex_Zip_type3_options[0]], check=True)
            return
        except subprocess.CalledProcessError as e_default:
            print(f"Error downloading default {ionex_Zip_type3_options[0]}. Error: {e_default}")
        
        print("Error downloading all file types.")

# Example usage:
# download_IONEX(2023, 150, "example_center", "your_username", "your_password")


