# Social Media Analytics Pipeline


## Usage

Ensure `.env` file is complete.

```
pipenv install
pipenv run python get_data.py
```
The data is output as a pickle binary: `./data/reddit.serial`


## Install 

Direct install github with: `pipenv install -e git+https://github.com/IMTorgOpenDataTools/GraphiPy.git@master#egg=graphipy`
Add `requirements.txt` to `.libs/` folder and: `xargs -rd\\n pipenv install < .libs/requirements.txt`


## Test

...