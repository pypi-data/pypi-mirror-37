export THE_PIKSI=192.168.2.68
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
python -m piksi_tools.serial_link -p /dev/cu.usbserial-A105YHGQ -b 230400 -l -o ~/SwiftNav/serial/ &
python -m piksi_tools.serial_link -t -p $THE_PIKSI:55555 -l -o ~/SwiftNav/ethernet &
cd ~/source/dz-scratch/dev_metrics/
#export THE_PIKSI=192.168.2.68 && ./pull_metrics.sh &
#gnuplot ~/source/dz-scratch/dev_metrics/plot1.gnuplot &
#gnuplot ~/source/dz-scratch/dev_metrics/plot2.gnuplot &
#gnuplot ~/source/dz-scratch/dev_metrics/plot3.gnuplot &

while [ 1 ] 
do
  sleep 15
  killall Preview 
  file=~/SwiftNav/ethernet/$(ls -rt ~/SwiftNav/ethernet | tail -n 1) && /usr/local/bin/python ~/source/dz-scratch/python-plotting/plot_imu_diff.py $file -f json && open $file.png &
  file=~/SwiftNav/serial/$(ls -rt ~/SwiftNav/serial | tail -n 1) && /usr/local/bin/python ~/source/dz-scratch/python-plotting/plot_imu_diff.py $file -f json && open $file.png &
done
