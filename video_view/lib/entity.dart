class DirList {
  String _path;
  List<Item> _items;

  DirList({String path, List<Item> items}) {
    this._path = path;
    this._items = items;
  }

  String get path => _path;
  set path(String path) => _path = path;
  List<Item> get items => _items;
  set items(List<Item> items) => _items = items;

  DirList.fromJson(Map<String, dynamic> json) {
    _path = json['path'];
    if (json['items'] != null) {
      _items = new List<Item>();
      json['items'].forEach((v) {
        _items.add(new Item.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['path'] = this._path;
    if (this._items != null) {
      data['items'] = this._items.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Item {
  String _type;
  String _name;

  Item({String type, String name}) {
    this._type = type;
    this._name = name;
  }

  String get type => _type;
  set type(String type) => _type = type;
  String get name => _name;
  set name(String name) => _name = name;

  Item.fromJson(Map<String, dynamic> json) {
    _type = json['type'];
    _name = json['name'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['type'] = this._type;
    data['name'] = this._name;
    return data;
  }
}
