#  Smart Study Planner & Timetable Generator

  

A Python desktop app that auto-generates a personalized, day-by-day study schedule based on your subjects, exam dates, and how confident you feel — so you always know what to study and when.

  

---

  

##  Features

  

-  **Smart Priority Weighting** — Subjects with closer deadlines *or* lower confidence automatically get more study time. No manual juggling.

-  **Day-by-Day Schedule** — Generates a full calendar from today to your last exam, with hours allocated per subject per day.

-  **Confidence-Aware** — Rate yourself 1–5 for each subject. Low confidence = more slots. High confidence = fewer. Simple.

-  **Clean GUI** — Built with Tkinter. No browser, no setup beyond Python. Just run it.

-  **15-Minute Rounding** — Allocated hours are rounded to the nearest quarter-hour for realistic, actionable scheduling.

  

---

  

##  Demo

  

```

📅 Monday, Apr 28:

• Mathematics: 2.25 hrs

• Physics: 1.0 hrs

• History: 0.75 hrs

  

📅 Tuesday, Apr 29:

• Mathematics: 2.5 hrs

• Physics: 1.5 hrs

```

  

---

  

##  Getting Started

  

### Prerequisites

  

- Python 3.7+

- Tkinter (bundled with most Python installations)

  

### Run

  

```bash

git  clone  https://github.com/your-username/smart-study-planner.git

cd  smart-study-planner

python  study_planner_2.py

```

  

No external packages needed.

  

---

  

##  How the Priority Algorithm Works

  

Each subject gets a **weight** calculated daily:

  

```

confidence_factor = 6 - confidence_level # Low confidence → higher factor

urgency_factor = 10 / (days_left + 1) # Closer exam → higher factor

  

weight = confidence_factor × urgency_factor

```

  

Daily hours are then distributed proportionally across all active subjects. A subject that's 2 days away and rated confidence 1 will dominate the schedule. One that's 3 weeks away and rated confidence 5 will get minimal time — as it should.

  

---

  

##  Usage

  

1.  **Add a subject** — Enter the subject name, exam date (YYYY-MM-DD format), and your confidence level (1 = barely know it, 5 = solid).

2.  **Set daily hours** — How many hours can you realistically study per day?

3.  **Generate** — Click *Generate Smart Schedule* and your full timetable appears instantly.

  

---

  

## Project Structure

  

```

smart-study-planner/

└── study_planner_2.py # Main application (single file)

```

  

---

  

##  Roadmap

  

- [ ] Export schedule to PDF or CSV

- [ ] Save/load subject lists between sessions

- [ ] Break reminders and Pomodoro integration

- [ ] Color-coded subjects in the output view

- [ ] Calendar view (week/month grid)

  

---

  

##  Contributing

  

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

  

---

  

