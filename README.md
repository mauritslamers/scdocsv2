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
- Add the namespaces (most specifically the SC namespace) to the parserawjson.js
- Add the namespace parsing to sc_to_cix.py
- perhaps at some point port the gencix_utils library to nodejs, to get rid of the python dependency.