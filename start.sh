docker run -it \
            -v  $(pwd | sed 's/^\/mnt//')/src:/usr/src/app \
            -w /usr/src/app \
            python:latest bash 