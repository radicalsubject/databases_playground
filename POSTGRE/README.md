## microservices 
N.B. for .sh files is critical to switch from CRLF to LF

to clean up all containers before building project de novo:
```
docker system prune -a
```
build and run project with docker-compose:
```
docker-compose up --build
```


## old readme
build cgrdb container:
```
docker build -t cgrdb .
```

to run your container next command should be used:
instead 'E:\learn' paste path to POSTGRE folder
```
docker run -it --rm -v E:\learn\POSTGRE\third_folder:/home -p 8888:8888 cgrdb
```
--rm removes volumes and containers after it exits
also may be run as an option for docker-compose containers 
```
--rm
``` 
---> Removes containers after run. Ignored in detached mode.

to set up cgrdb in container 
```
bash /my_script/file.sh
```

for jupyter-notebook running in docker-container
```
jupyter notebook --ip=0.0.0.0 --allow-root
```
in folder 'home' you can find notebooks and data files