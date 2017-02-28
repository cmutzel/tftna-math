import matplotlib.pyplot as plt

from src.products.product_factory import DataProductFactory

weekly_totals = DataProductFactory().get_product("weekly_activity_totals")
weekly_totals = weekly_totals.fillna(value=0)

# -------
# plot as bar heights 
f, axarr = plt.subplots(2, sharex=True, figsize=(20, 10))
plot1_rects = []
plot2_rects = []
width = 0.5

# plot 1 - The total hours each week spent for each activity

plot1_cols = [c for c in weekly_totals.columns if "activity_" in c]
plot2_cols = [c for c in weekly_totals.columns if "zone_" in c]
for i, col_name in enumerate(plot1_cols): 
    if "activity" in col_name:
        if i == 0:
            plot1_rects.append(axarr[0].bar(weekly_totals.index,
                               weekly_totals[col_name]))
            last = weekly_totals[col_name]
        else:
            plot1_rects.append(axarr[0].bar(weekly_totals.index,
                               weekly_totals[col_name], bottom=last))
            last = last + weekly_totals[col_name]
plot1_refs = [r[0] for r in plot1_rects]
plot1_labels = [c.replace("activity_", "") for c in plot1_cols]

axarr[0].set_title('Weekly Training Totals by Activity')
axarr[0].set_ylabel('Training hours')
axarr[0].legend(plot1_refs, plot1_labels)
axarr[0].set_ylim(0, 23)

# plot 2 - The total hours each week spent in each HR zone
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
          'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
for i, col_name in enumerate(plot2_cols): 
    if "zone" in col_name:
        if i == 0:
            plot2_rects.append(axarr[1].bar(weekly_totals.index,
                               weekly_totals[col_name], color=colors[i]))
            last = weekly_totals[col_name]
        else:
            plot2_rects.append(axarr[1].bar(weekly_totals.index,
                               weekly_totals[col_name], bottom=last,
                                            color=colors[i]))
            last = last + weekly_totals[col_name]
plot2_refs = [r[0] for r in plot2_rects]
plot2_labels = [c.replace("activity_", "") for c in plot2_cols]


axarr[1].set_title('Weekly Training Totals by Intensity/Type')
axarr[1].set_ylabel('Training hours')
axarr[1].set_xlabel('Week #')
axarr[1].set_ylim(0, 20)
axarr[1].legend(plot2_refs, plot2_labels)

#plt.yticks(np.arange(0, max(weekly_totals["total"] + 3), 2))
f.show()


