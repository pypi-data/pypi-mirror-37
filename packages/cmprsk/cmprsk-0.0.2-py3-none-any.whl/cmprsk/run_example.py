import numpy as np
import pandas as pd


from cmprsk import cmprsk

data  = pd.read_csv('tests/test_set.csv')
print(data)

subset = np.random.randint(0, 2, len(data)).astype(bool)

# kwargs = dict(failcode=1, cencode=2)
res = cmprsk.crr(data.time_to_event.values, data.outcome.values,
                 data[['pim', 'pom', 'pum']], failcode=1, cencode=2, subset=subset)


cmprsk.crr(data.time_to_event.values, data.outcome.values, data[['pim', 'pom', 'pum']], failcode=1, cencode=2)
