# Project FightMem
A customized Ebbinghaus Quizzing / Flash Cards App built with PyQt5.

Frontend designed to work for memorizing words specifically but could be easily modified.

Backend powered by [Ebisu](https://github.com/fasiha/ebisu "Ebisu"). In the current version it contains two Ebisu lists:
- `Newbie List` New entres just learned with needs to be reviewed within minutes
- `Eb List` Learned entries to be reviewed in longer time periods

The two lists has differently turned Ebisu parameters to serve their purpose. Refer to [Ebisu Documentation](https://github.com/fasiha/ebisu#choice-of-initial-model-parameters "Ebisu Documentation") for the parameters. 

An entry will first get into `Newbie List` and being tested very frequently, until enough correct quiz results, during when it will be transferred into `Eb List` for longer quizzing intervals in order to achieve long time memory.

## Run
First make the knowledge file -- essentially a Pandas DataFrame. `pdf2knowledge.py` serves this purpose for the document that the developer use.

To run the GUI,
```python
python main.py
```

## Todo List
- [x] Function Key with left click Yes, right click No
- [x] User configurable parameters
- [ ] Undo last action
- [ ] Trashcan Page
- [ ] Explore / Table Review Mode
- [ ] ToNewbie table button