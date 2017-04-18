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
import json
import glob
import requests
import shutil
import datetime
import subprocess
from time import sleep
from mapbox import Uploader


MAPBOX_STYLESAPI_URL = "https://api.mapbox.com/styles/v1/"


def prepDestFolder(dest_folder):
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    os.mkdir(dest_folder)
    
def createVectorTiles(layername, filepath, out_folder, zoom_min=0, zoom_max=12):

    mvt_creation = ["tippecanoe", "-o", os.path.join(out_folder,"{0}.mbtiles".format(layername)),
        "-q", "-Z", str(zoom_min), "-z", str(zoom_max), '{0}'.format(filepath)]
    
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


def cleanMVTStyle(styles_json, props):
    print("Cleaning MVT Style...")
    for pr in props:
        if pr in styles_json.keys():
            styles_json.pop(pr)


def checkMVTStyle(user, style_id):
    
    print("Checking if MVT Style exists...")
    
    url = "{0}{1}/{2}".format(MAPBOX_STYLESAPI_URL, user, style_id)

    headers = {}
    
    querystring = {"access_token": os.environ['MAPBOX_ACCESS_TOKEN']}

    resp = requests.request("GET", url, headers=headers, params=querystring, timeout=10)

    if resp.status_code != requests.codes.ok:
        if resp.json()['message'] == 'Style not found':
            return True
        else:
            resp.raise_for_status()
    
    return False


def createMVTStyle(user, style_path):
    
    with open(style_path, 'r') as style_data:
        json_data = json.load(style_data)
        
    if checkMVTStyle(user, json_data['id']):
        print('This MVT Style ({0}) already exists...'.format(json_data['id']))
        return
    
    url = "{0}{1}".format(MAPBOX_STYLESAPI_URL, user)
    
    cleanMVTStyle(json_data, [
        "created", "id", "modified", "owner", "draft"
        ])
    
    print("Creating new MVT style...")
    
    payload = json.dumps(json_data)
    
    headers = {'content-type': "application/json"}
    
    querystring = {"access_token": os.environ['MAPBOX_ACCESS_TOKEN']}

    resp = requests.request("POST", url, headers=headers, params=querystring, 
        data=payload, timeout=10)

    if resp.status_code != requests.codes.ok:
        resp.raise_for_status()
    
    print("MVT Styles created...")


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
    
    try:
    
        in_folder = sys.argv[1]
        out_folder = sys.argv[2]
        
        if len(sys.argv) > 3:
            mapbox_user = sys.argv[3]
            style_path = sys.argv[4]
            
            createMVTStyle(mapbox_user, style_path)
        
        layernames = glob.glob(os.path.join(in_folder,'*.geojson'))
        
        prepDestFolder(out_folder)
        
        for ly in layernames:
            sleep(1)
            # tdy = datetime.datetime.today().strftime('%Y%m%d')
            # mvt_name = "{0}_{1}".format(os.path.splitext(os.path.basename(ly))[0], tdy)
            mvt_name = os.path.splitext(os.path.basename(ly))[0]

            createVectorTiles(mvt_name, ly, out_folder, zoom_min=2, zoom_max=10)
            
            uploadToMapbox(mvt_name, os.path.join(out_folder, "{0}.mbtiles".format(mvt_name)))
    
    except Exception as err:
        print("Error: {0}".format(err))


if __name__ == '__main__':
    run()