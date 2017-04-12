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

IN_FOLDER="/mygeojsondatafolder"
OUT_FOLDER="/tmp/mvt_data/"

if [ -z ${MAPBOX_ACCESS_TOKEN+x} ];
then 
  echo "MAPBOX_ACCESS_TOKEN is unset. Exiting...";
  exit 1;
else 
  echo "MAPBOX_ACCESS_TOKEN is set";
fi

python3 createandupload_mvt.py "$IN_FOLDER" "$OUT_FOLDER"