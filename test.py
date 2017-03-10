from GnuplotParser import GnuplotParser as GP

"""
gnuplot_cmd = """
"""
set title 'Ptingule'
unset grid
set xlabel 'test_x_label'
set ylabel 'test_y_label'
set xrange [:1000]
set yrange [10:]
set logscale y
set logscale x
plot 'test_data_23_simple_tab.lis' ind 0 us 1:3 w steps lw 1 t '#Detector 1'
"""

gnuplot_cmd = """
Started 2017.02.22 15:15:24
reset
set terminal qt 0 enhanced raise  title 'test.flair-0: Ptingule'

set title 'Ptingule'
unset grid
set xlabel ''
set xtics
set ylabel ''
set ytics
set logscale x
set logscale y
unset logscale z
unset logscale cb
unset logscale x2
unset logscale y2
set key default
plot 'test_data_23_simple_tab.lis' ind 0 us (($1)*4999):(($3)*100) w steps lw 1 t '#Detector 1'
"""

#
# plot 'test_data_23_tab.lis' ind 1 every :::0::0  us 1:3 w steps lw 1 t '#Detector 1','test_data_23_simple_tab.lis' ind 0 us 1:3 w steps lw 1 t '#Detector 2'




GP().parseGnuplotComamnd(gnuplot_cmd)

