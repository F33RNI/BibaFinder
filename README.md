# BibaFinder
### Script to retrieve timetable by group number and prepods list from Moscow Polykek
<div style="width:100%;text-align:center;">
    <p align="center">
        <a href="https://twitter.com/f33rni"><img alt="Twitter" src="https://img.shields.io/twitter/url?label=My%20twitter&style=social&url=https%3A%2F%2Ftwitter.com%2Ff33rni" ></a>
        <img src="https://badges.frapsoft.com/os/v1/open-source.png?v=103" >
    </p>
</div>

----------

## How to use?

1. Get list of prepods from https://e.mospolytech.ru/old/index.php?p=rasp
    1. Open developer option (page source)
    2. Search for `<select data-placeholder="Выберите преподавателя" class="chosen-select" tabindex="-1" id="pps_select" style="width: 70%; display: none;">` element
    3. Copy all data under `<option value="0">Выберите преподавателя из списка</option>`
    4. Format to:
    ```
    1234,Бибова Биба Бибовна
    567,Дедус Дед
    ```
    5. Save file as `prepods.csv`

2. Open `BibaFinder.py` and type your groups number into `GROUPS =`
    1. Example: `GROUPS = ["123-456"]` or `GROUPS = ["123-456", "789-012"]`

3. Run `BibaFinder.py` `$ python3 BibaFinder.py`

4. Wait for completion

5. Open `Timetable.py` and type generated csv file into `BIBA_FILE =`
    1. Example: `BIBA_FILE = "123-456.csv"`

6. Type your group number into `GROUP =`
    1. Exmaple: `GROUP = "123-456"`

7. Run `Timetable.py` `$ python3 Timetable.py`

8. Wait for completion

9. Timetable will be written to the GROUPS_timetable.xlsx file
