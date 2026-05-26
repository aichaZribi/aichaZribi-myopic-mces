\* MCES *\
Minimize
OBJ: 0.5 edgepairs_((0,_1),_(4,_5)) + 0.5 edgepairs_((0,_1),_(4,_9))
 + 0.5 edgepairs_((0,_1),_(5,_6)) + 0.5 edgepairs_((0,_1),_(6,_7))
 + 0.5 edgepairs_((0,_1),_(7,_8)) + 0.5 edgepairs_((0,_1),_(8,_9))
 + edgepairs_((0,_1),__1) + 0.5 edgepairs_((1,_2),_(1,_2))
 + 0.5 edgepairs_((1,_2),_(2,_4)) + 1.5 edgepairs_((1,_2),__1)
 + 1.5 edgepairs_((1,_6),__1) + 0.5 edgepairs_((2,_3),_(1,_2))
 + 0.5 edgepairs_((2,_3),_(2,_4)) + 1.5 edgepairs_((2,_3),__1)
 + 0.5 edgepairs_((3,_4),_(1,_2)) + 0.5 edgepairs_((3,_4),_(2,_4))
 + 1.5 edgepairs_((3,_4),__1) + 0.5 edgepairs_((4,_5),_(1,_2))
 + 0.5 edgepairs_((4,_5),_(2,_4)) + 1.5 edgepairs_((4,_5),__1)
 + 1.5 edgepairs_((5,_6),__1) + 0.5 edgepairs_((5,_7),_(4,_5))
 + 0.5 edgepairs_((5,_7),_(4,_9)) + 0.5 edgepairs_((5,_7),_(5,_6))
 + 0.5 edgepairs_((5,_7),_(6,_7)) + 0.5 edgepairs_((5,_7),_(7,_8))
 + 0.5 edgepairs_((5,_7),_(8,_9)) + edgepairs_((5,_7),__1)
 + edgepairs_((7,_8),_(2,_3)) + edgepairs_((7,_8),__1)
 + edgepairs_((7,_9),_(0,_1)) + 2 edgepairs_((7,_9),__1)
 + edgepairs_(_1,_(0,_1)) + edgepairs_(_1,_(1,_2)) + 2 edgepairs_(_1,_(2,_3))
 + edgepairs_(_1,_(2,_4)) + 1.5 edgepairs_(_1,_(4,_5))
 + 1.5 edgepairs_(_1,_(4,_9)) + 1.5 edgepairs_(_1,_(5,_6))
 + 1.5 edgepairs_(_1,_(6,_7)) + 1.5 edgepairs_(_1,_(7,_8))
 + 1.5 edgepairs_(_1,_(8,_9))
Subject To
_C1: nodepairs_(0,_1) + nodepairs_(0,_2) + nodepairs_(0,_4) + nodepairs_(0,_5)
 + nodepairs_(0,_6) + nodepairs_(0,_7) + nodepairs_(0,_8) + nodepairs_(0,_9)
 <= 1
_C10: nodepairs_(9,_0) + nodepairs_(9,_3) <= 1
_C100: edgepairs_((4,_5),_(8,_9)) + edgepairs_((5,_7),_(8,_9))
 - nodepairs_(5,_8) - nodepairs_(5,_9) <= 0
_dummy: __dummy = 0
_C101: __dummy <= 0
_C102: __dummy <= 0
_C103: __dummy <= 0
_C104: __dummy <= 0
_C105: __dummy <= 0
_C106: __dummy <= 0
_C107: __dummy <= 0
_C108: __dummy <= 0
_C109: __dummy <= 0
_C11: nodepairs_(8,_0) + nodepairs_(9,_0) <= 1
_C110: __dummy <= 0
_C111: edgepairs_((7,_8),_(0,_1)) + edgepairs_((7,_9),_(0,_1))
 - nodepairs_(7,_1) <= 0
_C112: edgepairs_((5,_7),_(1,_2)) - nodepairs_(7,_1) - nodepairs_(7,_2) <= 0
_C113: edgepairs_((7,_8),_(2,_3)) + edgepairs_((7,_9),_(2,_3))
 - nodepairs_(7,_2) <= 0
_C114: edgepairs_((5,_7),_(2,_4)) - nodepairs_(7,_2) - nodepairs_(7,_4) <= 0
_C115: edgepairs_((5,_7),_(4,_5)) - nodepairs_(7,_4) - nodepairs_(7,_5) <= 0
_C116: edgepairs_((5,_7),_(4,_9)) - nodepairs_(7,_4) - nodepairs_(7,_9) <= 0
_C117: edgepairs_((5,_7),_(5,_6)) - nodepairs_(7,_5) - nodepairs_(7,_6) <= 0
_C118: edgepairs_((5,_7),_(6,_7)) - nodepairs_(7,_6) - nodepairs_(7,_7) <= 0
_C119: edgepairs_((5,_7),_(7,_8)) - nodepairs_(7,_7) - nodepairs_(7,_8) <= 0
_C12: nodepairs_(0,_1) + nodepairs_(1,_1) + nodepairs_(2,_1)
 + nodepairs_(3,_1) + nodepairs_(4,_1) + nodepairs_(5,_1) + nodepairs_(7,_1)
 <= 1
_C120: edgepairs_((5,_7),_(8,_9)) - nodepairs_(7,_8) - nodepairs_(7,_9) <= 0
_C121: edgepairs_((7,_8),_(0,_1)) - nodepairs_(8,_0) <= 0
_C122: __dummy <= 0
_C123: edgepairs_((7,_8),_(2,_3)) - nodepairs_(8,_3) <= 0
_C124: __dummy <= 0
_C125: __dummy <= 0
_C126: __dummy <= 0
_C127: __dummy <= 0
_C128: __dummy <= 0
_C129: __dummy <= 0
_C13: nodepairs_(0,_2) + nodepairs_(1,_2) + nodepairs_(2,_2)
 + nodepairs_(3,_2) + nodepairs_(4,_2) + nodepairs_(5,_2) + nodepairs_(7,_2)
 <= 1
_C130: __dummy <= 0
_C131: edgepairs_((7,_9),_(0,_1)) - nodepairs_(9,_0) <= 0
_C132: __dummy <= 0
_C133: edgepairs_((7,_9),_(2,_3)) - nodepairs_(9,_3) <= 0
_C134: __dummy <= 0
_C135: __dummy <= 0
_C136: __dummy <= 0
_C137: __dummy <= 0
_C138: __dummy <= 0
_C139: __dummy <= 0
_C14: nodepairs_(8,_3) + nodepairs_(9,_3) <= 1
_C140: __dummy <= 0
_C141: __dummy <= 0
_C142: __dummy <= 0
_C143: __dummy <= 0
_C144: __dummy <= 0
_C145: __dummy <= 0
_C146: __dummy <= 0
_C147: __dummy <= 0
_C148: __dummy <= 0
_C149: edgepairs_((7,_8),_(0,_1)) - nodepairs_(8,_0) <= 0
_C15: nodepairs_(0,_4) + nodepairs_(1,_4) + nodepairs_(2,_4)
 + nodepairs_(3,_4) + nodepairs_(4,_4) + nodepairs_(5,_4) + nodepairs_(7,_4)
 <= 1
_C150: edgepairs_((7,_9),_(0,_1)) - nodepairs_(9,_0) <= 0
_C151: edgepairs_((0,_1),_(1,_2)) - nodepairs_(0,_1) - nodepairs_(1,_1) <= 0
_C152: edgepairs_((1,_2),_(1,_2)) - nodepairs_(1,_1) - nodepairs_(2,_1) <= 0
_C153: - nodepairs_(1,_1) <= 0
_C154: edgepairs_((2,_3),_(1,_2)) - nodepairs_(2,_1) - nodepairs_(3,_1) <= 0
_C155: edgepairs_((3,_4),_(1,_2)) - nodepairs_(3,_1) - nodepairs_(4,_1) <= 0
_C156: edgepairs_((4,_5),_(1,_2)) - nodepairs_(4,_1) - nodepairs_(5,_1) <= 0
_C157: - nodepairs_(5,_1) <= 0
_C158: edgepairs_((5,_7),_(1,_2)) - nodepairs_(5,_1) - nodepairs_(7,_1) <= 0
_C159: edgepairs_((7,_8),_(0,_1)) - nodepairs_(7,_1) <= 0
_C16: nodepairs_(0,_5) + nodepairs_(1,_5) + nodepairs_(2,_5)
 + nodepairs_(3,_5) + nodepairs_(4,_5) + nodepairs_(5,_5) + nodepairs_(7,_5)
 <= 1
_C160: edgepairs_((7,_9),_(0,_1)) - nodepairs_(7,_1) <= 0
_C161: edgepairs_((0,_1),_(1,_2)) + edgepairs_((0,_1),_(2,_4))
 - nodepairs_(0,_2) - nodepairs_(1,_2) <= 0
_C162: edgepairs_((1,_2),_(1,_2)) + edgepairs_((1,_2),_(2,_4))
 - nodepairs_(1,_2) - nodepairs_(2,_2) <= 0
_C163: - nodepairs_(1,_2) <= 0
_C164: edgepairs_((2,_3),_(1,_2)) + edgepairs_((2,_3),_(2,_4))
 - nodepairs_(2,_2) - nodepairs_(3,_2) <= 0
_C165: edgepairs_((3,_4),_(1,_2)) + edgepairs_((3,_4),_(2,_4))
 - nodepairs_(3,_2) - nodepairs_(4,_2) <= 0
_C166: edgepairs_((4,_5),_(1,_2)) + edgepairs_((4,_5),_(2,_4))
 - nodepairs_(4,_2) - nodepairs_(5,_2) <= 0
_C167: - nodepairs_(5,_2) <= 0
_C168: edgepairs_((5,_7),_(1,_2)) + edgepairs_((5,_7),_(2,_4))
 - nodepairs_(5,_2) - nodepairs_(7,_2) <= 0
_C169: edgepairs_((7,_8),_(2,_3)) - nodepairs_(7,_2) <= 0
_C17: nodepairs_(0,_6) + nodepairs_(1,_6) + nodepairs_(2,_6)
 + nodepairs_(3,_6) + nodepairs_(4,_6) + nodepairs_(5,_6) + nodepairs_(7,_6)
 <= 1
_C170: edgepairs_((7,_9),_(2,_3)) - nodepairs_(7,_2) <= 0
_C171: __dummy <= 0
_C172: __dummy <= 0
_C173: __dummy <= 0
_C174: __dummy <= 0
_C175: __dummy <= 0
_C176: __dummy <= 0
_C177: __dummy <= 0
_C178: __dummy <= 0
_C179: edgepairs_((7,_8),_(2,_3)) - nodepairs_(8,_3) <= 0
_C18: nodepairs_(0,_7) + nodepairs_(1,_7) + nodepairs_(2,_7)
 + nodepairs_(3,_7) + nodepairs_(4,_7) + nodepairs_(5,_7) + nodepairs_(7,_7)
 <= 1
_C180: edgepairs_((7,_9),_(2,_3)) - nodepairs_(9,_3) <= 0
_C181: edgepairs_((0,_1),_(2,_4)) + edgepairs_((0,_1),_(4,_5))
 + edgepairs_((0,_1),_(4,_9)) - nodepairs_(0,_4) - nodepairs_(1,_4) <= 0
_C182: edgepairs_((1,_2),_(2,_4)) + edgepairs_((1,_2),_(4,_5))
 + edgepairs_((1,_2),_(4,_9)) - nodepairs_(1,_4) - nodepairs_(2,_4) <= 0
_C183: - nodepairs_(1,_4) <= 0
_C184: edgepairs_((2,_3),_(2,_4)) + edgepairs_((2,_3),_(4,_5))
 + edgepairs_((2,_3),_(4,_9)) - nodepairs_(2,_4) - nodepairs_(3,_4) <= 0
_C185: edgepairs_((3,_4),_(2,_4)) + edgepairs_((3,_4),_(4,_5))
 + edgepairs_((3,_4),_(4,_9)) - nodepairs_(3,_4) - nodepairs_(4,_4) <= 0
_C186: edgepairs_((4,_5),_(2,_4)) + edgepairs_((4,_5),_(4,_5))
 + edgepairs_((4,_5),_(4,_9)) - nodepairs_(4,_4) - nodepairs_(5,_4) <= 0
_C187: - nodepairs_(5,_4) <= 0
_C188: edgepairs_((5,_7),_(2,_4)) + edgepairs_((5,_7),_(4,_5))
 + edgepairs_((5,_7),_(4,_9)) - nodepairs_(5,_4) - nodepairs_(7,_4) <= 0
_C189: - nodepairs_(7,_4) <= 0
_C19: nodepairs_(0,_8) + nodepairs_(1,_8) + nodepairs_(2,_8)
 + nodepairs_(3,_8) + nodepairs_(4,_8) + nodepairs_(5,_8) + nodepairs_(7,_8)
 <= 1
_C190: - nodepairs_(7,_4) <= 0
_C191: edgepairs_((0,_1),_(4,_5)) + edgepairs_((0,_1),_(5,_6))
 - nodepairs_(0,_5) - nodepairs_(1,_5) <= 0
_C192: edgepairs_((1,_2),_(4,_5)) + edgepairs_((1,_2),_(5,_6))
 - nodepairs_(1,_5) - nodepairs_(2,_5) <= 0
_C193: - nodepairs_(1,_5) <= 0
_C194: edgepairs_((2,_3),_(4,_5)) + edgepairs_((2,_3),_(5,_6))
 - nodepairs_(2,_5) - nodepairs_(3,_5) <= 0
_C195: edgepairs_((3,_4),_(4,_5)) + edgepairs_((3,_4),_(5,_6))
 - nodepairs_(3,_5) - nodepairs_(4,_5) <= 0
_C196: edgepairs_((4,_5),_(4,_5)) + edgepairs_((4,_5),_(5,_6))
 - nodepairs_(4,_5) - nodepairs_(5,_5) <= 0
_C197: - nodepairs_(5,_5) <= 0
_C198: edgepairs_((5,_7),_(4,_5)) + edgepairs_((5,_7),_(5,_6))
 - nodepairs_(5,_5) - nodepairs_(7,_5) <= 0
_C199: - nodepairs_(7,_5) <= 0
_C2: nodepairs_(1,_1) + nodepairs_(1,_2) + nodepairs_(1,_4) + nodepairs_(1,_5)
 + nodepairs_(1,_6) + nodepairs_(1,_7) + nodepairs_(1,_8) + nodepairs_(1,_9)
 <= 1
_C20: nodepairs_(0,_9) + nodepairs_(1,_9) + nodepairs_(2,_9)
 + nodepairs_(3,_9) + nodepairs_(4,_9) + nodepairs_(5,_9) + nodepairs_(7,_9)
 <= 1
_C200: - nodepairs_(7,_5) <= 0
_C201: edgepairs_((0,_1),_(5,_6)) + edgepairs_((0,_1),_(6,_7))
 - nodepairs_(0,_6) - nodepairs_(1,_6) <= 0
_C202: edgepairs_((1,_2),_(5,_6)) + edgepairs_((1,_2),_(6,_7))
 - nodepairs_(1,_6) - nodepairs_(2,_6) <= 0
_C203: - nodepairs_(1,_6) <= 0
_C204: edgepairs_((2,_3),_(5,_6)) + edgepairs_((2,_3),_(6,_7))
 - nodepairs_(2,_6) - nodepairs_(3,_6) <= 0
_C205: edgepairs_((3,_4),_(5,_6)) + edgepairs_((3,_4),_(6,_7))
 - nodepairs_(3,_6) - nodepairs_(4,_6) <= 0
_C206: edgepairs_((4,_5),_(5,_6)) + edgepairs_((4,_5),_(6,_7))
 - nodepairs_(4,_6) - nodepairs_(5,_6) <= 0
_C207: - nodepairs_(5,_6) <= 0
_C208: edgepairs_((5,_7),_(5,_6)) + edgepairs_((5,_7),_(6,_7))
 - nodepairs_(5,_6) - nodepairs_(7,_6) <= 0
_C209: - nodepairs_(7,_6) <= 0
_C21: edgepairs_((0,_1),_(1,_2)) + edgepairs_((0,_1),_(2,_4))
 + edgepairs_((0,_1),_(4,_5)) + edgepairs_((0,_1),_(4,_9))
 + edgepairs_((0,_1),_(5,_6)) + edgepairs_((0,_1),_(6,_7))
 + edgepairs_((0,_1),_(7,_8)) + edgepairs_((0,_1),_(8,_9))
 + edgepairs_((0,_1),__1) = 1
_C210: - nodepairs_(7,_6) <= 0
_C211: edgepairs_((0,_1),_(6,_7)) + edgepairs_((0,_1),_(7,_8))
 - nodepairs_(0,_7) - nodepairs_(1,_7) <= 0
_C212: edgepairs_((1,_2),_(6,_7)) + edgepairs_((1,_2),_(7,_8))
 - nodepairs_(1,_7) - nodepairs_(2,_7) <= 0
_C213: - nodepairs_(1,_7) <= 0
_C214: edgepairs_((2,_3),_(6,_7)) + edgepairs_((2,_3),_(7,_8))
 - nodepairs_(2,_7) - nodepairs_(3,_7) <= 0
_C215: edgepairs_((3,_4),_(6,_7)) + edgepairs_((3,_4),_(7,_8))
 - nodepairs_(3,_7) - nodepairs_(4,_7) <= 0
_C216: edgepairs_((4,_5),_(6,_7)) + edgepairs_((4,_5),_(7,_8))
 - nodepairs_(4,_7) - nodepairs_(5,_7) <= 0
_C217: - nodepairs_(5,_7) <= 0
_C218: edgepairs_((5,_7),_(6,_7)) + edgepairs_((5,_7),_(7,_8))
 - nodepairs_(5,_7) - nodepairs_(7,_7) <= 0
_C219: - nodepairs_(7,_7) <= 0
_C22: edgepairs_((1,_2),_(1,_2)) + edgepairs_((1,_2),_(2,_4))
 + edgepairs_((1,_2),_(4,_5)) + edgepairs_((1,_2),_(4,_9))
 + edgepairs_((1,_2),_(5,_6)) + edgepairs_((1,_2),_(6,_7))
 + edgepairs_((1,_2),_(7,_8)) + edgepairs_((1,_2),_(8,_9))
 + edgepairs_((1,_2),__1) = 1
_C220: - nodepairs_(7,_7) <= 0
_C221: edgepairs_((0,_1),_(7,_8)) + edgepairs_((0,_1),_(8,_9))
 - nodepairs_(0,_8) - nodepairs_(1,_8) <= 0
_C222: edgepairs_((1,_2),_(7,_8)) + edgepairs_((1,_2),_(8,_9))
 - nodepairs_(1,_8) - nodepairs_(2,_8) <= 0
_C223: - nodepairs_(1,_8) <= 0
_C224: edgepairs_((2,_3),_(7,_8)) + edgepairs_((2,_3),_(8,_9))
 - nodepairs_(2,_8) - nodepairs_(3,_8) <= 0
_C225: edgepairs_((3,_4),_(7,_8)) + edgepairs_((3,_4),_(8,_9))
 - nodepairs_(3,_8) - nodepairs_(4,_8) <= 0
_C226: edgepairs_((4,_5),_(7,_8)) + edgepairs_((4,_5),_(8,_9))
 - nodepairs_(4,_8) - nodepairs_(5,_8) <= 0
_C227: - nodepairs_(5,_8) <= 0
_C228: edgepairs_((5,_7),_(7,_8)) + edgepairs_((5,_7),_(8,_9))
 - nodepairs_(5,_8) - nodepairs_(7,_8) <= 0
_C229: - nodepairs_(7,_8) <= 0
_C23: edgepairs_((1,_6),__1) = 1
_C230: - nodepairs_(7,_8) <= 0
_C231: edgepairs_((0,_1),_(4,_9)) + edgepairs_((0,_1),_(8,_9))
 - nodepairs_(0,_9) - nodepairs_(1,_9) <= 0
_C232: edgepairs_((1,_2),_(4,_9)) + edgepairs_((1,_2),_(8,_9))
 - nodepairs_(1,_9) - nodepairs_(2,_9) <= 0
_C233: - nodepairs_(1,_9) <= 0
_C234: edgepairs_((2,_3),_(4,_9)) + edgepairs_((2,_3),_(8,_9))
 - nodepairs_(2,_9) - nodepairs_(3,_9) <= 0
_C235: edgepairs_((3,_4),_(4,_9)) + edgepairs_((3,_4),_(8,_9))
 - nodepairs_(3,_9) - nodepairs_(4,_9) <= 0
_C236: edgepairs_((4,_5),_(4,_9)) + edgepairs_((4,_5),_(8,_9))
 - nodepairs_(4,_9) - nodepairs_(5,_9) <= 0
_C237: - nodepairs_(5,_9) <= 0
_C238: edgepairs_((5,_7),_(4,_9)) + edgepairs_((5,_7),_(8,_9))
 - nodepairs_(5,_9) - nodepairs_(7,_9) <= 0
_C239: - nodepairs_(7,_9) <= 0
_C24: edgepairs_((2,_3),_(1,_2)) + edgepairs_((2,_3),_(2,_4))
 + edgepairs_((2,_3),_(4,_5)) + edgepairs_((2,_3),_(4,_9))
 + edgepairs_((2,_3),_(5,_6)) + edgepairs_((2,_3),_(6,_7))
 + edgepairs_((2,_3),_(7,_8)) + edgepairs_((2,_3),_(8,_9))
 + edgepairs_((2,_3),__1) = 1
_C240: - nodepairs_(7,_9) <= 0
_C241: 0.5 edgepairs_((0,_1),_(4,_5)) + 0.5 edgepairs_((0,_1),_(4,_9))
 + 0.5 edgepairs_((0,_1),_(5,_6)) + 0.5 edgepairs_((0,_1),_(6,_7))
 + 0.5 edgepairs_((0,_1),_(7,_8)) + 0.5 edgepairs_((0,_1),_(8,_9))
 + edgepairs_((0,_1),__1) + 0.5 edgepairs_((1,_2),_(1,_2))
 + 0.5 edgepairs_((1,_2),_(2,_4)) + 1.5 edgepairs_((1,_2),__1)
 + 1.5 edgepairs_((1,_6),__1) + 0.5 edgepairs_((2,_3),_(1,_2))
 + 0.5 edgepairs_((2,_3),_(2,_4)) + 1.5 edgepairs_((2,_3),__1)
 + 0.5 edgepairs_((3,_4),_(1,_2)) + 0.5 edgepairs_((3,_4),_(2,_4))
 + 1.5 edgepairs_((3,_4),__1) + 0.5 edgepairs_((4,_5),_(1,_2))
 + 0.5 edgepairs_((4,_5),_(2,_4)) + 1.5 edgepairs_((4,_5),__1)
 + 1.5 edgepairs_((5,_6),__1) + 0.5 edgepairs_((5,_7),_(4,_5))
 + 0.5 edgepairs_((5,_7),_(4,_9)) + 0.5 edgepairs_((5,_7),_(5,_6))
 + 0.5 edgepairs_((5,_7),_(6,_7)) + 0.5 edgepairs_((5,_7),_(7,_8))
 + 0.5 edgepairs_((5,_7),_(8,_9)) + edgepairs_((5,_7),__1)
 + edgepairs_((7,_8),_(2,_3)) + edgepairs_((7,_8),__1)
 + edgepairs_((7,_9),_(0,_1)) + 2 edgepairs_((7,_9),__1)
 + edgepairs_(_1,_(0,_1)) + edgepairs_(_1,_(1,_2)) + 2 edgepairs_(_1,_(2,_3))
 + edgepairs_(_1,_(2,_4)) + 1.5 edgepairs_(_1,_(4,_5))
 + 1.5 edgepairs_(_1,_(4,_9)) + 1.5 edgepairs_(_1,_(5,_6))
 + 1.5 edgepairs_(_1,_(6,_7)) + 1.5 edgepairs_(_1,_(7,_8))
 + 1.5 edgepairs_(_1,_(8,_9)) <= 10
_C25: edgepairs_((3,_4),_(1,_2)) + edgepairs_((3,_4),_(2,_4))
 + edgepairs_((3,_4),_(4,_5)) + edgepairs_((3,_4),_(4,_9))
 + edgepairs_((3,_4),_(5,_6)) + edgepairs_((3,_4),_(6,_7))
 + edgepairs_((3,_4),_(7,_8)) + edgepairs_((3,_4),_(8,_9))
 + edgepairs_((3,_4),__1) = 1
_C26: edgepairs_((4,_5),_(1,_2)) + edgepairs_((4,_5),_(2,_4))
 + edgepairs_((4,_5),_(4,_5)) + edgepairs_((4,_5),_(4,_9))
 + edgepairs_((4,_5),_(5,_6)) + edgepairs_((4,_5),_(6,_7))
 + edgepairs_((4,_5),_(7,_8)) + edgepairs_((4,_5),_(8,_9))
 + edgepairs_((4,_5),__1) = 1
_C27: edgepairs_((5,_6),__1) = 1
_C28: edgepairs_((5,_7),_(1,_2)) + edgepairs_((5,_7),_(2,_4))
 + edgepairs_((5,_7),_(4,_5)) + edgepairs_((5,_7),_(4,_9))
 + edgepairs_((5,_7),_(5,_6)) + edgepairs_((5,_7),_(6,_7))
 + edgepairs_((5,_7),_(7,_8)) + edgepairs_((5,_7),_(8,_9))
 + edgepairs_((5,_7),__1) = 1
_C29: edgepairs_((7,_8),_(0,_1)) + edgepairs_((7,_8),_(2,_3))
 + edgepairs_((7,_8),__1) = 1
_C3: nodepairs_(2,_1) + nodepairs_(2,_2) + nodepairs_(2,_4) + nodepairs_(2,_5)
 + nodepairs_(2,_6) + nodepairs_(2,_7) + nodepairs_(2,_8) + nodepairs_(2,_9)
 <= 1
_C30: edgepairs_((7,_9),_(0,_1)) + edgepairs_((7,_9),_(2,_3))
 + edgepairs_((7,_9),__1) = 1
_C31: edgepairs_((7,_8),_(0,_1)) + edgepairs_((7,_9),_(0,_1))
 + edgepairs_(_1,_(0,_1)) = 1
_C32: edgepairs_((0,_1),_(1,_2)) + edgepairs_((1,_2),_(1,_2))
 + edgepairs_((2,_3),_(1,_2)) + edgepairs_((3,_4),_(1,_2))
 + edgepairs_((4,_5),_(1,_2)) + edgepairs_((5,_7),_(1,_2))
 + edgepairs_(_1,_(1,_2)) = 1
_C33: edgepairs_((7,_8),_(2,_3)) + edgepairs_((7,_9),_(2,_3))
 + edgepairs_(_1,_(2,_3)) = 1
_C34: edgepairs_((0,_1),_(2,_4)) + edgepairs_((1,_2),_(2,_4))
 + edgepairs_((2,_3),_(2,_4)) + edgepairs_((3,_4),_(2,_4))
 + edgepairs_((4,_5),_(2,_4)) + edgepairs_((5,_7),_(2,_4))
 + edgepairs_(_1,_(2,_4)) = 1
_C35: edgepairs_((0,_1),_(4,_5)) + edgepairs_((1,_2),_(4,_5))
 + edgepairs_((2,_3),_(4,_5)) + edgepairs_((3,_4),_(4,_5))
 + edgepairs_((4,_5),_(4,_5)) + edgepairs_((5,_7),_(4,_5))
 + edgepairs_(_1,_(4,_5)) = 1
_C36: edgepairs_((0,_1),_(4,_9)) + edgepairs_((1,_2),_(4,_9))
 + edgepairs_((2,_3),_(4,_9)) + edgepairs_((3,_4),_(4,_9))
 + edgepairs_((4,_5),_(4,_9)) + edgepairs_((5,_7),_(4,_9))
 + edgepairs_(_1,_(4,_9)) = 1
_C37: edgepairs_((0,_1),_(5,_6)) + edgepairs_((1,_2),_(5,_6))
 + edgepairs_((2,_3),_(5,_6)) + edgepairs_((3,_4),_(5,_6))
 + edgepairs_((4,_5),_(5,_6)) + edgepairs_((5,_7),_(5,_6))
 + edgepairs_(_1,_(5,_6)) = 1
_C38: edgepairs_((0,_1),_(6,_7)) + edgepairs_((1,_2),_(6,_7))
 + edgepairs_((2,_3),_(6,_7)) + edgepairs_((3,_4),_(6,_7))
 + edgepairs_((4,_5),_(6,_7)) + edgepairs_((5,_7),_(6,_7))
 + edgepairs_(_1,_(6,_7)) = 1
_C39: edgepairs_((0,_1),_(7,_8)) + edgepairs_((1,_2),_(7,_8))
 + edgepairs_((2,_3),_(7,_8)) + edgepairs_((3,_4),_(7,_8))
 + edgepairs_((4,_5),_(7,_8)) + edgepairs_((5,_7),_(7,_8))
 + edgepairs_(_1,_(7,_8)) = 1
_C4: nodepairs_(3,_1) + nodepairs_(3,_2) + nodepairs_(3,_4) + nodepairs_(3,_5)
 + nodepairs_(3,_6) + nodepairs_(3,_7) + nodepairs_(3,_8) + nodepairs_(3,_9)
 <= 1
_C40: edgepairs_((0,_1),_(8,_9)) + edgepairs_((1,_2),_(8,_9))
 + edgepairs_((2,_3),_(8,_9)) + edgepairs_((3,_4),_(8,_9))
 + edgepairs_((4,_5),_(8,_9)) + edgepairs_((5,_7),_(8,_9))
 + edgepairs_(_1,_(8,_9)) = 1
_C41: - nodepairs_(0,_1) <= 0
_C42: edgepairs_((0,_1),_(1,_2)) - nodepairs_(0,_1) - nodepairs_(0,_2) <= 0
_C43: - nodepairs_(0,_2) <= 0
_C44: edgepairs_((0,_1),_(2,_4)) - nodepairs_(0,_2) - nodepairs_(0,_4) <= 0
_C45: edgepairs_((0,_1),_(4,_5)) - nodepairs_(0,_4) - nodepairs_(0,_5) <= 0
_C46: edgepairs_((0,_1),_(4,_9)) - nodepairs_(0,_4) - nodepairs_(0,_9) <= 0
_C47: edgepairs_((0,_1),_(5,_6)) - nodepairs_(0,_5) - nodepairs_(0,_6) <= 0
_C48: edgepairs_((0,_1),_(6,_7)) - nodepairs_(0,_6) - nodepairs_(0,_7) <= 0
_C49: edgepairs_((0,_1),_(7,_8)) - nodepairs_(0,_7) - nodepairs_(0,_8) <= 0
_C5: nodepairs_(4,_1) + nodepairs_(4,_2) + nodepairs_(4,_4) + nodepairs_(4,_5)
 + nodepairs_(4,_6) + nodepairs_(4,_7) + nodepairs_(4,_8) + nodepairs_(4,_9)
 <= 1
_C50: edgepairs_((0,_1),_(8,_9)) - nodepairs_(0,_8) - nodepairs_(0,_9) <= 0
_C51: - nodepairs_(1,_1) <= 0
_C52: edgepairs_((0,_1),_(1,_2)) + edgepairs_((1,_2),_(1,_2))
 - nodepairs_(1,_1) - nodepairs_(1,_2) <= 0
_C53: - nodepairs_(1,_2) <= 0
_C54: edgepairs_((0,_1),_(2,_4)) + edgepairs_((1,_2),_(2,_4))
 - nodepairs_(1,_2) - nodepairs_(1,_4) <= 0
_C55: edgepairs_((0,_1),_(4,_5)) + edgepairs_((1,_2),_(4,_5))
 - nodepairs_(1,_4) - nodepairs_(1,_5) <= 0
_C56: edgepairs_((0,_1),_(4,_9)) + edgepairs_((1,_2),_(4,_9))
 - nodepairs_(1,_4) - nodepairs_(1,_9) <= 0
_C57: edgepairs_((0,_1),_(5,_6)) + edgepairs_((1,_2),_(5,_6))
 - nodepairs_(1,_5) - nodepairs_(1,_6) <= 0
_C58: edgepairs_((0,_1),_(6,_7)) + edgepairs_((1,_2),_(6,_7))
 - nodepairs_(1,_6) - nodepairs_(1,_7) <= 0
_C59: edgepairs_((0,_1),_(7,_8)) + edgepairs_((1,_2),_(7,_8))
 - nodepairs_(1,_7) - nodepairs_(1,_8) <= 0
_C6: nodepairs_(5,_1) + nodepairs_(5,_2) + nodepairs_(5,_4) + nodepairs_(5,_5)
 + nodepairs_(5,_6) + nodepairs_(5,_7) + nodepairs_(5,_8) + nodepairs_(5,_9)
 <= 1
_C60: edgepairs_((0,_1),_(8,_9)) + edgepairs_((1,_2),_(8,_9))
 - nodepairs_(1,_8) - nodepairs_(1,_9) <= 0
_C61: - nodepairs_(2,_1) <= 0
_C62: edgepairs_((1,_2),_(1,_2)) + edgepairs_((2,_3),_(1,_2))
 - nodepairs_(2,_1) - nodepairs_(2,_2) <= 0
_C63: - nodepairs_(2,_2) <= 0
_C64: edgepairs_((1,_2),_(2,_4)) + edgepairs_((2,_3),_(2,_4))
 - nodepairs_(2,_2) - nodepairs_(2,_4) <= 0
_C65: edgepairs_((1,_2),_(4,_5)) + edgepairs_((2,_3),_(4,_5))
 - nodepairs_(2,_4) - nodepairs_(2,_5) <= 0
_C66: edgepairs_((1,_2),_(4,_9)) + edgepairs_((2,_3),_(4,_9))
 - nodepairs_(2,_4) - nodepairs_(2,_9) <= 0
_C67: edgepairs_((1,_2),_(5,_6)) + edgepairs_((2,_3),_(5,_6))
 - nodepairs_(2,_5) - nodepairs_(2,_6) <= 0
_C68: edgepairs_((1,_2),_(6,_7)) + edgepairs_((2,_3),_(6,_7))
 - nodepairs_(2,_6) - nodepairs_(2,_7) <= 0
_C69: edgepairs_((1,_2),_(7,_8)) + edgepairs_((2,_3),_(7,_8))
 - nodepairs_(2,_7) - nodepairs_(2,_8) <= 0
_C7: __dummy <= 1
_C70: edgepairs_((1,_2),_(8,_9)) + edgepairs_((2,_3),_(8,_9))
 - nodepairs_(2,_8) - nodepairs_(2,_9) <= 0
_C71: - nodepairs_(3,_1) <= 0
_C72: edgepairs_((2,_3),_(1,_2)) + edgepairs_((3,_4),_(1,_2))
 - nodepairs_(3,_1) - nodepairs_(3,_2) <= 0
_C73: - nodepairs_(3,_2) <= 0
_C74: edgepairs_((2,_3),_(2,_4)) + edgepairs_((3,_4),_(2,_4))
 - nodepairs_(3,_2) - nodepairs_(3,_4) <= 0
_C75: edgepairs_((2,_3),_(4,_5)) + edgepairs_((3,_4),_(4,_5))
 - nodepairs_(3,_4) - nodepairs_(3,_5) <= 0
_C76: edgepairs_((2,_3),_(4,_9)) + edgepairs_((3,_4),_(4,_9))
 - nodepairs_(3,_4) - nodepairs_(3,_9) <= 0
_C77: edgepairs_((2,_3),_(5,_6)) + edgepairs_((3,_4),_(5,_6))
 - nodepairs_(3,_5) - nodepairs_(3,_6) <= 0
_C78: edgepairs_((2,_3),_(6,_7)) + edgepairs_((3,_4),_(6,_7))
 - nodepairs_(3,_6) - nodepairs_(3,_7) <= 0
_C79: edgepairs_((2,_3),_(7,_8)) + edgepairs_((3,_4),_(7,_8))
 - nodepairs_(3,_7) - nodepairs_(3,_8) <= 0
_C8: nodepairs_(7,_1) + nodepairs_(7,_2) + nodepairs_(7,_4) + nodepairs_(7,_5)
 + nodepairs_(7,_6) + nodepairs_(7,_7) + nodepairs_(7,_8) + nodepairs_(7,_9)
 <= 1
_C80: edgepairs_((2,_3),_(8,_9)) + edgepairs_((3,_4),_(8,_9))
 - nodepairs_(3,_8) - nodepairs_(3,_9) <= 0
_C81: - nodepairs_(4,_1) <= 0
_C82: edgepairs_((3,_4),_(1,_2)) + edgepairs_((4,_5),_(1,_2))
 - nodepairs_(4,_1) - nodepairs_(4,_2) <= 0
_C83: - nodepairs_(4,_2) <= 0
_C84: edgepairs_((3,_4),_(2,_4)) + edgepairs_((4,_5),_(2,_4))
 - nodepairs_(4,_2) - nodepairs_(4,_4) <= 0
_C85: edgepairs_((3,_4),_(4,_5)) + edgepairs_((4,_5),_(4,_5))
 - nodepairs_(4,_4) - nodepairs_(4,_5) <= 0
_C86: edgepairs_((3,_4),_(4,_9)) + edgepairs_((4,_5),_(4,_9))
 - nodepairs_(4,_4) - nodepairs_(4,_9) <= 0
_C87: edgepairs_((3,_4),_(5,_6)) + edgepairs_((4,_5),_(5,_6))
 - nodepairs_(4,_5) - nodepairs_(4,_6) <= 0
_C88: edgepairs_((3,_4),_(6,_7)) + edgepairs_((4,_5),_(6,_7))
 - nodepairs_(4,_6) - nodepairs_(4,_7) <= 0
_C89: edgepairs_((3,_4),_(7,_8)) + edgepairs_((4,_5),_(7,_8))
 - nodepairs_(4,_7) - nodepairs_(4,_8) <= 0
_C9: nodepairs_(8,_0) + nodepairs_(8,_3) <= 1
_C90: edgepairs_((3,_4),_(8,_9)) + edgepairs_((4,_5),_(8,_9))
 - nodepairs_(4,_8) - nodepairs_(4,_9) <= 0
_C91: - nodepairs_(5,_1) <= 0
_C92: edgepairs_((4,_5),_(1,_2)) + edgepairs_((5,_7),_(1,_2))
 - nodepairs_(5,_1) - nodepairs_(5,_2) <= 0
_C93: - nodepairs_(5,_2) <= 0
_C94: edgepairs_((4,_5),_(2,_4)) + edgepairs_((5,_7),_(2,_4))
 - nodepairs_(5,_2) - nodepairs_(5,_4) <= 0
_C95: edgepairs_((4,_5),_(4,_5)) + edgepairs_((5,_7),_(4,_5))
 - nodepairs_(5,_4) - nodepairs_(5,_5) <= 0
_C96: edgepairs_((4,_5),_(4,_9)) + edgepairs_((5,_7),_(4,_9))
 - nodepairs_(5,_4) - nodepairs_(5,_9) <= 0
_C97: edgepairs_((4,_5),_(5,_6)) + edgepairs_((5,_7),_(5,_6))
 - nodepairs_(5,_5) - nodepairs_(5,_6) <= 0
_C98: edgepairs_((4,_5),_(6,_7)) + edgepairs_((5,_7),_(6,_7))
 - nodepairs_(5,_6) - nodepairs_(5,_7) <= 0
_C99: edgepairs_((4,_5),_(7,_8)) + edgepairs_((5,_7),_(7,_8))
 - nodepairs_(5,_7) - nodepairs_(5,_8) <= 0
Binaries
edgepairs_((0,_1),_(1,_2))
edgepairs_((0,_1),_(2,_4))
edgepairs_((0,_1),_(4,_5))
edgepairs_((0,_1),_(4,_9))
edgepairs_((0,_1),_(5,_6))
edgepairs_((0,_1),_(6,_7))
edgepairs_((0,_1),_(7,_8))
edgepairs_((0,_1),_(8,_9))
edgepairs_((0,_1),__1)
edgepairs_((1,_2),_(1,_2))
edgepairs_((1,_2),_(2,_4))
edgepairs_((1,_2),_(4,_5))
edgepairs_((1,_2),_(4,_9))
edgepairs_((1,_2),_(5,_6))
edgepairs_((1,_2),_(6,_7))
edgepairs_((1,_2),_(7,_8))
edgepairs_((1,_2),_(8,_9))
edgepairs_((1,_2),__1)
edgepairs_((1,_6),__1)
edgepairs_((2,_3),_(1,_2))
edgepairs_((2,_3),_(2,_4))
edgepairs_((2,_3),_(4,_5))
edgepairs_((2,_3),_(4,_9))
edgepairs_((2,_3),_(5,_6))
edgepairs_((2,_3),_(6,_7))
edgepairs_((2,_3),_(7,_8))
edgepairs_((2,_3),_(8,_9))
edgepairs_((2,_3),__1)
edgepairs_((3,_4),_(1,_2))
edgepairs_((3,_4),_(2,_4))
edgepairs_((3,_4),_(4,_5))
edgepairs_((3,_4),_(4,_9))
edgepairs_((3,_4),_(5,_6))
edgepairs_((3,_4),_(6,_7))
edgepairs_((3,_4),_(7,_8))
edgepairs_((3,_4),_(8,_9))
edgepairs_((3,_4),__1)
edgepairs_((4,_5),_(1,_2))
edgepairs_((4,_5),_(2,_4))
edgepairs_((4,_5),_(4,_5))
edgepairs_((4,_5),_(4,_9))
edgepairs_((4,_5),_(5,_6))
edgepairs_((4,_5),_(6,_7))
edgepairs_((4,_5),_(7,_8))
edgepairs_((4,_5),_(8,_9))
edgepairs_((4,_5),__1)
edgepairs_((5,_6),__1)
edgepairs_((5,_7),_(1,_2))
edgepairs_((5,_7),_(2,_4))
edgepairs_((5,_7),_(4,_5))
edgepairs_((5,_7),_(4,_9))
edgepairs_((5,_7),_(5,_6))
edgepairs_((5,_7),_(6,_7))
edgepairs_((5,_7),_(7,_8))
edgepairs_((5,_7),_(8,_9))
edgepairs_((5,_7),__1)
edgepairs_((7,_8),_(0,_1))
edgepairs_((7,_8),_(2,_3))
edgepairs_((7,_8),__1)
edgepairs_((7,_9),_(0,_1))
edgepairs_((7,_9),_(2,_3))
edgepairs_((7,_9),__1)
edgepairs_(_1,_(0,_1))
edgepairs_(_1,_(1,_2))
edgepairs_(_1,_(2,_3))
edgepairs_(_1,_(2,_4))
edgepairs_(_1,_(4,_5))
edgepairs_(_1,_(4,_9))
edgepairs_(_1,_(5,_6))
edgepairs_(_1,_(6,_7))
edgepairs_(_1,_(7,_8))
edgepairs_(_1,_(8,_9))
nodepairs_(0,_1)
nodepairs_(0,_2)
nodepairs_(0,_4)
nodepairs_(0,_5)
nodepairs_(0,_6)
nodepairs_(0,_7)
nodepairs_(0,_8)
nodepairs_(0,_9)
nodepairs_(1,_1)
nodepairs_(1,_2)
nodepairs_(1,_4)
nodepairs_(1,_5)
nodepairs_(1,_6)
nodepairs_(1,_7)
nodepairs_(1,_8)
nodepairs_(1,_9)
nodepairs_(2,_1)
nodepairs_(2,_2)
nodepairs_(2,_4)
nodepairs_(2,_5)
nodepairs_(2,_6)
nodepairs_(2,_7)
nodepairs_(2,_8)
nodepairs_(2,_9)
nodepairs_(3,_1)
nodepairs_(3,_2)
nodepairs_(3,_4)
nodepairs_(3,_5)
nodepairs_(3,_6)
nodepairs_(3,_7)
nodepairs_(3,_8)
nodepairs_(3,_9)
nodepairs_(4,_1)
nodepairs_(4,_2)
nodepairs_(4,_4)
nodepairs_(4,_5)
nodepairs_(4,_6)
nodepairs_(4,_7)
nodepairs_(4,_8)
nodepairs_(4,_9)
nodepairs_(5,_1)
nodepairs_(5,_2)
nodepairs_(5,_4)
nodepairs_(5,_5)
nodepairs_(5,_6)
nodepairs_(5,_7)
nodepairs_(5,_8)
nodepairs_(5,_9)
nodepairs_(7,_1)
nodepairs_(7,_2)
nodepairs_(7,_4)
nodepairs_(7,_5)
nodepairs_(7,_6)
nodepairs_(7,_7)
nodepairs_(7,_8)
nodepairs_(7,_9)
nodepairs_(8,_0)
nodepairs_(8,_3)
nodepairs_(9,_0)
nodepairs_(9,_3)
End
