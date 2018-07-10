const Handlebars = require('handlebars');
const fse = require('fs-extra');
const path = require('path');
const yaml = require('js-yaml');
const docmatter = require('docmatter');
const Markdown = new require('markdown-it')({
    html: true, // enable HTML in Markdown
    typographer: true // have some nice pretty quotes
}).use(require('markdown-it-highlightjs'), {auto: true, code: false})

const outDir = 'html'; // TODO canonicalise?

fse.mkdirpSync(outDir);
fse.emptyDirSync(outDir);

compileTemplate = template => Handlebars.compile(template.toString('UTF-8'));

/**
 * Wraps HTML documents found in dirname with wrapperTemplate and writes them to outDir
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
    }).catch(err => {
        console.log(`Error processing regular directory ${dirname}/ - ${err}`);
    });
}

/**
 * Renders Markdown server READMEs found in dirname, wrap with template and write to outDir/dirname/
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
    }).catch(err => {
        console.log(`Error processing server directory ${dirname}/ - ${err}`);
    });
}

/**
 * Formats a date "Month DD, YYYY"
 * @param {Date} date
 * @returns {String} 
 */
function formatDate(date) {
    return date.toLocaleDateString("en-UK", {month:"long", day:"2-digit", year:"numeric"});
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
    }).catch(err => {
        console.log(`Error processing minutes directory ${dirname}/ - ${err}`);
    });
}

/**
 * Reads Markdown news articles from dirname and returns an array of news objects
 * @param {Object} results any previous results that this object carries on
 * @param {String} dirname directory to search for news
 * @return {Promise<Object>} `results` joined with news: {posts: Object[]}
 */
function readNews(results, dirname='news') {
    const re_date = /^(\d{4})-([01]\d)-([0-3]\d)/;
    return new Promise((resolve, reject) => {
        fse.readdir(dirname).then(listing => {
            let promises = listing.map(fn => fse.readFile(path.join(dirname,fn))
                .then(content => {
                    let matter = docmatter(content.toString('UTF-8'));
                    let header = yaml.safeLoad(matter.header);
                    let match_date = re_date.exec(fn);

                    let htBody = Markdown.render(matter.body);
                    let htMatch = /^(<p>[^]*?<\/p>)/i.exec(htBody.trim());
                    let date_t = new Date(match_date[0])
                    return {
                        body: htBody,
                        title: header.title,
                        date: formatDate(date_t),
                        date_t: date_t,
                        url: `${dirname}/${fn.replace(/\.md$/i,'.html')}`,
                        excerpt: htMatch[1]
                    };
                })
            );
            return Promise.all(promises).then(news => {
                let obj = {
                    news: {posts: news.sort((a,b) => Math.sign(b.date_t - a.date_t))}
                };
                let finalResult = Object.assign(obj, results)
                resolve(finalResult);
            })
        }).catch(err => {
            console.log(`Error processing news directory ${dirname}/ - ${err}`);
        });
    });
}

/**
 * Writes news.html and news articles from news object
 * @param {Object} results object including globalContext, news, and template objects
 * @param {String} dirname folder to write news to
 */
function writeNews(results, dirname='news') {
    // huh, stuff gets real simple when it's sync
    fse.mkdirpSync(path.join(outDir, dirname));

    let promises = results.news.posts.map(newsObj =>
        fse.writeFile(path.join(outDir, newsObj.url), 
            results.wrapperTemplate(
                Object.assign({
                    body: results.articleTemplate({
                        title: newsObj.title,
                        date: newsObj.date,
                        body: newsObj.body
                    }),
                    title: newsObj.title,                    
                }, results.globalContext)
            )
        )
    )
    promises.push(fse.writeFile(path.join(outDir, 'news.html'),
        results.wrapperTemplate(Object.assign({
            title: "News",
            body: results.newslistTemplate(results.news)
        }, results.globalContext))
    ))
    return Promise.all(promises);
}

/**
 * Writes the index page
 * @param {Object} results object including globalContext, news, and template objects.
 */
function writeIndex(results) {
    return fse.writeFile(path.join(outDir, 'index.html'), results.wrapperTemplate(
        Object.assign({
            body: results.indexTemplate(Object.assign({
                newslist: results.newslistTemplate({
                    posts: results.news.posts.slice(0,5),
                    link: true
                }) // first 5 news articles (if present)
            }, results.globalContext))
            // no title, handled by wrapper.handlebars
        }, results.globalContext)
    ));
}

/**
 * Reads context.yaml and returns its contents as an object
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
        fse.readFile('templates/server.handlebars').then(compileTemplate),
        fse.readFile('templates/article.handlebars').then(compileTemplate),
        fse.readFile('templates/index.handlebars').then(compileTemplate)
    ])
    .then(results => ({
        globalContext: results[0],
        wrapperTemplate: results[1],
        minutesTemplate: results[2],
        newslistTemplate: results[3],
        serverTemplate: results[4],
        articleTemplate: results[5],
        indexTemplate: results[6]
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

    p_contextAndTemplates.then(obj => {
        let p_news = readNews(obj, 'news');
        p_news.then(writeNews).then(()=>console.log("Writen news!"));
        p_news.then(writeIndex).then(()=>console.log("Writen index!"));
    });
    

p_mkOutDir.then(() => p_contextAndTemplates);
