"""
This is free and unencumbered software released into the public domain.
Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
For more information, please refer to <https://unlicense.org>
"""
import mechanize
from lxml import etree

import pandas

# Encoding of HTML page and xlsx file
HTML_ENCODING = "utf-8-sig"

# File with links to prepod's timetable
BIBA_FILE = "224-373.csv"

# CSV Separator
SEPARATOR = ","

# Number of group
GROUP = "224-373"

# Table first row
DAYS_OF_WEEK = ["Понедельник",
                "Вторник",
                "Среда",
                "Четверг",
                "Пятница",
                "Суббота",
                "Воскресенье"]

# Table first column
ROWS_IN_DAY = ["9:00 - 10:30",
               "10:40 - 12:10",
               "12:20 - 13:50",
               "14:30 - 16:00",
               "16:10 - 17:40",
               "17:50 - 19:20",
               "19:30 - 21:00"]

# Create list for storing data
timetable = [["" for _ in range(len(ROWS_IN_DAY))] for _ in range(len(DAYS_OF_WEEK))]

# Open prepods file
prepods = open(BIBA_FILE, "r", encoding="utf-8").readlines()

# Initialize browser
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.set_handle_refresh(False)
browser.addheaders = [("User-agent", "Mozilla/5.0")]

# List all prepods
for prepod in prepods:
    # Check prepod
    if len(prepod) > 1 and len(prepod.split(SEPARATOR)) > 2:
        # Get url
        prepod_url = prepod.split(SEPARATOR)[2].replace("\n", "").replace("\r", "").strip()

        # Search prepod timetable
        browser.open(prepod_url)
        response = browser.response()
        html = response.read()
        html_decoded = html.decode(HTML_ENCODING)

        # List all 7 days
        for data_day in range(7):
            # Get table for day
            table = etree.HTML(html_decoded).findall(".//*[@data-day-id='" + str(data_day + 1) + "']")

            # List all rows (times)
            for day_time in range(len(table)):
                # List all available lessons
                lessons = table[day_time].findall(".//*[@class='js-draggable lesson    ']")

                # Check list
                if len(lessons) > 0:
                    for lesson in lessons:
                        # Convert to string
                        lesson_str = etree.tostring(lesson, pretty_print=True).decode(HTML_ENCODING)

                        # Check group
                        if GROUP in lesson_str:
                            # Get auditory
                            auditory = lesson.find(".//*[@class='lesson__auditory with-print']").text

                            # Lesson date
                            lesson_date_object = lesson.find(".//*[@class='lesson__date ']")
                            if lesson_date_object is None:
                                lesson_date_object = lesson.find(".//*[@class='lesson__date lesson__date_oneday']")

                            # Get lesson date and subject
                            lesson_date = lesson_date_object.text
                            lesson_subject = lesson.find(".//*[@class='lesson__subject']").text

                            # Generate content
                            content = lesson_date + ": " + auditory + ": " + lesson_subject

                            # Add subject to timetable
                            timetable[day_time][data_day] += content + '\n\n'

                            # Print debug info
                            print("data_day:", data_day, "day_time:", day_time, "subject:", content)

# Create timetable and initialize days of week and group
data = pandas.DataFrame(columns=[GROUP] + DAYS_OF_WEEK)

# Add data
for row_index in range(len(ROWS_IN_DAY) + 1):
    if row_index > 0:
        data.loc[row_index] = [ROWS_IN_DAY[row_index - 1]] + timetable[row_index - 1]


# Write to file
writer = pandas.ExcelWriter(GROUP + "_timetable.xlsx", engine='xlsxwriter')
data.to_excel(writer, sheet_name=GROUP, index=False)

# Create formatter for subjects
subject_format = writer.book.add_format({"text_wrap": True})

# Write subjects
writer.sheets[GROUP].set_column(0, 0, 15)
for i in range(len(DAYS_OF_WEEK)):
    writer.sheets[GROUP].set_column(i + 1, i + 1, 30, subject_format)

# Write to file
writer.save()
