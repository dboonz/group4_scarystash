#!/bin/bash
echo "To set up the path properly: "
echo "1. Clone pelita in a folder called /home/student/pelita_tournament"
echo "2. Clone group4_scarystash from the same folder, so: "
echo "cd /home/student/pelita_tournament"
echo "git clone git@github.com:dboonz/group4_scarystash.git"
echo "git clone   git clone git://github.com/ASPP/pelita.git"
echo "group4_scarystash/setup_path.sh"

echo "export PYTHONPATH=\$PYTHONPATH:/home/student/pelita_tournament/pelita" >> ~/.bashrc
