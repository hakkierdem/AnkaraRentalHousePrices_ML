import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df = pd.read_csv("ankara_house_prices.csv")

geolocator = Nominatim(user_agent="my_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def get_coordinates(row):
    try:
        location = geocode(f"{row['Neighborhood']}, {row['County']}, Ankara, Türkiye",timeout = 10)
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Hata: {row['Neighborhood']}, {row['County']} -> {e}")
        return pd.Series([None, None])


df[['latitude', 'longitude']] = df.apply(get_coordinates, axis=1)


print(df.head())
print(df[['latitude', 'longitude']].isna().sum())


df.to_csv("added_cooridantes.csv", index=False)