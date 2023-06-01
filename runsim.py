import sys
import numpy as np
from util.bswfocus import BSWFocus


def main():
    Ml = np.load(sys.argv[1])
    i, j = int(sys.argv[2]), int(sys.argv[3])
    res = int(sys.argv[4])
    box_sy = float(sys.argv[5])
    box_sx = float(sys.argv[6])
    n_lo = float(sys.argv[7])
    n_hi = float(sys.argv[8])
    design_yr = [float(sys.argv[9]), float(sys.argv[10])]
    focus_yr = [float(sys.argv[11]), float(sys.argv[12])]

    Ml[i, j] = 1
    tM = np.vstack((Ml, np.flipud(Ml)))

    bsw = BSWFocus(sim_resolution=res,
                   design_yr=design_yr,
                   focus_yr=focus_yr,
                   n_lo=n_lo,
                   n_hi=n_hi,
                   box_sx=box_sx,
                   box_sy=box_sy)
    bsw.set_design(tM)
    bsw.run()
    field = bsw.get_focus_box_field()
    print("FIELD:\n{}".format(np.square(np.linalg.norm(field))))

if __name__ == '__main__':
    main()
