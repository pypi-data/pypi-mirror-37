"""
    askelerator.actions

    Functions processed during files and folder deployment
"""
import sys

def get_input(specs, item):
    """Ask user for input

    :specs: specification dictionnary
    :item: item to be processed in spec file
    :returns: result as a string

    """
    res = input(specs[item]["action"]["question"])
    return res

def upperize(specs, item):
    """Upperize a string

    :specs: specification dictionnary
    :item: item to be processed in spec file
    :returns: result as a string

    """
    if specs[item]["action"]["target"] in specs:
        if 'output' in specs[specs[item]["action"]["target"]]:
            res = specs[specs[item]["action"]["target"]]["output"].upper()
        else:
            print('ERROR: ' + specs[specs[item]["action"]["target"]]["output"] +
                  ' does not exists yet.\n'
                  'Check askelerator.json or template consistency.\n'
                  '(Maybe inputs are AFTER upperize...')
            sys.exit(1)
    else:
        print('ERROR: Key ' + specs[item]['action']['target'] + 'does not exists.'
              'Check askelerator.json or template consistency.\n')
        sys.exit(1)
    return res
