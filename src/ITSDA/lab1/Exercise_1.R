######################################################
#                     EXERCISE 1                     #
######################################################
library(xts)

# Step 1: Generate a semestral multivariate time series with 'ts'
set.seed(123)  # for reproducibility
num_years <- 10
num_variables <- 5

# Regularly distributed multivariative time series with ts
data_matrix <- matrix(rnorm(num_years * 2 * num_variables), ncol = num_variables)
colnames(data_matrix) <- paste0("Var", 1:num_variables)
ts_multivariate <- ts(data_matrix, start = 2000, frequency = 2)
print(ts_multivariate)

# Irregularly sampled multivariate time series with 'xts'
set.seed(456)
random_dates <- sort(sample(seq(as.Date("2022-01-01"), as.Date("2022-12-31"), by = "days"), 20))

# Create a matrix of random values for 5 variables
xts_data <- matrix(rnorm(length(random_dates) * num_variables), ncol = num_variables)
colnames(xts_data) <- paste0("Var", 1:num_variables)
xts_multivariate <- xts(xts_data, order.by = random_dates)
print(xts_multivariate)


######################################################
#                     EXERCISE 2                     #
######################################################
# The DFT converts a time series from the time domain to the frequency domain. 
# It represents the series as a sum of sinusoidal components, each characterized by:
# Amplitude: How strong the frequency is in the data.
# Phase: The offset of the sine wave from zero.
# Frequency: The number of oscillations per unit time.
# 
# Why is DFT Non-Data-Adaptive?
# The transformation is predefined and does not depend on the data.
# It always decomposes the series into sinusoidal components regardless of whether such patterns exist in the data.
# 

install.packages("TSrepr")
library(TSrepr)

# Load the souvenir time series
souvenir <- scan("http://robjhyndman.com/tsdldata/data/fancy.dat")
souvenir_ts <- ts(souvenir, frequency=12, start=c(1987,1))
print(souvenir_ts)
plot.ts(souvenir_ts)

# Apply DFT to souvenirtimeseries
dft_ts <- repr_dft(souvenir_ts, coef = 20)
print(dft_ts)

plot(souvenir_ts, col = "blue", lwd = 2, main = "Original vs Reconstructed Time Series", ylab = "Sales")
lines(dft_ts , col = "red", lwd = 2)
legend("topright", legend = c("Original", "Reconstructed (10 Coefficients)"), col = c("blue", "red"), lwd = 2)


######################################################
#                     EXERCISE 3                     #
######################################################
# Apply SAX with default parameters
souvenir_ts_znorm <- (souvenir_ts - mean(souvenir_ts)) / sd(souvenir_ts)

segments_0 <- 2  # `q` value for souvenir_sax_0
segments_1 <- 5  # `q` value for souvenir_sax_1
segments_2 <- 2  # `q` value for souvenir_sax_2

# Compute SAX representations
souvenir_sax_0 <- repr_sax(souvenir_ts_znorm, a = 6, q = 2, eps = 0.01)
souvenir_sax_1 <- repr_sax(souvenir_ts_znorm, a = 3, q = 5)
souvenir_sax_2 <- repr_sax(souvenir_ts_znorm, a = 10, q = 2)

# Print SAX representations
cat("SAX with Alphabet Size 6,  q = 2:\n", souvenir_sax_0, "\n")
cat("SAX with Alphabet Size 3,  q = 5:\n", souvenir_sax_1, "\n")
cat("SAX with Alphabet Size 10, q = 2:\n", souvenir_sax_2, "\n")

