# SPDX-License-Identifier: GPL-3.0-only
# Development flight only. Initialization precedes capture; thereafter the
# controller writes pilot controls, never position, attitude or sideslip.
setprop('/sim/freeze/master', 1);
setprop('/instrumentation/vertical-speed-indicator/serviceable',1);
setprop('/controls/flight/elevator-trim', 0);
setprop('/controls/flight/elevator', -0.62437453);
setprop('/controls/flight/aileron', 0);
setprop('/controls/flight/rudder', 0);
setprop('/controls/flight/speedbrake', 0);
setprop('/fdm/jsbsim/ic/lat-geod-deg', 45.2829);
setprop('/fdm/jsbsim/ic/long-gc-deg', -73.2845);
setprop('/fdm/jsbsim/ic/h-sl-ft', 6000);
setprop('/fdm/jsbsim/ic/vc-kts', 60);
setprop('/fdm/jsbsim/ic/psi-true-deg', 10);
setprop('/fdm/jsbsim/ic/phi-deg', 0);
setprop('/fdm/jsbsim/ic/alpha-deg', 1.6615083);
setprop('/fdm/jsbsim/ic/gamma-deg', -4.8990695);
setprop('/fdm/jsbsim/ic/p-rad_sec', 0);
setprop('/fdm/jsbsim/ic/q-rad_sec', 0);
setprop('/fdm/jsbsim/ic/r-rad_sec', 0);
setprop('/fdm/jsbsim/simulation/reset', 1);
setprop('/sim/freeze/master', 0);
setprop('/sim/menubar/visibility', 0);
var clip = func(x, a, b) { return math.max(a, math.min(b,x)); };


# Compare the two spoiler states at 60 kt IAS; never force vertical speed.
setprop('/sim/current-view/view-number',0);
setprop('/sim/current-view/internal',1);
setprop('/sim/current-view/x-offset-m',0.23);
setprop('/sim/current-view/y-offset-m',0.5);
setprop('/sim/current-view/z-offset-m',1.7);
setprop('/sim/current-view/heading-offset-deg',0);
setprop('/sim/current-view/pitch-offset-deg',-26);
setprop('/sim/current-view/field-of-view',42);
var start = getprop('/sim/time/elapsed-sec');
var last = start;
var bias = 0;
var base = '/sim/sw233/vario/';
var step = func {
    var now = getprop('/sim/time/elapsed-sec');
    var t = now-start;
    var dt = math.min(.1,now-last);
    last = now;
    var kt = getprop('/instrumentation/airspeed-indicator/indicated-speed-kt');
    bias = clip(bias+(kt-60)*dt*.0005,-.20,.10);
    var target = -.056506 + bias + .006*(kt-60);
    var phi = getprop('/fdm/jsbsim/attitude/phi-rad');
    var theta = getprop('/fdm/jsbsim/attitude/theta-rad');
    var p = getprop('/fdm/jsbsim/velocities/p-rad_sec');
    var q = getprop('/fdm/jsbsim/velocities/q-rad_sec');
    setprop('/controls/flight/aileron',clip(-2.5*phi-.8*p,-1,1));
    setprop('/controls/flight/elevator',clip(-.62437453+2*(theta-target)+1.1*q,-1,1));
    setprop('/controls/flight/speedbrake',clip((t-60)/4,0,1));
    setprop(base~'time',t);
    setprop(base~'kt',kt);
    setprop(base~'fpm',60*getprop('/velocities/vertical-speed-fps'));
    setprop(base~'ind',getprop('/instrumentation/vertical-speed-indicator/indicated-speed-fpm'));
    setprop(base~'brake',getprop('/fdm/jsbsim/fcs/speedbrake-pos-norm'));
    setprop(base~'roll',getprop('/orientation/roll-deg'));
    setprop(base~'wind',getprop('/environment/wind-speed-kt'));
    setprop(base~'phase',t >= 115 ? 5 : (t<60 ? 0 : 1));
    if (t >= 115) {
        setprop(base~'done',1);
        setprop('/sim/freeze/master',1);
        return;
    }
    settimer(step,0);
};
setprop(base~'done',0);
step();
