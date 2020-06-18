if (command -v pip3 > /dev/null 2>&1); then
    echo "pip3 found. Installing dependencies."
    pip3 install pymunk
    pip3 install pyglet
else
    echo "pip3 not found, resorting to pip"
    pip install pymunk
    pip install pyglet
fi

if (command -v python3 > /dev/null 2>&1); then
    echo "python3 found. Running game."
    python3 lander.py
else
    echo "python3 not found, resorting to python"
    python lander.py
fi