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
```shell
aerich init -t app.config.settings.ORM --location app/db/migrations
aerich init-db
cli apikey
cli user -u admin -p 1qw2er3ty -e admin@dark.works
```
