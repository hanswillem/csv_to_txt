# csv_to_txt

**Python script that converts a single column from a CSV file to one or more text files.**

### HOW TO USE

`python csv_to_txt.py epilepticfit.csv -ch 3  `

-ch = The EEG channel number.
<br>
Results in a single text file.

`python csv_to_txt_split.py epilepticfit.csv -ch 3  `

-ch = The EEG channel number.
<br>
Results in multiple text files of 32 values each.
