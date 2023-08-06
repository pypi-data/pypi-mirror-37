"""
# This file controls which input names call which functions.

"""

operations_dict = {
    "Normalization": {
        "zscorenorm": "vectoolslib.normalization.z_score_normalization",
        "quantnorm":  "vectoolslib.normalization.quantile_normalization",
        "medpolish":  "vectoolslib.normalization.median_polish_normalization"
    },
    "Math": {
        "add":         "vectoolslib.mathematics.add",
        "subtract":    "vectoolslib.mathematics.subtract",
        "multiply":    "vectoolslib.mathematics.multiply",
        "dotproduct":  "vectoolslib.mathematics.dot_product",
        "inverse":     "vectoolslib.mathematics.inverse",
        "divide":      "vectoolslib.analysis.divide",
        "determinant": "vectoolslib.mathematics.determinant",
        "eigenvec":    "vectoolslib.mathematics.eigen_vectors",
        "eigenvalues": "vectoolslib.mathematics.eigen_values",
        "sum":         "vectoolslib.mathematics.sum_up"
    },
    "Manipulation": {
        "append":       "vectoolslib.manipulation.append_values_to",
        "aggregate":    "vectoolslib.manipulation.aggregate",
        "creatematrix": "vectoolslib.manipulation.create_matrix",
        "format":       "vectoolslib.manipulation.format_vec",
        "colmerge":     "vectoolslib.manipulation.colmerge",
        "chop":         "vectoolslib.manipulation.chop",
        "concat":       "vectoolslib.manipulation.concatenate",
        "join":         "vectoolslib.manipulation.join",
        "vrep":         "vectoolslib.manipulation.vrep",
        "slice":        "vectoolslib.manipulation.vec_slice",
        "sort":         "vectoolslib.manipulation.vector_sort",
        "transpose":    "vectoolslib.manipulation.transpose",
        "unique":       "vectoolslib.manipulation.unique"
    },
    "Analysis and Statistics": {
        # "runLDA":   "vectoolslib.analysis.run_lda",
        "min":        "vectoolslib.analysis.minimum",
        "max":        "vectoolslib.analysis.maximum",
        "median":     "vectoolslib.analysis.median",
        "mode":       "vectoolslib.analysis.mode",
        "sd":         "vectoolslib.analysis.sd",
        "mean":       "vectoolslib.analysis.mean",
        "percentile": "vectoolslib.analysis.percentile",
        "pearson":    "vectoolslib.analysis.pearson_group",
        "pca":        "vectoolslib.analysis.run_pca",
        "spearman":   "vectoolslib.analysis.spearman",
        "confmat":    "vectoolslib.analysis.confusion_matrix",
        "roc":        "vectoolslib.analysis.roc_curve",
        "shape":      "vectoolslib.analysis.shape"
    },
    "Descriptors": {
        "ncomp":   "vectoolslib.descriptor_CLI_interfaces.ncomposition_command_line",
        "trans":   "vectoolslib.descriptor_CLI_interfaces.transitions_command_line",
        "summary": "vectoolslib.analysis.summary"
    },
    "Supervised Learning": {
        "svmtrain":    "vectoolslib.supervised_learning.svm_train",
        "svmclassify": "vectoolslib.supervised_learning.svm_classify",
        "linreg":      "vectoolslib.supervised_learning.linear_regression",
    },
    "Unsupervised Learning": {
        "kmeans":   "vectoolslib.unsupervised_learning.k_means_clustering",
        "dbscan":   "vectoolslib.unsupervised_learning.DBSCAN",
        "affcl":    "vectoolslib.unsupervised_learning.affinity_propagation_clustering",
        "hierarc":  "vectoolslib.unsupervised_learning.hierarchical_cluster",
        "silscore": "vectoolslib.unsupervised_learning.silhouette_score",
    },
}

