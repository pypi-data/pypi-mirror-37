![](http://i.imgur.com/S9hlqg0.png)

[Full Documentation](https://bitbucket.org/tvoverlord/tv-overlord/wiki)

![](https://badge.fury.io/py/tvoverlord.svg)

TV Overlord is a **semi automatic** command line tool to download and
manage TV shows from newsgroups or bittorent. It will download nzb files
or magnet links.

It searches multiple sites simultaneously and combines the results into
one list to select from.

TV Overlord keeps track of which shows have been downloaded and what
shows are available to download.

For each new episode of a tv show you are tracking, you are given a list
of possible downloads to choose. If you use a torrent search provider, a
magnet link is passed to the default bittorent client. If it is an NZB
search, an NZB file is placed in a folder that is configured in the
configuration file.

For torrent files, you can also have your shows organized after
downloading. If you use transmission or deluge, those clients can be
configured to call a script when each torrent is complete. This script
will extract the video file from the downloaded folder, rename it, and
put it in a separate folder organized into sub folders named for each tv
show.

There are several bittorent search providers and two NZB search
providers and new ones can be added fairly easily. See the search
providers
[README.org](https://bitbucket.org/tvoverlord/tv-overlord/src/master/tvoverlord/search_providers/README.org),
or by making a feature request in issues or a pull request.

#### Why semi automatic

Semi automatic means that you manually run it and select from a list
each episode you want. The reason for this is that not all torrents
follow a naming convention that is parsable, especially for more obscure
shows. So instead of writing a ton of code to try and figure out
information about an episode, I'll use the parser built into my brain.
Also I like that it runs when I like, its light weight, and there are no
background processes.


Features
--------

-   Keeps track of [dowloaded shows](
    https://bitbucket.org/tvoverlord/tv-overlord/wiki/Command-line-reference#list-available).
-   Show a list of shows [available for download](
    https://bitbucket.org/tvoverlord/tv-overlord/wiki/Command-line-reference#download).
-   Gives you a list of torrents or nzbs you can choose from.
-   You can [add new shows](
    https://bitbucket.org/tvoverlord/tv-overlord/wiki/Command-line-reference#add-new)
    from the command line.
-   Will [display info](https://bitbucket.org/tvoverlord/tv-overlord/wiki/Command-line-reference#info)
    showing what show will be next and how many days till broadcast.
    This list can be filtered and sorted in various ways.
-   Displays a [calendar of upcoming episodes](
    https://bitbucket.org/tvoverlord/tv-overlord/wiki/Command-line-reference#calender).
    You can also specify a range of days to display, past or future.
-   The ability to [query download history](
    https://bitbucket.org/tvoverlord/tv-overlord/wiki/Command-line-reference#history)
    and re-start a download.
-   [Organize](https://bitbucket.org/tvoverlord/tv-overlord/wiki/Rename-tags)
    you tv show downloads into folders.
-   Switch between [multiple configs](
    https://bitbucket.org/tvoverlord/tv-overlord/wiki/Config-file#multiple-configs).


Screenshots
-----------
Choose a file to download.

![Downloading screenshot](https://bytebucket.org/tvoverlord/tv-overlord/wiki/images/download-frame.gif)


Show what is available to download.

![Show new shows](https://bytebucket.org/tvoverlord/tv-overlord/wiki/images/showmissing.gif)


Install
-------

Requirements

Python 3.4 (or higher) -- on Linux, OSX, or Windows

Install

TV Overlord is a python 3 application and can be installed via pip3.

``` {.example}
sudo pip3 install tvoverlord
```

After its installed, you run it by typing:

``` {.example}
tvol --help
```

The first time it's run, it will create the appropriate config dir for
your platform and put the database and config.ini there.

After that you can start to use it, type:

``` {.example}
tvol add 'Doctor Who'
```

If this is the wrong show, try again but add the year:

``` {.example}
tvol add 'Doctor Who 2005'
```

Then

``` {.example}
tvol download
```

To get help for each command, you can use:

``` {.example}
tvol download --help
tvol add --help
# etc...
```

If you use Bash as your shell, you can have tab completions. Add this to
your .bashrc file:

``` {.bash}
eval "$(_TVOL_COMPLETE=source tvol)"
```

Setup the post download script

If you use Transmission or Deluge as your bittorent client there is a
script for each called transmission~done~ and deluge~done~. These will
take the episode that was downloaded and copy it to a folder where it
will be organized by how the template string in config.ini is
configured.

[Setup and configure post download scripts details](
https://bitbucket.org/tvoverlord/tv-overlord/wiki/Post-download-scripts)

Configure
---------

TV Overlord looks for the database and `config.ini` in the appropriate
directory for your platform. When tvoverlord is first run, it will
create a tvoverlord directory there.

OSX
:   `~/Library/Application Support/tvoverlord`

Linux
:   `~/.config/tvoverlord`

Windows
:   `C:\Users\<USERNAME>\AppData\Roaming\tvoverlord`

[Config file details](
https://bitbucket.org/tvoverlord/tv-overlord/wiki/Config-file)

Command line reference
----------------------

[Command line reference](
https://bitbucket.org/tvoverlord/tv-overlord/wiki/Command-line-reference)

Usefull shell commands
----------------------

This will show all the available shows for the current week from Sun to
Sat.

``` {.example}
tvol calendar --days -$(date '+%u'),7 -x
```

To bulk import shows from a csv file (showname can't have a comma in
it).

``` {.bash}
while IFS=, read showname season episode; do
    tvol add --bulk "${showname}" --season=${season} --episode=${episode}
done < allshows.csv
```

If using [multiple configs](
https://bitbucket.org/tvoverlord/tv-overlord/wiki/Config-file#multiple-configs):

``` {.bash}
for config in '' 'nzb' 'torrent'; do
    echo "Using $config config"
    tvol --config=$config list
    tvol --config=$config download
done
```
