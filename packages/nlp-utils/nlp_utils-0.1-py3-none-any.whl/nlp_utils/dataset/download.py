import logging
import os
import sys
from urllib.request import urlretrieve

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
    from urllib.request import urlretrieve
else:
    import urllib2
    import urlparse
    from urllib import urlretrieve


def getEmbeddings(name):
    if not os.path.isfile(name):
        download("https://public.ukp.informatik.tu-darmstadt.de/reimers/embeddings/"+name)


def download(url, destination=os.curdir, silent=False):
    filename = os.path.basename(urlparse.urlparse(url).path) or 'downloaded.file'

    def get_size():
        meta = urllib2.urlopen(url).info()
        meta_func = meta.getheaders if hasattr(
            meta, 'getheaders') else meta.get_all
        meta_length = meta_func('Content-Length')
        try:
            return int(meta_length[0])
        except:
            return 0

    def kb_to_mb(kb):
        return kb / 1024.0 / 1024.0

    def callback(blocks, block_size, total_size):
        current = blocks * block_size
        percent = 100.0 * current / total_size
        line = '[{0}{1}]'.format(
            '=' * int(percent / 2), ' ' * (50 - int(percent / 2)))
        status = '\r{0:3.0f}%{1} {2:3.1f}/{3:3.1f} MB'
        sys.stdout.write(
            status.format(
                percent, line, kb_to_mb(current), kb_to_mb(total_size)))

    path = os.path.join(destination, filename)

    logging.info(
        'Downloading: {0} ({1:3.1f} MB)'.format(url, kb_to_mb(get_size())))
    try:
        (path, headers) = urlretrieve(url, path, None if silent else callback)
    except:
        os.remove(path)
        raise Exception("Can't download {0}".format(path))
    else:
        print()
        logging.info('Downloaded to: {0}'.format(path))

    return path