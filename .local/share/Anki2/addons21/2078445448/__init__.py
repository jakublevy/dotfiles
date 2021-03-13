from aqt.qt import *
from aqt.browser import Browser, DataModel, SearchContext
from aqt.utils import showWarning
from aqt import gui_hooks
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

def search(self, txt: str) -> None:
    self.beginReset()
    self.cards = []
    error_message: Optional[str] = None
    try:
        ctx = SearchContext(search=txt, browser=self.browser)
        gui_hooks.browser_will_search(ctx)
        if ctx.card_ids is None:
            ctx.card_ids = self.col.find_cards(ctx.search, order=ctx.order)
        gui_hooks.browser_did_search(ctx)
        self.cards = ctx.card_ids
    except Exception as e:
        error_message = str(e)
    finally:
        self.endReset()

    if error_message:
        pass
        #self.browser.form.searchEdit.setStyleSheet("border: 1px solid red;")
        #showWarning(error_message)

Browser.quickFilter = quickFilter
Browser.setupSearch = wrap(Browser.setupSearch, onSetupSearch, "after")
DataModel.search = search