main_help = """
Analysis and Statistics
    confmat      - Generates a confusion matrix from a set of predictions.
    divide       - Divide values in a table by another.
    max          - Returns a vector containing the maximum value for each column in a matrix.
    mean         - Returns a vector containing the mean/average value for each column in a matrix.
    median       - Returns a vector containing the median value for each column in a matrix.
    min          - Returns a vector containing the minimum value for each column in a matrix.
    pca          - Maps data to a lower dimensional space with using principal component analysis.
    pearson      - Calculates the pearson correlation coefficient with a cutoff at a given threshold.
    percentile   - Returns a vector containing the percentile for each column in a vector.
    roc          - Calculates the receiver operating characteristic (ROC) curve for a binary classification.
    sd           - Returns a vector containing the standard deviation of values within each column in a matrix.
    shape        - Find the shape of a matrix
    spearman     - Calculates the Spearman's rank correlation coefficient.
Descriptors
    ncomp        - Calculates the n-composition of a FASTA sequence (default: amino acid composition).
    summary      - Summarizes a matrix column-wise.
    trans        - Calculates the percent transitions of a single character or group to another character or group.
Manipulation
    aggregate    - Aggregate values into rows based on key-columns.
    append       - Append values to a given matrix row or column wise.
    chop         - Removes rows from a matrix.
    concat       - Concatenates two matrices at a given axis
    creatematrix - Create matrices, either of m rows and n columns filled with values v or special e.g. identity matrices, etc.
    format       - Convert between various vector formats.
    join         - Joins two or more matrices on one or more columns.
    slice        - Manipulate matrix columns
    sort         - Sort a vector based on columns given by keys
    transpose    - Transposes a matrix.
    unique       - Returns unique rows in a matrix.
    vrep         - Returns rows which contain a given set of elements.
Math
    add          - Adds matrices or scalars to a matrix.
    determinant  - Calculates the determinant for square matrices.
    dotproduct   - Calculates the dot product of two vectors.
    eigenvalues  - Calculates the eigenvalues of a matrix. The order is the same as in the function eigenvectors
    eigenvec     - Calculates the eigen vectors of a given matrix. The order is the same as in the function eigenvalues
    inverse      - Calculates the inverse matrix for square matrices. (Must be invertible)
    multiply     - Multiplies matrices via matrix-multiplication or scalars.
    subtract     - Subtracts matrices or scalars from a matrix.
    sum          - Sums the columns of a matrix
Normalization
    medpolish    - Normalizes a matrix via median polish normalization.
    quantnorm    - Normalizes a matrix via quantile normalization normalization.
    zscorenorm   - Normalizes a matrix via z-score normalization normalization.
Supervised Learning
    linreg       - Preforms linear regression via least squares on a set of vectors.
    svmclassify  - Predicts the class of a set of unknown vectors using an SVM model.
    svmtrain     - Performs k-fold testing followed by independent set testing on a set of training vectors.
Unsupervised Learning
    affcl        - Preforms k-means clustering on a set of vectors.
    dbscan       - Preforms density based clustering of a set of vectors.
    hierarc      - Preform hierarchical/agglomerative clustering and returns cluster assignments or a linkage matrix.
    kmeans       - Preforms k-means clustering on a set of vectors.
    silscore     - Calculate the silhouette score of a set of clusters.
"""