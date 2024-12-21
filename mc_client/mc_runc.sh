#!/bin/bash

mc alias set $ALIAS http://$MINIO_HOST:$MINIO_PORT $MINIO_ACCESS_KEY $MINIO_SECRET_KEY &&
mc admin user add $ALIAS $USER $PASSWORD
mc mb $ALIAS/$BUCKET
mc quota set $ALIAS/$BUCKET $QUOTA
mc admin policy attach $ALIAS readwrite --user=$USER
