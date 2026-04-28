import re

with open("Student/index.html", "r") as f: s_idx = f.read()
s_idx = re.sub(r'(<div class="tank-metrics">)', r'<h3 class="health-title">AI Health Score</h3>\n        \1', s_idx)
s_idx = s_idx.replace("</style>", "  .health-title { margin: 0 0 16px; font-size: 16px; font-weight: 700; color: var(--text-dark); }\n  </style>")
with open("Student/index.html", "w") as f: f.write(s_idx)

with open("Teacher/index.html", "r") as f: t_idx = f.read()
t_idx = re.sub(r'(<div class="tank-metrics">)', r'<h3 class="health-title">AI Health Score</h3>\n        \1', t_idx)
t_idx = t_idx.replace("</style>", "  .health-title { margin: 0 0 16px; font-size: 16px; font-weight: 700; color: var(--text-dark); }\n  </style>")
with open("Teacher/index.html", "w") as f: f.write(t_idx)

with open("Student/profile.html", "r") as f: s_prof = f.read()
s_prof = s_prof.replace('src="../assets/sierraprofile.webp"', 'src="../assets/Pink Guy Icon.png"')
with open("Student/profile.html", "w") as f: f.write(s_prof)

print("Restored other changes")
