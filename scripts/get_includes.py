#get_includes.py
#Peter Grossmann
#6 July 2023
#$Id$
#$Log$

import argparse
import json
import os
import sys

def main() :

    option_parser = argparse.ArgumentParser()
    option_parser.add_argument("-clean", action="store_true", help="Clean out old repo clones")
    option_parser.add_argument("include_list", help="Specify JSON file to collect repository data from")

    options = option_parser.parse_args()

    include_list = options.include_list

    with open(include_list) as include_file :

        repo_data = json.loads(include_file.read())

        for repo in repo_data :

            if (options.clean) :
                clean_cmd = f'rm -rf {repo}'
                print("Clean command is: "+clean_cmd)
                os.system(clean_cmd)

            clone_cmd = f'git clone git@github.com:{repo_data[repo]["source"]}'
            print("Clone command is: "+clone_cmd)
            os.system(clone_cmd)

            checkout_cmd = f'cd {repo}; git checkout {repo_data[repo]["version"]}'
            print("Checkout command is: "+checkout_cmd)
            os.system(checkout_cmd)


if __name__ == "__main__" :
    main()
