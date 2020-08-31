# Model Parameters
EB_MODEL = (3., 3., 0.5)
EB_QUIZ_THRESH_DEFAULT = 0.7
NEWBIE_MODEL = (1.5, 1.5, 0.1)
NEWBIE_QUIZ_THRESH_DEFAULT = 0.9
NEWBIE_TO_EB_THRESH_DEFAULT = 4
LONG_MODEL = (2., 2., 24.)

HP_FULL = 120
# How many seconds should one knowledge in corresponding bank take to answer
HP_AWARD_EB = 5
HP_AWARD_NEWBIE = 8
HP_AWARD_NEW = 15

# Hard punishment
HARD_PUNISH_MULTIPLIER = 2  # hl /= 2


def NEWBIE_RETEST_SCHEDULE(correct_count):
    if correct_count == 0:
        return 0.5
    else:
        return correct_count ** 2
