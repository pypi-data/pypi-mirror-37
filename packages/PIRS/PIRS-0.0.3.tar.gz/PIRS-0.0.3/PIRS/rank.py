import pandas as pd
import numpy as np
from itertools import *
from scipy import stats
from sklearn import linear_model
import math
import scipy

class ranker:
    """
    Ranks and sorts expression profiles from most to least constitutive.


    This class takes a dataset of time series expression profiles.  It optionally performs an anova and removes time series with strong differential expression.  A linear regression is then performed and prediction intervals are calculated.  Ranking scores for an expression profile are produced by comparing the mean expression to the prediction intervals at each timepoint.


    Parameters
    ----------
    filename : str
        Path to the input dataset.
    anova : bool
        Whether or not to perform an ANOVA and remove profiles with strong differential expression.
    
    Attributes
    ----------
    data : dataframe
        This is where the input data is stored.
    anova : bool
        Whether an anova should be performed


    """
    def __init__(self, filename, anova=False):
        """
        Imports data and initializes a ranker object.


        Takes a file  which has one index column and a number of timepoint labeled data columns.

        """
        self.data = pd.read_csv(filename, sep='\t', header=0, index_col=0)
        self.anova = anova

    def get_tpoints(self):
        """
        Extracts timepoints from header of data.


        Splits strings in header based on required syntax and generates timepoints.


        Attributes
        ----------
        tpoints : array
            array of timepoints at which samples were collected.

        """

        tpoints = [i.replace('CT', '') for i in self.data.columns.values]
        tpoints = [int(i.split('_')[0]) for i in tpoints]
        #deprecated splitting for alternative header syntax
        #tpoints = [int(i.split('.')[0]) for i in tpoints]
        self.tpoints = np.asarray(tpoints)

    def remove_anova(self, alpha=0.05):
        """
        Performs anova to remove profiles with strong differential expression.


        Uses anova to detect expression profile with high confidence that some blocks of timepoint replicates have differential expression.  Removes these profiles as a filtering step since they definitionally will not be constitutively expressed.

        Parameters
        ----------
        alpha : float
            Significance threshold for anova filtering.

        """
        to_remove = []
        for index, row in self.data.iterrows():
            vals = []
            for i in list(set(self.tpoints)):
                vals.append([row.values[j] for j in range(len(row)) if self.tpoints[j] == i])
            f_val, p_val = stats.f_oneway(*vals)
            if p_val < alpha:
                to_remove.append(index)
        self.data = self.data[~self.data.index.isin(to_remove)]

    def calculate_scores(self, dof=len(np.unique(tpoints)), alpha=0.05):
        """
        Calculates prediction intervals and generates ranking scores.

        Performs linear regression and generates corresponding prediction intervals for each time series. Uses these values along with the expression mean to generate a ranking score.

        Parameters
        ----------
        alpha : float
        Significance threshold for anova filtering.

        Attributes
        ----------
        errors : series
            Prediction interval ranking scores for each expression profile.

        """
        es = {}
        for index in range(len(data)):
            regr = linear_model.LinearRegression()
            _ = regr.fit(np.array(tpoints)[:, np.newaxis], np.array(data.iloc[index]))
            rsq = np.sum((regr.predict(np.array(tpoints)[:, np.newaxis]) - np.array(data.iloc[index])) ** 2)
            regr_error = math.sqrt(rsq/(dof-2))
            xsq = np.sum((np.array(tpoints) - np.mean(np.array(tpoints))) ** 2)
            pred = []
            for x in np.array(tpoints):
                pred.append(regr.predict([[x]]) + scipy.stats.t.ppf(1.0-alpha/2., dof) * regr_error*math.sqrt(1+1/dof+(((x-np.mean(tpoints))**2)/xsq)))
                pred.append(regr.predict([[x]]) - scipy.stats.t.ppf(1.0-alpha/2., dof) * regr_error*math.sqrt(1+1/dof+(((x-np.mean(tpoints))**2)/xsq)))
            error = np.sum([(i - np.mean(np.array(data.iloc[index]))) ** 2 for i in pred])/(np.mean(np.array(data.iloc[index])**2))
            es[index] = np.mean(error)
        self.errors = pd.DataFrame.from_dict(es, orient='index')
        self.errors.columns = ['errors']
        self.errors.sort_values('errors', inplace=True)
        return self.errors

    def pirs_sort(self):
        """
        Runs analysis pipeline and outputs data sorted by prediction interval ranking score.


        Takes input data, calculates timepoints, runs anova filtering if applicable, calculates PIRS and outputs data.

        Returns
        -------
        sorted_data : dataframe
            Input data sorted by PIRS.

        """
        get_tpoints()
        if self.anova:
            remove_anova()
        calculate_scores()
        sorted_data = self.data.iloc[errors.index.values]
        return sorted_data

