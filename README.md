### Oura Daily Scores

Display your [Oura](https://ouraring.com/) Daily Scores in your terminal.

![Screenshot](screenshot.png)

---

### How It Works

Python is used to connect to the Oura API and retrieve the day's Readiness, Sleep, and Activity scores. These scores are then plotted as donut charts and the figure is saved. jp2a is passed the image and generates an ASCII art replica in the terminal. The image is then deleted.

---

### Dependencies
- [Oura API key](https://cloud.ouraring.com/v2/docs)
- [jp2a](https://github.com/cslarsen/jp2a)
- [python](https://www.python.org/)
- [python-matplotlib](https://matplotlib.org/)

---
### Instructions

**Clone the repo**
```
git clone https://github.com/callumr00/oura-daily-scores.git
```

**Insert your API key**

First, copy the sample config file.
```
cp config.sample.json config.json
```
Then, open config.json and replace "YOUR_API_KEY" with your actual API key.

**Create the alias command**

Add the following to your `~/.bashrc` file.
```
# Print Oura Daily Scores in terminal.
export OURA_DIR=path/to/oura-daily-scores
alias oura="(
    python ${OURA_DIR}oura.py &&
    jp2a ${OURA_DIR}daily_scores.png &&
    rm ${OURA_DIR}daily_scores.png
)"
```
Ensure to change the value of `OURA_DIR` accordingly.

**Execute**

After setting the alias, execute `oura` in the terminal. 
