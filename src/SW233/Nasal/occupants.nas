# SPDX-License-Identifier: GPL-3.0-only
# Editing properties are strings; effective weights belong to JSBSim.
var base = "/sim/sw233/occupants/";
var front = "/fdm/jsbsim/inertia/pointmass-weight-lbs";
var rear = "/fdm/jsbsim/inertia/pointmass-weight-lbs[1]";
var saved = nil;
var message = func(s) { setprop(base ~ "message", s); };
var stage = func(a, b) {
    setprop(base ~ "front", sprintf("%.17g", a));
    setprop(base ~ "rear", sprintf("%.17g", b));
};
var begin = func {
    saved = [getprop(front), getprop(rear)];
    stage(saved[0], saved[1]);
    message("Saisie en lb. Appliquer au sol, avion arrete.");
};
var stationary = func(wow, speed) { return wow == 1 and speed != nil and abs(speed) <= 1; };
var apply = func {
    var a = num(getprop(base ~ "front"));
    var b = num(getprop(base ~ "rear"));
    if (a == nil or b == nil or !(a >= 0 and a <= 300 and b >= 0 and b <= 300)) {
        message("Refus : saisir deux nombres entre 0 et 300 lb."); return 0;
    }
    var wow = getprop("/gear/gear/wow");
    var speed = getprop("/velocities/groundspeed-kt");
    if (!stationary(wow, speed)) {
        message("Refus : poser et immobiliser le planeur."); return 0;
    }
    setprop(front, a); setprop(rear, b);
    message("Applique. CG historique : enveloppe reelle non validee.");
    return 1;
};
var preset = func(a, b) { stage(a, b); apply(); };
var step = func(which, delta) {
    var a = getprop(front); var b = getprop(rear);
    if (which == 0) { a += delta; } else { b += delta; }
    stage(a, b); apply();
};
var restore = func { if (saved != nil) { stage(saved[0], saved[1]); apply(); } };
var dialog = gui.Dialog.new("/sim/sw233/occupants/dialog", "Aircraft/SW233/gui/dialogs/occupants.xml");
