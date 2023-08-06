from doi2bib import crossref
from pybtex.database.input import bibtex

import argparse
import sys
import webbrowser
from urllib import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('doi', nargs='?')
    parser.add_argument('--contributor', '-c')
    parser.add_argument('--key', '-k')
    parser.add_argument('--author', '-a', action='append')
    parser.add_argument('--title', '-T')
    parser.add_argument('--year', '-y', type=int)
    parser.add_argument('--journal', '-j')
    parser.add_argument('--tag', '-t', action='append')
    parser.add_argument('--url', '-u')
    parser.add_argument('--filelink', '-l')
    parser.add_argument('--notes', '-n')

    args = parser.parse_args()
    print(args)

    doi = args.doi
    contributor = args.contributor
    key = args.key
    authors = args.author
    title = args.title
    year = args.year
    journal = args.journal
    tags = args.tag
    url_field = args.url
    link_to_file = args.filelink
    notes = args.notes

    if doi:
        _, bib = crossref.get_bib(doi)
        bib = bibtex.Parser().parse_string(bib)
        key_ = bib.entries.keys()[0]
        bib = bib.entries[key_].fields

        if key is None:
            try:
                key = key_
            except:
                pass
        if authors is None:
            try:
                authors = bib['author'].split(' and ')
            except:
                pass
        if title is None:
            try:
                title = bib['title']
            except:
                pass
        if year is None:
            try:
                year = bib['year']
            except:
                pass
        if journal is None:
            try:
                journal = bib['journal']
            except:
                pass
        if url_field is None:
            try:
                url_field = bib['url']
            except:
                pass
        
    first_auth = last_auth = None
    if authors and len(authors) > 0:
        first_auth = authors[0]
        last_auth = authors[-1]
    if tags is None:
        tags = []

    url = (
        f"https://docs.google.com/forms/d/e/"
        f"1FAIpQLSdXLhs4MCiCQ1Vaf0LXc8DKYvqI1hmD2T8iXjAFQO_C4dCHJA"
        f"/viewform?usp=pp_url"
    )

    if contributor:
        url += f"&entry.943569882={parse.quote_plus(contributor)}"
    if key:
        url += f"&entry.2144633199={parse.quote_plus(key)}"
    if doi:
        url += f"&entry.2114556682={parse.quote_plus(doi)}"
    if first_auth:
        url += f"&entry.419048641={parse.quote_plus(first_auth)}"
    if last_auth:
        url += f"&entry.1319066450={parse.quote_plus(last_auth)}"
    if title:
        url += f"&entry.2105662805={parse.quote_plus(title)}"
    if year:
        url += f"&entry.824207115={parse.quote_plus(year)}"
    if journal:
        url += f"&entry.1879241245={parse.quote_plus(journal)}"

    for tag in tags:
        url += f"&entry.466618267={parse.quote_plus(tag)}"
    # TODO: support other option in tags
    #    url += f"&entry.466618267=__other_option__"
    #    url += f"&entry.466618267.other_option_response=other,+more"

    if authors:
        authors = ' and '.join(authors)
        url += f"&entry.1250982696={parse.quote_plus(authors)}"
    if url_field:
        url += f"&entry.341399538={parse.quote_plus(url_field)}"
    # TODO: support uploading files directly
    if link_to_file:
        url += f"&entry.997100911={parse.quote_plus(link_to_file)}"
    if notes:
        url += f"&entry.1573030049={parse.quote_plus(notes)}"

    webbrowser.open(url)

try:

    import gooey
    @Gooey
    def gui():
        main()
except:
    pass


if __name__ == "__main__":
    main()
