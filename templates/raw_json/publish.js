var fs = require('fs');
var util = require('util');
var path = require('path');
var repl = require('repl');

exports.publish = function (db, opts) {
  //util.log('contents: ' + util.inspect(db().stringify()));
  // util.log('opts: ' + util.inspect(opts));
  try {
    fs.mkdirSync(path.join(process.cwd(), opts.destination));
  }
  catch (e) {
    if (e.code !== 'EEXIST') throw e;
  }
  fs.writeFileSync(path.join(process.cwd(), opts.destination, 'raw.json'), db().stringify());
}