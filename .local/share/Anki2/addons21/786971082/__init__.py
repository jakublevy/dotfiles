##############################################################
# Increase autosave frequency
# Copyright 2018 Soren Bjornstad <contact@sorenbjornstad.com>
# Tested on Anki 2.1.1.
##############################################################

###############################################################################
# The MIT License:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

import time

import anki.collection

import aqt
from aqt import mw
from aqt.qt import QAction

# overwrite autosave function with one that triggers faster and can be forced
SAVE_THRESHOLD = mw.addonManager.getConfig(__name__)['saveEveryNSeconds']
def newAutosave(self, force=False):
    if force or time.time() - self._lastSave > SAVE_THRESHOLD:
        self.save()
        return True

anki.collection._Collection.autosave = newAutosave

# install new menu item to force a save
action = QAction(mw)
action.setText("Save now")
action.setShortcut("Ctrl+S")
mw.form.menuCol.addAction(action)
action.triggered.connect(lambda: mw.col.autosave(True))
