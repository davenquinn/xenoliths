import numpy as N
from pandas import DataFrame
from .data import get_tables
from .util import element, ree_only

class DepletionModel(object):
    """
    Core fitting routine for a MELTS-modeled depletion
    scenario.
    """
    def __init__(self, model_filename, **kwargs):
        """
        Initialize fitting with a datafile output by the
        MELTS model.

        kwargs:
               mode  'whole_rock'* or 'clinopyroxene'
            log_fit   False (fit logarithmically or linearly)
        """
        self.log_fit = kwargs.pop('log_fit',False)

        self.tables = get_tables(model_filename)

    def fit(self, table_id, data, criterion):
        """
        Fit depletion data to a dataset based
        on a criterion. Criterion can be a callable
        that returns a boolean, or a single component
        name (ex: Al2O3)

        Theoretically we could automatically decide
        which table to fit on based on oxide name(s)
        """
        trace = self.tables[table_id]

        if not hasattr(criterion, '__call__'):
            val = criterion
            criterion = lambda i: i == val

        def drop_unused(df):
            cols = [i for i in df.columns
                if not criterion(i)]
            return df.drop(cols,axis=1)

        # Prepare trace elements for fitting
        iters = trace.drop(
            ['mass','Pressure','Temperature'], axis=1)
        iters = drop_unused(iters)
        fit = drop_unused(data)

        # Ignore uncertainties for fitting
        fit = fit.applymap(lambda x: x.nominal_value)

        if self.log_fit:
            # Linearize data for minimization
            fit = N.log(fit)
            iters = N.log(iters)

        def __best_fit(row):
            residuals = row-iters
            sse = (residuals**2).sum(axis=1)
            ix = sse.idxmin()

            series = trace.loc[ix].copy()
            series['step_index'] = ix
            series['sse'] = sse.loc[ix]
            series['sample_id'] = row.name
            return series

        # Find best-fitting simulation step for each sample
        serie = [__best_fit(row)
                for i,row in fit.iterrows()]
        return DataFrame(serie).set_index('sample_id')

    def fit_HREE(self,data, **kwargs):
        """
        A special case of fitting targeted at
        heavy rare-earth elements.
        """
        table = kwargs.pop('table','Solid Trace')
        Tb, Lu = element('Tb'), element('Lu')
        func = lambda i: Tb <= element(i) <= Lu
        return self.fit(table, data, func)

    def enrichment(self,data,depleted):
        # Get mineral-melt partition coefficients for ending conditions
        # Could also just use computed values
        coeffs = self.tables['Partition Coefficients']
        params = [coeffs.loc[int(row['step_index'])]
                    for i,row in depleted.iterrows()]
        Dree = DataFrame(params).set_index(depleted.index)

        # Re-enrichment model
        # Currently, enrichment is modeled as a fully batch process
        delta = (data/depleted)
        # Don't know if I should divide by DREE
        enrichment = ree_only((data*delta)/Dree)
        enrichment = enrichment.applymap(lambda x: x.nominal_value)

        # Normalize to mean HREE *(in log space)
        hree = N.exp(N.log(enrichment[[66,67,68,70,71]]).mean(axis=1))
        # Amount of enriched liquid that is needed to reset values
        multiplier = 6/hree
        enrichment = enrichment.mul(multiplier,axis=0)
        return enrichment, multiplier

