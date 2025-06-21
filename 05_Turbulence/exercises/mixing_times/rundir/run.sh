mkdir tau_default
cp mixing_times_default.fds tau_default
cd tau_default
fds *.fds
cd -

mkdir tau_1000ms
cp mixing_times_1000ms.fds tau_1000ms
cd tau_1000ms
fds *.fds
cd -

mkdir tau_0100ms
cp mixing_times_0100ms.fds tau_0100ms
cd tau_0100ms
fds *.fds
cd -

mkdir tau_0010ms
cp mixing_times_0010ms.fds tau_0010ms
cd tau_0010ms
fds *.fds
cd -

mkdir tau_0001ms
cp mixing_times_0001ms.fds tau_0001ms
cd tau_0001ms
fds *.fds
cd -
