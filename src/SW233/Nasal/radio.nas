# SPDX-License-Identifier: GPL-3.0-only
# Generic simulation controls, not a replica of an identified radio.
var frequency = "/instrumentation/comm[0]/frequencies/selected-mhz";
var status = "/sim/sw233/radio/message";
var tune = func(channels) {
    var f = getprop(frequency);
    if (f == nil or !(f >= 118 and f <= 136.975)) {
        setprop(status, "Refus : frequence hors plage 118.000-136.975 MHz");
        return 0;
    }
    var index = math.floor((f-118)*40 + .5);
    if (abs(f-(118+index/40)) > .000001) {
        setprop(status, "Refus : canal hors grille 25 kHz ; utiliser le dialogue radio FlightGear");
        return 0;
    }
    var next = math.max(0, math.min(759, index+channels));
    setprop(frequency, 118+next/40);
    setprop(status, next == index ? "Butee COM1" : "COM1 active reglee");
    return 1;
};
