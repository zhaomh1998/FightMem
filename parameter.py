# Model Parameters
EB_MODEL = (3., 3., 0.5)
EB_QUIZ_THRESH_DEFAULT = 0.7
NEWBIE_MODEL = (1.5, 1.5, 0.1)
NEWBIE_QUIZ_THRESH_DEFAULT = 0.9
NEWBIE_TO_EB_THRESH_DEFAULT = 3
LONG_MODEL = (2., 2., 24.)


def NEWBIE_RETEST_SCHEDULE(correct_count):
    if correct_count == 0:
        return 0.5
    else:
        return correct_count ** 2
