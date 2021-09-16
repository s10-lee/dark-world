# ------------------------ #
#        WARNING           #
#   do not run in prod !   #
#                          #
# ------------------------ #

air init -t src.settings.ORM --location ./db/migrations
air init-db
air rotate-keys
air add-user -u admin -p 1qw2er3ty -e s10@artel.works
