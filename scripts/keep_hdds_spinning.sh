#!/usr/bin/env bash

find $1 -mindepth 1 -maxdepth 1 -type d | xargs -I {} ^C -c 'date > {}/.chia-manager-keep_hdd_spinning'