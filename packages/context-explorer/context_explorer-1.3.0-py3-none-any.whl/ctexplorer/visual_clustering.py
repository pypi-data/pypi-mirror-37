#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 18:18:04 2014
@author: Joel

Description:

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon


def done(self):
    self.lineEdit_min_roundness.setText(
        str(self.clustering_window.lineEdit_min_roundness.text()))
    self.lineEdit_max_roundness.setText(
        str(self.clustering_window.lineEdit_max_roundness.text()))
    self.lineEdit_min_size.setText(
        str(self.clustering_window.lineEdit_min_size.text()))
    self.lineEdit_max_size.setText(
        str(self.clustering_window.lineEdit_max_size.text()))
    self.lineEdit_epsilon.setText(
        str(self.clustering_window.doubleSpinBox_distance.value()))
    self.lineEdit_min_pts.setText(
        str(self.clustering_window.doubleSpinBox_min_points.value()))
    self.spinBox_resolution.setValue(
        self.clustering_window.spinBox_resolution.value())
    self.lineEdit_min_density.setText(
        str(self.clustering_window.lineEdit_min_density.text()))
    self.lineEdit_max_density.setText(
        str(self.clustering_window.lineEdit_max_density.text()))
    self.clustering_window.close()


def interactive_clustering(self, int_clust_color_col):
    data = self.clustering_window.data_cluster[
        self.clustering_window.data_cluster.Well ==
        self.clustering_window.comboBox_wells.currentText()]
    self.color = data[int_clust_color_col].values
#    color = data.AvgIntenCh2.values
#        if MainWindow.checkBox_low_resolution.isChecked():
#            self.pixsize = 256
#        else:
#    data = data.loc[data.Top <= data.Top.quantile(1 - self.top_edge)]
#    data = data.loc[data.Top >= data.Top.quantile(self.bottom_edge)]
#    data = data.loc[data.Left >= data.Left.quantile(self.left_edge)]
#    data = data.loc[data.Left <= data.Left.quantile(1 - self.right_edge)]
    # Filter out based on position
    # Filter out cells based on intensities
    # if 'ObjectAvgIntenCh1' in data.columns:
    #     data = data.loc[(data.ObjectAvgIntenCh1 <= self.ch1_max) &
    #                     (data.ObjectAvgIntenCh1 >= self.ch1_min)]
    # if 'AvgIntenCh2' in data.columns:
    #     data = data.loc[(data.AvgIntenCh2 <= self.ch2_max) &
    #                     (data.AvgIntenCh2 >= self.ch2_min)]
    # if 'AvgIntenCh3' in data.columns:
    #     data = data.loc[(data.AvgIntenCh3 <= self.ch3_max) &
    #                     (data.AvgIntenCh3 >= self.ch3_min)]
    # Filter based on position
    # data = (data.loc[data.TopPixsize <= data.TopPixsize.max() *
    #         (1 - self.top_edge)])
    # data = (data.loc[data.TopPixsize >= data.TopPixsize.min() +
    #         (data.TopPixsize.max() * self.bottom_edge)])
    # data = (data.loc[data.LeftPixsize <= data.LeftPixsize.max() *
    #         (1 - self.right_edge)])
    # data = (data.loc[data.LeftPixsize >= data.LeftPixsize.min() +
    #         (data.LeftPixsize.max() * self.left_edge)])
    current_cells = np.array(
        (data.LeftPixsize.values, data.TopPixsize.values)).T
    db = (DBSCAN(
        eps=self.clustering_window.doubleSpinBox_distance.value(),
        min_samples=self.clustering_window.doubleSpinBox_min_points.value(),
        algorithm='ball_tree')
            .fit(current_cells))
    return db, data


def plot_int_clust_results(self, db, data, visual_plot_params):
    self.min_roundness = visual_plot_params['min_roundness']
    self.max_roundness = visual_plot_params['max_roundness']
    self.min_size = visual_plot_params['min_size']
    self.max_size = visual_plot_params['max_size']
    self.min_density = visual_plot_params['min_density']
    self.max_density = visual_plot_params['max_density']
    self.ch1_min = visual_plot_params['ch1_min']
    self.ch1_max = visual_plot_params['ch1_max']
    self.ch2_min = visual_plot_params['ch2_min']
    self.ch2_max = visual_plot_params['ch2_max']
    self.ch3_min = visual_plot_params['ch3_min']
    self.ch3_max = visual_plot_params['ch3_max']
    self.top_edge = visual_plot_params['top_edge']
    self.bottom_edge = visual_plot_params['bottom_edge']
    self.left_edge = visual_plot_params['left_edge']
    self.right_edge = visual_plot_params['right_edge']
    ax = self.clustering_window.widget_matplotlib.canvas.ax
    # Discards the old graph
    ax.clear()
    # Keep X and Y lims the same
    ax.set(aspect='equal')
    # Plot data
    ax.scatter(data.LeftPixsize, data.TopPixsize, s=18, c=self.color,
               cmap=plt.cm.gist_heat, marker='.', edgecolor='none',
               linewidths=0.1)
    plot_labels = db.labels_.copy()
    plot_labels_uniq_noise = np.unique(plot_labels)
    plot_labels_uniq = plot_labels_uniq_noise[plot_labels_uniq_noise != -1]
    num_colonies = len(plot_labels_uniq)
    colony_sizes = [0 for x in range(num_colonies)]
    colony_densities = [0 for x in range(num_colonies)]
    colony_roundnesses = [0 for x in range(num_colonies)]
    for colony_label in plot_labels_uniq:
        # Relabel too small and too big colonies as noise
        colony_size = len(data[db.labels_ == colony_label].index)
        colony_sizes[colony_label] = colony_size
        if self.min_size < colony_size < self.max_size:
            # Append only the size of non-noise colonies to the dict
            # colony_size_dict.append(colony_size)
            # Create a new index for each colony except the noise
            idx_colony = np.where(plot_labels == colony_label)
            # Group cells after colonies so that they can be used to calculate
            # the convex hull in -plot_colonies_clustering-
            hull_points_array = np.asarray([
                data.LeftPixsize.iloc[idx_colony].values,
                data.TopPixsize.iloc[idx_colony].values]).T

            # ConvexHull and Delauny needs at least three values, errors
            # otherwise Also, all cells cannot be of the same x or y
            # coordinate. The convex hull can only be drawn if there are 2
            # dimensions
            if len(hull_points_array) > 2 and np.all([
               min(hull_points_array[:, 0]) != max(hull_points_array[:, 0]),
               min(hull_points_array[:, 1]) != max(hull_points_array[:, 1])]):
                hull = ConvexHull(hull_points_array)
                # Use the hull vertices to check how circular the object is.
                # Only include the colony if it is within the given roundness
                # range This calculation is a measrue of compactness (in this
                # case roundness)
                # http://gis.stackexchange.com/questions/85812/easily-calculate-roundness-compactness-of-a-polygon
                # There are many other ways to do this, but this is good for
                # now. It does not identify objects that are not equivilateral
                # very well but for equilateral object the below boundaries can
                # be used as with the toundness filter
                # pol_triangle = 0.5999908074321633
                # pol_square = 0.7853981633974483
                # pol_circle = 1
                pol = Polygon(hull_points_array[hull.vertices])
                colony_area = pol.area
                colony_roundness = (colony_area / pol.length**2) * 4 * np.pi
                colony_roundnesses[colony_label] = colony_roundness
                colony_density = colony_size * 10**6 / colony_area
                colony_densities[colony_label] = colony_density
                if ((self.min_roundness < colony_roundness < self.max_roundness)
                   and (self.min_density < colony_density < self.max_density)):
                    # Hull simplices are the indices for -cells_in_colonier- of
                    # the cells incuded in the convex hull
                    for simplex in hull.simplices:
                        # ax.hold(True)
                        ax.plot(hull_points_array[simplex, 0],
                                hull_points_array[simplex, 1],
                                'springgreen', linestyle='-', linewidth=2)
                else:
                    plot_labels[plot_labels == colony_label] = -1
            else:
                plot_labels[plot_labels == colony_label] = -1
        else:
            plot_labels[plot_labels == colony_label] = -1

    labels_uniq_post_filter = plot_labels_uniq[plot_labels_uniq != -1]
    num_cols = len(labels_uniq_post_filter)
    if len(plot_labels_uniq) > 0:
        str_avgs = (
            'Number of colonies\t ' + str(num_cols) +
            '\nMean size\t\t ' + str(
                int(round(sum(colony_sizes) / num_cols, 0))) +
            '\nMean roundness\t ' + str(
                round(sum(colony_roundnesses) / num_cols, 3)) +
            '\nMean density\t ' + str(
                int(round(sum(colony_densities) / num_cols, 0))))
        self.clustering_window.textEdit_avgs.setText(str_avgs)
    # Plot the a 500 units long scale bar
    ylim_mean = np.mean(ax.get_ylim())
    xlim_mean = np.mean(ax.get_xlim())
    ypos = ax.get_ylim()[0] + ylim_mean*0.03
    ax.plot([xlim_mean-250, xlim_mean+250], [ypos, ypos], linewidth=1.5,
            color='k')
    ax.scatter([xlim_mean-250, xlim_mean+250], [ypos, ypos], marker="|",
               s=40, linewidths=(1.5, 1.5), color='k')
    ax.annotate('500 units', xy=(xlim_mean, ypos), xytext=(0, -10),
                ha='center', textcoords='offset points', fontsize=9)

    self.clustering_window.widget_matplotlib.canvas.draw()
