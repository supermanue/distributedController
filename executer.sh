#!/bin/sh
set -x

echo "antes de ejecutar hay"
ls

echo "cambio los permisos del ejecutable"
chmod +x $1

echo "ejecuto la aplicacion"

./$@


echo "despues de ejecutar hay"
ls

echo "goodbye friendo"
