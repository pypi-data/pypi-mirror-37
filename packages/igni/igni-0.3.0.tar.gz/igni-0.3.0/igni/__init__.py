import requests

GITIGNORE_API = 'https://www.gitignore.io/api'
GITIGNORE_LIST_SEPERATOR = ','
LIST_REQUEST = 'list'
COMPLETION_SEPERATOR = ' '


def call_gitignore(*arguments):
    comma_deliniated_arguments = ",".join(arguments)
    return requests.get(f'{GITIGNORE_API}/{comma_deliniated_arguments}').text


def list_all():
    return call_gitignore(LIST_REQUEST)


def gitignore_completions():
    return list_all().replace(GITIGNORE_LIST_SEPERATOR, COMPLETION_SEPERATOR) \
                     .replace("\n", COMPLETION_SEPERATOR)


def shell_completions():
    return COMPLETION_SEPERATOR.join(SHELL_COMMANDS.keys())


def wordlist():
    return COMPLETION_SEPERATOR.join([
        LIST_REQUEST,
        gitignore_completions(),
        shell_completions()])


def bash_completion():
    return f'#/usr/bin/env bash\ncomplete -W "{wordlist()}" igni'


def fish_completion():
    return f'complete -c igni -a "{wordlist()}"'


SHELL_COMMANDS = {"bash-completion": bash_completion,
            "fish-completion": fish_completion}


def run(system_argv):
    if system_argv[1] in SHELL_COMMANDS:
        return SHELL_COMMANDS[system_argv[1]]()
    else:
        return call_gitignore(*system_argv[1:])
