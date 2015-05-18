//temporary file to be able to play with the data from jsdoc, without having to run jsdoc all the time
//uses the raw output as retrieved from the publish function in the template => db().stringify()
//
//
//
//


var pathlib = require('path');
var curDir = process.cwd();
var util = require('util');

var MODULE_NAMESPACE = 'module:';

function isModuleExports(doclet) {
    return doclet.longname && doclet.longname === doclet.name &&
        doclet.longname.indexOf(MODULE_NAMESPACE) === 0 && doclet.kind !== 'module';
}

/**
 * Find items in a TaffyDB database that match the specified key-value pairs.
 * @param {TAFFY} data The TaffyDB database to search.
 * @param {object|function} spec Key-value pairs to match against (for example,
 * `{ longname: 'foo' }`), or a function that returns `true` if a value matches or `false` if it
 * does not match.
 * @return {array<object>} The matching items.
 */
var find = exports.find = function(data, spec) {
    return data(spec).get();
};

/**
 * Retrieve all of the following types of members from a set of doclets:
 *
 * + Classes
 * + Externals
 * + Globals
 * + Mixins
 * + Modules
 * + Namespaces
 * + Events
 * @param {TAFFY} data The TaffyDB database to search.
 * @return {object} An object with `classes`, `externals`, `globals`, `mixins`, `modules`,
 * `events`, and `namespaces` properties. Each property contains an array of objects.
 */
var getMembers = function(data) {
    var members = {
        classes: find( data, {kind: 'class'} ),
        externals: find( data, {kind: 'external'} ),
        events: find( data, {kind: 'event'} ),
        globals: find(data, {
            kind: ['member', 'function', 'constant', 'typedef'],
            memberof: { isUndefined: true }
        }),
        mixins: find( data, {kind: 'mixin'} ),
        modules: find( data, {kind: 'module'} ),
        namespaces: find( data, {kind: 'namespace'} ),
        interfaces: find( data, {kind: 'interface'} )
    };

    // strip quotes from externals, since we allow quoted names that would normally indicate a
    // namespace hierarchy (as in `@external "jquery.fn"`)
    // TODO: we should probably be doing this for other types of symbols, here or elsewhere; see
    // jsdoc3/jsdoc#396
    members.externals = members.externals.map(function(doclet) {
        doclet.name = doclet.name.replace(/(^"|"$)/g, '');
        return doclet;
    });

    // functions that are also modules (as in `module.exports = function() {};`) are not globals
    members.globals = members.globals.filter(function(doclet) {
        return !isModuleExports(doclet);
    });

    return members;
};

function processIndividualClassv3(symbol) {

  var meta = symbol.meta;
  var name = symbol.name;
  var longName = symbol.longname;
  var methodNames = [];
  // The actual object is full of unnecessary crap, filter it out

  var classObj = {
    guid: symbol.___id,
    name: name,
    displayName: symbol.longname,
    objectType: 'symbol',
    filePath: pathlib.join(pathlib.relative(curDir, meta.path), meta.filename),

    isNamespace: (symbol.kind === 'namespace'),
    isPrivate: (symbol.access === 'private'),
    isStatic: (symbol.scope === 'static'),

    author: symbol.author,
    see: symbol.see,
    since: symbol.since,
    version: symbol.version,
    deprecated: symbol.deprecated,
    augments: symbol.augments,

    overview: symbol.classdesc,
    methods: [],
    properties: []
  };

  symbol.methods.forEach(function (m) {
    //if (m.memberof !== name && m.memberof !== longName) return;
    methodNames.push(m.name);
    classObj.methods.push({
      name: m.name,
      displayName: m.longname,
      objectType: 'method',

      isPrivate: (m.access === 'private'),
      isStatic: (m.scope === 'static'),

      author: m.author,
      see: m.see,
      since: m.since,
      version: m.version,
      deprecated: m.deprecated,
      augments: [],

      overview: m.description,
      exceptions: m.exceptions,
      returns: m.returns,
      params: m.params,

    })
  });

  // var methods = symbol.methods;
  // for (var i = 0, l = methods.length; i<l; i++) {

  //   var method = methods[i];

  //   if (method.memberOf !== classObj.name && method.memberOf !== classObj.displayName) {
  //     //print("Skipping "+method.name+", since it's a member of "+method.memberOf+", not "+classObj.name+" or "+classObj.displayName);
  //     continue;
  //   }

  //   classObj.methods.push({
  //     name: method.name,
  //     displayName: method.alias,
  //     objectType: 'method',

  //     isPrivate: method.isPrivate,
  //     isStatic: method.isStatic,

  //     author: method.author,
  //     see: method.see,
  //     since: method.since,
  //     version: method.version,
  //     deprecated: method.deprecated,
  //     augments: [],

  //     overview: method.desc,
  //     exceptions: method.exceptions,
  //     returns: method.returns,
  //     params: method.params

  //   });
  // }

  symbol.properties.forEach(function (p) {
    if (p.memberof !== name && p.memberof !== longName) return;
    //if (methodNames.indexOf(p) > -1) return; // don't include methods as properties
    classObj.properties.push({
      name: p.name,
      displayName: p.longname,
      objectType: 'property',

      propertyType: p.type,
      author: p.author,
      see: p.see,
      since: p.since,
      version: p.version,
      deprecated: p.deprecated,

      memberOf: p.memberof,
      overview: p.description,
      defaultValue: p.defaultValue,
      isConstant: (p.kind === 'constant'),
      isPrivate: (p.access === 'private'),
      original: p
    })
  });



  // var properties = symbol.properties;

  // for (var j = 0, len = properties.length; j<len; j++) {

  //   var property = properties[j];

  //   if (property.memberOf !== classObj.name && property.memberOf !== classObj.displayName) {
  //     //print("Skipping "+property.name+", since it's a property of "+method.memberOf+", not "+classObj.name+" or "+classObj.displayName);
  //     continue;
  //   }

  //   classObj.properties.push({
  //     name: property._name,
  //     displayName: property.alias,
  //     objectType: 'property',

  //     propertyType: property.type,
  //     author: property.author,
  //     see: property.see,
  //     since: property.since,
  //     version: property.version,
  //     deprecated: property.deprecated,

  //     memberOf: property.memberOf,
  //     overview: property.desc,
  //     defaultValue: property.defaultValue,
  //     isConstant: property.isConstant,
  //     isPrivate: property.isPrivate

  //   });
  // }

  return classObj;
}

util.log("Loading...")
var Taffy = require('./node_modules/jsdoc/node_modules/taffydb');
var raw = require('./out/raw.json');

var db = Taffy.taffy(raw);

util.log('starting the parsing, namespaces first');

var members = getMembers(db);
var classes = members.classes;
var processedSymbolSet = [];

// members.namespaces.filter(function (n) { return !n.memberof; }).forEach(function (n) {
//   util.log('namespace: ' + n.longname);
//   n.methods = db().filter({ kind: 'function', memberof: n.longname}).get();
//   n.properties = db().filter({ kind: 'member', memberof: n.longname}).get();
//   processIndividualClassv3(n);
// });

// members.namespaces.filter(function (n) { return !n.memberof; }).forEach(function (n) {
//   util.log('namespace: ' + n.longname);
//   n.methods = db().filter({ kind: 'function', memberof: n.longname}).get();
//   n.properties = db().filter({ kind: 'member', memberof: n.longname}).get();
//   n.properties = n.properties.filter(function (p) { // filter out existing classes
//     return !classes.some(function (c) {
//       return c.longname === p.longname;
//     });
//   });
//   // n.properties.forEach(function (p) {
//   //   if (classes.some(function (c) { return c.longname === p.longname; })) {
//   //     p.type = "Object";
//   //   }
//   // });
//   processedSymbolSet.push(processIndividualClassv3(n));
// });

// classes.forEach(function (c) {
//   util.log('class: ' + c.longname);
//   //c.events = members.events.filter({}  ) // there doesn't seem to be anything in events
//   c.methods = db().filter({ kind: 'function', memberof: c.longname }).get();
//   c.properties = db().filter({ kind: 'member', memberof: c.longname }).get();
//   processedSymbolSet.push(processIndividualClassv3(c));
// });

// we need to add the main namespaces and their properties and functions
var ctx = {
    members: members,
    db: db,
    classes: classes,
    symbols: processedSymbolSet
};


//require('fs').writeFileSync('scfixtures.json', JSON.stringify(processedSymbolSet));
require('repl').start(">>>").context.ctx = ctx;

//
//
//