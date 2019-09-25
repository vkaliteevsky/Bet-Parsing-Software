#!/bin/bash

echo "Started."
cd whill/
./getCommands.py
cd ../marathonbet/
./getCommands.py
echo "Finished"