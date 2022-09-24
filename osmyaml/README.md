
Checkout code

create a virtual environment (venv) `python3 -m venv venv`

activate it `source bin/activate` (Linux)
			`venv\Scripts\activate` (Windows)

install requirements using pip `pip install -r requirements.txt`

run `pip install .`, this will install in current venv (and make the 'vleer' binary available)
under windows, install sox (https://sourceforge.net/projects/sox/) and add to your PATH

(to remove (to reinstall), from within your activated venv: `pip remove osmyaml`)

Now you should be able to run

```
osmyaml --help

python -m osmyaml --help

# to see both layername and properties and queries
python -m osmyaml 

# to SKIP de queries:
python -m osmyaml -q

```

to deactivate venv, run 
		`deactivate` (Linux)
		`venv\Scripts\deactivate.bat`  (Windows)