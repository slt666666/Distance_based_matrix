import random
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, plot

import make_data
import parameters


class DistanceBasedMatrix:

    def __init__(self, clade_csv, gff_csv, ordered_csv, threshold, matrix_type="Distance", add_info=None):
        self.clade_csv = clade_csv
        self.gff_csv = gff_csv
        self.ordered_csv = ordered_csv
        self.threshold = threshold
        self.matrix_type = matrix_type
        self.add_info = add_info

    def make_data(self):

        data_make = make_data.DataMake(self.clade_csv, self.gff_csv, self.ordered_csv, self.threshold, self.matrix_type, self.add_info)
        return data_make.make()

    def remove_na_row_columns(self, z_data, hovertext, position_data):

        if self.matrix_type == "MADA":
            rest_index = sum(np.isnan(z_data)) != z_data.shape[0]
            z_data = z_data[rest_index[::-1], :][:, rest_index]
            hovertext = hovertext[rest_index[::-1], :][:, rest_index]
            position_data = position_data.loc[rest_index, :]

        else:
            rest_index = sum(z_data) != self.threshold * z_data.shape[0]
            z_data = z_data[rest_index[::-1], :][:, rest_index]
            hovertext = hovertext[rest_index[::-1], :][:, rest_index]
            position_data = position_data.loc[rest_index, :]

        return z_data, hovertext, position_data

    def draw_heatmap(self, filename, remove_na=False):

        ### make dataset
        z_data, hovertext, position_data = self.make_data()

        if remove_na:
            z_data, hovertext, position_data = self.remove_na_row_columns(z_data, hovertext, position_data)

        id_clades = position_data["id"]
        gene_num = position_data.shape[0]
        clades = position_data["clade"]

        ### base of heatmap
        params = dict(
            x=id_clades,
            y=id_clades.values[::-1],
            z=z_data,
            text=hovertext,
            hoverinfo="text"
        )
        ### additional parameters of heatmap
        params.update(parameters.HeatMapParams[self.matrix_type].value)

        trace = go.Heatmap(params)
        data = [trace]

        ### add separate lines of clade
        lines, colorlist = [], []
        start = -0.5
        for i, each_clade in enumerate(clades.unique()):
        
            ### color list of clade line
            colorlist.append("rgb"+str(tuple(np.random.random(size=3)*256)))
        
            start += clades.value_counts()[each_clade]
        
            ### vertical lines
            lines.append(
                dict(
                    type="line",
                    xref="x",
                    yref="y",
                    x0=start,
                    y0=-0.5,
                    x1=start,
                    y1=gene_num-0.5,
                    opacity=0.5,
                    line=dict(
                        color=colorlist[i],
                        width=0.5
                    )
                )
            )
            lines.append(
                dict(
                    type="line",
                    xref="x",
                    yref="y",
                    x0=-0.5,
                    y0=gene_num-1-start,
                    x1=gene_num-0.5,
                    y1=gene_num-1-start,
                    opacity=0.75,
                    line=dict(
                        color=colorlist[i],
                        width=0.5
                    )
                )
            )

        ### setting layout
        layout = go.Layout(
            margin=dict(
                l=130,
                t=160
            ),
            width=750,
            height=750,
            autosize=False,
            xaxis=dict(
                mirror="allticks",
                side="top",
                showgrid=False,
                tickfont=dict(
                    size=8
                )
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(
                    size=8
                )
            ),
            shapes=lines
        )

        fig = go.Figure(
            data=data,
            layout=layout
        )

        ### draw
        plot(fig, filename=filename)

class PhylogeneticDistanceBasedMatrix(DistanceBasedMatrix):

    def __init__(self, clade_csv, gff_csv, ordered_csv, nexus_tree, threshold, matrix_type="Distance", add_info=None):
        super().__init__(clade_csv, gff_csv, ordered_csv, threshold, matrix_type, add_info)
        self.nexus_tree = nexus_tree

    def make_data(self):
        data_make = make_data.PhylogeneticDataMake(self.clade_csv, self.gff_csv, self.ordered_csv, self.nexus_tree, self.threshold, self.matrix_type, self.add_info)
        return data_make.make()