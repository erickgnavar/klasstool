# Klasstool

# Development setup

# Django

- Install dependencies `pip install -r requirements/dev.txt`
- Run development server `./manage.py runserver`

## Elm

- Execute `elm-make src/Session.elm --debug --output=elm.js` inside `elm` folder to compile elm source
- Create static file `mkdir -p klasstool/static/js/`
- Make a symbolic link to the compiled file `ln -s $(pwd)/elm/elm.js $(pwd)/static/js/`

# Production setup

- Install dependencies `pip install -r requirements/prod.txt`
- Run worker server `./manage.py runworker`
- Run interface server `daphne config.asgi:channel_layer`
