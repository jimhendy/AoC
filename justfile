# Get current year and zero-padded day
year := `date +%Y`
day := `date +%d`

_default:
    @just --list

_format:
    uv run ruff format

_lint:
    -@uv run ruff check --select ALL --fix > /dev/null 2>&1
    uv run ruff check --fix

# Run both formatter and linter
ruff:
    just _format
    just _lint

# Create template files for a new year
new_year:
    uv run new_year.py 

# Run part a of the puzzle for the current day
a *args:
    uv run main.py {{year}}/{{day}}/a.py {{args}}

# Run part b of the puzzle for the current day
b *args:
    uv run main.py {{year}}/{{day}}/b.py {{args}}
