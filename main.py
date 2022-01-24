import distance_matrix


if __name__ == "__main__":

    '''
    sample matrix type

    DistanceBasedMatrix()

        "Distance" : genetic distance based matrix
        "LogFC2" : "Distance" + LogFC2 Root/Leef TPM values
        "Coexpression" : "Distance" + Coexpression using TPM of some parts
        "MADA" : "Distance" + MADA motif HMM scores
        "Direction" : "Distance" + gene direction
        "ID" : "Distance" + Integrated domain

    PhylogeneticDistanceBasedMatrix()

        "PhyloDistance" : phylogenetic distance based matrix
        "PhyloLogFC2" : "PhyloDistance" + LogFC2 Root/Leef TPM values
        "PhyloCoexpression" : "PhyloDistance" + Coexpression using TPM of some parts
        "PhyloMADA" : "PhyloDistance" + MADA motif HMM scores
    '''

    # Tomato NLR matrix
    clade = "data/tomato_clade.csv"
    gff = "data/tomato_NLR_gff.csv"
    MADA = "data/tomato_MADA.csv"
    root_leaf_TPM = "data/tomato_root_leaf_TPM.csv"
    multiple_TPM = "data/tomato_part_TPM.csv"

    Matrix = distance_matrix.DistanceBasedMatrix(clade, gff, None, 20000, "Distance", MADA)
    Matrix.draw_heatmap("html/Tomato_Distance.html", remove_na=False)
    # Matrix = distance_matrix.DistanceBasedMatrix(clade, gff, None, 20000, "MADA", MADA)
    # Matrix.draw_heatmap("html/Tomato_Distance_MADA.html", remove_na=False)
    # Matrix = distance_matrix.DistanceBasedMatrix(clade, gff, None, 20000, "LogFC2", root_leaf_TPM)
    # Matrix.draw_heatmap("html/Tomato_Distance_logFC2.html", remove_na=False)
    # Matrix = distance_matrix.DistanceBasedMatrix(clade, gff, None, 20000, "Coexpression", multiple_TPM)
    # Matrix.draw_heatmap("html/Tomato_Distance_Coexpression.html", remove_na=False)