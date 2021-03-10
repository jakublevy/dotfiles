from anki.hooks import wrap
from aqt.utils import tooltip
import anki.schedv2
import aqt
config = aqt.mw.addonManager.getConfig(__name__)
# config["burypoint"] #    5: automatically buries learning/relearning queue cards if you fail them this many times in a single day. does not add any tags.
# config["killpoint"] #  140: suspends cards if you review them successfully and the resulting interval is at least this value in days. adds a "auto-suspended" tag.

# burying and killing can be disabled for specific cards by adding special tags
# "No::Burry" to disable burying
# "No::Suspend" to disable killing

def checkKill(self, card, ease, early, _old):
    ret = _old(self, card, ease, early)
    if early:
        return ret
    
    note = card.note()
    if note.hasTag("No::Suspend"):
        return ret
    
    if card.ivl >= config["killpoint"]:
        self.suspendCards([card.id])
        note.addTag("auto-suspended")
        note.flush()
        tooltip(_("Card automatically auto-suspended and tagged due to high maturity"))
    return ret

to_bury = []

def checkBury(self, card, ease, _old):
    global to_bury
    ret = _old(self, card, ease)
    if ease != 1 or card.type not in [2,3]:
        return ret
    
    note = card.note()
    if note.hasTag("No::Burry"):
        return ret
    
    count_relapses_today = self.col.db.scalar("select count() from revlog where ease = 1 and type = 2 and cid = ? and id > ?", card.id, (self.col.sched.dayCutoff-86400)*1000)
    if count_relapses_today >= config["burypoint"]:
        tooltip(_("Card automatically buried until tomorrow"))
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
