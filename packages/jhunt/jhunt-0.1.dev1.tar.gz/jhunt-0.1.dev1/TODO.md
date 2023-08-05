# TODO

Widgets

- filtering from a search entry
- cellrender -> URL, combo, ...
- calendar (non trivial...)

## Version 0.1

- [x] Gtk.TreeView: add sorting, ellipsis
- [x] Update the Gtk.ListStore (model)
- [x] Use Gtk.Dialog instead "print(...)"
- [x] Use Gtk.Grid instead Gtk.Box
- [x] Add a locking system to avoid multiple instanciation of the application (and data lose)...
- [x] URL cliquable in Gtk.TreeView
- [x] Add a feature: edit/save job adverts (use a Gtk.Paned container)
- [x] Add a feature: search job adverts pannel
    - [x] Snippets TreeView CellRenders
    - [x] "Today status"
    - [x] "Last visit"
    - [x] Déplacer la liste des sites dans un fichier json
- [ ] GtkTreeView: add filtering (from a search entry)

## Version 0.2

- [ ] Add + Save/Edit: add "Sending application" (envoi de candidature) + date (or None by default)
    - [ ] Use the Gtk Calendar widget
- [ ] Save/Edit: add "Tracking application" (suivi de candidature) + TextView (dates, personnes, description des entretiens, ...)
- [ ] Save/Edit: "State" ("en cours", "refusé", ...)
- [ ] Add + Save/Edit: "Location"
- [ ] Clean... split code in multiple classes/modules (each container is a class)

## Version 0.3

- [ ] Score: select nothing by default
- [ ] Use the Gtk.Application locking method to avoid multiple instanciation of
      the application (see http://stackoverflow.com/questions/19072161/preventing-multiple-instances-of-a-gtk-application) instead fcntl

## Version 1.0

- [ ] Add a README.md file
- [ ] Add a Gtk.Menu and/or Toolbar (like a regular Gnome app)
- [ ] Add a setup.py file and add the app to PyPI
- [ ] Make a debian package

## Later ?

- [ ] Solve the redundancy problem of data/model: Gtk.ListStore (model) + dictionnaire "data" => redundant
