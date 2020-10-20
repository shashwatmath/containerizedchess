# containerizedchess
The project is designed to use Flask (Python) as front-end and Cassandra (with 4 nodes - dc 1: rack 1/2 and dc2: rack1/2). 

The front-end is a dummy Chess app (work in progress) which creates new game every time on click on <i>New Game</i> and lists all games with their UUIDs, on click of <i>Load Games</i>.

<b><u>How to Use:</u></b>
1. Pull the code. Exctract it to a folder.
2. Execute docker-compose up -d from command prompt / shell

   It will take couple of moments to run all the containers. In case any of the containers fail to run, execute them manually using docker run <containerid> (you can get containerid using docker ps -a)
3. Once all containers are up, go to your favourite browser and run using: http://localhost:5000
