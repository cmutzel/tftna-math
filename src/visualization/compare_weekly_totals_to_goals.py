# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from src.products.product_factory import DataProductFactory
factory = DataProductFactory()

weekly_totals = factory.get_product("weekly_activity_totals")
weekly_goals = factory.get_product("base_training_goals")

cols_to_compare = [
        "zone_1", 
        "zone_2",
        "zone_3",
        "zone_strength",
        "zone_max_strength",
        "zone_alpine_climbing",
        "zone_cragging"
]
final_goals = weekly_goals.set_index(["Date"])[cols_to_compare].fillna(value=0)
final_totals = weekly_totals.set_index(["Date"]).loc[final_goals.index][cols_to_compare].fillna(value=0)
diff = final_totals - final_goals

bars = np.zeros(len(cols_to_compare)*len(final_totals))

#make sure we get unique colors for eeach bar
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
          'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
rects = []
xpos = np.arange(1, len(diff)*len(cols_to_compare), len(cols_to_compare))
xlabels = diff.index
fig, ax = plt.subplots(figsize=(10, 5))
for i, col in enumerate(cols_to_compare):
    rects.append(ax.bar(xpos + i, diff[col], 1, color=colors[i]))
plot_refs = [r[0] for r in rects]
ax.legend(plot_refs, cols_to_compare)
ax.set_xticks(xpos)
#ax.set_xticklabels(str(dt.date()) for dt in xlabels )
ax.set_xticklabels(np.arange(1, len(diff), 1))
plt.xlabel("Week number (from start of base period)")
plt.ylabel("Difference between actual and goal (hours)")
plt.title("Showing deviations from training goals during base period")
plt.show()

# How about totals of all intensity/training types?
diff.sum().plot(kind="bar")


