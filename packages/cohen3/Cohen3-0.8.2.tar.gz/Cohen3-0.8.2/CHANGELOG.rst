0.8.2 - Fixes and enhancements
------------------------------

General:
    - Reintroduces WebUI
    - Improve documentation
    - Whole new design for web server html visualization

Fixes:
    - Fix Inotify events
    - Fix test_dbus reactors conflict
    - Fix some travis dependencies
    - Fix wrong log level for init function of the log module

0.8.1 - Fixes and enhancements
------------------------------

General:
    - Automate documentation building via travis
    - Add more sphinx documentation
    - Remove livestreamer as basic dependency
    - Migrate from pygtk to gi.repository
    - Migrate Gstreamer from version 0.10 to 1.0
    - Enhance Travis with more tests
    - Reformat according pep8 directives.

Fixes:
    - Fix quoted keys for some headers
    - Fix Inotify (now uses twisted's Inotify)
    - Fix all pep8/pylint errors

0.8.0 - Cohen3 project started
------------------------------

General:
    - Rename project from Cohen to Cohen3
    - Migrate source code to python version 3
    - Twisted >= 18.7.0 is now required
    - Louie-latest is now required (instead of Louie)

0.7.3 - Fixes and improvements
------------------------------

General:
    - Travis enhancements: make travis upload to pypi

Fixes:
    - Hotfix for LazyContainer

0.7.2 - Minor bugfixes
----------------------

Fixes:
    - Fix issue when Cohen fails to be discovered by xbox 360 dlna client
    - Fix issue when using Lazy Container on Samsung AllShare on 2012 Samsung TV fails

0.7.0 - Cohen project started
-----------------------------

General:
    - lots of refactoring
    - removed lots of Coherence stuff
    - moved to lxml instead of (c)ElementTree
    - Twisted >= 14.0 is now required
    - livestreamer is now required
    - cleanups and fixes

Backends:
    - twitch.tv backend added


0.0.1 - 0.7.0 - Coherence project
---------------------------------

Changelog skipped