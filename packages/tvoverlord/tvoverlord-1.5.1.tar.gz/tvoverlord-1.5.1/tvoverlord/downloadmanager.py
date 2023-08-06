
import os
import shutil
import re
import datetime
import subprocess
import sys
from pprint import pprint as pp
# import logging
import itertools
import click

from tvoverlord.config import Config
from tvoverlord.db import DB
from tvoverlord.notify import Tell
from tvoverlord.tvutil import disk_info, sxxexx, sxee


class DownloadManager:
    """Manage media files after they have been downloaded

    A torrent client calls it's resprective manager; transmission_done.py
    or deluge_done.py; when the torrent has finished downloading, then
    that manager calls this class.

    This probably should just be functions instead of a class since its
    really just a singleton.

    Usage:
        TorrentManger(torrent_hash, path, filename, debug=False)

    Args:
        torrent_hash: The torrent hash, retrieved from the magnet url
        path:         The source folder where the downloaded torrent is
        filename:     The name of the torrent, can be a file or dir
        debug:        If console output is wanted

    Two settings in config.ini control behaviour:
    torrent done: copy|move
    single file: yes|no

    If 'torrent done' is not defined, then nothing happens, else the
    content is copied or moved.

    if 'single file' is 'yes', then only the media file is
    transfered.  If it's 'no', then whatever was downloaded is
    transfered to the destination.
    """
    def __init__(self, torrent_hash, path, filename, debug=False):
        if debug:
            console = Config.logging.StreamHandler()
            formater = Config.logging.Formatter('>>> %(message)s')
            console.setFormatter(formater)
            Config.logging.getLogger('').addHandler(console)

        Config.logging.info('-' * 50)
        Config.logging.info('hash: %s', torrent_hash)
        Config.logging.info('path: %s', path)
        Config.logging.info('filename: %s', filename)

        filename = os.path.join(path, filename)
        DB.save_info(torrent_hash, filename)

        debug_command = '''export TR_TORRENT_NAME='%s'; export TR_TORRENT_DIR='%s'; export TR_TORRENT_HASH='%s'; transmission_done'''
        Config.logging.info(debug_command, filename, path, torrent_hash)

        if DB.is_oneoff(torrent_hash):
            Config.logging.info('Download is a one off, doing nothing.')
            return

        if not os.path.exists(Config.tv_dir):
            msg = 'Destination: "{}" does not exist'.format(Config.tv_dir)
            Config.logging.error(msg)
            raise OSError(msg)
            # sys.exit(msg)

        if not os.path.exists(filename):
            msg = 'Source does not exist'.format(filename)
            Config.logging.error(msg)
            raise OSError(msg)
            # sys.exit(msg)

        source = filename
        if Config.single_file:
            # extract largest file from dir
            source = self.get_show_file(filename)

        if Config.template:
            template = Config.template
        else:
            template = '{show}/{original}'
        dest_filename = self.pretty_names(source, torrent_hash, template)
        Config.logging.info('Destination filename: %s' % dest_filename)

        dest = os.path.join(Config.tv_dir, dest_filename)
        dest_path = os.path.dirname(dest)

        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)
            Config.logging.info('creating dir: %s' % dest)

        DB.save_dest(torrent_hash, dest)

        Config.logging.info('copying %s to %s' % (source, dest))
        if self.copy(source, dest, filename):
            Tell('%s done' % os.path.basename(dest))
            DB.set_torrent_complete(torrent_hash)
        else:
            Config.logging.info('Destination full')
            Tell('Destination full')
            sys.exit('Destination full')

    def copy(self, source, destination, downloaded_file_or_dir):
        """Copy files or dirs using the platform's copy tool"""

        source_size = self.get_size(source)
        destination_dir = os.path.dirname(destination)
        destination_free = disk_info(destination_dir)
        if source_size > destination_free:
            return False

        use_shell = False

        cmd = None
        if Config.is_win and os.path.isfile(source):
            # Windows needs the shell set to True to use the built in
            # commands like copy.
            use_shell = True
            cmd = ['copy', source, destination, '/Y']

        elif Config.is_win and os.path.isdir(source):
            # destination = os.path.join(destination, '*')
            # /I to prevent xcopy asking if dest is a file or folder
            cmd = ['xcopy', source, destination, '/E/S/Y/I']

        elif sys.platform.startswith(('darwin', 'linux')):
            cmd = ['cp', '-r', source, destination]
        else:
            sys.exit('Unknown platform')

        error_code = subprocess.call(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=use_shell)

        if error_code == 0:
            try:
                os.unlink(downloaded_file_or_dir)
            except IsADirectoryError:
                shutil.rmtree(downloaded_file_or_dir)
        else:
            sys.exit(error_code)

        return True

    def get_size(self, start_path):
        if os.path.isfile(start_path):
            return os.path.getsize(start_path)
        elif os.path.isdir(start_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return total_size
        else:
            sys.exit('Get size dir: "{}" does not exist'.format(start_path))

    def pretty_names(self, filename, torrent_hash, template=None):
        if not template:
            template = '{show}/{original}'

        fields = {}
        (fields['show'], fields['searchname'], fields['season'],
         fields['episode']) = DB.get_show_info(torrent_hash)
        fields['original'] = os.path.basename(filename)
        fields['s00e00'] = sxxexx(fields['season'], fields['episode'])
        fields['0x00'] = sxee(fields['season'], fields['episode'])
        fields['season'] = fields['season'].rjust(2, '0')
        fields['episode'] = fields['episode'].rjust(2, '0')

        if fields['searchname'] is None:
            fields['searchname'] = ''

        # search original filename for info
        fields['resolution'] = ''
        for res in Config.categories.resolution:
            if res.lower() in filename.lower():
                fields['resolution'] = res
        fields['source'] = ''
        for srs in Config.categories.sources:
            if srs.lower() in filename.lower():
                fields['source'] = srs
        fields['codec'] = ''
        for cod in Config.categories.codecs:
            if cod.lower() in filename.lower():
                fields['codec'] = cod
        fields['audio'] = ''
        for aud in Config.categories.audio:
            if aud.lower() in filename.lower():
                fields['audio'] = aud

        # short cut tags
        all = [fields['show'], fields['s00e00'], fields['resolution'],
               fields['source'], fields['codec'], fields['audio']]
        all = [i for i in all if i]  # remove empty
        fields['all'] = ' '.join(all)

        ext = ''
        if os.path.isfile(filename):
            ext = os.path.splitext(filename)[-1]

        broke = re.split('({.*?})', template)
        if not broke[-1]:
            broke = broke[:-1]

        new = []
        is_section = False

        for section in broke:
            if section.startswith('{'):
                chunks = section.strip('{}').split('|')
                field = chunks[0].lower()
                filters = [i for i in chunks[1:]]
                try:
                    if not fields[field]:
                        continue
                except KeyError:
                    continue
                complete = self.format(fields[field], filters)
                new.append(complete)
                is_section = True
            else:
                new.append(section)
                is_section = False
        # remove adjacent duplicates
        new = [i[0] for i in itertools.groupby(new)]
        if not is_section:
            new = new[:-1]
        new.append(ext)
        full = ''.join(new)
        full = os.path.normpath(full)
        return full

    def format(self, str, filters):
        for filter in filters:
            if filter == 'lower':
                str = str.lower()
            if filter == 'upper':
                str = str.upper()
            if filter == 'capitalize':
                str = ' '.join([i.capitalize() for i in str.split()])
            if filter == 'underscore':
                str = str.replace(' ', '_')
            if filter == 'dash':
                str = str.replace(' ', '-')
            if filter.startswith('rep:'):
                rep = filter.split(':')[1]
                old_str = rep[0]
                new_str = rep[1]
                if old_str and new_str:
                    str = str.replace(old_str, new_str)
            if filter.startswith('del:'):
                del_str = filter.split(':')[-1]
                if del_str:
                    str = str.replace(del_str, '')
            else:
                sys.exit('Invalid filter: {}'.format(filter))

        return str

    def get_show_file(self, name):
        """Find the largest file in a dir

        If name is a file, just return that name, else
        return the name of the largest file

        Args:
            name - The name of a dir or file

        Returns:
            Returns the name of the largest file
        """
        if not os.path.exists(name):
            return False
        if os.path.isfile(name):
            Config.logging.info('{} is a file'.format(name))
            return name
        files_sizes = []
        for root, dirs, files in os.walk(name):
            for filename in files:
                full_filename = os.path.join(root, filename)
                size = os.stat(full_filename).st_size
                files_sizes.append([size, full_filename])
        files_sizes.sort(key=lambda torrent: int(torrent[0]), reverse=True)
        return files_sizes[0][1]
