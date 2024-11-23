
# Install H2O
# pip install requests tabulate
# pip uninstall h2o
# pip install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o

import h2o
h2o.init() # localhost:54321

# obtain a high-level summary of the cluster status
# h2o.cluster_info()

print("\n\n\n")
print(h2o.ls())

# # import the prostate data
# df = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/prostate/prostate.csv.zip")
# colmeans = df.mean()
# print(colmeans)


from h2o.estimators.glm import H2OGeneralizedLinearEstimator

# import the prostate data
fr = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/prostate/prostate.csv.zip")

# make the 2nd column a factor
fr[1] = fr[1].asfactor()

# specify the model
m = H2OGeneralizedLinearEstimator(family="binomial")

# <class 'h2o.estimators.glm.H2OGeneralizedLinearEstimator'>
print(m.__class__)

# train the model
m.train(x=fr.names[2:], y="CAPSULE", training_frame=fr)

# print the model to screen
print(m)

