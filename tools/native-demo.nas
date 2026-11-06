# SPDX-License-Identifier: MIT
# Development flight only. Initialization precedes capture; thereafter the
# controller writes pilot controls, never position, attitude or sideslip.
setprop('/sim/freeze/master', 1);
setprop('/controls/flight/elevator-trim', 0);
setprop('/controls/flight/elevator', -0.62437453);
setprop('/controls/flight/aileron', 0);
setprop('/controls/flight/rudder', 0);
setprop('/controls/flight/speedbrake', 0);
setprop('/fdm/jsbsim/ic/lat-geod-deg', 45.2829);
setprop('/fdm/jsbsim/ic/long-gc-deg', -73.2845);
setprop('/fdm/jsbsim/ic/h-sl-ft', 2300);
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
var begin = getprop('/sim/time/elapsed-sec');
var recording = 0;
var lastSample = -1;
var step = func {
    var elapsed = getprop('/sim/time/elapsed-sec') - begin;
    var t = elapsed - 10; # settle for ten seconds before recording
    var spoilers = math.min(1, math.max(0,(t-14)/4), math.max(0,(28-t)/4));
    var slip = math.min(1, math.max(0,(t-34)/6), math.max(0,(58-t)/4));
    var phi = getprop('/fdm/jsbsim/attitude/phi-rad');
    var theta = getprop('/fdm/jsbsim/attitude/theta-rad');
    var p = getprop('/fdm/jsbsim/velocities/p-rad_sec');
    var q = getprop('/fdm/jsbsim/velocities/q-rad_sec');
    setprop('/controls/flight/aileron',clip(2.5*(0.34906585*slip-phi)-0.8*p,-1,1));
    # FlightGear reverses rudder sign when passing it to JSBSim.
    setprop('/controls/flight/rudder',-0.8*slip);
    setprop('/controls/flight/speedbrake',spoilers);
    setprop('/controls/flight/elevator',clip(-0.62437453+2*(theta+0.056506)+1.1*q,-1,1));
    setprop('/sim/sw233/demo/time-sec',t);
    setprop('/sim/sw233/demo/active',1);
    if (t < 8) {
        setprop('/sim/current-view/view-number',1);
        setprop('/sim/current-view/heading-offset-deg',25);
        setprop('/sim/current-view/pitch-offset-deg',22);
    } else {
        setprop('/sim/current-view/view-number',0);
        setprop('/sim/current-view/internal',1);
        setprop('/sim/current-view/y-offset-m',0.5);
        setprop('/sim/current-view/z-offset-m', t >= 30 and t < 58 ? 1.5 : 1.75);
        setprop('/sim/current-view/field-of-view',80);
        # Show the orange cockpit lever, then focus on the yaw string.
        var look = t < 30 or t >= 58;
        setprop('/sim/current-view/heading-offset-deg',0);
        setprop('/sim/current-view/pitch-offset-deg',look ? -25 : -9);
    }
    if (t >= 0 and !recording) {
        if (math.abs(getprop('/position/latitude-deg')-45.2944)>0.05 or getprop('/position/ground-elev-ft')<30 or getprop('/velocities/airspeed-kt')<40) {
            setprop('/sim/sw233/demo/active',0);
            print('SW233: CYJN, ground elevation or flying speed not confirmed; capture cancelled.');
            return;
        }
        fgcommand('video-start',{name:'SW233-CYJN-flight.mp4',codec:'libx264',quality:0.6});
        recording = 1;
    }
    if (recording and math.floor(t)>lastSample) {
        lastSample = math.floor(t);
        print(sprintf('SW233_SAMPLE %.2f %.3f %.3f %.3f %.2f %.6f %.6f %.1f',t,
            getprop('/fdm/jsbsim/fcs/speedbrake-pos-norm'),getprop('/fdm/jsbsim/aero/beta-deg'),
            getprop('/orientation/roll-deg'),getprop('/velocities/airspeed-kt'),
            getprop('/position/latitude-deg'),getprop('/position/longitude-deg'),
            getprop('/position/ground-elev-ft')));
    }
    if (t >= 66) {
        fgcommand('video-stop');
        setprop('/sim/freeze/master',1);
        setprop('/sim/sw233/demo/active',0);
        return;
    }
    settimer(step,0);
};
step();
