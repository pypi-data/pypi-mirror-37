"""
Generator class
"""

import sys
import os
import re
import json

from . import actions

class Generator():

    """A skeleton generator"""

    def prepare_specs(self):
        """Ask user for questions and compile regexp for further use"""
        for occ in self.specs:
            rgx = re.compile(self.specs[occ]["regexp"])
            self.specs[occ]["regexp"] = rgx
            if self.specs[occ]["action"]["type"] == 'input':
                self.specs[occ]["output"] = actions.get_input(self.specs, occ)
            elif self.specs[occ]["action"]["type"] == 'upperize':
                self.specs[occ]["output"] = actions.upperize(self.specs, occ)
            else:
                print("ERROR: Invalid action type for " + occ)
                sys.exit(1)


    def substitute(self, string):
        """Apply all substitutions to a target string

        :string: target string
        :returns: processed string

        """
        for rgx in self.specs:
            string = re.sub(self.specs[rgx]["regexp"], self.specs[rgx]["output"], string)
        return string


    def list_files(self, source_dir=None, target_dir=None):
        """Prepare two dictionnaries, one for directoy matching, the other for files"""
        if source_dir is None:
            source_dir = self.source_path
        if target_dir is None:
            target_dir = self.target_path

        for file_name in os.listdir(source_dir):
            if os.path.isdir(source_dir + '/' + file_name):
                target_name = self.substitute(file_name)
                self.source_to_target_dirs.update(
                    {source_dir + '/' + file_name: target_dir + '/' + target_name})
                self.list_files(source_dir + '/' + file_name, target_dir + '/' + target_name)
            elif os.path.isfile(source_dir + '/' + file_name):
                target_name = self.substitute(file_name)
                self.source_to_target_files.update(
                    {source_dir + '/' + file_name: target_dir + '/' + target_name})


    def check_files(self):
        """Check for no collisions in target skeleton"""
        for key in self.source_to_target_files:
            if os.path.lexists(self.source_to_target_files[key]):
                user_says = input(self.source_to_target_files[key] + ' already exists. '
                    '(O)verwrite, (A)bort ?')
                # TODO Enhance machine understanding ('o', 'Over', 'overwrite'...)
                if user_says != 'O':
                    print('Aborting...')
                    sys.exit(1)

        for key in self.source_to_target_dirs:
            if os.path.lexists(self.source_to_target_dirs[key]):
                if not os.path.isdir(self.source_to_target_dirs[key]):
                    user_says = input(self.source_to_target_dirs[key] + ' already exists '
                        'and is NOT a directory. (O)verwrite, (A)bort ?')
                    # TODO Enhance machine understanding ('o', 'Over', 'overwrite'...)
                    if user_says != 'O':
                        print('Aborting...')
                        sys.exit(1)


    def build_skel(self):
        """Build skeleton from template to taget"""
        for directory in self.source_to_target_dirs:
            if not os.path.lexists(self.source_to_target_dirs[directory]):
                os.makedirs(self.source_to_target_dirs[directory])
            else:
                if not os.path.isdir(self.source_to_target_dirs[directory]):
                    os.remove(self.source_to_target_dirs[directory])
                    os.makedirs(self.source_to_target_dirs[directory])

        for file in self.source_to_target_files:
            if not os.path.lexists(self.source_to_target_files[file]):
                buf = open(file, 'r')
                content = buf.read()
                buf.close()
                content = self.substitute(content)
                fout = open(self.source_to_target_files[file], 'w')
                fout.write(self.substitute(content))
                fout.close()


    def __init__(self, source, target_path):
        """Read json file from template

        :source: template location
        :target_path: target directory
        """
        self.target_path = target_path
        self.source_to_target_dirs = {}
        self.source_to_target_files = {}

        #TODO Ability to use full-pathed template
        print('Gerenator dreated')
        with open(source + '/askelerator.json') as json_data:
            self.specs = json.load(json_data)
        self.source_path = source + '/skel'
