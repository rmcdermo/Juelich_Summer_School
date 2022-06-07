# from pylab import *
from matplotlib import *
import matplotlib.pyplot as plt


def read_csv(base, chid):

    name_chid = "results/%s%s_pressit.csv" % (base, chid)
    print('open ', name_chid)

    chid_in = open(name_chid, 'r')
    chid_input = chid_in.readlines()
    chid_in.close()

    start = 1

    time = []
    step = []
    iter = []
    totl = []
    tcyc = []
    verr = []
    perr = []

    for line in chid_input:

        if (start > 0):
            start -= 1
            continue

        line, null = line.split("\n")
        quan = line.split(",")

        time0 = float(quan[0])
        step0 = int(quan[1])
        iter0 = int(quan[2])
        totl0 = int(quan[3])
        tcyc0 = int(quan[1])
        verr0 = float(quan[8])
        perr0 = float(quan[13])

        # print(time0, tcyc0, verr0, perr0)
        time.append(time0)
        step.append(step0)
        iter.append(iter0)
        totl.append(totl0)
        tcyc.append(tcyc0)
        verr.append(verr0)
        perr.append(perr0)

    return (time, step, iter, totl, tcyc, verr, perr)


def get_max(time, step, iter, totl, verr, perr):

    stp_old = -1

    ite = []
    ve = []
    pe = []

    ite1 = []
    ve1 = []
    pe1 = []
    ite2 = []
    ve2 = []
    pe2 = []

    part = 2
    count = 0

    for i in range(len(totl)):

        stp = step[i]

        if iter[i] == 1:
            if count == 0:
                part = 1
                count = 1
            else:
                part = 2
                count = 0

        if part == 1:
            ite1.append(iter[i])
            ve1.append(verr[i])
            pe1.append(perr[i])

        elif part == 2:
            ite2.append(iter[i])
            ve2.append(verr[i])
            pe2.append(perr[i])

        if step[i] > 1 and stp != stp_old:
            ite.append(max(ite1[-1], ite2[-1]))
            ve.append(max(ve1[-1], ve2[-1]))
            pe.append(max(pe1[-1], pe2[-1]))
            ite1 = []
            ve1 = []
            pe1 = []
            ite2 = []
            ve2 = []
            pe2 = []

        stp_old = stp

    return (ite, ve, pe)


def plot_verr(time, tend, step, iter, totl, tcyc, verr, tol, output):

    fig = plt.figure(facecolor='w')

    ax1 = fig.add_subplot(111)

    # ax1.set_xscale('log')
    ax1.set_yscale('log')

    ax1.grid(True)
    # ax1.plot(totl, verr, '-r', linewidth=1.0)
    ax1.plot(time, verr, '-r', linewidth=0.25)

    ax1.set_xlim(0, tend)
    ax1.set_xlim(10, 11)
    ax1.set_ylim(0.000000000000000001, 10.0)

    ax1.set_xlabel('Simulation Time [s]', fontsize=14, color='k')
    ax1.set_ylabel('Velocity Error [m/s] ', fontsize=14, color='k')

    for t1 in ax1.get_yticklabels():
        t1.set_color('k')

    output0 = "plots/%s_verr.png" % output
    print('output=', output0)
    plt.savefig(output0)
    plt.close
    plt.clf()


def plot_perr(time, tend, step, iter, totl, tcyc, perr, tol, output):

    fig = plt.figure(facecolor='w')

    ax1 = fig.add_subplot(111)
    # ax1.set_xscale('log')
    ax1.set_yscale('log')

    ax1.grid(True)
    ax1.plot(time, perr, '-k', linewidth=0.25)
    # ax1.set_title(r'Pressure Error', fontsize=16)

    ax1.set_xlim(0, tend)
    ax1.set_xlim(10, 11.0)
    ax1.set_yticks([0.0000000001, 0.00000001, 0.000001, 0.0001,
                    0.01, 1.0, 100.0, 10000.0])
    ax1.set_ylim(0.0000000001, 100000.0)
    plt.axhline(y=tol, color='m', linestyle='-', linewidth=1)

    ax1.set_xlabel('Simulation Time [s]', fontsize=14, color='k')
    ax1.set_ylabel('Pressure Error ', fontsize=14, color='k')

    for t1 in ax1.get_yticklabels():
        t1.set_color('k')

    output0 = "plots/%s_perr.png" % output
    plt.savefig(output0)
    plt.close
    plt.clf()


def plot_perr_detail(time, step, iter, totl, tcyc, perr, output, tol,
                     xleft, xmid, xright):

    fig = plt.figure(facecolor='w')

    if xmid - xleft < 10:
        xleft0 = xleft - 1
        xright0 = xright + 1
    else:
        xleft0 = xleft - 5
        xright0 = xright + 5

    ax1 = fig.add_subplot(111)
    ax1.set_yscale('log')

    # ax1.set_title(r'Pressure Error', fontsize=16)

    axes1 = plt.gca()
    axes2 = axes1.twiny()

    axes1.set_xlabel("Total number of pressure solutions", fontsize=14)
    axes1.set_xticks([xleft, xmid, xright])

    axes2.set_xticks([1, iter[xmid-1], iter[xright]])
    axes2.set_yticks([0.0000000001, 0.00000001, 0.000001, 0.0001,
                      0.01, 1.0, 100.0, 10000.0])

    plt.axhline(y=tol, color='m', linestyle='-', linewidth=1)

    msize = 2.0
    lsize = 1.0
    lstyle = '-'

    ax1.set_ylabel('Pressure Error ', fontsize=14, color='k')
    ax1.grid(True)
    if xmid - xleft > 50:
        if 'tol-3' in output:
            ax1.plot(totl, perr, 'r', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        elif 'glmat' in output:
            msize = 5
            ax1.plot(totl, perr, 'c', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        elif 'scarc' in output:
            msize = 5
            ax1.plot(totl, perr, 'b', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        elif 'tol-6' in output:
            ax1.plot(totl, perr, 'g', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        else:
            ax1.plot(totl, perr, 'k', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
    else:
        if 'tol-3' in output:
            ax1.plot(totl, perr, 'r', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        elif 'glmat' in output:
            msize = 5
            ax1.plot(totl, perr, 'c', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        elif 'scarc' in output:
            msize = 5
            ax1.plot(totl, perr, 'b', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        elif 'tol-6' in output:
            ax1.plot(totl, perr, 'g', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)
        else:
            ax1.plot(totl, perr, 'k', linestyle=lstyle, marker='.',
                     markersize=msize, linewidth=lsize)

    ax1.set_xlim(xleft0, xright0)
    ax1.set_ylim(1E-10, 1E+5)

    for t1 in ax1.get_yticklabels():
        t1.set_color('k')

    output0 = "plots/%s_perr_detail.png" % output
    plt.savefig(output0)
    plt.close


base = './'
tend = 30.0

chids = []
chids.append('tunnel_demo_fft_tol-3')
chids.append('tunnel_demo_fft_tol-6')
chids.append('tunnel_demo_glmat')
chids.append('tunnel_demo_scarc_insep')

nchid = len(chids)
for chid in chids:
    (time, step, iter, totl, tcyc, verr, perr) = read_csv(base, chid)


chid = 'tunnel_demo_fft_tol-3'
tol = 1.0E-3
(time, step, iter, totl, tcyc, verr, perr) = read_csv(base, chid)
(iter_last, verr_last, perr_last) = get_max(time, step, iter, totl, verr, perr)

# plot_verr(time, tend, step, iter, totl, tcyc, verr, tol, chid)
plot_perr(time, tend, step, iter, totl, tcyc, perr, tol, chid)
plot_perr_detail(time, step, iter, totl, tcyc, perr, chid, tol,
                 63454, 63516, 63598)

chid = 'tunnel_demo_fft_tol-6'
tol = 1.0E-6
(time, step, iter, totl, tcyc, verr, perr) = read_csv(base, chid)
(iter_last, verr_last, perr_last) = get_max(time, step, iter, totl, verr, perr)

# plot_verr(time, tend, step, iter, totl, tcyc, verr, tol, chid)
plot_perr(time, tend, step, iter, totl, tcyc, perr, tol, chid)
plot_perr_detail(time, step, iter, totl, tcyc, perr, chid, tol,
                 105654, 105747, 105873)

chid = 'tunnel_demo_glmat'
tol = 500.0
(time, step, iter, totl, tcyc, verr, perr) = read_csv(base, chid)
(iter_last, verr_last, perr_last) = get_max(time, step, iter, totl, verr, perr)

# plot_verr(time, tend, step, iter, totl, tcyc, verr, tol, chid)
plot_perr(time, tend, step, iter, totl, tcyc, perr, tol, chid)
plot_perr_detail(time, step, iter, totl, tcyc, perr, chid, tol,
                 5468, 5470, 5476)

chid = 'tunnel_demo_scarc_insep'
tol = 1.0E-8
(time, step, iter, totl, tcyc, verr, perr) = read_csv(base, chid)
(iter_last, verr_last, perr_last) = get_max(time, step, iter, totl, verr, perr)

# plot_verr(time, tend, step, iter, totl, tcyc, verr, tol, chid)
plot_perr(time, tend, step, iter, totl, tcyc, perr, tol, chid)
plot_perr_detail(time, step, iter, totl, tcyc, perr, chid, tol,
                 1027, 1028, 1029)
