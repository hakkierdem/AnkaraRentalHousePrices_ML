import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


df = pd.read_csv("added_coordinates.csv")

none_rows = df[df['latitude'].isnull() | df['longitude'].isnull()]
print(type(none_rows))


df.loc[df["Neighborhood"] == "Esenboğa Merkez Mahallesi","Neighborhood"] = "Esenboğa Mahallesi"
df.loc[df["Neighborhood"] == "Arka Topraklık Mahallesi","Neighborhood"] = "Arka Topraklık"
df.loc[df["Neighborhood"] == "Seğmenler Mahallesi","Neighborhood"] = "Seğmenler"
df.loc[df["Neighborhood"] == "Alcı Mahallesi","Neighborhood"] = "Alcı"

fixing_none_rows = df[df['latitude'].isnull() | df['longitude'].isnull()]
print(fixing_none_rows)


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


fixing_none_rows[['latitude', 'longitude']] = fixing_none_rows.apply(get_coordinates, axis=1)
df.update(fixing_none_rows)


df.loc[df["Neighborhood"] == "Arka Topraklık","Neighborhood"] = "Arka Topraklık Mahallesi"
df.loc[df["Neighborhood"] == "Seğmenler","Neighborhood"] = "Seğmenler Mahallesi"
df.loc[df["Neighborhood"] == "Alcı","Neighborhood"] = "Alcı Mahallesi"

print(df[['latitude', 'longitude']].isna().sum())

df.to_csv("ankarahouseprices_withcoordinates.csv", index=False)



