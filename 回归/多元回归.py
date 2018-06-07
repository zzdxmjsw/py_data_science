from sklearn.linear_model import LinearRegression
X = [[6, 2], [8, 1], [10, 0], [14, 2], [18, 0]]
y = [[7], [9], [13], [17.5], [18]]
model = LinearRegression()
model.fit(X, y)
X_test = [[8, 2], [9, 0], [11, 2], [16, 2], [12, 0]]
y_test = [[11], [8.5], [15], [18], [11]]
predictions = model.predict(X_test)
for i, prediction in enumerate(predictions):
    print('Predicted: %s, Target: %s' % (prediction, y_test[i]))
print('R-squared: %.2f' % model.score(X_test, y_test))


# ================
import pandas as pd
import numpy as np
import statsmodels.api as sm

df_adv=pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv',index_col=0)
X=df_adv[['TV','radio']]
y=df_adv['sales']

X=sm.add_constant(X)
est=sm.OLS(y,X).fit()
est.summary()

# =====================
import statsmodels.formula.api as smf
est=smf.ols(formula='sales ~ TV + radio',data=df_adv).fit()