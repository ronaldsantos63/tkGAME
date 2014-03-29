<!-- encoding: utf-8 -->


# CONTRIBUTORS

| Initials | Contributor | GitHub membership | Cool project | Current role | Previous role |
|:--------:|:------------|:-----------------:|:------------:|:------------:|:-------------:|
| RS | Raphaël Seban | **[tarball69] (https://github.com/tarball69)** | **[tkRAD] (https://github.com/tarball69/tkRAD)** | **developer** | author |
|  | next? |  |  |  |  |


# CHANGELOG


## $ 2014-03-29 RS $

* now switching to:

    Development Status :: 3 - Alpha


## $ 2014-03-24 RS $

* Gabe is now operational;

* back from MS-Windows:

    * TODO:

        * must adapt MouseWheel to ScrollView:

            * DONE;

        * must adapt `__run_script()` to win32:

            * DONE;

        * should update `^/xml/data/tkgame_sections.xml`:

            * DONE;

* gone testing under MS-Windows by now;

* in `MainWindow`:

    * in `__run_script()`:

        * now fully implemented for UNIX-likes;

        * must test under MS-Windows;

* in `lib.widgets.game_section_browser.GameSectionView`:

    * in `web_build()`:

        * testing some `threading.Thread()` features;

        * finally using `self.after()` instead: quite sufficient;

        * now this method works better; :happy:


## $ 2014-03-23 RS $

* in `MainWindow`:

    * in `__unzip_archive()`:

        * now fully implemented;


## $ 2014-03-22 RS $

* in `MainWindow`:

    * added new `__unzip_archive()`:

        * added very little bit of code today (busy elsewhere);

* after unzipping + installing + launching script, `gabe` will be
operational, at least for testing game archives;


## $ 2014-03-20 RS $

* swimming pool day?

* is Tkinter thread unsafe?

* removed all threading features;

* integrated `GameDownloadBox` into `gabe.MainWindow` directly;

* now it works without cancellation possibilities but -huh!- it works;

* this will be OK for the moment;


## $ 2014-03-19 RS $

* renamed `GameFileDownloadDialog` to `GameDownloadDialog`;

* renamed `GameFileDownloadBox` to `GameDownloadBox`;

* started implementing `GameDownloadBox.download()` probably with
threading features;

* @18:45 --> used `concurrent.futures.ThreadPoolExecutor()` async
thread features + `urllib.request.urlretrieve()` web features:

    * now implemented OK;

* will soon have to test with real remote file to retrieve from the
web (what about big ZIP archive?);


## $ 2014-03-18 RS $

* in `tkGAME.lib.widgets.game_file_download_box`:

    * in `GameFileDownloadDialog`:

        * upgraded code along
        `tkRAD.widgets.rad_dialog.RADButtonsDialog` class def;


## $ 2014-03-16 RS $

* maybe should I create `RADDialogWindow` + `RADXMLDialogWindow`
classes with modal features? Dialogs are essential to apps, in fact.

* added new `tkGAME.lib.widgets.game_file_download_box`:

    * filled up many, many code...

* in `tkGAME.src.MainWindow`:

    * implementing `_slot_open_item()` and affiliates;

    * added
    new `__download_package()`,
    new `__get_item_attrs()`,
    new `__open_item()`,
    new `__run_script()`:

        * almost fully implemented;


## $ 2014-03-15 RS $

* added new `tkGAME.lib.game_scroll_view.GameScrollView` class:

    * now almost fully implemented;

* now `tkGAME.lib.game_section_browser.GameSectionView` class
inherits new `GameScrollView` class;

* making some more tests;

* **Gabe** is slowly becoming some kind of interesting stuff;


## $ 2014-03-14 RS $

* making tests;

* renamed XML attrs `dest` --> `type`:

    * yet two fixed values: `editor` and `game` (default);

* optimized all over `game_section_browser.py` script;


## $ 2014-03-13 RS $

* in `tkGAME/lib/widgets/game_section_browser.py`:

    * in `GameSectionView`:

        * added new `_parse_attr_dest()`:

            * now fully implemented;

        * optimized code for `_open_item()` and `_open_section()`;


## $ 2014-03-12 RS $

* upgraded `tkGAME/tkRAD` lib to **tkRAD v1.4.1**;

* in `tkGAME/lib/widgets/game_section_browser.py`:

    * updated code along new tkRAD version for best use;


## $ 2014-03-11 RS $

* renamed `tkgame_browser.py` to `gabe.py` (Gabe - Game Browser);

* in `gabe.py`: updated code along new situation;

* in `tkGAME/lib/widgets/game_section_browser.py`:

    * added lots of new features;

    * now works fine with tkRAD v1.4;

* in `tkGAME/xml/data/tkgame_sections.xml`: updated data OK;


## $ 2014-03-09 RS $

* now switching to:

    Development Status :: 2 - Pre-Alpha

* in `MainWindow`:

    * implemented `GameSectionBrowser` widget in XML source code;

    * now using `game_section_browser` object;

    * missing only `open_item()` web/local procedure;

* in `game_section_browser.py`:

    * now estimated to 'fully implemented' state;

    * all classes are operational and ready-to-use;


## $ 2014-03-08 RS $

* in `game_section_browser.py`:

    * added some new code;


## $ 2014-03-07 RS $

* started wiki-ing a little;

* now using `tkRAD` lib for app development;

* in `tkgame_browser.py`:

    * implemented some code in `class Application`;

* in `src/` folder:

    * added new file `mainwindow.py`:

        * started some little code in `class MainWindow`;

* in `xml/` folder:

    * added new `menu/`, `widget/` folders;

    * added new `menu/topmenu.xml`, `widget/mainwindow.xml` XML files;

* in `topmenu.xml` XML file:

    * implemented some little menu code by now;

* in `mainwindow.xml` XML file:

    * implemented some little widget code by now;

* in `locale/` folder:

    * added new `fr_FR.po` i18n translations file for French LC_LANG;

* in `fr_FR.po` file:

    * started some translations from `en` (base english) to `fr_FR`
    (metropolitan french);

* in `tkGAME/lib/` folder:

    * added new `audio`, `editor`, `widget` folders (subpackages);

    * added new `widget/game_section_browser.py`:

        * implemented some bit of code;


## $ 2014-03-06 RS $

* initial commit;

* set up generic files and dirs (README, CHANGELOG, etc);

* renamed `tkgame.py` main file to `tkgame_browser.py` as `tkGAME`
application part would become a **game editors browser**, in fact;

* `tkGAME` project wil now have **two parts**:

    * `tkGAME.lib`: the Game **library** with lots of features,
    intended to developpers and proprietary game software development;

    * `tkGAME.tkgame_browser`: a game editors browser **app** made
    to ease up WYSIWYG simple game design + game code generation;


============================= END OF FILE =============================
