from os import walk
from pathlib import Path
import platform


def get_relevant_dir(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        for dirname in dirnames:
            if '.default' in dirname:
                f.append(dirpath + '/' + dirname)
        break
    return f


home = str(Path.home())
firefox_path = '%s/.mozilla/firefox' % home
thunderbird_path = '%s/.thunderbird' % home

# f = get_relevant_dir(firefox_path)
# print(f)


def get_firefox_site_data():
    """ Get firefox site data paths.
        Unix cmd: ls ${HOME}/.mozilla/firefox /${FIREFOX}/storage/default / | grep http

    Returns:
        list: paths of site data files
    """
    f = []
    for path in Path(firefox_path).glob("**/storage/default/http*"):
        f.append(path)
    return f


print(platform.system())

# Deleting Firefox History
# sqlite3 ${HOME}/.mozilla/firefox /${FIREFOX}/places.sqlite "SELECT datetime(moz_historyvisits.visit_date/1000000,'unixepoch'), moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id;"
# sqlite3 ${HOME}/.mozilla/firefox /${FIREFOX}/places.sqlite "delete from moz_historyvisits;"

# Deleting Firefox Cookies
# sqlite3 ${HOME}/.mozilla/firefox /${FIREFOX}/cookies.sqlite "select datetime(creationTime/1000000,'unixepoch'),host from moz_cookies; delete from moz_cookies;"

# Deleting Firefox Site Data

# find ${HOME}/.mozilla/firefox /${FIREFOX}/storage/default -name "http*" -type d - exec rm - r "{}" \
#    - prune

# Deleting Firefox Cache
# NUM =$(ls - 1 ${HOME}/.cache/mozilla/firefox /${FIREFOX}/cache2/entries | wc - l)
# SIZ =$(du - sbh ${HOME}/.cache/mozilla/firefox /${FIREFOX}/cache2/entries)
# SIZ =$(echo $SIZ | cut - d" " - f1)
# echo "Files: $NUM Size: $SIZ"
# find ${HOME}/.cache/mozilla/firefox /${FIREFOX}/cache2/entries - type f - delete 2 > /dev/null

# Deleting Thunderbird Cookies
# sqlite3 ${HOME}/.thunderbird/${THUNDERBIRD}/cookies.sqlite "select datetime(creationTime/1000000,'unixepoch'),host from moz_cookies; delete from moz_cookies;"
