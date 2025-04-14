# Tagalog Scraper

A web scraper for the tagalog dictionary from [Pinoy Dictionary](https://tagalog.pinoydictionary.com).
You can find a structured scrape results file under [split\_definitions.json](split_definitions.json).

The dataset isn't perfect, since the parsing of the data is flawed in some places.

Note, that further changes to the dataset should be manual and committed to the repository - feel free to open a PR.

## Scrape

```
poetry run scrapy crawl tagalog -o output.json
```

## Scrape debug repl

```
poetry run scrapy shell https://tagalog.pinoydictionary.com/list/a/
```

## Download Spacy NLP data

```
poetry run python -m spacy download en_core_web_sm
```

## Run normalisation

```
poetry run python process_definitions.py
```
