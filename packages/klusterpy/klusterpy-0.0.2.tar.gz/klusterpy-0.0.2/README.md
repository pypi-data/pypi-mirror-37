# KlusterPy
KlusterPy is a simple machine learning library that provides clustering algorithm such as 
[K-Means](https://en.wikipedia.org/wiki/K-means_clustering), 
[K-Medoids](https://en.wikipedia.org/wiki/K-medoids), 
[DBSCAN](https://en.wikipedia.org/wiki/DBSCAN), and 
[Agglomerative Clustering](https://en.wikipedia.org/wiki/Hierarchical_clustering). 

# Dependencies
1. NumPy
2. Python >= 3

# Installation
```
pip install klusterpy
```

# Example Code
```python
from klusterpy.cluster.dbscan import DBSCAN
from sklearn import datasets
import numpy as np
import pandas as pd

iris_data = datasets.load_iris()
iris_df = pd.DataFrame(data=np.c_[iris_data['data']], columns=iris_data['feature_names'])

dbscan = DBSCAN(epsilon=0.42, min_pts=5).fit(iris_df.values)
dbscan.labels
```

# Contributors
| [<img src="https://avatars0.githubusercontent.com/u/22999475?s=400&v=4" width=60px style="border-radius: 50%;"><br /><sub>Dewita Sonya<br />13515021</sub>](https://github.com/dewitast) | [<img src="https://avatars0.githubusercontent.com/u/20073050?s=400&u=881e4c44f50167fb8b447e608d8234d9adf369df&v=4" width=60px style="border-radius: 50%;"><br /><sub>Erick Wijaya<br />13515057</sub>](https://github.com/wijayaerick) | [<img src="https://avatars0.githubusercontent.com/u/26085823?s=400&v=4" width=60px style="border-radius: 50%;"><br /><sub>Kezia Suhendra<br />13515063</sub>](https://github.com/keziasuhendra) |
| :---: | :---: | :---: |
