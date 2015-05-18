This is a first attempt trying to make sproutcore use jsdoc v3 instead of jsdoc toolkit v2.4.0n.
At the same time I am trying to create a code intelligence file which can be used with SublimeCodeIntel,
as well as Komodo Edit and Komodo IDE.
You'll need to check out the sproutcore repo in ./sproutcore, and use the team/mauritslamers/jsdocv3 branch.

How it sort of currently works: when using jsdoc with the templates/raw_json template, it will write a complete dump of
the taffydb database containing all info jsdoc parsed in ./out/raw.json.
This is currently done to save time in not having to parse the entire SC code for small or larger fixes.

The parserawjson.js file loads this into a new instance of the taffydb, and parses it into a similar json structure as the original sc_fixture template would.
The sc_to_cix.py is a python script modelled after the jquery script included with KomodoEdit which parses the jquery xml documentation into a cix file. In order to run this script you need python, as well as having SublimeCodeIntel installed, as it uses python libraries from this package. The sc_to_cix.py script needs a reference to the absolute path of SublimeCodeIntel, so in order to run it change the path in is according to your system / location.

TODO:
- perhaps at some point port the gencix_utils library to nodejs, to get rid of the python dependency.
- It turns out the KomodoEdit source code needs to be around, as the sc_to_cix.py script runs into errors
  when the Sublime gencix_tools are used.
- At the moment only class methods seem to be supported, as I haven't been able to have the return types
and instances recognized properly.

## How to get code intel for SproutCore in

### Sublime Text 3

1. First install package control (if you don't already use it),
2. install the SublimeCodeIntel package.
3. Copy the sproutcore.cix file into the libs/codeintel2/catalogs folder in the SublimeCodeIntel package.
   The SublimeCodeIntel package can be found on a Mac at
   ~/Library/Application Support/Sublime Text 3/Packages/SublimeCodeIntel
4. Open the SublimeCodeIntel User preferences (Preferences > Package Settings > SublimeCodeIntel > Settings - User) and
  put the following when it is empty:
  ```
{
  "codeintel_language_settings": {
        "JavaScript": {
            "codeintel_scan_exclude_dir": ["/build/", "/min/", "/frameworks/sproutcore/", "/node_modules/", "/tmp/"],
            "codeintel_selected_catalogs": ["jQuery", "SproutCore"]
        }
    }]
}
  ```
You can of course add more paths to the codeintel_scan_exclude_dir.
I added the /frameworks/sproutcore/ because I almost always have sproutcore in the project folder.

### Sublime Text 2

The approach for ST2 is the same as for ST3, but I found that SublimeCodeIntel makes Sublime2
so slow that it is hardly usable.

### KomodoEdit / KomodoIDE

In the Preferences, under Code Intelligence, add the sproutcore.cix file as an API catalog. You might
have to restart KomodoEdit/IDE in order for the catalog to be visible in the list. As soon as it is visible,
make sure it is selected.


Then start typing :)
