# Make sure you replace the API and/or APP key below
# with the ones for your account

from cliapp import CliApp, output
import sys
import json
from os.path import expanduser
from os.path import exists as pexists


class GUtils(CliApp):

    def get_stats_by_author(self, author, since):
        cmd = "git log --graph --decorate --pretty=oneline --abbrev-commit  --numstat --author='{}' --since='{}'".format(
            author, since)
        print(cmd)
        o, r = self.shell_run(cmd, silent=True)
        if r != 0:
            return 'something wrong with the git command execution: {}'.format(o)
        additions = 0
        deletions = 0
        commits = 0
        if len(o) > 0:
            for line in o:
                line = line.decode(encoding='UTF-8')
                if line.startswith('*'):
                    commits += 1
                    continue
                if line.find('/vendor') > 0:
                    continue
                items = line.split('\t')
                if len(items) > 2:
                    try:
                        additions += int(items[0])
                        deletions += int(items[1])
                    except:
                        continue
        return "{}\t{}\t{}\t{}".format(author, commits, additions, deletions)

    def get_authors_from_config(self):
        cp = '{}/.gs'.format(expanduser('~'))
        if not pexists(cp):
            return []
        with open(cp, 'r') as f:
            cfg = json.load(f)
            return cfg['authors']

    @output
    def do_stats(self, **kwargs):
        """gus stats author=<author> since=<since>
        since is default to '3 month ago'
        When author is not specified, gus will try to read from ~/.gs (sample content: {"author":["author1","author2"]}
        """
        author = kwargs.get('author', None)
        since = kwargs.get('since', '3 month ago')
        out = list()
        out.append("{}\t{}\t{}\t{}".format('author', 'commits', 'additions', 'deletions'))
        try:
            if author is not None:
                out.append(self.get_stats_by_author(author, since))
            else:
                authors = self.get_authors_from_config()
                if authors is None or len(authors) == 0:
                    return 'there is no authors specified. you can specify authors through cli or ~/.gs config file'
                for author in authors:
                    out.append(self.get_stats_by_author(author, since))
        except Exception as e:
            return 'something is wrong: {}'.format(e)
        return '\n'.join(out)

    @output
    def do_who(self, **kwargs):
        """gus who path=<path> max=<max>
        max is default to 5
        path is default to . (current working directory)
        """
        path = kwargs.get('path', '.')
        max_str = kwargs.get('max', '5')
        try:
            max = int(max_str)
        except:
            max = 5
        out = list()
        items = dict()
        cmd = 'git shortlog -nse -- {}'.format(path)
        o, r = self.shell_run(cmd, silent=True)
        if r != 0:
            return 'something went wrong with the git shortlog command execution: {}'.format(o)
        if len(o) > 0:
            for line in o:
                line = line.decode(encoding='UTF-8')
                email = line[line.find("<") + 1:line.find(">")]
                if len(email) == 0:
                    continue
                parts = line.split('\t')
                thing = []
                if len(parts) == 2:
                    try:
                        thing = [int(parts[0]), parts[1]]
                    except:
                        continue
                if email in items:
                    thing[0] += items[email][0]
                items[email] = thing
            #print(items.items())
            sorted_items = [value for (key, value) in sorted(items.items(), key=lambda a: a[1][0], reverse=True)]
            out.append('commits\tauthor')
            for item in sorted_items[:max]:
                out.append('{}\t{}'.format(item[0],item[1]))
            return '\n'.join(out)
        return 'nothing'


if __name__ == '__main__':
    gus = GUtils()
    gus.run(sys.argv[1:])
