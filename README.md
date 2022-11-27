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


# Labgrow.io
___

### Course
- name
- slug
- description
- position
- is_active
- price
- currency ( $ USD )

### Chapter
- name
- slug
- description
- position
- is_active
- course_id

### Lecture
- name
- slug
- description
- position
- is_active
- course_id
- chapter_id = null

### User Course
- user_id
- course_id
- progress
- access (none, opened, all)



# QASE.IO
___
### Project
- name
- code
- users

### Custom fields

### Test Suite

### Test Case

### Test Plan

### Test Run

### Test Run Results