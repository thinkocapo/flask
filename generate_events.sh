#!/bin/bash

run_curl () {
 for ((i=0; i<=((RANDOM % 10)); i++))
 do
  curl "$@";
 done
}

NAME=flask
RANDOM_STRING=`openssl rand -base64 8`

run_curl https://will-flask-demo.herokuapp.com/handled
run_curl https://will-flask-demo.herokuapp.com/unhandled
run_curl -X POST https://will-flask-demo.herokuapp.com/checkout -H "Content-Type: application/json" -H "X-Session-ID: _${RANDOM_STRING}" -H "X-Transaction-ID: _${RANDOM_STRING}" -d "{\"email\":\"$X@yahoo.com\", \"cart\":[{\"id\":\"wrench\", \"name\":\"Wrench\", \"price\":500}]}"