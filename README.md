# Favorlang Dictionary Website

## Build

```sh
python3 build.py
```

This command builds the website into the root dir


## Developer's Notes

### Edit Website

Do not edit the html files in the root dir. They are automaticaally generated.
The content of the website is defined in `config.yml` and the markdown files in `content/`. Relations between markdown files and page content are defined in `config.yml`.

To modify the HTML structure, template, or Vue app, edit the corresponding files in `templates/`.


### Dictionary Data

The data needed for building this website are processed and served in another repo [`favorlanglang/dict`](https://github.com/favorlanglang/dict). To update the data, please refer to [`favorlanglang/dict`](https://github.com/favorlanglang/dict).
