# 
# 
# t-SNE Scikit-Learn
# https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
# 


from sklearn import datasets
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt


# Load MNIST Dataset
digits = datasets.load_digits()
_, axes = plt.subplots(nrows=1, ncols=4, figsize=(10, 3))
for ax, image, label in zip(axes, digits.images, digits.target):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation="nearest")
    ax.set_title("Training: %i" % label)

plt.show()

# t_SNE representation
X = digits.images.reshape(digits.images.shape[0], -1)
print(X.shape)
n_components = digits.images[0].flatten().shape[0]
embeddings = TSNE().fit_transform(X)
print(embeddings.shape)


# Plotting
colormap = {
    0: (255, 0, 0),       # Rojo
    1: (0, 255, 0),       # Verde
    2: (0, 0, 255),       # Azul
    3: (255, 255, 0),     # Amarillo
    4: (255, 0, 255),     # Magenta
    5: (0, 255, 255),     # Cian
    6: (128, 0, 128),     # Púrpura
    7: (255, 165, 0),     # Naranja
    8: (128, 128, 0),     # Oliva
    9: (128, 128, 128),   # Gris
}
colormap = {key: tuple(value / 255 for value in rgb) for key, rgb in colormap.items()}
colors = [ colormap[t] for t in digits.target ]
plt.scatter(embeddings[:, 0], embeddings[:, 1], c= colors)
plt.show()


