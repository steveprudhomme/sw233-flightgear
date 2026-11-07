# SPDX-License-Identifier: GPL-3.0-only
# Development flight only. Initialization precedes capture; thereafter the
# controller writes pilot controls, never position, attitude or sideslip.
setprop('/sim/freeze/master', 1);
setprop('/instrumentation/magnetic-compass/serviceable',1);
setprop('/controls/flight/elevator-trim', 0);
setprop('/controls/flight/elevator', -0.62437453);
setprop('/controls/flight/aileron', 0);
setprop('/controls/flight/rudder', 0);
setprop('/controls/flight/speedbrake', 0);
setprop('/fdm/jsbsim/ic/lat-geod-deg', 45.2829);
setprop('/fdm/jsbsim/ic/long-gc-deg', -73.2845);
setprop('/fdm/jsbsim/ic/h-sl-ft', 6000);
setprop('/fdm/jsbsim/ic/vc-kts', 60);
setprop('/fdm/jsbsim/ic/psi-true-deg', 317);
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

# The previous initialization is the only reset. Roll in using pilot controls.
setprop('/sim/current-view/view-number',0);
setprop('/sim/current-view/internal',1);
setprop('/sim/current-view/x-offset-m',0);
setprop('/sim/current-view/y-offset-m',0.5);
setprop('/sim/current-view/z-offset-m',1.7);
setprop('/sim/current-view/heading-offset-deg',0);
setprop('/sim/current-view/pitch-offset-deg',-25);
setprop('/sim/current-view/field-of-view',40);
var clock = func { return getprop('/sim/time/elapsed-sec'); };
var start = clock();
var since = start;
var phase = 0; # settle, right, hold, left, hold, end
var stableSince = -1;
var base = '/sim/sw233/turn/';
var wrap = func(x) { return x - 360*math.floor((x+180)/360); };
var step = func {
    var now = clock();
    var mag = getprop('/orientation/heading-magnetic-deg');
    var roll = getprop('/orientation/roll-deg');
    var indicated = getprop('/instrumentation/magnetic-compass/indicated-heading-deg');
    if (math.abs(wrap(indicated-mag)) <= 2 and math.abs(roll)<=3) {
        if (stableSince < 0) stableSince = now;
    } else { stableSince = -1; }
    var stable = stableSince >= 0 and now-stableSince >= 4;
    if (phase == 0 and now-since > 12 and stable or
        (phase == 1 or phase == 3) and now-since > 6 and
        math.abs(wrap((phase == 1 ? 30 : 330)-mag)) < 2 and math.abs(roll) < 3 or
        (phase == 2 or phase == 4) and ((now-since > 25 and stable) or now-since > 75)) {
        phase += 1;
        since = now;
    }
    var target = phase == 1 or phase == 2 ? 30 : 330;
    var bank = clip(wrap(target-mag)*1.5,-18,18);
    var theta = getprop('/fdm/jsbsim/attitude/theta-rad');
    var p = getprop('/fdm/jsbsim/velocities/p-rad_sec');
    var q = getprop('/fdm/jsbsim/velocities/q-rad_sec');
    setprop('/controls/flight/aileron',clip(2.5*((bank-roll)*0.0174533)-0.8*p,-1,1));
    setprop('/controls/flight/elevator',clip(-0.62437453+2*(theta+0.056506)+1.1*q,-1,1));
    setprop(base~'time',now-start);
    setprop(base~'phase',phase);
    setprop(base~'mag',mag);
    setprop(base~'ind',getprop('/instrumentation/magnetic-compass/indicated-heading-deg'));
    setprop(base~'roll',roll);
    setprop(base~'kt',getprop('/velocities/airspeed-kt'));
    setprop(base~'wind',getprop('/environment/wind-speed-kt'));
    if (phase >= 5 or now-start > 285) {
        setprop(base~'done',1);
        setprop('/sim/freeze/master',1);
        return;
    }
    settimer(step,0);
};
setprop(base~'done',0);
step();
