# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cciaapd.contenttypes -t test_scheda.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src cciaapd.contenttypes.testing.CCIAAPD_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_scheda.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Scheda
  Given a logged-in site administrator
    and an add scheda form
   When I type 'My Scheda' into the title field
    and I submit the form
   Then a scheda with the title 'My Scheda' has been created

Scenario: As a site administrator I can view a Scheda
  Given a logged-in site administrator
    and a scheda 'My Scheda'
   When I go to the scheda view
   Then I can see the scheda title 'My Scheda'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add scheda form
  Go To  ${PLONE_URL}/++add++Scheda

a scheda 'My Scheda'
  Create content  type=Scheda  id=my-scheda  title=My Scheda


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the scheda view
  Go To  ${PLONE_URL}/my-scheda
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a scheda with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the scheda title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
