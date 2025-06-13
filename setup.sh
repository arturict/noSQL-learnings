#!/bin/bash

export MONGODB_URI='mongodb://192.168.1.157:27017/'

echo "MongoDB M165 Project Setup"
echo "=========================="
echo "Environment variable MONGODB_URI has been set"
echo "Available applications:"
echo ""
echo "1. python environment_demo.py     - Environment variables demo"
echo "2. python database_explorer.py    - Database browser"
echo "3. python restaurant_crud.py      - Restaurant operations"
echo "4. python power_monitor.py        - System monitoring"
echo "5. python power_grapher.py        - Monitoring graphs (saves PNG files)"
echo ""
echo "To make environment variable persistent, add this to ~/.bashrc or ~/.zshrc:"
echo "export MONGODB_URI='mongodb://192.168.1.157:27017/'"
echo ""

read -p "Start an application? (1-5 or n): " choice

case $choice in
    1) python environment_demo.py ;;
    2) python database_explorer.py ;;
    3) python restaurant_crud.py ;;
    4) python power_monitor.py ;;
    5) python power_grapher.py ;;
    *) echo "Setup complete!" ;;
esac
