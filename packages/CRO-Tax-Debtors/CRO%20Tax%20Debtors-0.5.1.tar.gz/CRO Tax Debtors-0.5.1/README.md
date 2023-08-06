<h1>Cro Tax Debtors</h1>

[![PyPI version](https://badge.fury.io/py/CRO-Tax-Debtors.svg)](https://badge.fury.io/py/CRO-Tax-Debtors)

<p>Parse and search data from Croatian Tax Debtors website.</p>

<h2>Installation</h2>


```
pip install cro-tax-debtors
```

<h2>CLI</h2>

<p>file_path parameter is a path to yaml file with the source definition.<br/>
Check websites.yaml for definition structure.</p>

```
Usage: crotaxdebtors [OPTIONS] COMMAND [ARGS]...

Options:
  -f, --file_path FILENAME  Input YAML file
  --help                    Show this message and exit.

Commands:
  delete
  find
  parse
```

<p>Parse data from website:</p>

```
Usage: crotaxdebtors parse [OPTIONS]

Options:
  -p, --print_in_terminal  Print in terminal
  --help                   Show this message and exit.
```

<p>Search through scraped data:</p>

```
Usage: crotaxdebtors find [OPTIONS]

Options:
  -n, --name TEXT  Name of the debtor
  --help           Show this message and exit.
```

<p>Delete all data:</p>

```
Usage: crotaxdebtors delete [OPTIONS]

Options:
  --help           Show this message and exit.
```
