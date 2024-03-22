"""Estimate the model 2."""

'''
Model 2 - model 1 + individual okreses / candidates.
Parameters:
estimates: from polls
estimated turnout: 
- turnout from the previous election of the same type
- number of registered voters from the last possible elections
slopes and rates for okreses and candidates:
- basic calculation from the testing/model1 for the last relevant elections
- estimates from polls and estimated transfers of voters
'''

import datetime
import pandas as pd
import numpy as np

election_code = "president_2024-1"

# path
path = "/home/michal/dev/real-time-predictions-sk-2024/test/test02/estimate/"

# read data
df = pd.read_csv(path + "../extract/data.csv")
df_turnout = pd.read_csv(path + election_code + "_estimated_turnout.csv")
df_rates = pd.read_csv(path + election_code + "_estimated_rates.csv", header=1)
df_slopes = pd.read_csv(path + election_code + "_estimated_slopes.csv", header=1)
df_estimates = pd.read_csv(path + election_code + "_estimates.csv")

# get list of candidates, starting "votes_"
candidates_votes = list(df.columns[df.columns.str.startswith('votes_')])

# get candidate ids:
candidates_ids = [c.replace("votes_", "") for c in candidates_votes]

# prepare matrix for the current estimates
df_matrix = df.loc[:, candidates_votes]
df_matrix.columns = candidates_ids
df_matrix.index = df['okres_code']

df_rates_matrix = df_rates.loc[:, candidates_ids]
df_rates_matrix.index = df_rates['okres_code']

df_slope_matrix = df_slopes.loc[:, candidates_ids]
df_slope_matrix.index = df_slopes['okres_code']

df.index = df['okres_code']

df_turnout.index = df_turnout['okres_code']

# 0 - initial estimate
# calculate initial estimate, okresy x candidates
# it will not be exact, because the estimates were calculated independently
# df_turnout: estimated_voted
# df_rates
# df_estimates: estimate
# df_turnout * df_rates * df_estimates
df_turnout['estimated_voted'].index = df_turnout['estimated_voted'].index.astype(df_rates.columns.dtype)
dfe = df_estimates.loc[:, ['candidate_id', 'estimate']]
dfe.index = dfe['candidate_id']
x = df_rates_matrix.mul(df_turnout['estimated_voted'], axis=0)
x.columns = dfe['candidate_id']
# multiply by estimates['estimate']
initial_estimates = x.mul(dfe['estimate'], axis=1) / 100
initial_estimates.index = df_rates['okres_code']
# estimates for each candidate in each okres, 100% in each okres
initial_estimates_rates = initial_estimates.div(initial_estimates.sum(axis=1), axis=0)
initial_estimates_rates.columns = [str(c) for c in initial_estimates_rates.columns]


# weights, how much is already counted in each okres
# sum over okreses = 1
w_current = df_matrix.sum(axis=1) / df_matrix.sum().sum()


# current rates for each candidate overall
df_matrix_current_candidates_rates = df_matrix.sum(axis=0) / df_matrix.sum().sum()
df_matrix_current_candidates_rates.fillna(0, inplace=True)


# where each candidate stands in the initial rates - average of the initial estimates weighted by the current okreses' rates w_current
candidates_standing_at = w_current @ df_rates_matrix
candidates_standing_at.fillna(1, inplace=True)


# current results in each okres (percentage of votes for each candidate
df_matrix_current_rates = df_matrix.div(df_matrix.sum(axis=1), axis=0)
df_matrix_current_rates.fillna(0, inplace=True)


# current turnout rates for each okres
current_turnout = df['voted'] / df['voters']
current_turnout.fillna(0, inplace=True)


# rate, how much polling stations are already counted in each okres
currently_counted_polling_stations_rate = df['counted_polling_stations'] / df['polling_stations']
# rate, how much voters are already counted in each okres, may be over 100%
currently_counted_voters_rate = df['voters'] / df_turnout['last_voters']
# overall rates
currently_counted_total_polling_stations_rate = df['counted_polling_stations'].sum() / df['polling_stations'].sum()
currently_counted_total_voters_rate = df['voters'].sum() / df_turnout['last_voters'].sum()


# slope adjustment for each candidate and each okres
# from df_matrix_current_rates
# add to every candidate's current rate the slope of the regression, it is in percentage
slope_matrix = np.matrix(df_slope_matrix)
currently_counted_polling_stations_rate_df = (100 - currently_counted_polling_stations_rate * 100).to_frame()
currently_counted_polling_stations_rate_df.index = df_slope_matrix.index
slope_additions = df_slope_matrix.mul(currently_counted_polling_stations_rate_df[0], axis=0)

# add slope additions to the current rates
df_matrix_current_rates_sloped = df_matrix_current_rates.add(slope_additions / 100)


# estimated rates for each candidate in each okres based on where they stand, current basic rate
df_estimate_rated = df_rates_matrix * (1 / candidates_standing_at) * df_matrix_current_candidates_rates


# estimate overall voted for each okres
# at the beggining it is base on currently_counted_voters_rate, later on currently_counted_polling_stations_rate
# limit currently_counted_voters_rate to max 100%
ccvr1 = currently_counted_voters_rate.apply(lambda x: 1 if x > 1 else x)
# currently_counted_polling_stations_rate0_5 is 0 for currently_counted_polling_stations_rate < 0.5, and goes up to 1 for currently_counted_polling_stations_rate = 1
breakpoint = 0.7
ccpsr0_5 = currently_counted_polling_stations_rate.apply(lambda x: 0 if x < breakpoint else (x - breakpoint) * (1 / (1 - breakpoint)))
# (ccpsr0_5 * currently_counted_polling_stations_rate) + (1 - ccpsr0_5) * ccvr1
estimated_voted = df['voted'] + (1 - ccvr1) * df_turnout['estimated_voted']


# estimate rates
# w1: initial_estimates_rates # from initial estimates
# w2: df_estimate_rated # from other okreses
# w3: df_matrix_current_rates_sloped # from current okres only
# currently_counted_total_polling_stations_rate # overall polling stations
# currently_counted_total_voters_rate # overall voters (may be over 100%)
# limit df_matrix_current_rates_sloped to 0-100%
dmcrs01 = df_matrix_current_rates_sloped.applymap(lambda x: 1 if (x > 1) else (0 if (x < 0) else x))
# combine the three estimates based on the current rates
# if counted 0 in okres and currently_counted_total_voters_rate < 0.10: initial_estimates_rates
# if counted 0 in okres and currently_counted_total_voters_rate >= 0.10: combine df_estimate_rated and initial_estimates_rates
# for counted < 40 in okres: effect of initial_estimates_rates - breakpoint1
# for 10 < counted < 80 in okres: effect of df_estimate_rated - breakpoint2
breakpoint1 = 0.1
breakpoint20 = 0.0
breakpoint21 = 0.6
breakpoint3 = 0.0
w1u = 0.5 * (currently_counted_voters_rate).apply(lambda x: (breakpoint1 - x) / breakpoint1 if x < breakpoint1 else 0)
w2u = 2 * (currently_counted_voters_rate).apply(lambda x: (x - breakpoint20) / (breakpoint21 - breakpoint20) if (x > breakpoint20) & (x < breakpoint21) else 0)
w3u = 3 * (currently_counted_voters_rate).apply(lambda x: (x - breakpoint3) / (1 - breakpoint3) if x > breakpoint3 else 0)
w1 = w1u / (w1u + w2u + w3u)
w2 = w2u / (w1u + w2u + w3u)
w3 = w3u / (w1u + w2u + w3u)
# combine the three estimates based on the current rates
# estimated_rates = w1 * initial_estimates_rates + w2 * df_estimate_rated + w3 * dmcrs01
estimated_rates = initial_estimates_rates.apply(lambda row: row * w1[row.name], axis=1) + df_estimate_rated.apply(lambda row: row * w2[row.name], axis=1) + dmcrs01.apply(lambda row: row * w3[row.name], axis=1).fillna(0)


# estimated votes
estimated_votes = estimated_rates.apply(lambda row: row * estimated_voted[row.name], axis=1)


# estimated results
estimated_results = estimated_votes.sum()
results = pd.DataFrame(estimated_results / estimated_results.sum() * 100)
results.fillna(0, inplace=True)

# save results
results['candidate'] = "votes_" + results.index
results.columns = ['result', 'candidate']
results.to_csv(path + "estimates.csv", index=False)


# add intervals to results:
# interval = estimate +- max(3 * (a * estimate + b * uncounted + c), 0.01)
#   interval         a         b         c
# 0     0-20  0.072811  0.023337 -1.892220
# 1    20-80  0.020267  0.002202 -0.044920
# 2    80-95  0.009523  0.002697 -0.005142
# 3   99-100  0.001419  0.038707 -0.005951
# 4    95-99  0.003043  0.003209  0.002660
interval_parameters = [
  {'min': 0, 'max': 20, 'a': 0.072811, 'b': 0.023337, 'c': -1.892220},
  {'min': 20, 'max': 80, 'a': 0.020267, 'b': 0.002202, 'c': -0.044920},
  {'min': 80, 'max': 95, 'a': 0.009523, 'b': 0.002697, 'c': -0.005142},
  {'min': 95, 'max': 99, 'a': 0.003043, 'b': 0.003209, 'c': 0.002660},
  {'min': 99, 'max': 100, 'a': 0.001419, 'b': 0.038707, 'c': -0.005951}
]
df_ip = pd.DataFrame(interval_parameters)
# get the correct bin from the counted
counted = currently_counted_total_polling_stations_rate * 100
pars = df_ip[(df_ip['min'] <= counted) & (df_ip['max'] >= counted)].iloc[0]
results_rich = results.copy()
results_rich['hi'] = results_rich['result'] + (3 * (pars['a'] * results_rich['result'] + pars['b'] * (100 - counted) + pars['c']).apply(lambda x: 0.01 if x < 0.01 else x))
results_rich['lo'] = results_rich['result'] - (3 * (pars['a'] * results_rich['result'] + pars['b'] * (100 - counted) + pars['c']))
# limit to 0-100
results_rich['hi'] = results_rich['hi'].apply(lambda x: 100 if x > 100 else (0 if x < 0 else x))
results_rich['lo'] = results_rich['lo'].apply(lambda x: 100 if x > 100 else (0 if x < 0 else x))
results_rich.to_csv(path + "estimates_rich.csv", index=False)


# save info about the datetimes used
df_info = pd.read_csv(path + "../extract/info.csv")
df_info.rename(columns={'datetime': 'value'}, inplace=True)
items = [
  {
    'name': 'estimating_' + election_code,
    'value': datetime.datetime.now().isoformat(timespec='seconds')
  },
  {
    'name': 'counted_' + election_code,
    'value': currently_counted_total_polling_stations_rate * 100
  }
]
df_info = pd.concat([df_info, pd.DataFrame(items)])
df_info.to_csv(path + "info.csv", index=False)

print("Estimation done.")
