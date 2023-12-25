Django project of a web app for listing and adding new books. Created for testing response time using load-balancer and 2 , 5 and 15 server replicas.


To run this project i recommand using linux operationg system:

Create a folder on your device where you will open the terminal. In the terminal run the following command:

```bash
git clone https://github.com/DinoLadavac/ResponseTimeTesting.git
```

After the repository is done cloning. Please enter the following command to enter the main directory:

```bash
cd ipvo
```

To start up the server please choose one of the recommended docker-compose.yml and nginx.conf files. The default is set for 15 replicas of web server. You can choose the already created files for 2 replicas or 5 replicas (the name of the file is docker-compose(2 balancers).yml)

After that, all you need to do is run

```bash
docker-compose up --build
```

And visit:

```bash
http://127.0.0.1:8080/books
```


If you want to test the web application with load, you will need to install the recommended tools:

```bash
sudo apt-get update
sudo apt-get apache2-utils
```

You will maybe need to restart your device after this command.

Run the server in one terminal and test the load in other using command:

```bash
ab -n 20000 -c 10 -k -r -l -p post-data.txt http://127.0.0.1:8080/add_book/
```
