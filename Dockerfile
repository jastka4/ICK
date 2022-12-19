# TODO - add multistage Docker build
FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

ADD ./ /code/
WORKDIR /code

RUN pip install cmake
RUN pip install dlib
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

CMD ["flask", "run", "--host", "0.0.0.0"]
