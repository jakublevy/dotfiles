from anki import hooks
from anki.hooks import wrap
from aqt.utils import tooltip
from anki.schedv2 import Scheduler
from aqt import mw
from aqt import gui_hooks
#from aqt.utils import showWarning

config = mw.addonManager.getConfig(__name__)
# config["burypoint"] #    5: automatically buries learning/relearning queue cards if you fail them this many times in a single day. does not add any tags.
# config["suspendpoint"] #  140: suspends cards if you review them successfully and the resulting interval is at least this value in days. adds a config["suspendTag"] tag.

# burying and suspending can be disabled for specific cards by adding special tags
# config["disableBuryTag"] to disable burying
# config["disableSuspendTag"] to disable suspending

# Called after answering a review card
def checkSuspend(card, ease, early):
    note = card.note()
    if early:
        return
    if note.hasTag(config["disableSuspendTag"]):
        return
    if card.ivl >= config["suspendpoint"]:
        card.queue = -1 #suspend card
        note.addTag(config["suspendTag"])
        note.flush()
        card.flush()
        tooltip(_("Card automatically suspended and tagged due to high maturity"))

to_bury = []

# Called after answering an arbitrary card
def checkBury(reviewer, card, ease):
    #showWarning("checkBury() called, card.type: {}".format(card.type))
    note = card.note()                      #cards.lapses is the number of times a review card is failed back to relearning. Failed learning and relearning cards are not counted.
    if ease != 1 or card.type not in [0,1]: #card.type seems to be "new" = 0, "learning" = 1, "review" = 2, "in learning" = 3, "preview" = 4
        return                              #for more info see ankidroid github docs
    if note.hasTag(config["disableBuryTag"]):
        return                                                                                                    # (reviewer.mw.col.sched.dayCutoff-86400) start of this day in seconds
    count_relapses_today = reviewer.mw.col.db.scalar("select count() from revlog where ease = 1 and type >= 0 and type <= 1 and cid = ? and id > ?", card.id, (reviewer.mw.col.sched.dayCutoff-86400)*1000)
    #showWarning("count_relapses_today: {}".format(count_relapses_today))
    if config["burypoint"] >= 0 and (count_relapses_today % config["burypoint"] == 0):
        reviewer.onBuryCard()
        reviewer.mw.col.sched.buryCards([card.id], manual=False)
        reviewer.mw.col.sched._resetLrn()
        #global to_bury
        #to_bury.append(card.id)
        tooltip(_("Card automatically buried until tomorrow due to high failure"))


# def handleBury(self, card, ease, _old):
#     ret = _old(self, card, ease)

#     global to_bury
#     for cid in to_bury:
#         self.buryCards(to_bury, manual=False)
#         self._resetLrn()
#     to_bury = []
#     return ret


# def checkBury(self, card, ease, _old):
#     global to_bury
#     ret = _old(self, card, ease)
#     if ease != 1 or card.type not in [2,3]:
#         return ret
    
#     note = card.note()
#     if note.hasTag(config["disableBuryTag"]):
#         return ret
    
#     count_relapses_today = self.col.db.scalar("select count() from revlog where ease = 1 and type = 2 and cid = ? and id > ?", card.id, (self.col.sched.dayCutoff-86400)*1000)
#     showWarning(count_relapses_today)
#     if count_relapses_today >= config["burypoint"]:
#         tooltip(_("Card automatically buried until tomorrow"))
#         to_bury += [card.id]
#     return ret


# def handleBury(self, card, ease, _old):
#     global to_bury
#     ret = _old(self, card, ease)
#     if to_bury is not []:
#         self.buryCards(to_bury, manual=False)
#         self._resetLrn()
#     to_bury = []
#     return ret

# Scheduler._answerLrnCard = wrap(Scheduler._answerLrnCard, checkBury, "around")
# Scheduler.answerCard = wrap(Scheduler.answerCard, handleBury, "around")


hooks.schedv2_did_answer_review_card.append(checkSuspend)
gui_hooks.reviewer_did_answer_card.append(checkBury)
#Scheduler.answerCard = wrap(Scheduler.answerCard, handleBury, "around")
