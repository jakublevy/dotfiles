import os
from aqt.reviewer import Reviewer
from aqt.utils import (
    TR,
    tr,
    downArrow
)

thisScriptDir = os.path.dirname(__file__)

def bottomHTML(self) -> str:
    return open(os.path.join(thisScriptDir, "bottom.html"), "r").read() % dict(
        rem=self._remaining(),
        edit=tr(TR.STUDYING_EDIT),
        editkey=tr(TR.ACTIONS_SHORTCUT_KEY, val="E"),
        more=tr(TR.STUDYING_MORE),
        downArrow=downArrow(),
        time=self.card.timeTaken() // 1000,
    )

Reviewer._bottomHTML = bottomHTML