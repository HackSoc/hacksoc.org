const Handlebars = require('handlebars');
const fse = require('fs-extra');
const path = require('path');
const yaml = require('js-yaml');
const docmatter = require('docmatter');

const outDir = 'html'; // TODO cannonicalize

fse.mkdirpSync(outDir);
fse.emptyDirSync(outDir);

compileTemplate = template => Handlebars.compile(template.toString('UTF-8'));

function regularDir(dirname, wrapperTemplate, globalContext) {
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
                     * content begins with a YAML header.
                     * {Buffer} content: contents of `filename`
                     */

                    let matter = docmatter(content.toString('UTF-8'));

                    return wrapperTemplate(Object.assign({ // Merge this object with the properties in context.yaml
                        body: matter.body,
                        title: filename.replace(/\.html$/i,'') // TODO title from YAML
                    }, globalContext, yaml.safeLoad(matter.header)))
                })
                .then(html => fse.writeFile(path.join(outDir, filename), html))
            );
        return Promise.all(promises)

    })
}

function getGlobalContext() {
    return fse.readFile('templates/context.yaml')
        .then(contents => {
            /**
             * {Buffer} contents: the contents of the YAML file
             */
            return yaml.safeLoad(contents.toString('UTF-8'));
        })
}

getGlobalContext().then(globalContext => {
    
    Promise.resolve(
        fse.readFile('templates/wrapper.handlebars') // Read the template
            .then(compileTemplate) // compile it
            .then(wrapperTemplate => regularDir('regular', wrapperTemplate,globalContext)) // pass it to the Promise to apply it to all in regular/
    ).then(() => {console.log(`Writen regular files!`)})
    .catch(console.error);
    
    fse.copySync('static', path.join(outDir, 'static'))
    console.log(`Copied static/ directory!`)

})

