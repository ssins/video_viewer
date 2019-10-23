import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:chewie/chewie.dart';
import 'package:video_player/video_player.dart';
import 'package:dio/dio.dart';
import 'entity.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:wakelock/wakelock.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Video Viewer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Video Viewer'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Map<String, VideoPlayerController> vpControllerMap = Map();
  String vpcNowKey;
  ChewieController chewieController;
  Future future;
  String ip;
  String nginxPort;
  String serverPort;
  String prePath;
  String dirPath;
  List dirHistory;
  GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  _saveConfig() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('vv_ip', ip);
    await prefs.setString('vv_nginxPort', '7070');
    await prefs.setString('vv_serverPort', '7878');
  }

  Future<Map<String, String>> _loadConfig() async {
    Map<String, String> map = Map();
    SharedPreferences prefs = await SharedPreferences.getInstance();
    map['ip'] = prefs.getString('vv_ip') ?? '192.168.0.115';
    map['nginxPort'] = prefs.getString('vv_nginxPort') ?? '7070';
    map['serverPort'] = prefs.getString('vv_serverPort') ?? '7878';
    return map;
  }

  void _init() {
    prePath = '/index/dir';
    dirPath = '/';
    dirHistory = [];
    future = getdata('http://' + ip + ':' + serverPort + prePath + dirPath);
    vpControllerMap[vpcNowKey].pause();
    vpcNowKey = 'init';
    chewieController.dispose();
    chewieController = ChewieController(
      videoPlayerController: vpControllerMap[vpcNowKey],
      autoPlay: true,
    );
  }

  @override
  void initState() {
    vpControllerMap.putIfAbsent('init',()=>VideoPlayerController.network('http://localhost:2333/test.mp4'));
    vpcNowKey = 'init';
    chewieController = ChewieController(
      videoPlayerController: vpControllerMap[vpcNowKey],
      autoPlay: true,
    );
    Wakelock.enable();
    _loadConfig().then((map) {
      ip = map['ip'];
      nginxPort = map['nginxPort'];
      serverPort = map['serverPort'];
      _init();
      setState(() {});
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: _onWillPop,
      child: Scaffold(
        body: Container(
          child: Column(
            children: <Widget>[
              Chewie(
                controller: chewieController,
              ),
              Container(
                padding: EdgeInsets.all(5.0),
                child: Card(
                  child: Row(
                    children: <Widget>[
                      Expanded(
                        child: Text(dirPath),
                      ),
                      IconButton(
                        icon: Icon(
                          Icons.arrow_back_ios,
                          color: Colors.blueGrey,
                        ),
                        onPressed: () {
                          if (dirHistory.length > 0) {
                            setState(() {
                              dirPath = dirHistory.last;
                              dirHistory.removeLast();
                              future = getdata('http://' +
                                  ip +
                                  ':' +
                                  serverPort +
                                  prePath +
                                  dirPath);
                            });
                          }
                        },
                      ),
                      IconButton(
                        icon: Icon(
                          Icons.settings,
                          color: Colors.blueGrey,
                        ),
                        onPressed: _setConfig,
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                child: Container(
                  padding: EdgeInsets.all(5.0),
                  child: Card(
                    child: buildFutureBuilder(),
                  ),
                ),
                flex: 1,
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    chewieController.dispose();
    vpControllerMap.forEach((k, v) {
      v.dispose();
    });
    Wakelock.disable();
    super.dispose();
  }

  FutureBuilder<DirList> buildFutureBuilder() {
    return FutureBuilder<DirList>(
      builder: (context, AsyncSnapshot<DirList> asyncSnapshot) {
        if (asyncSnapshot.hasData) {
          DirList data = asyncSnapshot.data;
          return ListView.builder(
            itemCount: data.items.length,
            itemBuilder: (context, index) {
              Item item = data.items[index];
              return FlatButton(
                child: Text('${item.name}'),
                onPressed: () {
                  if (item.type == 'file') {
                    setState(() {
                      chewieController.dispose();
                      vpControllerMap[vpcNowKey].pause();
                      vpcNowKey =data.path + item.name;
                      String url = 'http://' +ip + ':' +nginxPort + vpcNowKey;
                      if(!vpControllerMap.containsKey(vpcNowKey)){
                        VideoPlayerController vpController = VideoPlayerController.network(url);
                        vpControllerMap.putIfAbsent(vpcNowKey,()=>vpController);
                      }
                      chewieController = ChewieController(
                        videoPlayerController: vpControllerMap[vpcNowKey],
                        autoPlay: true,
                      );
                    });
                  } else if (item.type == 'dir') {
                    setState(() {
                      dirHistory.add(dirPath);
                      dirPath = data.path + item.name;
                      future = getdata('http://' +
                          ip +
                          ':' +
                          serverPort +
                          prePath +
                          dirPath);
                    });
                  }
                },
              );
            },
          );
        }
        return Center(
          child: CircularProgressIndicator(),
        );
      },
      future: future,
    );
  }

  Future<DirList> getdata(String url) async {
    var dio = Dio();
    Response response = await dio.get(url);
    DirList dirList = DirList.fromJson(json.decode(response.data));
    return dirList;
  }

  void _setConfig() {
    showDialog(
      context: context,
      builder: (context) => Container(
        padding: const EdgeInsets.all(32.0),
        child: Card(
          child: Container(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                children: <Widget>[
                  Expanded(
                    child: Column(
                      children: <Widget>[
                        TextFormField(
                          decoration: InputDecoration(
                            labelText: '服务器ip或域名',
                            prefixText: 'http://',
                          ),
                          initialValue: ip,
                          validator: (val) {
                            return val.length > 0 ? null : '不可为空';
                          },
                          onSaved: (val) {
                            ip = val;
                          },
                        ),
                        TextFormField(
                          decoration: InputDecoration(
                            labelText: '文件列表端口',
                          ),
                          initialValue: serverPort,
                          validator: (val) {
                            return val.length > 0 ? null : '不可为空';
                          },
                          onSaved: (val) {
                            serverPort = val;
                          },
                        ),
                        TextFormField(
                          decoration: InputDecoration(
                            labelText: '视频源端口',
                          ),
                          initialValue: nginxPort,
                          validator: (val) {
                            return val.length > 0 ? null : '不可为空';
                          },
                          onSaved: (val) {
                            nginxPort = val;
                          },
                        ),
                      ],
                    ),
                    flex: 1,
                  ),
                  Row(
                    children: <Widget>[
                      Expanded(
                        child: Text(''),
                      ),
                      FlatButton(
                        child: Text('取消'),
                        onPressed: () {
                          Navigator.of(context).pop();
                        },
                      ),
                      FlatButton(
                        child: Text('确认'),
                        onPressed: () {
                          if (_forSubmitted()) {
                            Navigator.of(context).pop();
                            setState(() {});
                          }
                        },
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  bool _forSubmitted() {
    var _form = _formKey.currentState;
    if (_form.validate()) {
      _form.save();
      _init();
      _saveConfig();
      return true;
    }
    return false;
  }

  Future<bool> _onWillPop() {
    if (dirHistory.length > 0) {
      setState(() {
        dirPath = dirHistory.last;
        dirHistory.removeLast();
        future = getdata('http://' + ip + ':' + serverPort + prePath + dirPath);
      });
      return Future(() => false);
    }
    return showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: Text('Are you sure?'),
            content: Text('Do you want to exit an App'),
            actions: <Widget>[
              FlatButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: Text('No'),
              ),
              FlatButton(
                onPressed: () => Navigator.of(context).pop(true),
                child: Text('Yes'),
              ),
            ],
          ),
        ) ??
        false;
  }
}
