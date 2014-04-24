*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${accordion_tile_location}  "accordion"
${content_tree}  .formTabs .formTab:nth-child(2) a
${folder_selector}  .ui-draggable .contenttype-folder
${tile_selector}  div.tile-container div.tile
${title_field_id}  accordion

*** Test cases ***

Test Accordions Tile
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description  Empty layout

    # add a accodions tile to the layout
    Edit Cover Layout
    Add Tile  ${accordion_tile_location}
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover

    # drag & drop folder
    # not working
    Open Content Chooser
    Click Link  css=${content_tree}
    Drag And Drop  css=${folder_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.accordion

    # test the folder
    Click Link  link=View
    Page Should Contain  My SubFolder1
    Page Should Contain  My SubFolder2

    # delete the tile
    Edit Cover Layout
    Delete Tile
    Save Cover Layout