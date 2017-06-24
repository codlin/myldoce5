from .config import get_config
from optparse import OptionParser
from ..lexicon.generate import LexiconFactory


def run(argv):
    config = get_config()

    # Parse arguments
    optparser = OptionParser()
    optparser.set_defaults(debug=False)
    optparser.add_option(
        '--debug', action='store_true', help='Enable debug mode')
    (options, args) = optparser.parse_args(argv)


    # Load the configuration file
    config.debug = options.debug
    config.load()

    factory = LexiconFactory()
    factory.run()
    pass