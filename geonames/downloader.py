"""Data downloader."""

from __future__ import unicode_literals

import logging
import time
import os
import ssl
import zipfile

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urllib import urlopen
    from urlparse import urlparse


# modificato da cities con licenza MIT https://github.com/shun-miyama/cities/blob/main/LICENSE
class Downloader(object):

    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    def download(self, force=False):
        """Download self._source file/url to self._destination."""
        logger = logging.getLogger('geonames')

        # Prevent copying itself
        if self.source_matches_destination():
            logger.info('Download self._source matches self._destination file')
            return False

        if not self.needs_downloading(force):
            logger.info('Assuming local download is up to date for %s', self._source)
            return True

        logger.info('Downloading %s into %s', self._source, self._destination)

        try:
            source_stream = urlopen(self._source)
        except Exception as ex:
            ssl._create_default_https_context = ssl._create_unverified_context
            source_stream = urlopen(self._source)
        with open(self._destination, 'wb') as local_file:
            local_file.write(source_stream.read())

        return True

    def source_matches_destination(self):
        """Return True if self._source and self._destination point to the same file."""
        parsed_source = urlparse(self._source)
        if parsed_source.scheme == 'file':
            source_path = os.path.abspath(os.path.join(parsed_source.netloc,
                                                       parsed_source.path))
            if not os.path.exists(source_path):
                raise Exception("SourceFileDoesNotExist %s" % source_path)

            if source_path == self._destination:
                return True
        return False

    def needs_downloading(self, force):
        """Return True if self._source should be downloaded to self._destination."""
        try:
            src_file = urlopen(self._source)
        except Exception as ex:
            ssl._create_default_https_context = ssl._create_unverified_context
            src_file = urlopen(self._source)
        try:
            src_size = int(src_file.headers['content-length'])
            src_last_modified = time.strptime(
                src_file.headers['last-modified'],
                '%a, %d %b %Y %H:%M:%S %Z'
            )

            if os.path.exists(self._destination) and not force:
                local_time = time.gmtime(os.path.getmtime(self._destination))
                local_size = os.path.getsize(self._destination)

                if local_time >= src_last_modified and local_size == src_size:
                    return False
        except:
            # not all servers return last-modified (e.g. istat)
            pass
        return True

    def single_file_if_zip(self, partial_names):
        '''
        partial_names can be a string or a list of strings; in the latter case all of them must match
        :return: the file-like object matching the partial_names
        https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.open
        '''
        try:
            zf = zipfile.ZipFile(self._destination)
            for f in zf.filelist:
                matches = True
                if type(partial_names) == list:
                    for partial_name in partial_names:
                        matches = matches and (partial_name in f.orig_filename)
                else: # it is a string
                    matches = partial_names in f.orig_filename
                if matches:
                    break
                else:
                    f = None
            if f:
                exctracted_path = '%s%s' % (self._destination, os.path.split(f.orig_filename)[1])
                full_exctracted_path = zf.extract(f, exctracted_path)
                return full_exctracted_path
            else:
                return None
        except:
            return None
