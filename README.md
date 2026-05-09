# note_app

A small TUI note-taking application built as a learning project for the
[Textual](https://textual.textualize.io/) framework.

The goal of the project is educational: explore Textual screens, widgets,
styling, and reactive state by building a working notes/folders interface
rather than reading docs in isolation.

## Features

- Browse notes organized into folders
- Markdown rendering for note content
- Domain / repository / screen layout to keep concerns separated
- Configurable data directory

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/)

## Installation

```bash
poetry install
```

## Usage

Run the app with the default data directory:

```bash
poetry run app
```

Or pass a custom path where notes should be stored:

```bash
poetry run app /path/to/notes
```

## Development

Lint the code with Ruff:

```bash
poetry run lint
```

## Project structure

```text
note_app/
    app.py            # Textual App entry point
    cli.py            # CLI launcher
    config/           # App settings
    domain/           # Note and Folder models
    repositories/    # Persistence layer
    screens/          # Textual screens
    widgets/          # Custom widgets
```
# textual-demo-app
