def get_parser(parser, specs):
    """TODO: Docstring for get_parser.

    :parser: TODO
    :specs: TODO
    :returns: TODO

    """
    for key in specs:
        parser.add_argument('--' + key, specs[key]['help'])
