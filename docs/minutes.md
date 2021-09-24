# Uploading meeting minutes

Meeting minutes are exported (from Google Docs etc) in PDF format for practical reasons. To upload them to the website, they must be renamed to `YYYY-MM-DD_Minutes_n.pdf`, where:
 - `YYYY` is the full year
 - `MM` and `DD` are the 0-padded month and day number when the meeting took place
 - `n` is the meeting number **of this committee**

For example, the minutes from first committee meeting of the 2021/22 committee should be named `2021-03-09_Minutes_1.pdf`. Other documents, such as the constitution, may be uploaded, but they must also start with `YYYY-MM-DD-` so they are in order. The website will consider everything between the date and the `.pdf` extension to be the title of the document, and will replace underscores (_) with spaces, so that `2021-03-09_Minutes_1.pdf` becomes `Minutes 1`. Once renamed, minutes should be placed in the correct committee directory in `static/minutes/`.

