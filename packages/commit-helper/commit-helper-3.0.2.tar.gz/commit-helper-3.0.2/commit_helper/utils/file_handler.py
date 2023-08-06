from yaml import safe_load
from yaml import YAMLError
from os import system
# utils imports
from .utils import create_file
from .utils import debug
from .utils import get_text
from .utils import get_context
from .utils import gen_co_author
# conventions imports
from commit_helper.conventions.karma_angular import angular_convention
from commit_helper.conventions.changelog import changelog_convention
from commit_helper.conventions.symphony_cmf import symphony_convention
from commit_helper.conventions.no_convention import just_message


def handle_file_based_commit(file_path, debug_mode, args):
    with open(str(file_path), 'r') as stream:
        try:
            config = safe_load(stream)
            debug('convention from file', config['convention'], debug_mode)
            if config['convention'] is not None:
                convention = str(config['convention']).lower()
            else:
                convention = 'none'

            if convention == 'none':
                print('You are not using a convention')
                commit_message = just_message()

            else:
                print('You are using the %s convention' % convention)
                tag, msg = get_text()
                if convention == 'angular' or convention == 'karma':
                    context = get_context()
                    commit_message = angular_convention(tag, msg, context)
                elif convention == 'changelog':
                    commit_message = changelog_convention(tag, msg)
                elif convention == 'symphony':
                    commit_message = symphony_convention(tag, msg)

            commit_message += gen_co_author(args.co_author)
            debug('commit message', commit_message, debug_mode)
            system('git commit -m "%s"' % commit_message)

        except YAMLError as err:
            print(err)
