#set term post eps "Times-Roman" 12 color solid enh
#set term post"Times-Roman" 12
#set output "corr_k2.eps"
set xlabel "1/(omega)^2"
set ylabel "Chi(q2,omega)"
#set title "m2a"
#set zlabel " L"
#set logscale
#set key graph 0.85, graph 0.85
#set xtics (0.56,0.57,0.58,0.59)
#set ytics (0.000,0.005,0.010,0.015)
set xrange [0:1.0]
set yrange [0:]
#set xrange [0.556067:0.557669]
#set nokey
set key right bottom
#set logscale y
#set logscale x
plot "./corr_k2.txt" using ($1)**(-2.0):2:3 with yerrorbars
#smooth csplines notitle  w linespoints
pause -1
