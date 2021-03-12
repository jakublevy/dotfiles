from aqt.qt import *
from aqt.browser import Browser
from anki.hooks import wrap, addHook
import unicodedata

def onSetupSearch(self):
    self.form.searchEdit.lineEdit().textEdited.connect(self.quickFilter)

def quickFilter(self, text):
    if self.form.searchEdit.lineEdit().text() == self._searchPrompt:
        self.form.searchEdit.lineEdit().setText("deck:current ")

    txt = self.form.searchEdit.lineEdit().text()
    txt = unicodedata.normalize("NFC", txt)

    self._lastSearchTxt = txt
    self.search()

Browser.quickFilter = quickFilter
Browser.setupSearch = wrap(Browser.setupSearch, onSetupSearch, "after")
