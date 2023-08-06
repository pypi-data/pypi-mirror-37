# Wright Group Reference Library

This is a relatively simple tool to autofill a [google form](https://docs.google.com/forms/d/e/1FAIpQLSdXLhs4MCiCQ1Vaf0LXc8DKYvqI1hmD2T8iXjAFQO_C4dCHJA/viewform) which is then recorded into a [google spreadsheet](https://docs.google.com/spreadsheets/d/1YOjpePLLKy1xJsWKCsuzZ9uAsSNl90iUQlUJnytscO4/edit)

This tool can take a DOI and fill out many of the fields, or they can be overwritten by adding specific flags. (e.g. `-y` or `--year` to set the year field)

Most fields accept only one value (and the last given is preferred). Author and tags can be repeated arbitrarily many times (and the first and last authors will be extracted from the list given in order).

Difficult to acquire articles can be linked to with `--filelink` (which needs to be a link to a previously existing file accessible on the internet)



NOTE: Running this command does not record into the spreadsheet, it simply opens the browser with the fields filled out, you MUST click submit in the browser to actually record the entry.

## Example usage

```bash

$ wg-reflib # Just open the form, nothing entered
$ wg-reflib 10.1366/12-06657 # Prefill with entries from the given DOI
$ wg-reflib 10.1366/12-06657 -c Kyle # Also fill out the contributor field
```

## Help
```bash
$ wg-reflib --help
usage: wg-reflib [-h] [--contributor CONTRIBUTOR] [--key KEY]
                 [--author AUTHOR] [--title TITLE] [--year YEAR]
                 [--journal JOURNAL] [--tag TAG] [--url URL]
                 [--filelink FILELINK] [--notes NOTES]
                 [doi]

positional arguments:
  doi

optional arguments:
  -h, --help            show this help message and exit
  --contributor CONTRIBUTOR, -c CONTRIBUTOR
  --key KEY, -k KEY
  --author AUTHOR, -a AUTHOR
  --title TITLE, -T TITLE
  --year YEAR, -y YEAR
  --journal JOURNAL, -j JOURNAL
  --tag TAG, -t TAG
  --url URL, -u URL
  --filelink FILELINK, -l FILELINK
  --notes NOTES, -n NOTES
```


