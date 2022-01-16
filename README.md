# Python bot

This is an app Python bot

### Usage

```shell
docker build --rm -f docker/Dockerfile -t pybot:latest .
docker run -v $(pwd)/src:/app pybot:latest
```
