
IN_FOLDER="/media/cayetano/Data/documentos/cayetano/gdrive/Geographica/Proyectos/IUCN MED/operaciones/geojson_data"
OUT_FOLDER="/tmp/mvt_data/"

if [ -z ${MAPBOX_ACCESS_TOKENDD+x} ];
then 
  echo "MAPBOX_ACCESS_TOKEN is unset. Exiting...";
  exit 1;
else 
  echo "MAPBOX_ACCESS_TOKEN is set";
fi

python3 createandupload_mvt.py "$IN_FOLDER" "$OUT_FOLDER"