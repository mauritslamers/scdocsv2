#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
#
# The Original Code is Komodo code.
#
# The Initial Developer of the Original Code is ActiveState Software Inc.
# Portions created by ActiveState Software Inc are Copyright (C) 2000-2008
# ActiveState Software Inc. All Rights Reserved.
#
# Contributor(s):
#   ActiveState Software Inc
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
#
# Contributers (aka Blame):
#  - Todd Whiteman
#

"""Generate Ext JavaScript library CIX for use in Komodo.

    Command line tool that parses up Ext's own javascript library to
    produce a Komodo CIX file. Works by grabbing a specified copy of ext online
    code and then parsing the JavaScript files to produce "ext.cix".

    Requirements:
      * cElementTree    (http://effbot.org/downloads/#cElementTree)

    Website download from:
      * http://extjs.com/download
"""

import os
import sys

#sys.path.append('/Users/maurits/Development/sproutcore/sclang/KomodoEdit/src/codeintel/lib/codeintel2')

import glob
import urllib
import zipfile
import json
from cStringIO import StringIO
from optparse import OptionParser

sys.path.append('/Users/maurits/Development/sproutcore/sclang/KomodoEdit/src/codeintel/lib')
sys.path.append('/Users/maurits/Library/Application Support/Sublime Text 3/Packages/SublimeCodeIntel/arch')
sys.path.append('/Users/maurits/Library/Application Support/Sublime Text 3/Packages/SublimeCodeIntel/libs')
#sys.path.append('/Users/maurits/Development/sproutcore/sclang/KomodoEdit/src/silvercity/PySilverCity')


#sys.path.append('/Users/maurits/Library/Application Support/Sublime Text 3/Packages/SublimeCodeIntel/libs/codeintel2')
print sys.path
#sys.path.reverse().append('/Users/maurits/Development/sproutcore/sclang/KomodoEdit/src/codeintel/lib/codeintel2').reverse()

from codeintel2.gencix_utils import *

library_name = "SproutCore"
library_version = "1.11.0"
library_version_major_minor = ".".join(library_version.split(".")[0:2])
#library_info = ext_data[library_version]



# def generateCIXFromXML(root):
#     # Find all main doc namespaces
#     cix = createCixRoot(name="%s_v%s" % (library_name,
#                                          library_version.replace(".", "")),
#                         description="%s JavaScript library - version %s" % (
#                                          library_name, library_version))
#     cixfile = createCixFile(cix, "", lang="JavaScript")
#     cixmodule = createCixModule(cixfile,
#                                 "%s_v%s" % (library_name,
#                                             library_version.replace(".", "")),
#                                 lang="JavaScript")


#     # For jQuery, everything is an operation using the jQuery object.
#     # Create this jQuery object now, everything will be assigned to it!
#     cixscope = createCixClass(cixmodule, "jQuery")
#     ctor = createCixFunction(cixscope, "jQuery", attributes="__ctor__")
#     ctor.set("signature", "jQuery(arg <String|Element|Array of Elements|Function|jQuery>, context <Element|jQuery>) -> jQuery")
#     ctor.set("doc", """\
# String: Create DOM elements on-the-fly from the provided String of raw HTML.
# Element|Array: Wrap jQuery functionality around single or multiple DOM Element(s).
# Function: To be executed when the DOM document has finished loading.

# If 'context' is specified, accepts a string containing a CSS or basic XPath selector
# which is then used to match a set of elements.""")

#     # "$" is a reference to the jQuery class.
#     alt_scope = createCixVariable(cixmodule, "$", )
#     alt_scope.set("citdl", "jQuery")

#     # Add the methods.
#     for categoryElem in root.getchildren():
#         if categoryElem.tag != "cat":
#             print "Unknown category tag: %r" % (categoryElem.tag, )
#             continue
#         category = categoryElem.get("value")
#         print "%r" % (category, )
#         for subCategoryElem in categoryElem.getchildren():
#             if subCategoryElem.tag != "subcat":
#                 print "Unknown subcategory tag: %r" % (subCategoryElem.tag, )
#                 continue
#             subcategory = subCategoryElem.get("value")
#             print "  %r" % (subcategory, )
#             for element in subCategoryElem.getchildren():
#                 elementname = element.get("name")
#                 scope = cixscope
#                 if element.tag in ("function", "property"):
#                     print "    %r: %r" % (element.tag, element.get("name"), )
#                     sp = elementname.split(".")
#                     if sp[0] == "jQuery":
#                         if len(sp) == 1:
#                             print "      ** Ignoring this function: %r **" % (sp[0], )
#                             continue
#                         sp = sp[1:]
#                     elementname = sp[0]
#                     if len(sp) > 1:
#                         # Example navigator.language
#                         if len(sp) > 2:
#                             raise "Namespace too long: %r" % elementname
#                         subname = sp[0]
#                         if subname not in cixscope.names:
#                             print "      ** Ignoring this function: %r **" % (subname, )
#                             #print sorted(cixscope.names.keys())
#                             continue
#                         scope = cixscope.names[subname]
#                         elementname = sp[1]

#                     if elementname in scope.names:
#                         print "      ** Element already exists in scope, ignoring **"

#                     isFunction = False
#                     if element.tag == "property":
#                         createCixMethod = createCixVariable
#                     else:
#                         isFunction = True
#                         createCixMethod = createCixFunction
#                     cixelement = createCixMethod(scope, elementname)

#                     # Add the documentation.
#                     descnodes = element.findall('./desc')
#                     if descnodes:
#                         if len(descnodes) != 1:
#                             raise "Too many docnodes for: %r" % elementname
#                         if descnodes[0].text:
#                             setCixDoc(cixelement, descnodes[0].text, parse=True)

#                     if element.get("private") is not None:
#                         cixelement.set("attributes", "private __hidden__")

#                     citdl = standardizeJSType(element.get("return"))
#                     if citdl:
#                         if citdl in ("Any", ):
#                             citdl = None
#                         #else:
#                         #    print "        citdl: %r" % (citdl, )
#                     if isFunction:
#                         if citdl:
#                             cixelement.set("returns", citdl)
#                         # See if there are arguments.
#                         params = element.findall('./params')
#                         param_names = [ x.get("name") for x in params ]
#                         signature = "%s(%s)" % (elementname, ", ".join(param_names))
#                         if citdl:
#                             signature += " -> %s" % (citdl, )
#                         setCixSignature(cixelement, signature)
#                         for param in params:
#                             addCixArgument(cixelement,
#                                            param.get("name"),
#                                            standardizeJSType(param.get("type")),
#                                            param.findall("desc")[0].text)
#                     else:
#                         # It's a variable.
#                         if citdl:
#                             cixelement.set("citdl", citdl)
#                 elif element.tag == "selector":
#                     pass    # Not much we can do here...
#                 else:
#                     print "Unknown tag: %r" % (element.tag, )
#     return cix

# we need to read from json

def parseToCix(data):
  cix = createCixRoot(name="%s" % (library_name),
                      description="%s JavaScript library - version %s" % (
                                       library_name, library_version))
  cixfile = createCixFile(cix, "", lang="JavaScript")
  cixmodule = createCixModule(cixfile,
                              "%s_v%s" % (library_name,
                                          library_version.replace(".", "")),
                              lang="JavaScript")

  topLevelClasses = {}

  for el in data:
    #top level el is always a class or namespace
    if el['isNamespace'] is True:
      cixscope = createCixClass(cixmodule, el['displayName'])
      print "creating namespace %s" % (el['displayName'], )
      topLevelClasses[el['displayName']] = cixscope
    else:
      topLevelC = topLevelClasses[el['displayName'].split(".")[0]]
      cixscope = createCixClass(topLevelC, el['name'])
      #also create an object property on the top level, perhaps that solves the issue with second level
      #cixelement = createCixVariable(topLevelC, el['name'])
      #cixelement.set("citdl", "Object")
      print "creating class %s" % (el['displayName'], )
      if 'augments' in el.keys():
        cixscope.set("classrefs", " ".join(el['augments']))

    methods = el['methods']
    props = el['properties']
    for m in methods:
      cixelement = createCixFunction(cixscope, m['name'])
      if 'overview' in m.keys():
        setCixDoc(cixelement, m['overview'], parse=True) #not sure whether it needs to be parsed, and what that parsing is
      if 'isPrivate' in m.keys():
        if m['isPrivate'] is True:
          cixelement.set("attributes", "private __hidden__")
        else :
          if 'isStatic' in m.keys():
            if m['isStatic'] is True:
              if m['name'] == 'create':
                #cixelement.set("attributes", "__ctor__ __classmethod__")
                cixelement.set("attributes", "__classmethod__")
              else:
                cixelement.set("attributes", "__classmethod__")
            else :
              cixelement.set("attributes", "__instancemethod__")

      citdl = None
      if 'returns' in m.keys():
        if len(m['returns']) > 0:
          if 'type' in m['returns'][0].keys():
            citdl = standardizeJSType(m['returns'][0]['type']['names'][0])

      if citdl:
        if citdl in ("Any", ):
          citdl = None
      if citdl:
        cixelement.set("returns", citdl)
      if 'params' in m.keys():
        for x in m['params']:
          if 'name' in x.keys():
            param_names = [ x['name'] for x in m['params'] ]
            signature = "%s(%s)" % (m['name'], ", ".join(param_names))
            if citdl:
              signature += " -> %s" % (citdl, )
            setCixSignature(cixelement, signature)

        for param in m['params']:
            paramdesc = None
            paramtype = None
            paramname = None
            if 'description' in param.keys():
              paramdesc = param['description']
            if 'type' in param.keys():
              paramtype = param['type']['names'][0]
            if 'name' in param.keys():
              paramname = param['name']
            if paramname is not None:
              addCixArgument(cixelement,
                             paramname,
                             standardizeJSType(paramtype),
                             paramdesc)

    for p in props:
      cixelement = createCixVariable(cixscope, p['name'])
      if 'overview' in p.keys():
        setCixDoc(cixelement, p['overview'], parse=True) #not sure whether it needs to be parsed, and what that parsing is
      if 'isPrivate' in p.keys():
        if p['isPrivate'] is True:
          cixelement.set("attributes", "private __hidden__")
      citdl = None
      if 'propertyType' in p.keys():
        citdl = standardizeJSType(p['propertyType']['names'][0])
      if citdl:
          if citdl in ("Any", ):
              citdl = None
      if citdl:
        cixelement.set("citdl", citdl)
      if 'isConstant' in p.keys():
        if p['isConstant'] is True:
          cixelement.set("attributes", "__const__")

  return cix

def updateCix(filename, content):
    file(filename, "wb").write(content.encode("utf-8"))

def main(cix_filename):
    cix = createCixRoot(name="%s_%s" % (library_name,
                                        library_version.replace(".", "")),
                        description="%s JavaScript framework - version %s" % (
                                         library_name, library_version))

    data = json.load(file("scfixtures.json"))
    cixtree = parseToCix(data)
    #file(cix_filename, "w").write(get_cix_string(cixtree))

    #files = getFilesFromWebpage()
    #files = getFiles()
    # jscile = JavaScriptCiler(Manager(), "SproutCore")
    # for path, (dirname, filename, content) in files.items():
    #     dir_split = dirname.split("/")
    #     print "filename: %r" % (os.path.join(dirname, filename))
    #     jscile.path = filename
    #     jscile.scan_puretext(content.decode("utf-8"), updateAllScopeNames=False)

    # jscile.cile.updateAllScopeNames()
    # jscile.cile.name = "%s_%s" % (library_name.lower(),
    #                               library_version.replace(".", ""))
    # # Convert the Javascript to CIX, content goes into cix element
    # jscile.convertToElementTreeFile(cix, "JavaScript")
    # Write out the tree
    updateCix(cix_filename, get_cix_string(cixtree))

# When run from command line
if __name__ == '__main__':
    import logging
    logging.basicConfig()

    parser = OptionParser()
    parser.add_option("-u", "--update", dest="update_inline",
                      action="store_true", help="edit the real scc cix file")
    (opts, args) = parser.parse_args()

    #cix_filename = "%s_%s.cix" % (library_name.lower(), library_version_major_minor)
    cix_filename = "sproutcore.cix"
    if opts.update_inline:
        scriptpath = os.path.dirname(sys.argv[0])
        if not scriptpath:
            scriptpath = "."
        scriptpath = os.path.abspath(scriptpath)

        cix_directory = scriptpath
        # Get main codeintel directory
        for i in range(4):
            cix_directory = os.path.dirname(cix_directory)
        cix_filename = os.path.join(cix_directory, "lib", "codeintel2", "catalogs", cix_filename)
    main(cix_filename)
