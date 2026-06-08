set shell := ["bash", "-cu"]

# Launch the interactive Dev Portal and Control Tower
task-web:
    @python3 ../_taskmaster/server.py

# Launch the Update Builder v2 (Vite)
run-update-builder:
    cd update-builder-v2 && npm run dev

# Generate a poster agentically from a natural language prompt or arguments
make-poster *args:
    .venv/bin/python3 scripts/make_poster.py {{args}}
