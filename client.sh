#!/usr/bin/env bash
trap 'killall' INT

killall() {
    trap '' INT TERM
    echo "**** Shutting down... ****"
    kill -TERM 0
    wait
    echo DONE
}

(cd UI/front-end/ && yarn start)
