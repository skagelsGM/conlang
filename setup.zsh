#!/bin/zsh
function setup_log() {
    echo "\n[setup] $@"
}

setup_log "Loading aliases... " && source ./aliases
setup_log "Setting up Python virtual environment..." && conlang-venv-create
setup_log "Activating virtual environment... " && conlang-venv-activate
setup_log "[venv config]\n$(cat .venv-py313/pyvenv.cfg)"
setup_log "Setting PYTHONPATH: " && conlang-setenv && echo $PYTHONPATH
setup_log "pytest location: $(which pytest)"
setup_log "[aliases] " && alias | grep -e 'conlang\|wordgen'