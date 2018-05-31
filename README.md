# pointilist
**NOTE: Currently this README only acts as a mission statement for what pointilist is supposed to become but does not describe the current state of the project.**

**pointilist** will be a standalone tool that allows you to either draw on your github contribution calender, or just have it filled automatically with random data.

There are already several tools that do this in one form or another, e.g.:

* [gitfitti](https://github.com/gelstudios/gitfiti)
* [github-contributions](https://github.com/IonicaBizau/github-contributions)
* [Git Draw](https://github.com/ben174/git-draw)
* [Badass](https://github.com/umayr/badass)

And even one from myself:

* [ghdecoy](https://github.com/tickelton/ghdecoy)

While all of these tool work well and fulfill a purpose I encountered certain shortcomings during my work on ghdecoy:

Some of the existing solutions require a multi step process to create the fake repository and push it to github (github-contributions, git-draw).

Others automate this process which leads to very weird constructs (python scripts generating shell scripts executing git commands, ... (gitfiti, ghdecoy)).

And finally all of them require an existing, working, properly configured git installation on the host they are to be run on.

**pointilist** tries to address these issues with the following approach:

* single step process: just run a single command line tool to randomize your graph, or create a custom pattern with the GUI tool and push to github with a single click.
* no external tools necessary: **pointilist** is going to be a pure python tool. No auxiliary scripts or git clients will be required.
* As a side effect this also leads to platform independence. **pointilist** will work on Windows just as well as on Linux (and possibly OSX, if i can get my hands on a system to test it).


If you are interested in the project, just check back here whenever you feel like it. As soon as a working version is available it will be announced here.

Also if you are interested in contributing, feel free to contact me at [tickelton@gmail.com](mailto:tickelton@gmail.com).

