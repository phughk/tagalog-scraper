# Tagalog Scraper

A web scraper for the tagalog dictionary from [Pinoy Dictionary](https://tagalog.pinoydictionary.com).
You can find a structured scrape results file under 

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
