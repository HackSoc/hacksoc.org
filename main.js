const Handlebars = require('handlebars');
const fse = require('fs-extra');
const path = require('path');

const outDir = 'html'; // TODO cannonicalize

fse.mkdirpSync(outDir);
fse.emptyDirSync(outDir);

compileTemplate = template => Handlebars.compile(template.toString('UTF-8'));

function regularDir(dirname, wrapperTemplate) {
    return fse.readdir(dirname).then(listing => {
        /**
         * {String[]} listing: filenames in regular/
         */
        let promises = listing //.filter(fn => /.*\.html/.test(fn)) // Filter to only HTML files
            .map(filename => 
                fse.readFile(path.join(dirname, filename))// open each file
                .then(content => {
                    /**
                     * Takes content and applies the wraper template to it
                     * {Buffer} content: contents of `filename`
                     */
                    // TODO seperate YAML header
                    return wrapperTemplate({
                        body: content.toString('UTF-8'),
                        title: filename.replace(/\.html$/i,'') // TODO title from YAML
                    })
                })
                .then(html => fse.writeFile(path.join(outDir, filename), html))
            );
        return Promise.all(promises)

    })
}

Promise.resolve(
    fse.readFile('templates/wrapper.handlebars') // Read the template
        .then(compileTemplate) // compile it
        .then(wrapperTemplate => regularDir('regular', wrapperTemplate)) // pass it to the Promise to apply it to all in regular/
).then(() => {console.log(`Writen regular files!`)})
.catch(console.error);

fse.copySync('static', path.join(outDir, 'static'))
console.log(`Copied static/ directory!`)

