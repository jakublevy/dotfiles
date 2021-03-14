from aqt import gui_hooks
from aqt.browser import Browser 
from aqt.utils import show_invalid_search_error
from anki.errors import InvalidInput
import unicodedata

def connectSearchOnType(browser):
    browser._returnPressed = False
    browser.form.searchEdit.lineEdit().textEdited.connect(browser._quickFilter)
    browser.form.searchEdit.lineEdit().returnPressed.connect(browser._explicitSearch)

def quickFilter(self, text):
    txt = self.form.searchEdit.lineEdit().text()
    txt = unicodedata.normalize("NFC", txt)

    self._returnPressed = False
    self._lastSearchTxt = txt
    self.search()

def explicitSearch(self):
    self._returnPressed = True

# Monkey patch to alter appearance of error input message. 
# This error message is shown only if searched was invoked using Enter key.
def search(self) -> None:
    try:
        self.model.search(self._lastSearchTxt)
    except Exception as err:
        if(self._returnPressed):
            show_invalid_search_error(err)
            self._returnPressed = False
    if not self.model.cards:
        # no row change will fire
        self._onRowChanged(None, None)


# Monkey patch to alter appearance of error input message. 
# This error message is shown only if searched was invoked using Enter key.
def onSearchActivated(self) -> None:
    text = self.form.searchEdit.lineEdit().text()
    try:
        normed = self.col.build_search_string(text)
    except InvalidInput as err:
        if(self._returnPressed):
            show_invalid_search_error(err)
            self._returnPressed = False
    else:
        self.search_for(normed)
        self.update_history()

gui_hooks.browser_menus_did_init.append(connectSearchOnType)
Browser._quickFilter = quickFilter
Browser._explicitSearch = explicitSearch
Browser.search = search
Browser._onSearchActivated = onSearchActivated