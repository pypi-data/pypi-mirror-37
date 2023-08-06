# Igni

Igni is a simple client for [gitignore.io](http://gitignore.io) that uses the `/list` endpoint
to generate completions for your shell.  Output is printed directly to stdout. 

# Usage

Generate a `.gitignore` file

    igni python venv > .gitignore

Generate completions for bash

    igni bash-completion > igni-completion.bash
    source igni-completion.bash

Generate completions for fish
    
    igni fish-completion > igni-completion.fish
    mkdir -p ~/.config/fish/completions
    mv igni-completions ~/.config/fish/completions
