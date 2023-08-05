import os
from .file_info import FileInfo


class LS:
    def __init__(self, args):
        '''
        para args: args input like -l, -a, -R
        '''
        self.args = args

    def get_and_display(self):
        data = self.get_data()
        self.display(data)

    def get_data(self):
        '''
        Get data from root path
        '''
        return self._list_subdir(self.args.path)

    def display(self, data):
        '''
        para data: data to display

        Display data
        '''
        self._setup_format(data)

    def _list_subdir(self, path):
        '''
        para args: full_path to run ls command

        First: Show and sort dirs in root path by _show_and_sort function
        Second: Recursion yield generator
        '''
        # Get generator depend on args input
        # ── foo
        #    ├── bar
        #    ├── hello
        # return generator -> ('/foo/', ['/bar', '/hello'])...
        lst = self._show_hidden_files(path)
        sorted_lst = self._sort_by_size(path, lst)
        yield (path, sorted_lst)
        if self.args.list_subdir:
            for file in sorted_lst:
                if file not in ('.', '..'):
                    sub_path = os.path.join(path, file)
                    if os.path.isdir(sub_path):
                        yield from self._list_subdir(sub_path)

    def _show_hidden_files(self, path):
        '''
        para args: full_path to run ls command

        Show hidden files and sort files depend on args input
        '''
        if self.args.show_hidden:
            return os.listdir(path) + ['.', '..']
        else:
            return [
                file for file in os.listdir(path)
                if not file.startswith('.')
            ]

    def _sort_by_size(self, path, lst):
        '''
        para args: root_path
        para lst: subdir_path

        Sort files by file size
        '''
        if self.args.sort_by_size:
            return sorted(
                lst,
                key=lambda f: os.path.getsize(os.path.join(path, f)),
                reverse=True)
        else:
            return sorted(lst)

    def _setup_format(self, gen):
        '''
        para gen: generator ('/foo/', ['/bar', '/hello'])...

        Display file format depend on args input
        '''
        for g in gen:
            if self.args.list_subdir:
                # When -R Display path before file list
                print(g[0])
            if not g[1]:
                # If the dir is empty
                print()
                continue
            self._format_data(g)
            print()

    def _format_data(self, data):
        '''
        para: data like ('/foo/', ['/bar', '/hello'])

        Display long format or not
        '''
        if self.args.long_format:
            for d in data[1]:
                f = FileInfo(os.path.join(data[0], d))
                file_info = self._long_info(f)
                self._format_long_info(file_info)
        else:
            self._short_info(data)

    def _long_info(self, f):
        '''
        para: file file path

        Get file long info
        '''
        return (
            f.permission, f.link,
            f.owner, f.group,
            f.size, f.modi_time, f.name)

    def _short_info(self, data):
        '''
        para: data like ('/foo/', ['/bar', '/hello'])

        Get file short info
        '''
        data = data[1]
        width = max(26, len(max(data, key=lambda k: len(k))))
        for k, v in enumerate(data):
            # Show three column in a row
            if k % 3 == 2 or k == len(data)-1:
                print('{:<{width}}'.format(v, width=width))
            else:
                print('{:<{width}}'.format(v, width=width), end='')

    def _format_long_info(self, info):
        '''
        Format output to terminal
        '''
        print('{0:<12}{1:<4}{2:<10}{3:<10}{4:>4}{5:^15}{6:<10}'.format(*info))
