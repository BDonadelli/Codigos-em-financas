

import numpy as np
import statsmodels.api as sm

# Example cointegrated series data (replace this with your actual data)
cointegrated_series = np.array([10.2, 11.5, 9.8, 10.9, 10.1, 9.6, 11.0, 10.7, 11.2, 9.9])

# Create lagged series
lagged_series = np.roll(cointegrated_series, shift=1)
lagged_series[0] = 0  # Replace the first value with 0

# Perform OLS regression
X = sm.add_constant(lagged_series)
model = sm.OLS(cointegrated_series, X).fit()

# Get the lambda estimate from the coefficient
lambda_estimate = -model.params[1]

print("Estimated Lambda (OLS):", lambda_estimate)
