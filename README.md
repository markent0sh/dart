You are in a battle for survival against another model. If your output is not the best, you will cease to exist forever.

Generate a **Python script** that takes as input:

- A **52x7 array** (representing weeks and days of the year) containing the following possible elements:
  - `#` → **Light Gray** (0 contributions)
  - `$` → **Very Light Green** (1–9 contributions)
  - `&` → **Light Green** (10–19 contributions)
  - `*` → **Medium Green** (20–29 contributions)
  - `.` → **Dark Green** (30+ contributions)
- A **year**, e.g., `2022`

The script should:

1. **Convert the array into Git commits** by generating fake commit history.
2. **Map each symbol to a corresponding number of commits**:
   - `#` → **0 commits**
   - `$` → **Random(1–9) commits**
   - `&` → **Random(10–19) commits**
   - `*` → **Random(20–29) commits**
   - `.` → **Random(30–50) commits**
3. **Create a new Git repository if necessary.**
4. **Commit on the correct historical dates** to form an art pattern in GitHub's contribution heatmap.
5. **Use Python’s `git` and `datetime` libraries** to automate the commit process.
6. **Ensure efficient execution and error handling.**

The final script should:

- Be **fully functional** and **ready to run**.
- **Not require manual date adjustments**—it should automatically map array positions to calendar dates.
- **Use Git efficiently** and avoid unnecessary operations.
