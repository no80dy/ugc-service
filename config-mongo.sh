#!/usr/bin/env bash

docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh'

docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.status()" | mongosh'

docker exec -it mongors1n1 bash -c 'echo "use moviesDb" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"moviesDb\")" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"moviesDb.movies\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"moviesDb.movies\", {\"_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"moviesDb.users\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"moviesDb.users\", {\"_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"moviesDb.bookmarks\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"moviesDb.bookmarks\", {\"_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"moviesDb.likes\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"moviesDb.likes\", {\"_id\": \"hashed\"})" | mongosh'

docker exec -it mongos1 bash -c 'echo "db.createCollection(\"moviesDb.reviews\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"moviesDb.reviews\", {\"_id\": \"hashed\"})" | mongosh'
