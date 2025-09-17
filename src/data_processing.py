from sklearn.base import BaseEstimator, TransformerMixin

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
        X = X.drop("Neighborhood", axis=1,errors="ignore")
        return X
'''
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