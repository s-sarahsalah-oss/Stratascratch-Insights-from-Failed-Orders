import matplotlib.pyplot as plt

# Counts from the original chart (3 "rejected by system after assignment" excluded)
data = [
    ("Cancelled by client\nbefore driver assigned", 4496, "#1F4E79"),
    ("Rejected by system\nbefore driver assigned",  3406, "#6FA0D0"),
    ("Cancelled by client\nafter driver assigned",  2811, "#A6A6A6"),
]
total = sum(v for _, v, _ in data)          # 10,713
before = data[0][1] + data[1][1]            # 7,902

fig, ax = plt.subplots(figsize=(11, 6.2))
fig.patch.set_facecolor("white")
ys = list(range(len(data)))[::-1]

for y, (label, v, c) in zip(ys, data):
    ax.barh(y, v, color=c, height=0.62)
    ax.text(v + 60, y, f"{v:,}  ({v/total:.0%})", va="center", fontsize=12, color="#404040")
    ax.text(-80, y, label, va="center", ha="right", fontsize=12, color="#404040")

# bracket for "before assignment"
bx = 5900
ax.plot([bx, bx + 120, bx + 120, bx], [ys[0] + .3, ys[0] + .3, ys[1] - .3, ys[1] - .3], color="#1F4E79", lw=1.5)
ax.text(bx + 200, (ys[0] + ys[1]) / 2, f"{before/total:.0%} of failed orders\nfail before a driver\nis assigned",
        va="center", fontsize=12.5, color="#1F4E79", fontweight="bold")

ax.set_xlim(0, 8400); ax.set_ylim(-0.7, 2.6)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

fig.text(0.04, 0.945, f"{before/total:.0%} of failed orders fail before a driver is assigned",
         fontsize=19, fontweight="bold", color="#404040")
fig.text(0.04, 0.885, f"Breakdown of {total:,} failed orders by who ended the order and when",
         fontsize=13, color="#707070")
fig.text(0.04, 0.17, "The data shows when orders fail, not why. Is it wait time, driver availability, or customers\n"
         "changing their minds? Time of day and time-to-cancellation can help answer this.",
         fontsize=11.5, color="#404040")
fig.text(0.04, 0.04, "Note: 3 system rejections after driver assignment (<0.03%) are excluded.  "
         "Data: DoorDash failed orders dataset (StrataScratch).", fontsize=9.5, color="#808080")
plt.subplots_adjust(left=0.27, right=0.97, top=0.82, bottom=0.25)
plt.savefig("failure_reasons_story.png", dpi=150)