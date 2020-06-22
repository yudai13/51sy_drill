
"""パラメータ設定"""

HEAD = 1  #HEAD1なら(1)、HEAD2なら(2)
SP = 1  #SP1加工なら(1)、SP2加工なら(2)

NAME = "EX-GDS"  #名称
DIAMETER = 10  #直径
SHANK = 10 #シャンク径
POINT = 1  #ドリル刃先端の厚さ
     
VELOCITY = 60  #周速

POSITION = 20  #ワーク左側端面をz=0.0とした時の右側端面のz位置
DEPTH = 11  #穴深さ
MARGIN = 2  #位置決め余裕の距離
STEP = 2  #ステップ
FEED = 0.1  #送り



"""これより下は書き換えないこと"""

import math

class Dorill:
    def __init__(self, name, diameter, shank, point):
        self.name = name
        self.diameter = diameter
        self.shank = shank
        self.point = point

    def condition(self, velocity):
        self.n = 1000 * velocity / (math.pi * self.diameter)
        self.n = round(self.n)
        return self.n

    def parameter(self, position, depth, margin, step, feed):
        program_start = f"N1G10P0Z0({self.name})\n\
G0G97G99S{int(self.n)}T101M{93 if SP==1 else 193}P{11 if SP==1 else 21}\n\
Z{float(position+margin if SP==1else 0.0-margin)}M{91 if SP==1 else 191}\n\
X0.0Y0.0M{8 if HEAD==1 else 108}M{28 if HEAD==1 else 128}\n"
        
        program_end = f"G0X100.0M{29 if HEAD==1 else 129}\nG28{'U0Y0' if HEAD==1 else 'U0'}\n"

        total_step =[]

        for n in range(1, (depth+self.point)//step + 1):
            one_step =f"G1Z{float(position-step*n if SP==1 else step*n)}F{float(feed)}\n\
G4U0.2\n\
G1Z{float(position+margin if SP==1else 0.0-margin)}F0.5\n"
            total_step.append(one_step)
        one_step = f"G1Z{float(position - (depth+self.point) if SP==1 else depth+self.point)}F{float(feed)}\n\
G4U0.2\n\
G1Z{float(position+margin if SP==1else 0.0-margin)}F0.5\n"
        total_step.append(one_step)

        drill_cycle = "".join(total_step)

        return program_start + drill_cycle + program_end


def main():
    dorill = Dorill(NAME, DIAMETER, SHANK, POINT)
    dorill.condition(VELOCITY)
    print("------PROGRAM------")
    print(dorill.parameter(POSITION, DEPTH, MARGIN, STEP, FEED))

if __name__ == "__main__":
    main()
