MANAGER = 'manager'
DEVELOPER = 'developer'
QAENGINEER = 'qaengineer'

NEW = "start"
INPROGRESS = "in_progress"
COMPLETED = "completed"


USER_TYPES = (
  (DEVELOPER, 'Developer'),
  (QAENGINEER, 'Quality Assurance Engineer'),
)

BUG = 'bug'
FEATURE = 'feature'

BUG_TYPE = (
  (BUG, 'Bug'),
  (FEATURE, 'Feature'),
)

STATUS_PARTIAL = (
  (NEW, "New"),
  (INPROGRESS, "In Progress"),
)

BUG_STATUS = STATUS_PARTIAL + ((COMPLETED, "Resolved"),)
FEATURE_STATUS = STATUS_PARTIAL + ((COMPLETED, "Completed"),)

DEV_INDEX = 0
QAE_INDEX = 1
