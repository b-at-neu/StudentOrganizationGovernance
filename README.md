# TO DO

## Vital functionality
- Add ability to move around articles and sections
- Move handling of old v new content into views.py
- Add testing
    - Model testing (finish for constitution)
    - Form testing
    - Move view interactions with models into models and test
    - Better error wording on template errors (rendering)
    - Add helpful messages to all assert statements
    - Add model testing checking for improper creation of objects
- Add helpful error messages in testing view class by catching errors
- Make submit_constitution require club on view
- Add JS
- Add POST decorator to check for method type before all other checks
- Change error text on tests to not read "Able to access" but something more clear


## Upcoming features
- Add comments for denial on specific items
- Allow people to have multiple clubs
- Create confirmation screens for important tasks (submit, edit, approve, etc)
- Add unsaved changes warning to edit page
- Adds tentative club status
- Board overview page: allow filtering and sorting
- Add multiple pages to club, user, and board view
- Create nicer home page
- Add links to SOP, SOAR, and templates
- Add status that club needs to update their constitution due to a recent SOP update
- Allow individual board members to review consitutions and comment, only allow head of board to make final changes
- Improve algorithm for identifying which text has been replaced
- Add way to import all existing constitutions
- Override AbstractBaseUser class and add custom methods
- Add more standard functions to models like __str__ and __reqr__
- Standarize using the objects.create function
- Add model managers to models
- Add help text, labels, and error-messages to front end forms
- Add ability to create bullet points in sections (mostly for the role definitions)
- Improve front-end formatting of forms
- Improve formatting of links
- Add warning that you cant delete last article or section
- Consolidate multiple POST funcs into one view with more params


## Useful features
- Add SOP rules to auto-enforce
- Notification when a const edit is submitted
- Add links to engage pages of the clubs
- Add bylaws?
- Email confirmation and NEU emails only
- Add undo's


## Bug tracking
- Sections and Articles content not saving!
- Model allows clubs without constitution
- Club creation does not take you to club page immediately
- Cleaner code: remove club_url arg from post functions and test the proper club without decorator
- Add link to a board overview of a specific club to board overview page (link doesn't lead anywhere)
- User signup requires password to be unique from email but not from username
- When deleting a model object during test, if view is run twice, errors occur (temp solution: don't test admin)
