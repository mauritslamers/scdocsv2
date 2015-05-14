/*jshint node:true*/

/*
purpose of this script is to walk through all files in sproutcore/frameworks and find the following:

- move @private to the bottom of the doc block
- move @namespace to the bottom of the doc block
- move @override to the bottom of the doc block
- rename @property without parameters to @member
- change @param {[type]...} to @param {...[type]}
 */


var fslib = require('fs');
var pathlib = require('path');

function handleFile (filepath) {
  var c = fslib.readFileSync(filepath).toString();
  var lines = c.split("\n");
  var ret = [];
  var inComment = false;
  var indent = "";
  var atPrivateOpen = "/** @private";
  var commentOpen = "/**";
  var commentClose = "*/";
  var atPrivateOpenLength = atPrivateOpen.length;
  var privateFound = false;
  var namespaceFound = false;
  var overrideFound = false;
  lines.forEach(function (l) {
    var commentOpenIndex = l.indexOf(commentOpen);
    var commentCloseIndex = l.indexOf(commentClose);
    if (!inComment && commentOpenIndex > -1) {
      indent = l.substr(0, commentOpenIndex);
      inComment = true;
    }
    // we need to check whether this line contains @private
    if (inComment) {
      if (l.indexOf("@private") > -1) { // found in current line
        privateFound = true;
        // remove it at current location
        l = l.replace("@private", "");
      }
      if (l.indexOf("@namespace") > -1) {
        namespaceFound = true;
        l = l.replace("@namespace", "");
      }
      if (l.indexOf("@override") > -1) {
        overrideFound = true;
        l = l.replace("@override", "");
      }
      // we also fix @param {String...} or equivalent here, as in jsdoc3 it needs to be ...String
      var r = /@param[\s\S]+\{(.+)?\.\.\.\}/;
      var m = r.exec(l);
      if (m) {
        l = l.replace(m[1] + "...", "..." + m[1]);
      }
      // we also try to fix @property, which seems to have become @member
      var atPropIndex = l.indexOf("@property");
      // @property should have parameters, which need to be in {}, so we check for a { existing on the same
      // line after @property. If it doesn't exist, we replace @property with @member
      if (atPropIndex > -1 && l.indexOf("{") < atPropIndex) {
        l = l.replace("@property", "@member");
      }
      // also fix things like @param {Array|String} => @param {(Array|String)}
      if (l.indexOf("@param") > -1 && l.indexOf("|") > -1) {
        var openBraceIndex = l.indexOf("{");
        var closeBraceIndex = l.indexOf("}");
        l = l.slice(0, openBraceIndex + 1) + "(" + l.slice(openBraceIndex + 1, closeBraceIndex) + ")" + l.slice(closeBraceIndex);
      }
      if (commentCloseIndex > -1) { // comment close is in this line
        if (commentOpenIndex > -1) { // everything on one line
          if (privateFound) {
            commentCloseIndex = l.indexOf(commentClose);
            l = l.slice(0, commentCloseIndex) + "@private " + l.slice(commentCloseIndex);
            privateFound = false;
          }
          if (namespaceFound) {
            commentCloseIndex = l.indexOf(commentClose);
            l = l.slice(0, commentCloseIndex) + "@namespace " + l.slice(commentCloseIndex);
            namespaceFound = false;
          }
          if (overrideFound) {
            commentCloseIndex = l.indexOf(commentClose);
            l = l.slice(0, commentCloseIndex) + "@override " + l.slice(commentCloseIndex);
            overrideFound = false;
          }
        }
        else { // multiline
          // we need to add a few lines before the current one
          if (privateFound) {
            ret.push(indent + "  @private");
            privateFound = false;
          }
          if (namespaceFound) {
            ret.push(indent + "  @namespace");
            namespaceFound = false;
          }
          if (overrideFound) {
            ret.push(indent + "  @override");
            overrideFound = false;
          }
        }
        inComment = false;
      } // end if comment close
    } // end if inComment
    ret.push(l);
  });
  fslib.writeFileSync(filepath, ret.join("\n"));
}

function handleDir (dir) {
  var c = fslib.readdirSync(dir);
  c.forEach(function (f) {
    var fn = pathlib.join(dir, f);
    var stat = fslib.statSync(fn);
    if (stat.isFile() && pathlib.extname(fn) === ".js") {
      console.log('handling file: ' + fn);
      handleFile(fn);
    }
    else if (stat.isDirectory()) {
      console.log('handling dir: ' + fn);
      handleDir(fn);
    }
  });
}

// now the part where we walk the filesystem
var baseDir = "./sproutcore/frameworks";
handleDir(baseDir);