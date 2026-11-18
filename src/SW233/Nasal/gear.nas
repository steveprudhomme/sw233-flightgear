# SPDX-License-Identifier: GPL-3.0-only
# Visual suspension for the 20-sided main wheel, not a tyre elasticity model.
var base = "/sim/sw233/gear/";
var offset = func(compression, pitch, roll, wow) {
    if (wow != 1 or compression == nil or pitch == nil or roll == nil) return 0;
    if (compression != compression or pitch != pitch or roll != roll) return 0;
    if (compression < 0 or compression > 0.5 or abs(pitch) > 45 or abs(roll) > 60) return 0;
    var theta = pitch * math.pi / 180;
    var phi = roll * math.pi / 180;
    var nx = -math.sin(theta);
    var ny = -math.sin(phi) * math.cos(theta);
    var nz = math.cos(phi) * math.cos(theta);
    var support = 0;
    for (var i = 0; i < 20; i += 1) {
        var a = i * math.pi / 10;
        support = math.max(support, -0.245 * (nx * math.cos(a) + nz * math.sin(a)));
    }
    support += 0.075 * abs(ny);
    return math.max(0, compression * 0.3048 + (support - 0.245 * nz) / nz);
};
var update = func {
    setprop(base ~ "main-offset-m", offset(
        getprop("/fdm/jsbsim/gear/unit/compression-ft"),
        getprop("/orientation/pitch-deg"), getprop("/orientation/roll-deg"),
        getprop("/gear/gear/wow")));
};
var loop = func { update(); settimer(loop, 0.02); };
setprop(base ~ "main-offset-m", 0);
settimer(loop, 0.02);
