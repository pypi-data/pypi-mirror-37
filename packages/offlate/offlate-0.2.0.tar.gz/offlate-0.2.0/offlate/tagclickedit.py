from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import re
import sys
from urllib.parse import quote
import html

class TagClickEdit(QTextBrowser):
    def __init__(self, *args):
        QTextBrowser.__init__(self, *args)

    def createLinks(self):
        text = self.toHtml()
        for word_object in re.finditer(r'@[a-z]+{[^}]*}', text):
            rep = word_object.string[word_object.span()[0] : word_object.span()[1]]
            text = text.replace(rep, '<a href="#' + quote(html.unescape(rep)) + '">' + rep + '</a>')
        self.setHtml(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TagClickEdit()
    w.setText("GNU@tie{}Hello provides the @command{hello} command.")
    w.createLinks()
    w.show()
    sys.exit(app.exec_())
