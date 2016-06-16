import numpy as N
from pandas import DataFrame
from .data import get_tables
from .util import element

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
        mode = kwargs.pop('mode','whole_rock')
        self.log_fit = kwargs.pop('log_fit',False)

        self.tables = get_tables(model_filename)

    def fit(self, table_id, data, criterion):
        """
        Fit depletion data to a dataset based
        on a criterion.
        """
        trace = self.tables[table_id]

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

            series = trace.loc[ix]
            series['step_index'] = ix
            series['sse'] = sse.loc[ix]
            series['sample_id'] = row.name
            return series

        # Find best-fitting simulation step for each sample
        serie = [__best_fit(row)
                for i,row in fit.iterrows()]
        return DataFrame(serie).set_index('sample_id')

    def fit_HREE(self,data):
        """
        A special case of fitting targeted at
        heavy rare-earth elements.
        """
        Tb, Lu = element('Tb'), element('Lu')
        func = lambda i: Tb <= element(i) <= Lu
        return self.fit('Solid Trace', data, func)

