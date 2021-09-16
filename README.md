Directory
  
```
mkdir dark-world && cd dark-world
```

Git clone
```shell
git clone git@github.com:s10-lee/dark-world.git .
```

`.env` vars
```shell
cd app
cp app/.env.example app/.env
vi app/.env
# ...
source app/.env
# or inenv
```

Virtual environment
```shell
python3 -m venv --copies venv
source venv/bin/activate
```


## DB
Init and migrate
```shell
air init -t src.settings.ORM --location ./db/migrations
air init-db
air rotate-keys
air add-user -u admin -p 1qw2er3ty -e admin@artel.works
```
