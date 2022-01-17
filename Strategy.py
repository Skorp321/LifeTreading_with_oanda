import pandas as pd
import tpqoa
from datetime import datetime


# api = tpqoa.tpqoa('oanda.cfg')
# api.get_instruments()  # Get aveilabel instruments
# api.get_history(instrument='EUR_USD', start='2021-03-29', end='2021-03-31',
#                granularity='M1', price='M', localize=False)
# api.stream_data("EUR_USD", stop=20)


class CloneClass(tpqoa.tpqoa):

    def __init__(self, config_file, instrument, bar_lenght):
        super().__init__(config_file)
        self.instrument = instrument
        self.bar_lenght = pd.to_timedelta(bar_lenght)
        self.tick_data = pd.DataFrame()
        self.last_bar = pd.to_datetime(datetime.utcnow()).tz_localize("UTC")

    def on_success(self, time, bid, ask):
        print(self.ticks, end=" ")

        # Collect and store tics data
        recent_tick = pd.to_datetime(time)
        df = pd.DataFrame({self.instrument: (bid + ask) / 2},
                          index=[recent_tick])
        self.tick_data = self.tick_data.append(df)

        # If a time longer than the bar length has elapsed between last and the
        # most recent tick
        if recent_tick - self.last_bar > self.bar_lenght:
            self.resample_and_join()

    def resample_and_join(self):
        self.data = self.tick_data.resample(self.bar_lenght, label="right") \
                        .last().ffill().iloc[:-1]
        self.last_bar = self.data.index[-1] # Update time of last full bar


api = CloneClass("oanda.cfg", "5s")
api.stream_data("EUR_USD", stop=20)

print(api.data)
