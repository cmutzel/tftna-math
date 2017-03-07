# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from src.products.product_factory import DataProductFactory
from src.visualization.plotting_utils import COLORS, pretty_label

# ------- Get the data products will use to generate these plots
factory = DataProductFactory()
weekly_totals = factory.get_product("weekly_activity_totals")
weekly_goals = factory.get_product("base_training_goals")
base_weekly_totals = weekly_totals[weekly_totals["training_period"] == "base"]

cols_to_compare = [
        "zone_1", 
        "zone_2",
        "zone_3",
        "zone_strength",
        "zone_max_strength",
        "zone_alpine_climbing",
        "zone_cragging"
]
pretty_labels = [pretty_label(s) for s in cols_to_compare]

final_goals = weekly_goals.set_index(["Date"])[cols_to_compare].fillna(value=0)
final_totals = base_weekly_totals.set_index(["Date"]).loc[final_goals.index][cols_to_compare].fillna(value=0)
diff = final_totals - final_goals

# calc total % difference overall all weeks between the types of activity we 
#  did and what we should have done
percentage_totals = ((diff.sum() / final_goals.sum()) * 100)

# ------- Plot 1
# The difference between our training totals and training goals by week

fig1, ax = plt.subplots(figsize=(10, 5))

rects = []
xlabels = diff.index
xpos = np.arange(1, len(diff)*len(cols_to_compare), len(cols_to_compare))
bars = np.zeros(len(cols_to_compare)*len(final_totals))

for i, col in enumerate(cols_to_compare):
    rects.append(ax.bar(xpos + i, diff[col], 1, color=COLORS[i]))
plot_refs = [r[0] for r in rects]
ax.legend(plot_refs, pretty_labels)
ax.set_xticks(xpos)
#ax.set_xticklabels(str(dt.date()) for dt in xlabels )
ax.set_xticklabels(np.arange(1, len(diff), 1))

plt.xlabel("Week number (from start of base period)")
plt.ylabel("Difference between actual and goal [hours]")
plt.title("Showing deviations from training goals during base period")
plt.show()
fig1.savefig("../../reports/figures/compare_weekly_totals_by_week.jpg",
             bbox_inches="tight")

# two plots with shared x-axis
fig2, ax = plt.subplots(figsize=(12,6))
xticks = np.arange(1, len(percentage_totals) + 1)
ax.bar(xticks, percentage_totals, .8, tick_label=pretty_labels)
plt.xlabel("Intensity/Training Type")
plt.ylabel("""(Sum of actual - sum of weekly goals)/
        (sum of weekly goals) [%]""")
plt.title("Percentage difference between total hours trained and goal")
ax.set_ylim(-75, 400)

#  Add labels to above each bar so its easy to determine their height
#   ...probably a better way to do this
for i, value in enumerate(percentage_totals):
    x = i + .5
    y = value
    text = ""
    if value >= 0:
        y += 10
        text = "+"
    else: 
        y += -20
        text = "-"
    # show both the perentage and abs values of totals hours with the correct
    #  amount of precision
    text += "{}% ({} hrs)".format(
            value.astype("int"), diff.sum().iloc[i].round(2))
    ax.text(x, y, text)
    
# ----- Label plot 2 
#  For the y labels, the arrow should point to the top of the bar

x_label_strength = 4
y_label_strength = 0
ax.annotate(
"""Missed nearly 8 hours
of strength training over
8 weeks.  Roughly a session
a week...""",
     xy=(x_label_strength, y_label_strength + 10),
     xytext=(x_label_strength - .5, y_label_strength + 150),
     arrowprops=dict(facecolor='black', shrink=0.05))

x_label_cragging = 6
y_label_cragging = percentage_totals.iloc[5]
ax.annotate(
"""Drastically exceeded time spent cragging
and alpine climbing at the expense of strength
and overtraining. Most of this occurred on 
climbing trips where it was hard to manage
hours spent out.""",
     xy=(x_label_cragging, y_label_cragging + 50),
     xytext=(x_label_cragging - 1.5, y_label_cragging + 150),
     arrowprops=dict(facecolor='black', shrink=0.05))

fig2.savefig("../../reports/figures/percentage_of_training_goals_met.jpg",
             bbox_inches="tight")

