import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class StudyPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Study Planner & Timetable")
        self.root.geometry("650x550")
        
        self.subjects = []

        # --- UI Setup ---
        input_frame = ttk.LabelFrame(self.root, text="Add Subject", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)

        # Subject Name
        ttk.Label(input_frame, text="Subject:").grid(row=0, column=0, sticky="w")
        self.entry_subject = ttk.Entry(input_frame, width=20)
        self.entry_subject.grid(row=0, column=1, padx=5, pady=5)

        # Exam Date
        ttk.Label(input_frame, text="Exam Date (YYYY-MM-DD):").grid(row=0, column=2, sticky="w")
        self.entry_date = ttk.Entry(input_frame, width=15)
        self.entry_date.grid(row=0, column=3, padx=5, pady=5)

        # Confidence Level
        ttk.Label(input_frame, text="Confidence (1=Low, 5=High):").grid(row=1, column=0, sticky="w")
        self.combo_confidence = ttk.Combobox(input_frame, values=[1, 2, 3, 4, 5], width=5, state="readonly")
        self.combo_confidence.current(2) # Default to 3
        self.combo_confidence.grid(row=1, column=1, padx=5, pady=5)

        # Add Button
        self.btn_add = ttk.Button(input_frame, text="Add Subject", command=self.add_subject)
        self.btn_add.grid(row=1, column=3, sticky="e", pady=5)

        # --- Subject List ---
        list_frame = ttk.LabelFrame(self.root, text="Your Subjects", padding="10")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=("Subject", "Date", "Confidence"), show="headings", height=5)
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Date", text="Exam Date")
        self.tree.heading("Confidence", text="Confidence")
        self.tree.pack(fill="both", expand=True)

        # --- Generator Settings ---
        gen_frame = ttk.Frame(self.root, padding="10")
        gen_frame.pack(fill="x", padx=10)

        ttk.Label(gen_frame, text="Daily Study Hours:").pack(side="left")
        self.entry_hours = ttk.Entry(gen_frame, width=10)
        self.entry_hours.pack(side="left", padx=5)
        
        self.btn_generate = ttk.Button(gen_frame, text="Generate Smart Schedule", command=self.generate_schedule)
        self.btn_generate.pack(side="right")

        # --- Output Text ---
        self.text_output = tk.Text(self.root, wrap="word", height=12)
        self.text_output.pack(fill="both", expand=True, padx=10, pady=10)

    def add_subject(self):
        name = self.entry_subject.get().strip()
        date_str = self.entry_date.get().strip()
        confidence = self.combo_confidence.get()

        if not name or not date_str:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Validate date format
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Incorrect date format. Use YYYY-MM-DD.")
            return

        subject_data = {"name": name, "date": date_str, "confidence": int(confidence)}
        self.subjects.append(subject_data)
        
        self.tree.insert("", "end", values=(name, date_str, confidence))
        
        # Clear inputs
        self.entry_subject.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)

    def generate_schedule(self):
        if not self.subjects:
            messagebox.showwarning("Warning", "Add at least one subject first.")
            return

        try:
            daily_hours = float(self.entry_hours.get())
            if daily_hours <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of daily hours.")
            return

        self.text_output.delete(1.0, tk.END)
        
        today = datetime.now().date()
        # Find the latest exam date to know when to stop generating the schedule
        end_date = max(datetime.strptime(s["date"], "%Y-%m-%d").date() for s in self.subjects)

        if end_date < today:
            self.text_output.insert(tk.END, "All exams are in the past!\n")
            return

        self.text_output.insert(tk.END, f"--- Generating Schedule ({daily_hours} hrs/day) ---\n")

        current_day = today
        
        # Loop day-by-day from today until the last exam
        while current_day <= end_date:
            active_subjects = []
            total_weight = 0

            for sub in self.subjects:
                exam_date = datetime.strptime(sub["date"], "%Y-%m-%d").date()
                days_left = (exam_date - current_day).days
                
                # Only schedule subjects if the exam hasn't passed yet
                if days_left >= 0:
                    # --- PRIORITY WEIGHTING LOGIC ---
                    # 1. Lower confidence (1) gives higher multiplier (5). High confidence (5) gives lower multiplier (1).
                    confidence_factor = 6 - sub["confidence"] 
                    
                    # 2. Closer deadlines give an exponentially higher weight. (+1 prevents division by zero if exam is today)
                    urgency_factor = 10 / (days_left + 1) 
                    
                    weight = confidence_factor * urgency_factor
                    active_subjects.append({"name": sub["name"], "weight": weight})
                    total_weight += weight

            if total_weight > 0:
                self.text_output.insert(tk.END, f"\n📅 {current_day.strftime('%A, %b %d')}:\n")
                
                # Distribute hours based on the calculated weights
                for sub in active_subjects:
                    allocated_hours = daily_hours * (sub["weight"] / total_weight)
                    
                    # Round to nearest 15 mins (0.25 hours) for realistic scheduling
                    allocated_hours = round(allocated_hours * 4) / 4 
                    
                    if allocated_hours > 0:
                        self.text_output.insert(tk.END, f"  • {sub['name']}: {allocated_hours} hrs\n")

            current_day += timedelta(days=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyPlannerApp(root)
    root.mainloop()