<!-- encoding: utf-8 -->


# CONTRIBUTORS

| Initials | Contributor | GitHub membership | Cool project | Current role | Previous role |
|:--------:|:------------|:-----------------:|:------------:|:------------:|:-------------:|
| RS | Raphaël Seban | **[tarball69] (https://github.com/tarball69)** | **[tkRAD] (https://github.com/tarball69/tkRAD)** | **developer** | author |
|  | next? |  |  |  |  |


# CHANGELOG


## $ 2014-03-11 RS $

* renamed `tkgame_browser.py` to `gabe.py` (Gabe - Game Browser);


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
