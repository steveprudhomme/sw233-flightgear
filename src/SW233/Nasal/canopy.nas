# SPDX-License-Identifier: GPL-3.0-only
# Visual canopy only. Dimensions, duration and lock are simulation choices.
var base = "/sim/sw233/canopy/";
var position = 0;
var target = 0;
var refused = 0;
var stationary = func(wow, speed) {
    return wow == 1 and speed != nil and abs(speed) <= 0.2;
};
var publish = func {
    setprop(base ~ "position", position);
    setprop(base ~ "target", target);
    setprop(base ~ "locked", position == 0 and target == 0);
    var fr = getprop("/sim/sw233/language") != "en";
    var state = position == 0 and target == 0 ? (fr ? "Fermée et verrouillée" : "Closed and locked")
        : position == 1 ? (fr ? "Ouverte" : "Open")
        : (fr ? "En mouvement ou arrêtée" : "Moving or stopped");
    if (refused) state = fr ? "Refus : poser et immobiliser le planeur" : "Denied: land and stop the glider";
    setprop(base ~ "status", state);
};
var request = func(open) {
    if (open != 0 and open != 1) return 0;
    if (open and !stationary(getprop("/gear/gear/wow"), getprop("/velocities/groundspeed-kt"))) {
        refused = 1; publish(); return 0;
    }
    refused = 0; target = open; publish(); return 1;
};
var toggle = func { request(target == 0); };
var step = func(dt) {
    if (dt <= 0 or dt > 0.1) return;
    if (getprop("/sim/freeze/master") or getprop("/sim/freeze/clock")) return;
    # If motion starts while opening, hold this position. Never teleport shut.
    if (target > position and !stationary(getprop("/gear/gear/wow"),
                                         getprop("/velocities/groundspeed-kt"))) {
        target = position; refused = 1;
    }
    if (position < target) position = math.min(target, position + dt / 3);
    if (position > target) position = math.max(target, position - dt / 3);
    publish();
};
var reset = func { position = 0; target = 0; refused = 0; publish(); };
var status_line = nil;
var render_status = func(surface) {
    surface.set("view[0]",520).set("view[1]",55);
    surface.setColorBackground(0.96,0.96,0.93,1);
    status_line = surface.createGroup().createChild("text")
        .setFont("LiberationFonts/LiberationSans-Regular.ttf")
        .setFontSize(18).set("fill","#151515").setTranslation(10,32);
    status_line.setText(getprop(base ~ "status"));
};
setlistener(base ~ "status", func {
    if (status_line != nil) status_line.setText(getprop(base ~ "status"));
});
var loop = func { step(0.05); settimer(loop, 0.05); };
var dialog = gui.Dialog.new("/sim/sw233/canopy/dialog", "Aircraft/SW233/gui/dialogs/canopy.xml");
setlistener("/sim/sw233/language", publish);
setlistener("/sim/signals/reinit", func(n) { if (!n.getValue()) reset(); });
reset();
settimer(loop, 0.05);
