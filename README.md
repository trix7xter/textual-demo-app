# note_app

A small TUI note-taking application built as a learning project for the
[Textual](https://textual.textualize.io/) framework.

The goal of the project is educational: explore Textual screens, widgets,
styling, and reactive state by building a working notes/folders interface
rather than reading docs in isolation.

## Features

- Browse notes organized into folders via a tree widget
- Markdown rendering for note content
- Layered architecture: domain models, repositories, screens, widgets
- Filesystem-backed repositories with base-path sandboxing (no access
  outside the configured data directory)
- Configurable data directory passed through `AppSettings`

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
    config/           # App settings (AppSettings)
    domain/           # Note and Folder dataclasses
    repositories/     # Abstract bases + filesystem implementations
        base_folder_repository.py
        base_note_repository.py
        folder_repository.py
        note_repository.py
    screens/          # Textual screens (MainScreen)
    widgets/          # Custom widgets (FileTreeWidget, NoteViewWidget)
```

## Architecture notes

- `domain/` holds plain dataclasses (`Note`, `Folder`) with `Path`-typed
  locations.
- `repositories/` defines abstract interfaces (`BaseFolderRepository`,
  `BaseNoteRepository`) and filesystem implementations. All path
  operations are validated against the configured base path.
- Screens receive `AppSettings` and instantiate the repositories they
  need, then inject them into widgets — widgets depend on the abstract
  base, not the concrete implementation.
