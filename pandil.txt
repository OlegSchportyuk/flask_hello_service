docker exec -it <CONTAINER ID> bash

docker exec -it <CONTAINER ID> python train_model.py

curl -X POST -H "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,7"}' \
  http://localhost:5000/iris_post

curl.exe -X POST -H "content-type: application/json" -d "{ \"flower\": \"1,2,3,7\" }" http://localhost:5000/iris_post  