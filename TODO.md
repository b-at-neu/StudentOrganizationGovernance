# TO DO

## High Priority

### General
[ ] Add form testing
[ ] Move all model interactions that views do to the respective model
    [ ] Add more standard functions to models like __str__ and __reqr__
[ ] Add testing for all model functions
[ ] Add tests that check for bad model creation
[ ] Add JS to do async POST requests
[ ] Standarize using the objects.create function NOT instantiating the class
[ ] Add model managers to all models
[ ] Add help text, labels, and error-messages to front end forms

### Clubs
[ ] Finish adding model testing for Constitution model

## Medium Priority

### General
[ ] Add more and better wording for assertion errors in testing suite
    [ ] Change "able to access" to something else, they usually can't access
[ ] Change function decorator system to be more expansive and simpler
[ ] Check that all POST views only take POST methods
[ ] Consolidate multiple POST funcs into one view with more params

### Clubs
[ ] Add ability to move around articles and sections in edit mode
[ ] Add async JS autosave to editing page (and unsaved changes warning)
[ ] Add ability to create bullet points in sections (mostly for the role definitions)
[ ] Add warning that you cant delete last article or section when editing (JS?)

### Board
[ ] Add filtering and sorting to overview page (JS?)
[ ] Improve algorithm for identifying which text has been replaced

## Low Priority

### General
[ ] Create confirmation screens for important tasks (submit, edit, approve, etc)
[ ] Make long lists take up multiple pages (club list, users, etc)
[ ] Create nice home page
[ ] Improve front-end formatting of forms
[ ] Improve formatting of links

### Clubs
[ ] Add ability for board members to deny certain sections and provide reasoning
[ ] Allow e-board member to have more than one club
[ ] Add club status to clubs (tentative, conditional, etc)
[ ] Add direct links to SOP and SOAR
[ ] Add undos for editing

### Board
[ ] Create template constitution editable to board members (multiple templates?)
[ ] Allow individual board members to review consitutions and comment, only allow head of board to make final changes 

### Users
[ ] Override AbstractBaseUser class and add custom methods
[ ] Only allow NEU emails, require that they be confirmed

## Future Ideas
[ ] Interaction with engage?
[ ] Expand to allow use by SOA
[ ] Clubs are warned when SOP updates
[ ] Add way to import all existing constitutions (pdf reader?)
[ ] Add notifications when edits are submitted for board/returned for e-board
[ ] Add bylaws?