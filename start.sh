docker run -it \
            -v  $(pwd | sed 's/^\/mnt//')/src:/usr/src/app \
            -v  $(pwd | sed 's/^\/mnt//')/json:/usr/src/app/json \
            -w /usr/src/app \
            python:latest bash 