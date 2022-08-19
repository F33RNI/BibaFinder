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

import traceback

import mechanize

# URL to get prepod rasp
GET_API = "https://kaf.dmami.ru/lessons/teacher-html?id="

# Timeout in seconds to open url
TIMEOUT = 5.0

# Encoding of HTML page and xlsx file
HTML_ENCODING = "utf-8-sig"

# File containing prepod ids and names
PREPODS_CSV_FILE = "prepods.csv"

# CSV file separator
SEPARATOR = ","

# Number of group
GROUPS = ["123-456", "123-457", "123-458"]

# List for results
results = [[] for i in range(len(GROUPS))]

# Open file
prepods_list = open(PREPODS_CSV_FILE, "r", encoding=HTML_ENCODING).readlines()

# Initialize browser
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.set_handle_refresh(False)
browser.addheaders = [("User-agent", "Mozilla/5.0")]

# Counter for progress
counter = 0

# List all prepods
for prepod in prepods_list:

    # Increment counter
    counter += 1

    try:
        # Check separator
        if SEPARATOR in prepod:

            # Get prepod ID
            prepod_id = int(prepod.split(SEPARATOR)[0])

            # Check prepod ID
            if prepod_id > 0:

                # Get prepod name
                prepod_name = prepod.split(SEPARATOR)[1].replace("\n", "").replace("\r", "").strip()

                # Calculate and print progress
                progress = int((counter / len(prepods_list)) * 100)
                print("Searching", prepod_name, "\t", str(counter) + "/" + str(len(prepods_list)),
                      "(" + str(progress) + "%)")

                # Create url
                url = GET_API + str(prepod_id)

                # Search prepod
                browser.open(url, timeout=TIMEOUT)
                response = browser.response()
                html = response.read()
                html_decoded = html.decode(HTML_ENCODING)

                for i in range(len(GROUPS)):
                    # Get group
                    group = GROUPS[i]

                    # If group found
                    if group in html_decoded:
                        # Append result
                        results[i].append([str(prepod_id), prepod_name, url])

                        # Print prepod name and url
                        print(group, prepod_name, "found! URL:", url)

    # Print error message
    except Exception:
        traceback.print_exc()

# Write result to the files
if len(results) > 0:
    print(results)
    print("Writing to files...")

    for i in range(len(GROUPS)):
        if len(results[i]) > 0:
            # Get group
            group = GROUPS[i]

            # Write group to file
            with open(group + ".csv", "w", encoding=HTML_ENCODING) as result_file:
                for result in results[i]:
                    line = SEPARATOR.join(result) + "\n"
                    result_file.write(line)
            result_file.close()
print("Done")
