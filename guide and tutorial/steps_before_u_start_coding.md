Before you start coding on the `src` and `sql` folders after cloning the repo and installing PyCharm and a SQL tool, here are the key steps you should follow:

### For Python Environment Setup and Dependencies
1. **Open the project** in PyCharm.
2. **Create and activate a virtual environment** inside the project folder:
   - Open PyCharm terminal and run:
     ```
     python -m venv .venv
     ```
   - Activate virtual environment:
     - Windows: `.venv\Scripts\activate`
     - macOS/Linux: `source .venv/bin/activate`
3. **Install required Python packages**:
   - Run:
     ```
     pip install -r requirements.txt
     ```
4. **Configure PyCharm** to use this `.venv` as the Python interpreter.

### For SQL Database Setup
5. **Open the `.sql` scripts** (`schema.sql`, `seed.sql`) in their SQL software/IDE.
6. **Run the `schema.sql`** script to create database tables.
7. **Run the `seed.sql`** script to insert example data.

### Before Starting Coding
8. **Pull latest changes** from the remote branch to ensure up-to-date code:
   ```
   git pull origin main
   ```
9. **Create a new branch** (optional but recommended) if working on a feature or fix:
   ```
   git checkout -b feature/your-feature-name
   ```

***

### After setup, they can edit or add Python scripts in `src/` and SQL scripts in `sql/`.

This workflow will ensure everyone works with the same environment and correct database schema, avoiding conflicts.