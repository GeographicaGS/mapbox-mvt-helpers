#
#  Author: Cayetano Benavent, 2017.
#  https://github.com/GeographicaGS/mapbox-mvt-helpers
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import sys
import os
import glob
import shutil
import datetime
import subprocess
from time import sleep
from mapbox import Uploader


def prepDestFolder(dest_folder):
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    os.mkdir(dest_folder)
    
def createVectorTiles(layername, filepath, out_folder, zoom_min=0, zoom_max=12):

    mvt_creation = ["tippecanoe", "-o", os.path.join(out_folder,"{0}.mbtiles".format(layername)),
        "-Z", str(zoom_min), "-z", str(zoom_max), '{0}'.format(filepath)]
    
    print("Launched MVT creation...")
    out, err = cmdCall(mvt_creation)
    if err:
        print("MVT creation Error: {0}".format(err))
    else:
        print("MVT creation: successfully process! (File: {0})".format(layername))


def uploadToMapbox(layername, filepath):
    """
    """
    try:
        service = Uploader()
        
        print("Uploading data to Mapbox...")

        with open(filepath, 'rb') as src:
            upload_resp = service.upload(src, layername)

        if upload_resp.status_code == 422:
            for i in range(5):
                sleep(5)
                with open(filepath, 'rb') as src:
                    upload_resp = service.upload(src, layername)
                if upload_resp.status_code != 422:
                    break
    
    except Exception as err:
        print("Upload mvt error: {0}".format(err))


def cmdCall(params):
    """
    Launch shell commands
    """
    try:
        cmd_call = subprocess.Popen(params, stderr=subprocess.PIPE)
        out, err = cmd_call.communicate()
        return(out, err)

    except ValueError as err:
        print("Invalid arguments: {0}".format(err))

    except Exception as err:
        print("Shell command error: {0}".format(err))


def run():
    
    in_folder = sys.argv[1]
    out_folder = sys.argv[2]
    layernames = glob.glob(os.path.join(in_folder,'*.geojson'))
    
    prepDestFolder(out_folder)
    
    for ly in layernames:
        tdy = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        mvt_name = "{0}_{1}".format(os.path.splitext(os.path.basename(ly))[0], tdy)

        createVectorTiles(mvt_name, ly, out_folder, zoom_min=2, zoom_max=10)
        
        # uploadToMapbox(mvt_name, os.path.join(out_folder, "{0}.mbtiles".format(mvt_name)))


if __name__ == '__main__':
    run()