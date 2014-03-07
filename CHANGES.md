<!-- encoding: utf-8 -->


# CONTRIBUTORS

| Initials | Contributor | GitHub membership | Cool project | Current role | Previous role |
|:--------:|:------------|:-----------------:|:------------:|:------------:|:-------------:|
| RS | Raphaël Seban | **[tarball69] (https://github.com/tarball69)** | **[tkRAD] (https://github.com/tarball69/tkRAD)** | **developer** | author |
|  | next? |  |  |  |


# CHANGELOG

## $ 2014-03-07 RS $

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
