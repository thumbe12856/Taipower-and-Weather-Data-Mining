# n_components: morning, afternoon, night
pca = PCA(n_components=1)

# Fit and transform the data to the model
reduced_data_pca = pca.fit_transform(northSupply)

# Inspect the shape
print("Shape of reduced_data_pca:", reduced_data_pca.shape)
print("---")

print("---")
print("PCA:")
print(reduced_data_pca)
