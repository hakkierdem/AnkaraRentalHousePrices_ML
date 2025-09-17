from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
import pandas as pd
import joblib


file_path = "data/ankarahouseprices_withcoordinates.csv"
df = pd.read_csv(file_path,index_col=0)

X = df.drop("Price",axis=1)
y = df["Price"]

'''class FeatureEngineering(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=10, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = None
        
    def fit(self, X, y=None):
        # KMeans ile coğrafi kümeleri öğreniyoruz
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state, n_init=10)
        self.kmeans.fit(X[['latitude','longitude']])
        return self
    
    def transform(self, X):
        X = X.copy()
        # Feature engineering
        X["total_room"] = X["Room"] + X["Saloon"]
        X['cluster_id'] = self.kmeans.predict(X[['latitude','longitude']])
        # Kullanılmayacak sütunları düşüyoruz
        X = X.drop(["Neighborhood","longitude"], axis=1,errors="ignore")
        return X'''

class FeatureEngineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        
        X["total_room"] = X["Room"] + X["Saloon"]
        
        X = X.drop(["Neighborhood", "longitude", "latitude"], axis=1, errors="ignore")
        return X



categorical_features = ["County"]
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough' 
)

pipeline = Pipeline(steps=[
    ("feature_engineering", FeatureEngineering()),
    ("preprocessor", preprocessor),
    ("model", GradientBoostingRegressor(
        subsample = 0.9,
        n_estimators = 900,
        min_samples_split = 17,
        min_samples_leaf = 2,
        max_features = None,
        max_depth = 4,
        learning_rate = 0.01
    ))
])

kf = KFold(n_splits=5, shuffle=True, random_state=42)
splits = list(kf.split(X))
best_train_index, best_test_index = splits[1]

X_train, y_train = X.iloc[best_train_index], y.iloc[best_train_index]
X_test, y_test = X.iloc[best_test_index], y.iloc[best_test_index]

pipeline.fit(X_train, y_train)

joblib.dump(pipeline, "ankara_house_rent_pipeline_simple.pkl")
