#!/bin/bash

wrk -t8 -c20 -d30s -s post.lua http://127.0.0.1:38094/async/copying_type
