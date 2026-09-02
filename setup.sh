#!/usr/bin/bash

export AST_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source $AST_HOME/.venv/bin/activate
alias asteroid="$AST_HOME/bin/asteroid.sh"
