import os
import sys

from pathspec import PathSpec

from reloadex.reloader_argparsing import get_parser
from reloadex.common.utils_reloader import LaunchParams

DEFAULT_RELOADIGNORE = """
# Ignore everything ..
*
*/

# .. except *.py files
!*.py
"""


class Reloader:
    def __init__(self, platform_reloader, working_directory, argparse_args):
        self.platform_reloader = platform_reloader
        self.launch_params = LaunchParams(
            working_directory=working_directory,
            argparse_args=argparse_args,
            file_triggers_reload_fn=self.file_triggers_reload
        )

        self.spec = None
        self.reload_reloadignore()

    def start(self):
        self.platform_reloader.main(self.launch_params)

    def file_triggers_reload(self, filename_bytes):
        filename_str = filename_bytes.decode(sys.getfilesystemencoding())

        rel_filename = os.path.relpath(filename_str, self.launch_params.working_directory)
        if rel_filename == '.reloadignore':
            self.reload_reloadignore()

        triggers_reload = not self.spec.match_file(rel_filename)
        return triggers_reload

    def reload_reloadignore(self):
        try:
            # have to specify full path here, otherwise file is not found
            with open(self.launch_params.working_directory + '/.reloadignore', 'r') as fh:
                self.spec = PathSpec.from_lines('gitwildmatch', fh)
        except IOError as e:
            if e.errno == 2:
                # may happen if file is deleted and inotifyevent is triggered for that
                # print("'.reloadignore' not found. Using default spec.")
                self.spec = PathSpec.from_lines('gitwildmatch', DEFAULT_RELOADIGNORE.splitlines())
            else:
                raise


def parse_args():
    parser = get_parser()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    argparse_args = parser.parse_args()

    working_directory = os.getcwd()
    return working_directory, argparse_args


def main():
    if sys.platform.startswith("linux"):
        from reloadex.linux import reloader_linux
        platform_reloader = reloader_linux
    elif sys.platform.startswith("win32"):
        from reloadex.windows import reloader_windows
        platform_reloader = reloader_windows
    else:
        raise NotImplementedError("unsupported platform: %s" % sys.platform)

    working_directory, argparse_args = parse_args()
    reloader = Reloader(platform_reloader=platform_reloader, working_directory=working_directory, argparse_args=argparse_args)
    reloader.start()


if __name__ == "__main__":
    main()