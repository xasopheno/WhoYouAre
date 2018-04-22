#!/usr/bin/env bash
trap 'killall' INT

killall() {
    trap '' INT TERM
    echo "**** Shutting down... ****"
    kill -TERM 0
    wait
    echo DONE
}

python3 ./UI/server/server.py;
