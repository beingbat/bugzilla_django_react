MANAGER = 'manager'
DEVELOPER = 'developer'
QAENGINEER = 'qaengineer'

NEW = "New"
INPROGRESS = "Started"
RESOLVED = "Resolved"
COMPLETED = "Completed"


USER_TYPES = (
  (DEVELOPER, 'Developer'),
  (QAENGINEER, 'Quality Assurance Engineer'),
)

BUG_TYPE = (
  ('bug', 'Bug'),
  ('feature', 'Feature'),
)

STATUS_PARTIAL = (
  ('start', NEW),
  ('in_progress', INPROGRESS),
)

BUG_STATUS = STATUS_PARTIAL + (('completed', RESOLVED),)
FEATURE_STATUS = STATUS_PARTIAL + (('completed', COMPLETED),)

DEV_INDEX = 0
QAE_INDEX = 1
