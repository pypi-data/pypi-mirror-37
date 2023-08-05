""" The gettext format. """

import polib
import datetime
from dateutil.tz import tzlocal
from .entry import POEntry

class GettextFormat:
    def __init__(self, conf):
        self.po = polib.pofile(conf["file"])
        self.pot = polib.pofile(conf["pot"])
        self.conf = conf

    def content(self):
        po = [POEntry(x) for x in self.po]
        return po

    def save(self):
        self.po.metadata['PO-Revision-Date'] = str(datetime.datetime.now(tzlocal()).__format__("%Y-%m-%d %H:%M%z"))
        self.po.metadata['Last-Translator'] = self.conf['fullname']
        self.po.metadata['Language'] = self.conf['lang']
        self.po.metadata['X-Generator'] = 'Offlate ' + self.conf['version']
        self.po.save()

    def merge(self, older, callback):
        older.po.merge(self.pot)
        self.po.save()
        for oentry in older.po:
            for nentry in self.po:
                if oentry.msgid == nentry.msgid:
                    if oentry.msgstr == nentry.msgstr:
                        break
                    if oentry.msgstr == "":
                        break
                    if nentry.msgstr == "":
                        nentry.msgstr = oentry.msgstr
                        break
                    # otherwise, nentry and oentry have a different msgstr
                    nentry.msgstr = callback(nentry.msgid, oentry.msgstr, nentry.msgstr)
                    break
        self.po.save()

