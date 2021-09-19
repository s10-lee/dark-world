echo "--- init ---"

# ---- cli
if [ ! -f cli ]
then
  cp app/cli/cmd.py ./cli
  chmod 0775 ./cli
  echo "+++ ./cli"
fi


# ---- Venv
if [ ! -d venv ]
then
  python3 -m venv --copies venv >> /dev/null
  echo "+++ ./venv"
fi

# ---- Patch Venv
if [ ! -f venv/bin/patched.txt ]
then
  _app="$(pwd)"
  echo '
alias cli="'$_app'/cli"

if [ -f '$_app'/.env ]
then
    export $(cat '$_app'/.env | sed "s/#.*//g" | xargs)
fi' >> venv/bin/activate
  chmod 0775 venv/bin/activate
  touch venv/bin/patched.txt
  echo "+++  ...patched"
fi
