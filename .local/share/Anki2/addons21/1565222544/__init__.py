from anki import hooks
from anki.hooks import wrap
from aqt.utils import tooltip
from anki.schedv2 import Scheduler
from aqt import mw
from aqt.utils import showWarning

config = mw.addonManager.getConfig(__name__)
# config["burypoint"] #    5: automatically buries learning/relearning queue cards if you fail them this many times in a single day. does not add any tags.
# config["suspendpoint"] #  140: suspends cards if you review them successfully and the resulting interval is at least this value in days. adds a config["suspendTag"] tag.

# burying and suspending can be disabled for specific cards by adding special tags
# config["disableBuryTag"] to disable burying
# config["disableSuspendTag"] to disable suspending

to_bury = []

def checkSuspend(card, ease, early):
    if early:
        return
    
    note = card.note()
    if note.hasTag(config["disableSuspendTag"]):
        return
    
    if card.ivl >= config["suspendpoint"]:
        card.queue = -1 #suspend card
        note.addTag(config["suspendTag"])
        note.flush()
        card.flush()
        tooltip(_("Card automatically suspended and tagged due to high maturity"))
    
def checkBury(self, card, ease, _old):
    global to_bury
    ret = _old(self, card, ease)
    if ease != 1 or card.type not in [2,3]:
        return ret
    
    note = card.note()
    if note.hasTag(config["disableBuryTag"]):
        return ret
    
    count_relapses_today = self.col.db.scalar("select count() from revlog where ease = 1 and type = 2 and cid = ? and id > ?", card.id, (self.col.sched.dayCutoff-86400)*1000)
    showWarning(count_relapses_today)
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


hooks.schedv2_did_answer_review_card.append(checkSuspend)

Scheduler._answerLrnCard = wrap(Scheduler._answerLrnCard, checkBury, "around")
Scheduler.answerCard = wrap(Scheduler.answerCard, handleBury, "around")