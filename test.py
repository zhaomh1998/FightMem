import core

if __name__ == '__main__':
    fm = core.FightMem('data/GRE1450.fmknowledge')
    fm.new_entry(0)
    fm.new_entry(1)
    fm.new_entry(2)
    fm.new_entry(3)
    fm.new_entry(4)
    fm.refresh_db_prediction()
    print(fm.db)