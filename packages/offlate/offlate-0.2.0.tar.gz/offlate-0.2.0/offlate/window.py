import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import json
import re
import os
import math
from urllib.parse import unquote

from .manager import ProjectManager
from .spellcheckedit import SpellCheckEdit
from .tagclickedit import TagClickEdit

class ProjectTab(QTabWidget):
    def __init__(self, parent = None):
        super(ProjectTab, self).__init__(parent)

class Interface:
    def __init__(self):
        self.value = None

    def ok(self):
        self.value = self.qd.textValue()

    def askPassword(self):
        self.qd = QInputDialog()
        self.qd.setLabelText(self.qd.tr("Please enter your password:"))
        self.qd.setTextEchoMode(QLineEdit.Password)
        self.qd.accepted.connect(self.ok)
        self.qd.exec_()
        return self.value

class ProjectView(QWidget):
    translationModified = pyqtSignal()

    def __init__(self, project, showTranslated = True, showUntranslated = True,
                showFuzzy = True, monospace = False, parent = None):
        super(ProjectView, self).__init__(parent)
        self.project = project
        self.content = self.project.content()
        self.currentContent = list(self.content.keys())[0]
        self.showTranslated = showTranslated
        self.showUntranslated = showUntranslated
        self.showFuzzy = showFuzzy
        self.monospace = monospace
        self.fuzzyColor = QBrush(QColor(255, 127, 80))
        self.emptyColor = QBrush(QColor(255, 240, 235))
        self.initUI()

    def updateContent(self):
        self.treeWidget.clear()
        items = []
        for entry in self.content[self.currentContent]:
            if entry.isObsolete():
                continue
            cont = False
            if self.showTranslated and entry.isTranslated():
                cont = True
            if self.showUntranslated and not entry.isTranslated():
                cont = True
            if self.showFuzzy and entry.isFuzzy():
                cont = True
            if not cont:
                continue
            item = QTreeWidgetItem([entry.msgids[0].replace('\n', ' '),
                                    entry.msgstrs[0].replace('\n', ' ')])
            if entry.isFuzzy():
                item.setForeground(1, self.fuzzyColor)
            if not entry.isTranslated():
                item.setBackground(1, self.emptyColor)
            item.setFont(0, QFont("sans-serif", 10))
            item.setFont(1, QFont("sans-serif", 10))
            item.setSizeHint(0, QSize(-1, 22))
            item.setData(0, Qt.UserRole, entry)
            items.append(item)
        self.treeWidget.insertTopLevelItems(0, items)
        self.translationModified.emit()

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        model = QStandardItemModel()
        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.msgid = QTextEdit()
        self.msgid.setReadOnly(True)
        self.msgstr = SpellCheckEdit(self.project.lang)
        self.filechooser = QComboBox()
        for project in list(self.content.keys()):
            self.filechooser.addItem(project)
        self.filechooser.currentIndexChanged.connect(self.changefile)

        self.buttons = QVBoxLayout()
        self.copyButton = QPushButton(self.tr("Copy"))
        self.copyButton.clicked.connect(self.copy)
        self.buttons.addWidget(self.copyButton)

        if self.filechooser.count() > 1:
            vbox.addWidget(self.filechooser)

        self.updateContent()
        vbox.addWidget(self.treeWidget, 4)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.msgid)
        self.hbox.addLayout(self.buttons)
        self.hbox.addWidget(self.msgstr)
        vbox.addLayout(self.hbox, 1)
        size = self.treeWidget.size()
        self.treeWidget.setColumnWidth(0, size.width()/2)
        self.treeWidget.currentItemChanged.connect(self.selectItem)

    def changefile(self):
        self.currentContent = list(self.content.keys())[self.filechooser.currentIndex()]
        self.updateContent()

    def nextItem(self):
        index = self.treeWidget.currentIndex()
        nextItem = self.treeWidget.itemFromIndex(self.treeWidget.indexBelow(index))
        self.treeWidget.setCurrentItem(nextItem)

    def previousItem(self):
        index = self.treeWidget.currentIndex()
        nextItem = self.treeWidget.itemFromIndex(self.treeWidget.indexAbove(index))
        self.treeWidget.setCurrentItem(nextItem)

    def copy(self):
        if self.msgstr.__class__.__name__ == "SpellCheckEdit":
            text = self.msgid.toPlainText()
            self.msgstr.setText(text)
        else:
            text = self.msgid.currentWidget().toPlainText()
            self.msgstr.currentWidget().setText(text)

    def copyTag(self, tag):
        tag = tag.toDisplayString()[1:]
        tag = unquote(tag)
        if self.msgstr.__class__.__name__ == "SpellCheckEdit":
            self.msgstr.insertPlainText(tag)
            self.msgstr.setFocus(True)
        else:
            self.msgstr.currentWidget.insertPlainText(tag)
            self.msgstr.currentWidget.setFocus(True)

    def selectItem(self, current, old):
        if current == None:
            return
        if self.msgstr.__class__.__name__ == "SpellCheckEdit":
            self.msgstr.clearFocus()
        else:
            self.msgstr.currentWidget.clearFocus()
        data = current.data(0, Qt.UserRole)
        self.hbox.removeWidget(self.msgid)
        self.hbox.removeItem(self.buttons)
        self.hbox.removeWidget(self.msgstr)
        self.msgid.deleteLater()
        self.msgstr.deleteLater()

        font = "monospace" if self.monospace else "sans-serif"
        focuser = None

        if len(data.msgstrs) > 1:
            self.msgid = QTabWidget();
            self.msgstr = QTabWidget();
            singular = TagClickEdit()
            singular.setFont(QFont(font))
            singular.setReadOnly(True)
            singular.setText(data.msgids[0])
            singular.createLinks()
            singular.anchorClicked.connect(self.copyTag)
            plural = TagClickEdit()
            plural.setFont(QFont(font))
            plural.setReadOnly(True)
            plural.setText(data.msgids[1])
            plural.createLinks()
            plural.anchorClicked.connect(self.copyTag)
            self.msgid.addTab(singular, self.tr("Singular"))
            self.msgid.addTab(plural, self.tr("Plural"))
            i = 0
            for msgstr in data.msgstrs:
                form = SpellCheckEdit(self.project.lang)
                form.setFont(QFont(font))
                form.setText(msgstr)
                form.textChanged.connect(self.modify)
                self.msgstr.addTab(form, str(i))
                if i == 0:
                    focuser = form
                i=i+1
        else:
            self.msgid = TagClickEdit()
            self.msgid.setFont(QFont(font))
            self.msgid.setReadOnly(True)
            self.msgid.setText(data.msgids[0])
            self.msgid.createLinks()
            self.msgid.anchorClicked.connect(self.copyTag)
            self.msgstr = SpellCheckEdit(self.project.lang)
            self.msgstr.setFont(QFont(font))
            self.msgstr.setText(data.msgstrs[0])
            self.msgstr.textChanged.connect(self.modify)
            focuser = self.msgstr
        self.hbox.addWidget(self.msgid)
        self.hbox.addLayout(self.buttons)
        self.hbox.addWidget(self.msgstr)
        focuser.setFocus()

    def modify(self):
        item = self.treeWidget.currentItem()
        data = item.data(0, Qt.UserRole)
        if self.msgstr.__class__.__name__ == "SpellCheckEdit":
            msgstr = self.msgstr.toPlainText()
            data.update(0, msgstr)
            item.setText(1, msgstr.replace('\n', ' '))
        else:
            i = 0
            for msgstr in data.msgstrs:
                data.update(i, self.msgstr.widget(i).toPlainText())
                i=i+1
            item.setText(1, data.get(0).replace('\n', ' '))
        item.setForeground(1, QBrush())
        if data.isTranslated():
            item.setBackground(1, QBrush())
        else:
            item.setBackground(1, self.emptyColor)
        self.translationModified.emit()


    def save(self):
        self.project.save()

    def send(self):
        self.project.save()
        self.project.send(Interface())

    def askmerge(self, msgid, oldstr, newstr):
        # TODO: Actually do something more intelligent
        return newstr

    def update(self):
        self.project.save()
        self.project.update(self.askmerge)
        self.content = self.project.content()
        self.updateContent()

    def filter(self, showTranslated, showUntranslated, showFuzzy):
        self.showTranslated = showTranslated
        self.showUntranslated = showUntranslated
        self.showFuzzy = showFuzzy
        self.updateContent()

    def setFont(self, monospace):
        self.monospace = monospace
        current = self.treeWidget.currentItem()
        self.selectItem(current, current)

class NewWindow(QDialog):
    def __init__(self, manager, parent = None):
        super().__init__(parent)
        self.name = ""
        self.lang = ""
        self.system = 0
        self.manager = manager
        self.askNew = False
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        predefinedbox = QVBoxLayout()
        self.searchfield = QLineEdit()
        predefinedbox.addWidget(self.searchfield)
        self.predefinedprojects = QListWidget()
        with open(os.path.dirname(__file__) + '/data.json') as f:
            self.projectdata = json.load(f)
            for d in self.projectdata:
                item = QListWidgetItem(d['name'])
                item.setData(Qt.UserRole, d)
                self.predefinedprojects.addItem(item)
        predefinedbox.addWidget(self.predefinedprojects)

        contentbox = QVBoxLayout()
        formbox = QGroupBox(self.tr("Project information"))
        self.formLayout = QFormLayout()
        formbox.setLayout(self.formLayout)

        self.nameWidget = QLineEdit()
        self.langWidget = QLineEdit()
        self.formLayout.addRow(QLabel(self.tr("Name:")), self.nameWidget)
        self.formLayout.addRow(QLabel(self.tr("Target Language:")), self.langWidget)
        self.combo = QComboBox()
        self.combo.addItem(self.tr("The Translation Project"))
        self.combo.addItem(self.tr("Transifex"))
        self.formLayout.addRow(self.combo)

        self.nameWidget.textChanged.connect(self.modify)
        self.langWidget.textChanged.connect(self.modify)

        hhbox = QHBoxLayout()
        cancel = QPushButton(self.tr("Cancel"))
        self.okbutton = QPushButton(self.tr("OK"))
        self.okbutton.setEnabled(False)
        hhbox.addWidget(cancel)
        hhbox.addWidget(self.okbutton)
        contentbox.addWidget(formbox)
        contentbox.addLayout(hhbox)
        hbox.addLayout(predefinedbox)
        hbox.addLayout(contentbox)

        self.additionalFields = []
        self.additionalFields.append([])
        self.additionalFields.append([])
        self.transifexOrganisation = QLineEdit()
        self.transifexOrganisation.textChanged.connect(self.modify)
        transifexOrganisationLabel = QLabel(self.tr("Organization"))
        self.additionalFields[1].append({'label': transifexOrganisationLabel,
            'widget': self.transifexOrganisation})

        self.setLayout(hbox)

        self.predefinedprojects.currentItemChanged.connect(self.fill)
        cancel.clicked.connect(self.close)
        self.okbutton.clicked.connect(self.ok)
        self.searchfield.textChanged.connect(self.filter)
        self.combo.currentIndexChanged.connect(self.othersystem)

    def ok(self):
        self.askNew = True
        self.close()

    def fill(self):
        item = self.predefinedprojects.currentItem()
        data = item.data(Qt.UserRole)
        self.nameWidget.setText(data['name'])
        self.combo.setCurrentIndex(int(data['system']))
        if data['system'] == 1:
            self.transifexOrganisation.setText(data['organisation'])

    def filter(self):
        search = self.searchfield.text()
        self.predefinedprojects.clear()
        regexp = re.compile(".*"+search)
        for d in self.projectdata:
            if regexp.match(d['name']):
                item = QListWidgetItem(d['name'])
                item.setData(Qt.UserRole, d)
                self.predefinedprojects.addItem(item)

    def modify(self):
        enable = False
        if self.nameWidget.text() != '' and self.langWidget.text() != '':
            enable = True
            for widget in self.additionalFields[self.combo.currentIndex()]:
                if widget['widget'].text() == '':
                    enable = False
                    break
        self.okbutton.setEnabled(enable)

    def wantNew(self):
        return self.askNew

    def getProjectName(self):
        return self.nameWidget.text()

    def getProjectLang(self):
        return self.langWidget.text()

    def getProjectSystem(self):
        return self.combo.currentIndex()

    def getProjectInfo(self):
        if self.getProjectSystem() == 0:
            return {}
        if self.getProjectSystem() == 1:
            return {'organization': self.additionalFields[1][0]['widget'].text()}
        return {}

    def othersystem(self):
        for system in self.additionalFields:
            for widget in system:
                self.formLayout.takeRow(widget['widget'])
                widget['widget'].hide()
                widget['label'].hide()
        self.formLayout.invalidate()
        for widget in self.additionalFields[self.combo.currentIndex()]:
            self.formLayout.addRow(widget['label'], widget['widget'])
            widget['widget'].show()
            widget['label'].show()
        self.modify()

class SettingsWindow(QDialog):
    def __init__(self, preferences, parent = None):
        super().__init__(parent)
        self.data = preferences
        self.done = False
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        tab = QTabWidget()
        self.addTPTab(tab)
        self.addTransifexTab(tab)

        buttonbox = QHBoxLayout()
        cancel = QPushButton(self.tr("Cancel"))
        ok = QPushButton(self.tr("OK"))
        buttonbox.addWidget(cancel)
        buttonbox.addWidget(ok)

        vbox.addWidget(tab)
        vbox.addLayout(buttonbox)
        self.setLayout(vbox)
        cancel.clicked.connect(self.close)
        ok.clicked.connect(self.ok)

    def addTransifexTab(self, tab):
        formBox = QGroupBox(self.tr("Transifex"))
        formLayout = QFormLayout()
        self.TransifexToken = QLineEdit()

        if not "Transifex" in self.data:
            self.data["Transifex"] = {}
        try:
            self.TransifexToken.setText(self.data["Transifex"]["token"])
        except Exception:
            pass

        self.TransifexToken.textChanged.connect(self.updateTransifex)
        label = QLabel(self.tr("You can get a token from <a href=\"#\">https://www.transifex.com/user/settings/api/</a>"))
        label.linkActivated.connect(self.openTransifex)

        formLayout.addRow(QLabel(self.tr("Token:")), self.TransifexToken)
        formLayout.addRow(label)

        formBox.setLayout(formLayout)
        tab.addTab(formBox, "Transifex")

    def openTransifex(self):
        QDesktopServices().openUrl(QUrl("https://www.transifex.com/user/settings/api/"));

    def updateTransifex(self):
        self.data["Transifex"] = {}
        self.data["Transifex"]["token"] = self.TransifexToken.text()

    def addTPTab(self, tab):
        formBox = QGroupBox(self.tr("Translation Project"))
        formLayout = QFormLayout()

        self.TPemail = QLineEdit()
        self.TPuser = QLineEdit()
        self.TPserver = QLineEdit()
        self.TPfullname = QLineEdit()

        if not "TP" in self.data:
            self.data["TP"] = {}

        if 'email' in self.data['TP']:
            self.TPemail.setText(self.data["TP"]["email"])
        if 'user' in self.data['TP']:
            self.TPuser.setText(self.data["TP"]["user"])
        if 'server' in self.data['TP']:
            self.TPserver.setText(self.data["TP"]["server"])
        if 'fullname' in self.data['TP']:
            self.TPfullname.setText(self.data["TP"]["fullname"])

        self.TPemail.textChanged.connect(self.updateTP)
        self.TPuser.textChanged.connect(self.updateTP)
        self.TPserver.textChanged.connect(self.updateTP)
        self.TPfullname.textChanged.connect(self.updateTP)

        formLayout.addRow(QLabel(self.tr("Email:")), self.TPemail)
        formLayout.addRow(QLabel(self.tr("Server:")), self.TPserver)
        formLayout.addRow(QLabel(self.tr("User Name:")), self.TPuser)
        formLayout.addRow(QLabel(self.tr("Full Name (John Doe <john@doe.me>):")), self.TPfullname)

        formBox.setLayout(formLayout)
        tab.addTab(formBox, "TP")

    def updateTP(self):
        self.data["TP"] = {}
        self.data["TP"]["email"] = self.TPemail.text()
        self.data["TP"]["user"] = self.TPuser.text()
        self.data["TP"]["server"] = self.TPserver.text()
        self.data["TP"]["fullname"] = self.TPfullname.text()

    def ok(self):
        self.done = True
        self.close()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = ProjectManager()
        self.initUI()

    def initOpenProjects(self, menu):
        l = self.manager.listProjects()
        for p in l:
            name = p['name']
            act = QAction(name, self) 
            act.triggered.connect((lambda name: (lambda : self.open(name)))(name))
            menu.addAction(act)

    def open(self, name):
        try:
            project = self.manager.getProject(name)
        except Exception:
            self.qd = QErrorMessage()
            self.qd.showMessage(self.tr("Unsupported / Unknown project"))
            self.qd.exec_()
            return
        tab = ProjectView(project,
            showTranslated = self.showTranslatedAct.isChecked(),
            showUntranslated = self.showUntranslatedAct.isChecked(),
            showFuzzy = self.showFuzzyAct.isChecked(),
            monospace = self.monospaceAct.isChecked())
        tab.translationModified.connect(self.count)
        self.tabs.addTab(tab, name)
        self.count()

    def count(self, item = -1):
        widget = self.tabs.currentWidget()
        content = widget.content[widget.currentContent]
        total = 0
        translated = 0
        for d in content:
            total += 1
            if d.isTranslated() and not d.isFuzzy():
                translated += 1
        percent = 100 if total == 0 else math.floor(1000 * translated / total)/10
        self.countLabel.setText(self.tr("{} translated on {} total ({}%).").format(translated, total, percent))

    def save(self):
        self.tabs.currentWidget().save()

    def new(self):
        w = NewWindow(self.manager)
        w.exec_()
        if not w.wantNew():
            return
        self.manager.createProject(w.getProjectName(), w.getProjectLang(),
                    w.getProjectSystem(), w.getProjectInfo())
        self.open(w.getProjectName())

    def send(self):
        self.tabs.currentWidget().send()

    def update(self):
        self.tabs.currentWidget().update()
        self.manager.update()
        self.manager.writeProjects()

    def closeProject(self):
        self.tabs.removeTab(self.tabs.currentIndex())

    def settings(self):
        w = SettingsWindow(self.manager.getConf())
        w.exec_()
        if w.done:
            self.manager.updateSettings(w.data)

    def filter(self):
        for i in range(0, self.tabs.count()):
            self.tabs.widget(i).filter(
                self.showTranslatedAct.isChecked(),
                self.showUntranslatedAct.isChecked(),
                self.showFuzzyAct.isChecked())

    def setFont(self):
        for i in range(0, self.tabs.count()):
            self.tabs.widget(i).setFont(self.monospaceAct.isChecked())

    def previousItem(self):
        self.tabs.currentWidget().previousItem()

    def nextItem(self):
        self.tabs.currentWidget().nextItem()

    def initUI(self):
        # Build menu
        exitAct = QAction(QIcon('exit.png'), self.tr('Exit'), self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip(self.tr('Exit application'))
        exitAct.triggered.connect(qApp.quit)

        saveAct = QAction(QIcon('save.png'), self.tr('Save'), self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip(self.tr('Save current project'))
        saveAct.triggered.connect(self.save)

        newAct = QAction(QIcon('new.png'), self.tr('New'), self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip(self.tr('New project'))
        newAct.triggered.connect(self.new)

        updateAct = QAction(QIcon('download.png'), self.tr('Update'), self)
        updateAct.setShortcut('Ctrl+U')
        updateAct.setStatusTip(self.tr('Get modifications from upstream'))
        updateAct.triggered.connect(self.update)

        sendAct = QAction(QIcon('close.png'), self.tr('Close'), self)
        sendAct.setStatusTip(self.tr('Close current project'))
        sendAct.triggered.connect(self.closeProject)

        closeAct = QAction(QIcon('upload.png'), self.tr('Send'), self)
        closeAct.setShortcut('Ctrl+E')
        closeAct.setStatusTip(self.tr('Send modifications upstream'))
        closeAct.triggered.connect(self.send)

        settingsAct = QAction(QIcon('settings.png'), self.tr('Settings'), self)
        settingsAct.setShortcut('Ctrl+P')
        settingsAct.setStatusTip(self.tr('Set parameters'))
        settingsAct.triggered.connect(self.settings)

        self.showTranslatedAct = QAction(self.tr('Show Translated'), self, checkable=True)
        self.showTranslatedAct.setChecked(True)
        self.showTranslatedAct.triggered.connect(self.filter)
        self.showFuzzyAct = QAction(self.tr('Show Fuzzy'), self, checkable=True)
        self.showFuzzyAct.setChecked(True)
        self.showFuzzyAct.triggered.connect(self.filter)
        self.showUntranslatedAct = QAction(self.tr('Show Empty Translation'), self, checkable=True)
        self.showUntranslatedAct.setChecked(True)
        self.showUntranslatedAct.triggered.connect(self.filter)
        self.monospaceAct = QAction(self.tr('Use a monospace font'), self, checkable=True)
        self.monospaceAct.setChecked(False)
        self.monospaceAct.triggered.connect(self.setFont)

        self.previousShortcut = QShortcut(QKeySequence("Ctrl+Up"), self)
        self.previousShortcut.activated.connect(self.previousItem)

        self.previous2Shortcut = QShortcut(QKeySequence("Ctrl+Shift+Return"), self)
        self.previous2Shortcut.activated.connect(self.previousItem)

        self.nextShortcut = QShortcut(QKeySequence("Ctrl+Down"), self)
        self.nextShortcut.activated.connect(self.nextItem)

        self.next2Shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.next2Shortcut.activated.connect(self.nextItem)

        self.countLabel = QLabel()
        self.statusBar()
        self.statusBar().addWidget(self.countLabel)

        openMenu = QMenu(self.tr('Open'), self)
        self.initOpenProjects(openMenu)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu(self.tr('&File'))
        fileMenu.addAction(newAct)
        fileMenu.addMenu(openMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        projectMenu = menubar.addMenu(self.tr('&Project'))
        projectMenu.addAction(updateAct)
        projectMenu.addAction(saveAct)
        projectMenu.addAction(sendAct)
        projectMenu.addSeparator()
        projectMenu.addAction(closeAct)

        editMenu = menubar.addMenu(self.tr('&Edit'))
        editMenu.addAction(settingsAct)

        viewMenu = menubar.addMenu(self.tr('&View'))
        viewMenu.addAction(self.showTranslatedAct)
        viewMenu.addAction(self.showUntranslatedAct)
        viewMenu.addAction(self.showFuzzyAct)
        viewMenu.addSeparator()
        viewMenu.addAction(self.monospaceAct)

        self.tabs = ProjectTab()
        self.tabs.currentChanged.connect(self.count)

        self.setCentralWidget(self.tabs)

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Offlate')
        self.show()

def main():
    app = QApplication(sys.argv)
    translator = QTranslator()
    if translator.load(QLocale(), "offlate", "_",
            os.path.dirname(os.path.realpath(__file__))+"/locales"):
        app.installTranslator(translator);

    w = Window()

    sys.exit(app.exec_())

