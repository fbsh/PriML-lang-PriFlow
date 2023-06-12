import unittest
from hogwildsgd import HogWildRegressor
import scipy.sparse
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


class TestHogwild(unittest.TestCase):

    def test_work(self):
        X = scipy.sparse.random(20000,10, density=.2).toarray()  # Guarantees sparse grad updates
        poly = PolynomialFeatures(degree=50, interaction_only=True)
        X = poly.fit_transform(X)
        
        n_features = X.shape[1]
        real_w = np.random.uniform(0,1,size=(n_features,1))
        y = np.dot(X,real_w)

        hw = HogWildRegressor(n_jobs = 16, 
                              n_epochs = 5,
                              batch_size = 1, 
                              chunk_size = 32,
                              lr = .001,  
                              generator=None,
                              verbose=2,
                              loss='squared_loss')
        hw = hw.fit(X,y)

        y_hat = hw.predict(X)
        y = y.reshape((len(y),))
        score = np.mean(abs(y-y_hat))
        self.assertTrue(score < 1) 


if __name__ == '__main__':
    unittest.main()
