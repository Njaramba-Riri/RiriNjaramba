FROM python:3.9.11

#set working directory
WORKDIR /app

#Copy local contents into the container.
ADD . /app

#Upgrade pip and Install all dependancies
RUN python -m pip install pip --upgrade &&\
    pip install -r requirements.txt

#Make port 5000 available to the world outside of this container.
EXPOSE 5000

#Run main.py when when the container launches
CMD ["python", "main.py"]

#Got permission denied while trying to connect to the Docker daemon socket at unix