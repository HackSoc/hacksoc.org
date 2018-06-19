const Handlebars = require('handlebars');
const fse = require('fs-extra');
const path = require('path');
const yaml = require('js-yaml');
const docmatter = require('docmatter');
const Markdown = new require('markdown-it')({
    html: true, // enable HTML in Markdown
}).use(require('markdown-it-highlightjs'), {auto: true, code: false})

const outDir = 'html'; // TODO cannonicalize

fse.mkdirpSync(outDir);
fse.emptyDirSync(outDir);

compileTemplate = template => Handlebars.compile(template.toString('UTF-8'));

/**
 * 
 * @param {string} dirname The directory to read HTML content from
 * @param {Handlebars.TemplateDelegate} wrapperTemplate Handlebars template to apply to the content
 * @param {Object} globalContext Context to use for every page
 * @returns {Promise} no resolve value, wraps around a Promise.all of all of the files
 */
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
                        body: matter.body
                    }, globalContext, yaml.safeLoad(matter.header)))
                })
                .then(html => fse.writeFile(path.join(outDir, filename), html))
            );
        return Promise.all(promises)
    })
}

/**
 * 
 * @param {string} dirname name to find Markdown source files
 * @param {Handbars.TemplateDelegate} serverTemplate Handlebars template to make the page
 * @param {Object} globalContext Misc context (navbar, servers, etc)
 * @returns {Promise} wraps around a Promise.all for each file in `dirname`
 */
function servers(dirname, serverTemplate, globalContext) {
    return fse.readdir(dirname).then(listing => {
        /**
         * {String[]} listing: filenames in servers/
         */
        let promises = listing.map(filename => 
                fse.readFile(path.join(dirname,filename))
                .then(content => {
                    /**
                     * {Buffer} content: contents of `filename`
                     */
                    let matter = docmatter(content.toString('UTF-8'));

                    return serverTemplate(
                        Object.assign({
                            body: Markdown.render(matter.body)
                        }, globalContext, yaml.safeLoad(matter.header))
                    );
                }).then(html => fse.writeFile(path.join(outDir, dirname, filename.replace(/\.md$/i,".html")), html))
                
            )
        return fse.mkdirp(path.join(outDir, dirname)).then(Promise.all(promises));
    })
}

/**
 * Generates an index of a directories PDF files, and copies them to the HTML folder.
 * @param {string} dirname Directory to find .PDF files in
 * @param {string} filename Filename of this page
 * @param {Handlebars.TemplateDelegate} wrapperTemplate Handlebars template to apply to the whole page
 * @param {Handlebars.TemplateDelegate} minuteTemplate Template to use on the listing
 * @param {Object} globalContext Context to use for every page
 */
function minutes(dirname, filename, wrapperTemplate, minuteTemplate, globalContext) {
    return fse.readdir(dirname).then(listing => {
        let minutes = listing.filter(l => /\.pdf$/.test(l))
                        .map(fn => {
                            let m = /^(\d{4}-\d\d-\d\d)-([a-z0-9 ]+)\.pdf$/i.exec(fn);
                            return {
                                url: path.join(dirname, fn),
                                meeting: m[2],
                                date: m[1],
                                date_t: new Date(m[1])
                            }
                        }).sort((f1, f2) => Math.sign(f1.date_t - f2.date_t));
                        // Has the potential to have meeting on the same date in the wrong order
                        // Cross that bridge when etc

        fse.writeFile(path.join(outDir, filename), 
            wrapperTemplate(Object.assign({
                body: minuteTemplate(minutes),
                title: "Minutes"
            }, globalContext))
        ).then(fse.copy(dirname, path.join(outDir, dirname)))
    })
}

/**
 * @param {Object} results any previous results that this object carries on
 */
function readNews(results) {
    return new Promise((resolve, reject) => {
        let obj = {}
        
        /* TODO
         * read news/
         * foreach:
         *   map listing => content => html => news object
         * return under news
         */

        resolve(Object.assign(obj,results));
    });
}


/**
 * @returns {Promise<Object>} Resolves to the global context object
 */
function getGlobalContext() {
    return fse.readFile('templates/context.yaml')
        .then(contents => {
            /**
             * {Buffer} contents: the contents of the YAML file
             */
            return yaml.safeLoad(contents.toString('UTF-8'));
        })
}

// Main stuff here.       
let p_mkOutDir = fse.mkdirp(outDir)
    .then(() => fse.emptyDir(outDir));

let p_copyStatic = fse.copy('static', path.join(outDir, 'static'))
    .then(console.log("Copied static files!"));
    
    p_mkOutDir.then(() => p_copyStatic);

    let hljsStylesheet = 'solarized-light';
    p_copyStatic.then(() => fse.copyFile(`node_modules/highlight.js/styles/${hljsStylesheet}.css`, path.join(outDir, 'static', 'highlight.css')));

let p_contextAndTemplates = Promise.all(
    [
        getGlobalContext(),
        fse.readFile('templates/wrapper.handlebars').then(compileTemplate),
        fse.readFile('templates/minutes.handlebars').then(compileTemplate),
        fse.readFile('templates/newslist.handlebars').then(compileTemplate),
        fse.readFile('templates/server.handlebars').then(compileTemplate)
    ])
    .then(results => ({
        globalContext: results[0],
        wrapperTemplate: results[1],
        minutesTemplate: results[2],
        newslistTemplate: results[3],
        serverTemplate: results[4]
    }))

    
    p_contextAndTemplates.then(obj => regularDir('regular',obj.wrapperTemplate, obj.globalContext))
        .then(()=>console.log("Written regular files!"))
        .catch(console.log);
    p_contextAndTemplates.then(obj => minutes('minutes', 'minutes.html', obj.wrapperTemplate, obj.minutesTemplate, obj.globalContext))
        .then(()=>console.log("Written minutes files!"))
        .catch(console.log);

    p_contextAndTemplates.then(obj => servers('servers', obj.serverTemplate, obj.globalContext))
        .then(()=>console.log("Written server files!"))
        .catch(console.log)

    

p_mkOutDir.then(() => p_contextAndTemplates);
