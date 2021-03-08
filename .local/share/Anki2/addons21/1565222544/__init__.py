from anki.hooks import wrap
from aqt.utils import tooltip
import anki.schedv2
import aqt
config = aqt.mw.addonManager.getConfig(__name__)
# config["burypoint"] #    5: automatically buries learning/relearning queue cards if you fail them this many times in a single day. does not add any tags.
# config["killpoint"] #  140: suspends cards if you review them successfully and the resulting interval is at least this value in days. adds a "suspended" tag.

# burying and killing can be disabled for specific cards by adding special tags
# "no_burry" to disable burying
# "no_suspend" to disable killing

def checkKill(self, card, ease, early, _old):
    ret = _old(self, card, ease, early)
    if early:
        return ret
    
    note = card.note()
    if note.hasTag("no_suspend"):
        return ret
    
    if card.ivl >= config["killpoint"]:
        self.suspendCards([card.id])
        note.addTag("suspended")
        note.flush()
        tooltip(_("Card automatically suspended and tagged due to high maturity - DA KILL Z0NE"))
    return ret

to_bury = []

def checkBury(self, card, ease, _old):
    global to_bury
    ret = _old(self, card, ease)
    if ease != 1 or card.type not in [2,3]:
        return ret
    
    note = card.note()
    if note.hasTag("no_burry"):
        return ret
    
    count_relapses_today = self.col.db.scalar("select count() from revlog where ease = 1 and type = 2 and cid = ? and id > ?", card.id, (self.col.sched.dayCutoff-86400)*1000)
    if count_relapses_today >= config["burypoint"]:
        tooltip(_("Card automatically buried until tomorrow - DA BURY Z0NE"))
        to_bury += [card.id]
    return ret

def handleBury(self, card, ease, _old):
    global to_bury
    ret = _old(self, card, ease)
    if to_bury is not []:
        self.buryCards(to_bury, manual=False)
        self._resetLrn()
    to_bury = []
    return ret

anki.schedv2.Scheduler._rescheduleRev = wrap(anki.schedv2.Scheduler._rescheduleRev, checkKill, "around")
anki.schedv2.Scheduler._answerLrnCard = wrap(anki.schedv2.Scheduler._answerLrnCard, checkBury, "around")
anki.schedv2.Scheduler.answerCard = wrap(anki.schedv2.Scheduler.answerCard, handleBury, "around")
