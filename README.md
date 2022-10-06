# Social Media Analytics Pipeline


## Usage

Ensure `.env` file is complete.

Modify `config/_constants.py > subreddits` to ensure all are listed.

```
pipenv install
pipenv run python main.py
```

The data is output as a pickle binary: `./data/reddit.serial`


## Install 

Direct install github with: `pipenv install -e git+https://github.com/IMTorgOpenDataTools/GraphiPy.git@master#egg=graphipy`
Add `requirements.txt` to `.libs/` folder and: `xargs -rd\\n pipenv install < .libs/requirements.txt`


## Test

...



## TODO


* add subreddits: r/Banks, 
  - r/WallStreetBets, r/Stocks, r/Bogleheads, r/Economics
  - r/Money, r/HomeLoans, r/CreditCards, r/CreditUnions, r/Credit, rLoans, r/Borrow, r/Banking, r/realestateinvesting, r/StudentLoans, r/povertyfinance, r/AskCarSales
  - rFinance, r/PersonalFinance, r/Investing, r/financialindependence, r/PFtools, r/FinancialPlanning, r/Budget, r/Frugal, r/Investing
  - r/BitCoin, r/btc, r/CryptoCurrency, r/CryptoMarkets