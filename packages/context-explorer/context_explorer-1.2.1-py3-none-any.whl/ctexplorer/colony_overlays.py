#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 14:47:55 2017
@author: joel

Create aggregation plots to summarize multiple wells of the same treatment.
"""

from joblib import Parallel, delayed
import matplotlib.pyplot as plt
from natsort import natsorted
from datetime import datetime
import seaborn as sns
from time import time
import pandas as pd
import numpy as np
import os


def tp(string):
    '''
    Only including this here, since passing `self` to the multiCPU call throws
    a QtGuiClipboard error, so there is not way of passing `self.tp` to
    `cluster_cells_dbscan`.
    '''
    current_time = datetime.now().strftime('[%H:%M:%S]')
    print('{} {}'.format(current_time, string))


def prep_colony_overlays(self):
    if self.checkBox_agg_col_exclude_cells.isChecked():
        agg_data = self.data.loc[self.data['Colony'] != -1].copy()
    else:
        agg_data = self.data.copy()
    line_params = {}
    line_params['y_col'] = self.comboBox_agg_col_line_y.currentText()
    line_params['x_col'] = self.comboBox_agg_col_line_x.currentText()
    line_params['x_bins'] = self.spinBox_agg_col_bins.value()
    line_params['save_bin_data'] = self.data['Colonies'] = (
            self.checkBox_agg_col_save_bin_stats.isChecked())
    hb_params = {}
    hb_params['y_col'] = self.comboBox_agg_col_hb_y.currentText()
    hb_params['x_col'] = self.comboBox_agg_col_hb_x.currentText()
    hb_params['color'] = self.comboBox_agg_col_hb_color.currentText()
    hb_params['gridsize'] = self.spinBox_agg_col_hb_gridsize.value()
    start_time = time()
    self.tp('Plotting overlays...')

    Parallel(n_jobs=1)(
        delayed(plot_overlays)  # Function
        (num, cond_name, cond_df.copy(), line_params, hb_params,
            start_time, self.ce_dir_name)  # Parameters
        for num, (cond_name, cond_df) in enumerate(
            agg_data.groupby(['Condition'])))  # For loop to parallize

    # Unnecessary to keep this in memory, could be big
    del agg_data

    self.tp('Total time {} s.\n'.format(time() - start_time))
    return None


def plot_overlays(num, cond_name, cond_df, line_params, hb_params, start_time,
                  ce_dir_name):
    '''
    Wrapper to make it cleaner and not include all code for the hexbins
    and linebins here. Also allows easier modifcation of passing different axes
    if needed.
    '''
    date = datetime.fromtimestamp(start_time).strftime('%Y%m%d-%H%M%S')
    fig_overlays, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    plot_hexbins(ax1, fig_overlays, cond_name, cond_df, hb_params)
    plot_linebins(ax2, cond_name, cond_df, line_params, ce_dir_name, date)
    sns.despine()

    fig_path = os.path.join(ce_dir_name, 'Overlays-{}-{}-{}.png'.format(
        cond_name, hb_params['color'], date))
    fig_overlays.savefig(fig_path, bbox_inches='tight')
    plt.close(fig_overlays)
    tp('Plot saved to {}.'.format(fig_path))
    return None


def plot_hexbins(ax, fig, cond_name, cond_df, hb_params):
    '''
    Plotting the hexbins
    '''
    # hb = ax.hexbin(
    ax.hexbin(
        cond_df[hb_params['x_col']], cond_df[hb_params['y_col']],
        C=cond_df[hb_params['color']], cmap='inferno', mincnt=1, linewidth=0,
        edgecolor='none', gridsize=hb_params['gridsize'])
    ax.set_aspect('equal', 'datalim')
    # fig.colorbar(hb)  # this is for changing the colorbar
    pass


def plot_linebins(ax, cond_name, cond_df, line_params, ce_dir_name, date):
    ''' Create the mean, std, and CI and join them with a line '''
    # If defining an integer instead of a linspace to pd.cut, there is an
    # uneven amount of bins between `sns.pointplot` and `ax.errorbar` if the x
    # col has negative values (or close to, so a negative bin limit created)
    bins = np.linspace(0, cond_df[line_params['x_col']].max(),
                       line_params['x_bins'] + 1)
    line_params['bin_x_col'] = 'Bin{}'.format(line_params['x_col'])
    cond_df[line_params['bin_x_col']] = pd.cut(
        cond_df[line_params['x_col']], bins)
    # For `plt.errorbar`, the values need to be calculated manually
    # Each colony gets one value per bin
    bin_data = (cond_df[['Well', 'Colony', line_params['bin_x_col'],
                line_params['y_col']]]
                .groupby(['Well', 'Colony', line_params['bin_x_col']])
                .mean()
                .reset_index())
    # The same bins are grouped across colonies
    # Each colony has max one value per bin. The values are aggreated.
    bin_means = bin_data.groupby(
            line_params['bin_x_col'])[line_params['y_col']].mean()
    bin_stds = bin_data.groupby(
            line_params['bin_x_col'])[line_params['y_col']].std()
    # Need to sort the categorical numbers in the right order for plotting
    bin_means = bin_means.reindex(natsorted(bin_means.index))
    bin_stds = bin_stds.reindex(natsorted(bin_stds.index))

    # Save bin data to csv
    if line_params['save_bin_data']:
        bin_counts = bin_data.groupby(
            line_params['bin_x_col'])[line_params['y_col']].count()
        bin_counts = bin_counts.reindex(natsorted(bin_counts.index))
        bin_stats = pd.concat([bin_counts, bin_means, bin_stds], axis=1)
        bin_stats.columns = ['ColoniesInBin',
                             'Mean{}'.format(line_params['y_col']),
                             'Std{}'.format(line_params['y_col'])]
        bin_stats = bin_stats.reset_index()
        bin_stats_path = os.path.join(
            ce_dir_name, 'Bin-stats-{}-{}.csv'.format(cond_name, date))
        bin_stats.to_csv(bin_stats_path, index=False)
        bin_data_path = os.path.join(
                ce_dir_name, 'Bin-data-{}-{}.csv'.format(cond_name, date))
        bin_data.to_csv(bin_data_path, index=False)

    ax.errorbar(range(0, len(bin_means.values)), bin_means.values,
                yerr=bin_stds.values, color='r', ecolor='gray', capsize=0)
    # For `sns.pointplot`, the mean and CI are calculated as part of the
    # plotting function
    sns.pointplot(x=line_params['bin_x_col'], y=line_params['y_col'],
                  data=bin_data, scale=0.6, markers=[''], ax=ax, ci=95,
                  color='k', join=False)
    ax.set_ylabel(line_params['y_col'], fontsize=6, x=0.6)
    ax.set_xlabel('Bins of {}'.format(line_params['bin_x_col']))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
    return None
