# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from src.products.product_factory import DataProductFactory
from src.visualization.plotting_utils import COLORS, pretty_label


# ------- Get the data products will use to generate these plots
weekly_totals = DataProductFactory().get_product("weekly_activity_totals")
base_weekly_totals = weekly_totals[weekly_totals["training_period"] == "base"]
base_weekly_totals = base_weekly_totals.fillna(value=0)

# ------- Plot 1 -  Two plots with shared x-axis 
fig, axarr = plt.subplots(2, sharex=True, figsize=(20, 10))
plot1_rects = []
plot2_rects = []
width = 0.5

# ------- Sub-plot 1 - The total hours each week spent for each activity
plot1_cols = [c for c in base_weekly_totals.columns if "activity_" in c]
plot2_cols = [c for c in base_weekly_totals.columns if "zone_" in c]
for i, col_name in enumerate(plot1_cols): 
    if "activity" in col_name:
        if i == 0:
            plot1_rects.append(axarr[0].bar(
                    base_weekly_totals.index,
                    base_weekly_totals[col_name],
                    color=COLORS[i]))
            last = base_weekly_totals[col_name]
        else:
            plot1_rects.append(axarr[0].bar(
                    base_weekly_totals.index,
                    base_weekly_totals[col_name],
                    bottom=last))
            last = last + base_weekly_totals[col_name]
            
plot1_refs = [r[0] for r in plot1_rects]
plot1_labels = [c.replace("activity_", "").capitalize() for c in plot1_cols]

axarr[0].set_title('Weekly Training Totals by Activity')
axarr[0].set_ylabel('Training hours')
axarr[0].legend(plot1_refs, plot1_labels)
axarr[0].set_xticks(base_weekly_totals.index)
axarr[0].set_xlim(12.5, 30)
axarr[0].set_ylim(0, 23)

# ------- Sub-plot 2 - The total hours each week spent in each HR zone
for i, col_name in enumerate(plot2_cols): 
    if "zone" in col_name:
        if i == 0:
            plot2_rects.append(axarr[1].bar(
                    base_weekly_totals.index,
                    base_weekly_totals[col_name],
                    color=COLORS[i]))
            last = base_weekly_totals[col_name]
        else:
            plot2_rects.append(axarr[1].bar(
                    base_weekly_totals.index,
                    base_weekly_totals[col_name], bottom=last,
                    color=COLORS[i]))
            last = last + base_weekly_totals[col_name]
plot2_refs = [r[0] for r in plot2_rects]

plot2_labels = [pretty_label(s) for s in plot2_cols]
    

axarr[1].set_title('Weekly Training Totals by Intensity/Type')
axarr[1].set_ylabel('Training hours')
axarr[1].set_xlabel('Week # (Beginning {}, Ending {})'.format(
        min(base_weekly_totals["Date"]).date(), max(base_weekly_totals["Date"]).date()
           ))
axarr[1].set_ylim(0, 20)
axarr[1].legend(plot2_refs, plot2_labels, borderaxespad=0.2,
     loc='upper right')

# ----- Label subplot 2 
#  For the y labels, the arrow should point to the top of the bar
x_start_max_strength = 13
y_start_max_strength = base_weekly_totals.iloc[0][plot2_cols].sum()
x_start_musc_endur = 21
y_start_musc_endur = base_weekly_totals.iloc[(21-13)][plot2_cols].sum()

axarr[1].annotate("Start max strength training",
     xy=(x_start_max_strength, y_start_max_strength),
     xytext=(x_start_max_strength + 0.5, y_start_max_strength + 8),
     arrowprops=dict(facecolor='black', shrink=0.05))
axarr[1].annotate("""End max strength,
focus on muscular endurance""",
     xy=(x_start_musc_endur, y_start_musc_endur),
     xytext=(x_start_musc_endur + 0.5, y_start_musc_endur + 3),
     arrowprops=dict(facecolor='black', shrink=0.05)) 
fig.show()
fig.savefig("../../reports/figures/weekly_totals.jpg", bbox_inches="tight")

