echo "--- init ---"

# ---- Venv
if [ ! -d venv ]
then
  python3.9 -m venv --copies venv>>/dev/null
  echo "+++ ./venv"
fi

# ---- Patch Venv
if [ ! -f venv/bin/patched.txt ]
then
  _app="$(pwd)"
  echo '
alias cli="'$_app'/cli"

if [ -f '$_app'/app/.env ]
then
    export $(cat '$_app'/app/.env | sed "s/#.*//g" | xargs)
fi' >> venv/bin/activate
  chmod 0775 venv/bin/activate
  touch venv/bin/patched.txt
  echo "+++  ...patched"
fi
