March
=====

[![Build Status](https://magnum.travis-ci.com/patrickwhite256/march.svg?token=Urtvk4fuxUP8Zg5qkWzT)](https://magnum.travis-ci.com/patrickwhite256/march)

A Stepmania chart editor. Created as the Internal Mini-Project component of SE390.

Technologies
------------

- Python
- PyQt

Logical Components
------------------

- Data Models
 - Notes Complete before 20 September (YW, PW) [Complete]
 - Work on some necessary model helper functions (PW)
- Playing selections of audio (.ogg)
 - Decide on library by 20 September (KM) [~]
  - Some libraries looked, some issues with all.
 - Trying PyQt sound stuff (KM)
- Parser / Serializer
 - Begin parsing simfile into internal representation (PW)
- User Interface
 - Play with PyGUI and see if it's crap by 20 September (JM, AW) [Complete]
  - It is in fact crap, using PyQt instead
 - Create wireframe designs for UI (JM, YW)

Group Members
-------------

- Kelly McBride
- Joel Mizzoni
- Patrick White
- Amanda Wiskar
- Yeting Wang

Setup Directions
----------------

- PyQt Installation - follow http://pyqt.sourceforge.net/Docs/PyQt5/installation.html
 - You may also have to install Qt 5.4.1. You can get it here http://www.qt.io/download-open-source/


| Must-Haves               | Nice-to-haves       |
|--------------------------|---------------------|
| - jump to bar            | - mods              |
| - general metadata editor| - playing at speed  |
| - sample player          | - copypaste sections|
| - drag & drop track      | - waveform bg       |
| - difficulty tabs        | - keyboard          |
| - dialogs for new things |                     |
| - zooming                |                     |
