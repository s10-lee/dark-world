# ...
___
Directory
  
```shell
mkdir sso.artel.works
cd sso.artel.works
```

Git clone
```shell
git clone git@github.com:s10-lee/sso.artel.works.git .
```

Virtual environment
```shell
python -m venv venv
source venv/bin/activate
```

`.env` vars
```shell
cd app
cp .env.example .env
vi .env
...
source .env
```
## DB
Init and migrate
```shell
air init -t src.settings.ORM --location ./db/migrations
air init-db
air rotate-keys
```
