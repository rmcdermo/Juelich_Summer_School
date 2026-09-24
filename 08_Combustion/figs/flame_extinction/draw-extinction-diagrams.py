"""Rebuild schematic extinction figures; geometry is illustrative, not measured data."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Rectangle, Ellipse, Polygon
from matplotlib.path import Path as MPath
from PIL import Image

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 19, 'svg.hashsalt': 'extinction-diagrams'})

def save(fig, name):
    fig.savefig(OUT / name, transparent=True, metadata={'Date': None})
    plt.close(fig)

def path(ax, points, color='#888', width=1.3):
    ax.add_patch(PathPatch(MPath(points, [MPath.MOVETO]+[MPath.CURVE4]*(len(points)-1)),
                           facecolor='none', edgecolor=color, lw=width))

def opposed_jet():
    fig, ax = plt.subplots(figsize=(6,5))
    fig.subplots_adjust(0,0,1,1);ax.set(xlim=(0,1),ylim=(0,1),aspect='equal');ax.axis('off')
    # Nozzles, opposed streamlines, stagnation plane, and flame sheet.
    for sign in [-1,1]:
        def xy(x,y): return (x, .5+sign*y)
        path(ax,[xy(.2,.46),xy(.27,.45),xy(.28,.34),xy(.28,.3)],width=2.5)
        ax.plot([.28,.72],[.5+sign*.3]*2,color='#999',lw=2.5)
        path(ax,[xy(.72,.3),xy(.72,.34),xy(.73,.45),xy(.8,.46)],width=2.5)
        for x in [.3,.4,.6,.7]:
            end=.06 if x<.5 else .94
            path(ax,[xy(x,.29),xy(x,.13),xy(end,.08),xy(end,.018)])
    ax.plot([.04,.96],[.5,.5],ls='--',lw=1.2,color='#999')
    ax.add_patch(Ellipse((.5,.55),.86,.022,color='#9bb7e5'))
    ax.text(.5,.86,'Oxidizer',ha='center');ax.text(.5,.12,'Fuel',ha='center')
    ax.annotate('',(.5,.48),(.5,.22),arrowprops={'arrowstyle':'-|>','color':'black','lw':1.3})
    ax.annotate('',(.71,.22),(.5,.22),arrowprops={'arrowstyle':'-|>','color':'black','lw':1.3})
    ax.text(.52,.42,r'$x$');ax.text(.63,.24,r'$r$')
    save(fig,'opposed-jet.svg')

def aerodynamic_quenching():
    fig, ax=plt.subplots(figsize=(7,5.5));fig.subplots_adjust(left=.18,bottom=.18,right=.96,top=.95)
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    for end in [(1,0),(0,1)]:
        ax.annotate('',end,(0,0),arrowprops={'arrowstyle':'-|>','color':'black','lw':1.7})
    x=np.linspace(0,.78,160);y=.12+.85*(x/.78)**2.3
    ax.plot(x,y,color='#5b9bd5',lw=2.5)
    ax.text(.11,.61,'burning\n'+r'$\mathrm{Da}>1$',color='red',linespacing=1.5)
    ax.text(.61,.2,'extinct\n'+r'$\mathrm{Da}<1$',color='#5b9bd5',linespacing=1.5)
    ax.text(.65,.98,r'$\mathrm{Da}=1$',ha='center')
    ax.text(.5,-.13,r'strain rate (s$^{-1}$)',ha='center')
    ax.text(-.2,.52,'CFT (K)',ha='center',rotation=90)
    save(fig,'aerodynamic-quenching.svg')

def dilution_cells():
    fig,ax=plt.subplots(figsize=(8,3.8));fig.subplots_adjust(0,0,1,1)
    ax.set(xlim=(0,8),ylim=(0,3.8),aspect='equal');ax.axis('off')
    for x,c in [(.3,'#a5a5a5'),(4.4,'#4fa2ef')]:
        ax.add_patch(Rectangle((x,.3),3.2,3.2,facecolor=c,edgecolor='#999',lw=1))
    ax.text(.62,2.9,'Fuel');ax.text(4.72,2.9,'Air')
    ax.add_patch(Ellipse((2.4,1),1.25,.8,color='#4fa2ef'))
    ax.text(2.4,1,'Air',ha='center',va='center')
    # Flame silhouette, tracing the same conceptual fuel pocket as the source.
    verts=[(6.15,1.05),(5.3,1.25),(5.4,1.7),(5.7,2.0),(5.68,1.6),(5.93,1.5),(5.95,1.5),
           (5.68,2.1),(6.12,2.55),(6.2,2.65),(6.03,2.1),(6.38,2.1),(6.35,1.8),
           (6.48,1.85),(6.58,2.06),(6.57,2.1),(7.04,1.43),(6.65,1.02),(6.15,1.05)]
    ax.add_patch(PathPatch(MPath(verts,[MPath.MOVETO]+[MPath.CURVE4]*18),facecolor='#e66b37',edgecolor='none'))
    ax.text(6.2,.63,'Fuel',ha='center')
    save(fig,'dilution-cells.svg')

def flame_islands():
    fig,ax=plt.subplots(figsize=(5,5));fig.subplots_adjust(0,0,1,1)
    ax.imshow(Image.open(OUT/'turbulent-composition-field.png'));ax.axis('off')
    w,h=Image.open(OUT/'turbulent-composition-field.png').size
    for cx,cy,r in [(.22,.32,.11),(.7,.6,.16)]:
        theta=np.arange(24)*np.pi/12;radius=np.where(np.arange(24)%2==0,r,r*.55)
        ax.add_patch(Polygon(np.c_[w*(cx+radius*np.cos(theta)),h*(cy+radius*np.sin(theta))],
                            facecolor='#ed7d31',edgecolor='#ffff00',lw=1.4))
    save(fig,'flame-islands.svg')

if __name__=='__main__':
    opposed_jet();aerodynamic_quenching();dilution_cells();flame_islands()
