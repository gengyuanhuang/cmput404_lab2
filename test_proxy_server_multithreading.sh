#!/bin/sh

END=100
for i in $(seq 1 $END)
do
    python proxy_client.py
done