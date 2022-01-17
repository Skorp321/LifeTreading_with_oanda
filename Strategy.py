import pandas as pd
import tpqoa

api = tpqoa.tpqoa('oanda.cfg')
api.get_instruments() # Get aveilabel instruments
api.get_history(instrument='EUR_USD', start='2021-03-29', end='2021-03-31',
                granularity='M1', price='M', localize=False)
api.stream_data('EUR_USD', stop=20)
