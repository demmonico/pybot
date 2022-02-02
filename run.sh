#!/usr/bin/env bash

read -r -d '' HELP_STRING <<'EOF'
-----------------------------------------------------------
Help information
-----------------------------------------------------------
Bot runner script aimed in help to build/run Docker container with Bot.

FORMAT: <SCRIPT_NAME> <ACTION>

<ACTION> - TF action you want to run:
    - build         - build Docker image based on Dockerfile
    - run           - run Docker container
    - help          - help of this runner

EOF

ACTION="$1"
case "${ACTION}" in
    'build')
        docker build --rm -f docker/Dockerfile -t pybot:latest .
        exit;;
    'talk')
        docker run -ti -v $(pwd)/src:/app pybot:latest
        exit;;
    'debug')
        docker run -ti -v $(pwd)/src:/app pybot:latest "-v"
        exit;;
    'test')
        while read phrase; do
          docker run -v $(pwd)/src:/app pybot:latest "$phrase"
          echo ''
        done < src/test/demo.suite
        exit;;
    'help')
        echo "${HELP_STRING}"
        exit;;
    '')
        echo -e "${RC}Error${NC}: ACTION param is required"
        echo "${HELP_STRING}"
        exit 1;;
esac

