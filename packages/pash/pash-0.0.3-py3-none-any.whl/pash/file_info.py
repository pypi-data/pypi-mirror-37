import os
import pwd
import grp
from datetime import datetime, timezone


class FileInfo:
    def __init__(self, file):
        self.file = file
        self.isdir = os.path.isdir(self.file)

    @property
    def permission(self):
        return self._get_permission()

    @property
    def link(self):
        return self._get_link()

    @property
    def owner(self):
        return self._get_owner()

    @property
    def group(self):
        return self._get_group()

    @property
    def size(self):
        return self._get_size()

    @property
    def name(self):
        return self._get_name()

    @property
    def modi_time(self):
        return self._get_modi_time()

    def _get_permission(self):
        dic = {
            '7': 'rwx', '6': 'rw-',
            '5': 'r-x', '4': 'r--',
            '3': '-wx', '2': '-w-',
            '1': '--x', '0': '---',
        }
        permission = []
        dir = 'd' if self.isdir else '-'
        permission.append(dir)
        # 755, 644
        permission_oct = oct(os.stat(self.file).st_mode)[-3:]
        for per in permission_oct:
            permission.append(dic[per])
        return ''.join(permission)

    def _get_link(self):
        if self.isdir:
            return len(os.listdir(self.file)) + 2
        return 1

    def _get_owner(self):
        return pwd.getpwuid(os.stat(self.file).st_uid).pw_name

    def _get_group(self):
        return grp.getgrgid(os.stat(self.file).st_gid).gr_name

    def _get_size(self):
        return os.stat(self.file).st_size

    def _get_modi_time(self):
        utc_time = datetime.fromtimestamp(
            os.path.getmtime(self.file), timezone.utc)
        local_time = utc_time.astimezone()
        return local_time.strftime("%b %d %H:%M")

    def _get_name(self):
        return os.path.basename(self.file)
