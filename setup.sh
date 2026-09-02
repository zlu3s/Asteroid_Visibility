#!/usr/bin/bash

export AST_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "${AST_HOME}/.venv" ]; then
    echo "Setting up Virtual Environment"
    python3 -m venv "${AST_HOME}/.venv"
    source "${AST_HOME}/.venv/bin/activate"

    python3 -m pip install --upgrade "pip<26" "pip-tools==7.6.0"
    echo "Installing packages"
    pip-compile "${AST_HOME}/requirements.in"
    pip install -r "${AST_HOME}/requirements.txt"
    pip install --upgrade pip
    rm "${AST_HOME}/requirements.txt"
    echo "Setup Complete"
else
    source "${AST_HOME}/.venv/bin/activate"
fi

source $AST_HOME/.venv/bin/activate
alias asteroid="$AST_HOME/bin/asteroid.sh"
