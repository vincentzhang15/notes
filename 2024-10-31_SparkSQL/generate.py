"""
Generate random CSV data for SparkSQL practice.

Created: 2024-10-31
Updated: 2024-10-31
"""

import pandas as pd
import numpy as np

num_rows = 1000
data = {
    'id': range(1, num_rows + 1),
    'name': [f'Name_{i}' for i in range(1, num_rows + 1)],
    'age': np.random.randint(18, 70, size=num_rows),
    'salary': np.random.randint(30000, 120000, size=num_rows),
    'department': np.random.choice(['HR', 'Engineering', 'Sales', 'Marketing'], size=num_rows),
    'join_date': pd.date_range(start='2015-01-01', periods=num_rows, freq='D')
}
df = pd.DataFrame(data)
df.to_csv('random_data.csv', index=False)
