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
# Five rays parallel to model-up define a local plane under the main tyre.
# aircraftToCart uses forward/right/down; mesh coordinates use aft/right/up.
var ground_height = func(dx, dy) {
    var o = aircraftToCart({x:-(2.559214+dx), y:dy, z:0.845});
    var a = aircraftToCart({x:-(2.559214+dx), y:dy, z:-1.155});
    var hit = get_cart_ground_intersection(a, {x:o.x-a.x, y:o.y-a.y, z:o.z-a.z});
    if (hit == nil) return nil;
    var p = geodtocart(hit.lat, hit.lon, hit.elevation);
    var h = ((p[0]-o.x)*(a.x-o.x) + (p[1]-o.y)*(a.y-o.y)
           + (p[2]-o.z)*(a.z-o.z)) / 2;
    return h != h or abs(h) > 0.5 ? nil : h;
};
var plane = func(h, xp, xm, yp, ym) {
    foreach (var v; [h,xp,xm,yp,ym]) {
        if (v == nil or v != v or abs(v) > 0.5) return nil;
    }
    var sx = (xp-xm)/0.5;
    var sy = (yp-ym)/0.5;
    if (abs(sx) > 2 or abs(sy) > 2) return nil;
    # Reject steps/edges instead of inventing a plane across discontinuities.
    if (abs((xp+xm)/2-h) > 0.01 or abs((yp+ym)/2-h) > 0.01) return nil;
    return [h,sx,sy];
};
var terrain_offset = func(p, wow) {
    if (wow != 1 or p == nil) return 0;
    var support = 0;
    for (var i = 0; i < 20; i += 1) {
        var a = i * math.pi / 10;
        support = math.max(support, 0.245*(p[1]*math.cos(a)-math.sin(a)));
    }
    return math.max(0, p[0]+support+0.075*abs(p[2])-0.245);
};
var update = func {
    var wow = getprop("/gear/gear/wow");
    var p = nil;
    if (wow == 1) p = plane(ground_height(0,0), ground_height(0.25,0),
        ground_height(-0.25,0), ground_height(0,0.25), ground_height(0,-0.25));
    var fallback = offset(getprop("/fdm/jsbsim/gear/unit/compression-ft"),
        getprop("/orientation/pitch-deg"), getprop("/orientation/roll-deg"), wow);
    setprop(base ~ "terrain-valid", p != nil);
    setprop(base ~ "mode", wow != 1 ? "airborne" : p == nil ? "fallback-flat" : "terrain");
    if (p != nil) {
        setprop(base ~ "terrain-height-m", p[0]);
        setprop(base ~ "terrain-slope-x", p[1]);
        setprop(base ~ "terrain-slope-y", p[2]);
    }
    setprop(base ~ "main-offset-m", p == nil ? fallback : terrain_offset(p,wow));
};
var loop = func { update(); settimer(loop, 0.05); };
setprop(base ~ "main-offset-m", 0);
setprop(base ~ "terrain-valid", 0);
settimer(loop, 0.05);
