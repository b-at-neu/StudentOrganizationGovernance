# TO DO

## High Priority

### General
- Move all model interactions that views do to the respective model
- Add tests that check for bad model creation

## Medium Priority

### General
- Add more and better wording for assertion errors in testing suite
    - Change "able to access" to something else, they usually can't access
- Change function decorator system to be more expansive and simpler
- Consolidate multiple POST funcs into one view with more params

### Clubs
- Add ability to move around articles and sections in edit mode
- Add ability to create bullet points in sections (mostly for the role definitions)
- Make sure more than one user can't edit a constitution at the same time
- get_constitution_data needs testing (commented out)
- figure out how to test get_json function with DIDs

### Board
- Add filtering and sorting to overview page (JS?)
- Add ability to toggle between viewing red-lined version and regular
- Add ability to disable additional red-lining algorithm (on a user-by-user basis?)

## Low Priority

### General
- Create confirmation screens for important tasks (submit, edit, approve, etc)
- Make long lists take up multiple pages (club list, users, etc)
- Add form testing
- Add dark mode

### Clubs
- Add ability for board members to deny certain sections and provide reasoning
- Allow e-board member to have more than one club
- Add club status to clubs (tentative, conditional, etc)
- Add undos and redos for editing

### Board
- Create template constitution editable to board members (multiple templates?)
- Allow individual board members to review consitutions and comment, only allow head of board to make final changes 

### Users
- Override AbstractBaseUser class and add custom methods
- Only allow NEU emails, require that they be confirmed

## Future Ideas
- Interaction with engage?
- Expand to allow use by SOA
- Clubs are warned when SOP updates
- Add way to import all existing constitutions (pdf reader?)
- Add notifications when edits are submitted for board/returned for e-board
- Add bylaws?
