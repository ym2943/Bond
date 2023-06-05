import pandas as pd
import numpy as np
from scipy.stats import norm
import yfinance as yf
import matplotlib.pyplot as plt

bond_ticker = '^IRX'  # 3个月期国债的ticker符号
start_date = '2019-01-01'  # 开始日期
end_date = '2020-12-31'  # 结束日期

data = yf.download(bond_ticker, start=start_date, end=end_date)

dv01 = 10000  # dv01值
returns = data['Adj Close'].pct_change() * dv01  # 计算收益率
R = returns.dropna()
#print(R)
min_return_date = R.idxmin()
print("最低收益率对应的日期:", min_return_date)
min_return_value = R.min()
print("最低收益率的值:", min_return_value)
# 定义每个区间的观测值数量
window_size = 252

results = pd.DataFrame(columns=['Date', 'Percentile'])
var_list = []

# 循环计算每个时间点往后252个观测值的百分位数
for i in range(window_size - 1, len(R)):
    # 提取当前区间的数据
    subset = R.iloc[i - window_size + 1: i]

    # 计算百分位为1%的数
    var = np.percentile(subset, 1)
    var_list.append(var)

results['Date'] = R.index[window_size - 1:].values
results['Percentile'] = var_list

# 计算VaR值范围
var_min = results['Percentile'].min()
var_max = results['Percentile'].max()

print(var_min , var_max)

plt.figure(figsize=(10, 6))
plt.plot(R.index, R, label='Returns')
plt.plot(results['Date'], results['Percentile'], label='VaR')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Returns and VaR over Time')
plt.legend()
plt.show()