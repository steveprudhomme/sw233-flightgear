# SPDX-License-Identifier: GPL-3.0-only
# Session-only language choice. No aircraft controls are written.
var path = "/sim/sw233/language";
var busy = 0;
# Legacy 2024.1 dialog labels do not decode UTF-8 in this tested UI.
# Normalize only the active checklist copy, never source translations or textures.
var display_text = func(text) {
    foreach (var pair; [["é","e"],["è","e"],["ê","e"],["É","E"],
                         ["à","a"],["â","a"],["î","i"],["ô","o"],
                         ["ç","c"],["œ","oe"],["’","'"]])
        text = string.replace(text,pair[0],pair[1]);
    return text;
};
var apply = func {
    if (busy) return;
    busy = 1;
    var lang = getprop(path);
    if (lang != "fr" and lang != "en") { lang = "fr"; setprop(path,lang); }
    var dialog = props.Node.new({"dialog-name":"checklist"});
    var was_open = fgcommand("dialog-close",dialog);
    var target = props.globals.getNode("/sim/checklists",1);
    target.removeChildren();
    props.copy(props.globals.getNode("/sim/sw233/translations/"~lang),target);
    var version = getprop("/sim/version/flightgear");
    var legacy = version != nil and find("2024.1.",version) == 0;
    setprop("/sim/sw233/checklist-ascii",legacy);
    if (legacy) {
        foreach (var list; target.getChildren("checklist")) {
            var title = list.getNode("title");
            title.setValue(display_text(title.getValue()));
            foreach (var item; list.getChildren("item")) {
                foreach (var field; item.getChildren())
                    if (field.getName() == "name" or field.getName() == "value")
                        field.setValue(display_text(field.getValue()));
            }
        }
    }
    # Titles change; select the first list and discard old checklist UI state.
    props.globals.getNode("/sim/gui/dialogs/checklist",1).removeChildren();
    setprop("/sim/sw233/language-label",lang == "fr" ? "Français" : "English");
    busy = 0;
    if (was_open) gui.showDialog("checklist");
};
var choose = func(lang) { if (lang == "fr" or lang == "en") setprop(path,lang); };
var toggle = func { choose(getprop(path) == "fr" ? "en" : "fr"); };
setlistener(path,apply,1,0);
