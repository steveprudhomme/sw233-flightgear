# SPDX-License-Identifier: GPL-3.0-only
# Session-only language choice. No aircraft controls are written.
var path = "/sim/sw233/language";
var busy = 0;
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
    setprop("/sim/sw233/checklist-ascii",0);
    # Titles change; select the first list and discard old checklist UI state.
    props.globals.getNode("/sim/gui/dialogs/checklist",1).removeChildren();
    setprop("/sim/sw233/language-label",lang == "fr" ? "Français" : "English");
    busy = 0;
    if (was_open) gui.showDialog("checklist");
};
var choose = func(lang) { if (lang == "fr" or lang == "en") setprop(path,lang); };
var toggle = func { choose(getprop(path) == "fr" ? "en" : "fr"); };
setlistener(path,apply,1,0);

# The aircraft owns this dialog; no installation files or font settings change.
var checklist_dialog = gui.Dialog.new("/sim/sw233/checklist/dialog",
    "Aircraft/SW233/gui/dialogs/checklists.xml");
var select_list = func(index) {
    var lists = props.globals.getNode("/sim/checklists").getChildren("checklist");
    if (index < 0 or index >= size(lists)) return;
    setprop("/sim/gui/dialogs/checklist/selected-checklist",lists[index].getNode("title").getValue());
    fgcommand("dialog-close",props.Node.new({"dialog-name":"checklist"}));
    gui.showDialog("checklist");
};
var render_checklist = func(surface) {
    surface.set("view[0]",780).set("view[1]",500);
    surface.setColorBackground(0.96,0.96,0.93,1);
    var group = surface.createGroup();
    var text = func(value,x,y,size,color) {
        group.createChild("text").setText(value)
            .setFont("LiberationFonts/LiberationSans-Regular.ttf")
            .setFontSize(size).set("fill",color).setTranslation(x,y);
    };
    var lists = props.globals.getNode("/sim/checklists").getChildren("checklist");
    var selected = getprop("/sim/gui/dialogs/checklist/selected-checklist");
    var list = lists[0];
    foreach (var candidate; lists)
        if (candidate.getNode("title").getValue() == selected) list = candidate;
    var title = list.getNode("title").getValue();
    setprop("/sim/gui/dialogs/checklist/selected-checklist",title);
    setprop("/sim/gui/dialogs/checklist/selected-page",0);
    text(title,18,30,23,"#151515");
    var row = 0;
    foreach (var item; list.getChildren("item")) {
        var name = item.getNode("name").getValue();
        text(name,18,66+row*51,19,"#151515");
        text(substr(name,0,1),18,66+row*51,19,"#b02020");
        text(item.getNode("value").getValue(),36,87+row*51,17,"#333333");
        row += 1;
    }
    text(getprop(path) == "fr" ? "Simulation uniquement — Français" : "Simulation only — English",
         18,488,15,"#444444");
};
