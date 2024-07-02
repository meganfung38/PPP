import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/run_python', methods=['POST'])
def run_python():
    data = request.json
    file = request.files['file']
    pg = data.get('pg', None)
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)
    ppp = create_ppp(file_path, pg)
    os.remove(file_path)
    return jsonify(ppp)


def format_task(target, og_target, corporate_initiative, name, dri, is_overdue=False):
    """formats the progress, plan, and overdue tasks"""
    if is_overdue:  # task is overdue
        overdue = f"OVERDUE: "
    else:
        overdue = ""
    bolded_initiative = f"**{corporate_initiative}**"
    if og_target:  # if an original target date exists, include it
        return f"{overdue}{target} ({og_target}) {bolded_initiative}: {name} [{dri}]"
    else:
        return f"{overdue}{target} {bolded_initiative}: {name} [{dri}]"


def format_problem_task(name, comment):
    """formats problem tasks"""
    bolded_name = f"**{name}**"
    if comment:  # comment for why problem task is blocked, exists
        return f"{bolded_name}- {comment}"
    else:
        return f"{bolded_name}- no comments"


def create_ppp(file_path, pg=None):
    """takes a file path and a page to an Excel sheet (provided optionally)
    and generates a PPP for it"""
    try:
        if pg:  # page to Excel sheet provided
            df = pd.read_excel(file_path, sheet_name=pg)
        else:  # no page to Excel sheet provided
            df = pd.read_excel(file_path)

        # converting dates to datetime
        df['Target Date'] = pd.to_datetime(df['Target Date'], format='%m/%d/%Y', errors='coerce')
        df['Complete Date'] = pd.to_datetime(df['Complete Date'], format='%m/%d/%Y', errors='coerce')

        # check for optionally existing columns: comments or original target date
        has_og_target_date = 'Original Target Date' in df.columns
        has_comments = 'Comments' in df.columns

        # get range of dates for progress and plan sections
        today = datetime.now()  # today's date
        last_week = today - timedelta(days=7)  # 7 days ago
        two_months = today + timedelta(days=60)  # 60 days from now

        # getting tasks for each section
        # progress -- completed within last week
        # plan -- new or being worked on for next two months
        # problems -- blocked or overdue

        progress_section = df[(df['Complete Date'] >= last_week) & (df['Complete Date'] <= today)]
        plan_section = df[((df['Status'] != 'Completed') & (df['Status'] != 'Canceled')) &
                          ((df['Target Date'] > today) & (df['Target Date'] <= two_months))]
        blocked_section = df[df['Status'] == 'Blocked']
        overdue_section = df[(df['Target Date'] <= today) * (df['Status'] != 'Completed')]

        # sorting tasks by completion date or target date
        progress = progress_section.sort_values(by='Complete Date')
        plan = plan_section.sort_values(by='Target Date')
        blocked = blocked_section.sort_values(by='Target Date')
        overdue = overdue_section.sort_values(by='Target Date')

        progress_tasks = [
            format_task(row['Complete Date'].strftime('%m/%d'),
                        row['Target Date'].strftime('%m/%d') if pd.notna(row['Target Date']) else None,
                        row['Corporate Initiative'],
                        row['Project Name'],
                        row['Project DRI'])
            for index, row in progress.iterrows()
        ]

        plan_tasks = [
            format_task(row['Target Date'].strftime('%m/%d'),
                        row['Original Target Date'].strftime('%m/%d')
                        if has_og_target_date and pd.notna(row['Original Target Date']) else None,
                        row['Corporate Initiative'],
                        row['Project Name'],
                        row['Project DRI'])
            for index, row in plan.iterrows()
        ]

        problem_tasks = [
            format_problem_task(row['Project Name'],
                                row['Comments']
                                if has_comments and pd.notna(row['Comments']) else None)
            for index, row in blocked.iterrows()
        ] + [
            format_task(row['Target Date'].strftime('%m/%d'),
                        row['Original Target Date'].strftime('%m/%d')
                        if has_og_target_date and pd.notna(row['Original Target Date']) else None,
                        row['Corporate Initiative'],
                        row['Project Name'],
                        row['Project DRI'],
                        is_overdue=True)
            for index, row in overdue.iterrows()
        ]

        ppp = (
            "**Progress [Last Week]** \n" +
            "\n".join(f"- {task}" for task in progress_tasks) + "\n\n" +
            "**Plans [Next Two Months]** \n" +
            "\n".join(f"- {task}" for task in plan_tasks) + "\n\n" +
            "**Progress [Ongoing]** \n" +
            "\n".join(f"- {task}" for task in problem_tasks) + "\n\n"
        )

        return ppp

    except Exception as e:
        return str(e)


def main():
    app.run()


if __name__ == '__main__':
    main()
