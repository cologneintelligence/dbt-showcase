import argparse
from scripts.dbcontrol import reset,increment_demo,snapshot_demo
func_map={"reset":reset,"inc":increment_demo,"snap":snapshot_demo}

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-o', '--option', type=str, choices=['reset', 'inc', 'snap'], help="choose between reset, [inc]rement and [snap]shot")

args = parser.parse_args()

func_map[args.option]()



