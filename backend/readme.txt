To elevate the docker container:
& 'C:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon

To start the postgres database:
docker run --name online-exam-db -p 5432:5432 -e POSTGRES_DB=online-exam -e POSTGRES_PASSWORD=0NLIN3-ex4m -d postgres