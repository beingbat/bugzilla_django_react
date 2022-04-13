# USER MANAGEMENT

MANAGER = 'manager'
DEVELOPER = 'developer'
QAENGINEER = 'qaengineer'

USER_TYPES = (
  (DEVELOPER, 'Developer'),
  (QAENGINEER, 'Quality Assurance Engineer'),
)

DEV_INDEX = 0
QAE_INDEX = 1


# BUG MANAGEMENT

BUG = 'bug'
FEATURE = 'feature'

BUG_TYPE = (
  (BUG, 'Bug'),
  (FEATURE, 'Feature'),
)

ALL = "all"
NEW = "start"
INPROGRESS = "in_progress"
COMPLETED = "completed"

STATUS_PARTIAL = (
  (NEW, "New"),
  (INPROGRESS, "In Progress"),
)

BUG_STATUS = STATUS_PARTIAL + ((COMPLETED, "Resolved"),)
FEATURE_STATUS = STATUS_PARTIAL + ((COMPLETED, "Completed"),)
