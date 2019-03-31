import sys,os,requests,json,random,urllib.parse,re,hashlib,time,uuid,socket,threading,datetime,sqlite3

createSign = lambda param: hashlib.md5(('nJi9o;/' + param).encode("utf8")).hexdigest()
requestId = lambda: str(uuid.uuid1()) + str(round(time.time() * 1000))

def writeRawVarint32(paramInt):
  paramBytes = b''
  while (-128 & paramInt) != 0 :
    paramBytes += bytes([paramInt & 127 | 128]); paramInt >>= 7;
  paramBytes += bytes([paramInt])
  return paramBytes

requestHeader = lambda : b'\xC9\x01\x00' + writeRawVarint32(round(time.time() * 1000)) + b'\x11\x20\x64\x38\x31\x66\x64\x61\x35\x37\x33\x66\x39\x31\x30\x65\x36\x38\x61\x30\x34\x30\x62\x62\x30\x38\x64\x32\x61\x63\x66\x32\x34\x63\x21\x20\x32\x2E\x30\x43\x63\x77\x6E\x4C\x61\x66\x30\x30\x6E\x42\x30\x30\x42\x46\x36\x35\x33\x39\x64\x34\x38\x37\x4E\x79\x63\x74\x48\x45\x28\x09\x30\x04\x7A\x4E\x40\x00\x48\x05\x51\x33\x4D\x65\x69\x7A\x75\x2D\x45\x33\x5F\x5F\x73\x69\x6E\x61\x6C\x69\x76\x65\x73\x64\x6B\x5F\x5F\x34\x2E\x39\x2E\x33\x5F\x5F\x61\x6E\x64\x72\x6F\x69\x64\x5F\x5F\x61\x6E\x64\x72\x6F\x69\x64\x36\x2E\x30\x2E\x30\x59\x0A\x31\x30\x35\x34\x30\x39\x35\x30\x31\x30\x61\x00\x68\x10\x71\x03\x32\x2E\x30\xA1\x01\x00\xA9\x01\x24' + bytes(str(uuid.uuid1()), encoding='utf-8')

def Message(userId, userName, userLevel, roomId, type, priority):
  requestSet =  b'\x7B\x22\x63\x6F\x6E\x74\x65\x6E\x74\x22\x3A\x22\x7B\x5C\x22\x74\x5C\x22\x3A' + bytes(type, encoding='utf-8') + b'\x2C\x5C\x22\x75\x5C\x22\x3A' + bytes(userId, encoding='utf-8') + b'\x2C\x5C\x22\x6E\x5C\x22\x3A\x5C\x22' + bytes(userName, encoding='utf-8') + b'\x5C\x22\x2C\x5C\x22\x6C\x5C\x22\x3A' + bytes(str(userLevel), encoding='utf-8') + b'\x2C\x5C\x22\x6D\x5C\x22\x3A\x30\x2C\x5C\x22\x66\x5C\x22\x3A\x5C\x22' + bytes(roomId, encoding='utf-8') + b'\x5C\x22\x2C\x5C\x22\x76\x5C\x22\x3A\x31\x2C\x5C\x22\x76\x69\x70\x5C\x22\x3A\x30\x2C\x5C\x22\x76\x74\x5C\x22\x3A\x30\x7D\x22\x2C\x22\x74\x79\x70\x65\x22\x3A\x30\x2C\x22\x63\x75\x73\x74\x6F\x6D\x5F\x74\x79\x70\x65\x22\x3A\x30\x2C\x22\x65\x78\x74\x22\x3A\x22\x22\x2C\x22\x72\x6F\x6F\x6D\x5F\x69\x64\x22\x3A\x22' + bytes(roomId, encoding='utf-8') + b'\x22\x2C\x22\x6F\x70\x65\x72\x61\x74\x69\x6F\x6E\x5F\x74\x79\x70\x65\x22\x3A\x31\x30\x30\x2C\x22\x6F\x66\x66\x73\x65\x74\x22\x3A\x2D\x31\x2C\x22\x65\x78\x74\x65\x6E\x73\x69\x6F\x6E\x22\x3A\x22\x22\x2C\x22\x72\x65\x71\x75\x65\x73\x74\x65\x72\x5F\x69\x6E\x66\x6F\x22\x3A\x7B\x22\x75\x69\x64\x22\x3A' + bytes(userId, encoding='utf-8') + b'\x2C\x22\x6E\x69\x63\x6B\x6E\x61\x6D\x65\x22\x3A\x22' + bytes(userName, encoding='utf-8') + b'\x22\x7D\x2C\x22\x70\x72\x69\x6F\x72\x69\x74\x79\x22\x3A' + bytes(priority, encoding='utf-8') + b'\x7D'
  requestSetlength = len(requestSet)
  data = (208 + requestSetlength).to_bytes(4, byteorder="little") + requestHeader() + writeRawVarint32(requestSetlength +3) + b'\x01' + writeRawVarint32(requestSetlength) + requestSet
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.connect(('39.97.7.181', 12580));
  sock.send(data); recvdata = sock.recv(528); sock.close();

def Content(userId, userName, userLevel, roomId, type, priority, content):
  requestSet =  b'\x7B\x22\x63\x6F\x6E\x74\x65\x6E\x74\x22\x3A\x22\x7B\x5C\x22\x74\x5C\x22\x3A' + bytes(type, encoding='utf-8') + b'\x2C\x5C\x22\x75\x5C\x22\x3A' + bytes(userId, encoding='utf-8') + b'\x2C\x5C\x22\x63\x5C\x22\x3A\x5C\x22' + bytes(content, encoding='utf-8') + b'\x5C\x22\x2C\x5C\x22\x6E\x5C\x22\x3A\x5C\x22' + bytes(userName, encoding='utf-8') + b'\x5C\x22\x2C\x5C\x22\x6C\x5C\x22\x3A' + bytes(str(userLevel), encoding='utf-8') + b'\x2C\x5C\x22\x6D\x5C\x22\x3A\x30\x2C\x5C\x22\x66\x5C\x22\x3A\x5C\x22' + bytes(roomId, encoding='utf-8') + b'\x5C\x22\x2C\x5C\x22\x76\x5C\x22\x3A\x31\x2C\x5C\x22\x76\x69\x70\x5C\x22\x3A\x30\x2C\x5C\x22\x76\x74\x5C\x22\x3A\x30\x7D\x22\x2C\x22\x74\x79\x70\x65\x22\x3A\x30\x2C\x22\x63\x75\x73\x74\x6F\x6D\x5F\x74\x79\x70\x65\x22\x3A\x30\x2C\x22\x65\x78\x74\x22\x3A\x22\x22\x2C\x22\x72\x6F\x6F\x6D\x5F\x69\x64\x22\x3A\x22' + bytes(roomId, encoding='utf-8') + b'\x22\x2C\x22\x6F\x70\x65\x72\x61\x74\x69\x6F\x6E\x5F\x74\x79\x70\x65\x22\x3A\x31\x30\x30\x2C\x22\x6F\x66\x66\x73\x65\x74\x22\x3A\x2D\x31\x2C\x22\x65\x78\x74\x65\x6E\x73\x69\x6F\x6E\x22\x3A\x22\x22\x2C\x22\x72\x65\x71\x75\x65\x73\x74\x65\x72\x5F\x69\x6E\x66\x6F\x22\x3A\x7B\x22\x75\x69\x64\x22\x3A' + bytes(userId, encoding='utf-8') + b'\x2C\x22\x6E\x69\x63\x6B\x6E\x61\x6D\x65\x22\x3A\x22' + bytes(userName, encoding='utf-8') + b'\x22\x7D\x2C\x22\x70\x72\x69\x6F\x72\x69\x74\x79\x22\x3A' + bytes(priority, encoding='utf-8') + b'\x7D'
  requestSetlength = len(requestSet)
  data = (208 + requestSetlength).to_bytes(4, byteorder="little") + requestHeader() + writeRawVarint32(requestSetlength +3) + b'\x01' + writeRawVarint32(requestSetlength) + requestSet
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.connect(('39.97.7.181', 12580));
  sock.send(data); recvdata = sock.recv(528); sock.close();

def Tip(content, roomId, userID, nickName, priority):
  requestSet = {
    "content": json.dumps(content, separators=(',', ':'), ensure_ascii=False), 
    "type":0, "custom_type":0, "ext":"", "room_id":roomId, "operation_type":100, "offset":-1, "extension":"",
    "requester_info":{"uid":userID, "nickname":nickName}, 
    "priority":priority
  }
  requestSet = bytes(json.dumps(requestSet, separators = (',', ':'), ensure_ascii = False).replace('/',  r'\\\/'), encoding='utf-8');
  requestSetlength = len(requestSet)
  data = (208 + requestSetlength).to_bytes(4, byteorder="little") + requestHeader() + writeRawVarint32(requestSetlength +3) + b'\x01' + writeRawVarint32(requestSetlength) + requestSet
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.connect(('39.97.7.181', 12580));
  sock.send(data); recvdata = sock.recv(528); sock.close();

def Grab(roomId, redPacketList, interval, anchorId, anchorName, logger, tab, roomRank):
  time.sleep(round(roomRank / 20, 1));
  roomIdList.append(roomId); num = 0; global total; grabAmount = 0; #conn = sqlite3.connect(sys.path[0] + r'\kila.db');
  #全部账号
  while len(redPacketList)>0 and len(Daily)>0 :
    k = random.randint(0,len(Daily)-1); lag = interval; isGrab = False;
    try : 
      userId = Daily[k][0]; xAuthToken = Daily[k][1]; userName = Daily[k][2]; userLevel = Daily[k][3]; userPortrait = Daily[k][4];
      #print(type(userId), type(xAuthToken), type(userName), type(userLevel), type(userPortrait))
    except Exception as e : continue
    if random.random() < 0.5 : Message(userId, userName, userLevel, roomId, '101', '3'); Message(userId, userName, userLevel, roomId, '211', '2');
    #红包列表
    for j in redPacketList :
      grabRequestBody = 'id=' + str(j['id']) + '&roomId=' + roomId
      rid = requestId(); grabHeader = {'ua': ua + rid, 'x-auth-token': xAuthToken, 'requestId': rid, 'Content-Length': '87'}
      response = json.loads(requests.post(grabURL, data =  grabRequestBody + '&sign=' + createSign(grabRequestBody), headers = {**commHeader, **grabHeader}).text)
      try : amount = response['b']['amount']
      except Exception as e :
        #抢红包的次数达到上限
        if response['h']['msg'] == '你今天抢红包的次数达到上限啦！' :
          lock.acquire(True)
          try : Daily.remove((userId, xAuthToken, userName, userLevel, userPortrait))
          except Exception as e : print('内存删除上限出错', userId, userName)
          conn.execute("delete from Daily where Id = " + userId); conn.commit()
          lock.release()
          lag = 0; break;
        #抢红包其他错误
        elif response['h']['msg'] != '操作成功' : print('\n抢包失败', response['h']['msg'], userName, anchorName); lag = 0; continue
      #抢红包成功
      else : logger += '\n' + userId + ' ' + userName + ' ' + str(userLevel) + '级 ' + str(amount) + ' '; isGrab = True; num += 1; grabAmount += amount;
    
    #加人数
    rid = requestId(); countHeader = {'ua': ua + rid, 'x-auth-token': xAuthToken, 'requestId': rid, 'Content-Length': '64'}
    requests.post(countURL, data =  'roomId=' + roomId + '&sign=' + createSign('roomId=' + roomId), headers = {**commHeader, **countHeader})
    
    #关注
    if isGrab == True :
      followRequestBody = 'fromUid=' + userId + '&toUid=' + anchorId
      rid = requestId(); followHeader = {'ua': ua + rid, 'x-auth-token': xAuthToken, 'requestId': rid, 'Content-Length': '79'}
      response = json.loads(requests.post(isfollowURL, data = followRequestBody + '&sign=' + createSign(followRequestBody), headers = {**commHeader, **followHeader}).text)
      try : 
        if response['b']['isFollow'] == False :
          requests.post(followURL, data = followRequestBody + '&sign=' + createSign(followRequestBody), headers = {**commHeader, **followHeader})
          Message(userId, userName, userLevel, roomId, '230', '3')
      except Exception as e : print('\n判断关注失败:', response); continue;
    
    #感谢
    if isGrab == True and random.random() < 0.15 : 
      if interval > 5 : time.sleep(random.randint(1,2))
      Content(userId, userName, userLevel, roomId, '200', '2', thankList[random.randint(0,3)]); logger += '感谢 '
    #打赏
    if tab == 'hot' : probability = 0.03
    else : probability = 0.02
    if isGrab == True and random.random() < probability : 
      if interval > 5 : time.sleep(random.randint(1,2))
      rid = requestId(); Header = {'request-page': 'Android_LiveStreamingActivity_GiftListFragment', 'ua': ua + rid, 'x-auth-token': xAuthToken, 'requestId': rid, 'Content-Length': '125'}
      RequestBody = 'goodsId=15060&orderType=2&quantity=1&receiveId=' + anchorId + '&roomId=' + roomId
      try :
        msg = json.loads(requests.post(tipLiveURL, data = RequestBody + '&sign=' + createSign(RequestBody), headers ={**commHeader, **Header}).text)['h']['msg']
      except Exception as e : print('\n打赏失败', msg); continue;
      if msg != '操作成功' : print('\n打赏失败', msg); continue;

      lun = round(time.time() * 1000); userId = int(userId);
      content1 = { "t":220, "u":userId, "a":userPortrait, "n":userName, "c":{ "name":'樱花', "pic":'https://img.hongrenshuo.com.cn/c1189321-b83f-4cfa-b9ff-ecc6715855ed.png?t=1510640271000', "id":15060, "lottieId":0, "doubleCount":1, "price":10, "isDoubleHit":True, "lun":lun, "giftReceiverID":int(anchorId), "giftReceiverName":anchorName, "sizeType":4, "receiverHeadImageUrl":"" }, "l":userLevel, "m":0, "f":roomId, "v":1, "vip":0, "vt":0 }
      content2 = { "t":10004, "u":userId, "a":userPortrait, "n":userName, "c":{ "name":'樱花', "id":0, "lottieId":0, "doubleCount":1, "price":-1, "isDoubleHit":False, "lun":lun, "giftReceiverID":int(anchorId), "giftReceiverName":anchorName, "sizeType":0, "receiverHeadImageUrl":"" }, "l":userLevel, "m":0, "f":roomId, "v":1, "vip":0, "vt":0 }
      Tip(content1, roomId, userId, userName, 1); Tip(content2, roomId, userId, userName, 1)
      logger += '打赏 '
    time.sleep(lag)
    try :
      redPacketJSON = json.loads(requests.get(redPacketURL + roomId + '&sign=' + createSign('roomId=' + roomId), headers = commHeader).text)
      redPacketList = redPacketJSON['b']['sendRedPacketInfoList']
    except Exception as e : print('\n更新红包失败', redPacketJSON['h']['msg'])
  roomIdList.remove(roomId); total += grabAmount
  print(logger); print(num, grabAmount, total, len(Daily), datetime.datetime.now().time());
  
def roomChannel(tab) :
  if tab == 'hot' :
    try :
      roomChannel = json.loads(requests.get('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=0&genderType=0&pageNo=1&pageSize=20&sign=15c0833a2467ae28854de2e3581e9ba0', headers = commHeader).text)
      roomList = roomChannel['b']['data']
      roomChannel = json.loads(requests.get('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=0&genderType=0&pageNo=2&pageSize=20&sign=1f3d198b5838b113864b26d4a9037170', headers = commHeader).text)
      roomList += roomChannel['b']['data'];
      roomChannel = json.loads(requests.get('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=0&genderType=0&pageNo=3&pageSize=20&sign=409c7e91513fb335bd2e7de498542b01', headers = commHeader).text)
      roomList += roomChannel['b']['data'];
    except Exception as e : print('\n获取房间列表失败', roomChannel['h']['msg']); return
    
  else :
    try :
      roomChannel = json.loads(requests.get('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=107&genderType=0&pageNo=1&pageSize=20&sign=da814340721e98253bde11db2987abaf', headers = commHeader).text)
      roomList = roomChannel['b']['data']
      roomChannel = json.loads(requests.get('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=107&genderType=0&pageNo=2&pageSize=20&sign=4c4065d621e003f06b3465aa97377189', headers = commHeader).text)
      roomList += roomChannel['b']['data'];
    except Exception as e : print('\n获取房间列表失败', roomChannel['h']['msg']); time.sleep(1); return

  roomRank = 1;
  #直播间内
  for i in roomList :
    roomId = str(i['roomResq']['roomIdStr'])
    #有红包
    if 'hongbao' in str(i['roomResq']['iconUrlList']) and i['roomResq']['price']==0 and roomId not in roomIdList : 
      try :
        redPacketJSON = json.loads(requests.get(redPacketURL + roomId + '&sign=' + createSign('roomId=' + roomId), headers = commHeader).text)
        redPacketList = redPacketJSON['b']['sendRedPacketInfoList'] 
      except Exception as e : print('\n获取红包信息失败', redPacketJSON['h']['msg']); continue
      redPacketInfo = ''; redPacketNum = 0;
      for j in redPacketList : redPacketInfo += str(j['count']) + '/' + str(round(j['amount'] / j['count'])) + ' '; redPacketNum += j['count'];
      if redPacketNum > 4:
        anchorId = str(i['userResp']['id']); anchorName = i['userResp']['nickname'];
        auto = round(abs(21-datetime.datetime.now().hour)*0.1 + roomRank//10 + 1/(i['roomResq']['onlineNumber']/600) ** 0.5, 1)
        if tab == 'new' : auto += 3
        if tab == 'hot' and redPacketNum >= 30 : auto = auto * 0.3
        logger = '\n' + str(auto)[:3] + ' ' + tab + ' ' + str(roomRank) + ' ' + anchorName + ' ' + str(i['roomResq']['onlineNumber']) + '人 ' + str(round((time.time() - i['roomResq']['liveStartTime']/1000)/60)) + '分钟 ' + redPacketInfo + roomId;
        threading.Thread(target=Grab, args=(roomId, redPacketList, auto, anchorId, anchorName, logger, tab, roomRank)).start()
    roomRank += 1;

roomIdList = []; total = 0;
thankList = ['谢包', '谢谢红包', '谢谢', '谢红包',]
redPacketURL = 'https://hongrenshuo.com.cn/api/v170/red/packet/list/of/room?roomId='
queryByIdURL = 'https://hongrenshuo.com.cn/api/v170/room/queryById?roomId='
countURL = 'https://hongrenshuo.com.cn/api/v170/room/countwatcher'
grabURL = 'https://hongrenshuo.com.cn/api/v170/red/packet/grab'
isfollowURL = 'https://hongrenshuo.com.cn/api/v170/userrelation/isfollow'
followURL = 'https://hongrenshuo.com.cn/api/v170/userrelation/follow'
tipLiveURL = 'https://hongrenshuo.com.cn/api/v170/order/create'
ua = 'os=6.0.0&imei=&m=E3&s=1080x1920&c=2&vc=170&vn=4.9.3&n=hrs&cn=03&cm=00&rid='
commHeader = {'request-page': 'Android_RoomFragment', 'ua': ua, '_c':'2', 'Connection': 'keep-alive', 'Accept': '*/*', 'x-auth-token': '34f8f647-d6dc-4643-9a88-a61747e2ea4f', 'requestId': '', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'hongrenshuo.com.cn', 'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/${project.version}'}

lock = threading.Lock()
if os.path.isfile(sys.path[0] + r'/db.db') == False : print('数据库文件不存在')
else : 
  conn = sqlite3.connect(sys.path[0] + r'/db.db', check_same_thread = False); cursor = conn.cursor();
  cursor.execute("select Id, xAuthToken, Name, Level, Portrait from Daily"); conn.commit(); 
  Daily = cursor.fetchall(); print(len(Daily),'个账号')
  
  #只要还有账号
  while len(Daily):
    '''
    roomChannel('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?pageNo=1&pageSize=50&tag=0&type=0&sign=ef0f565ea2c3c4f7ac80e97f24dc159c', 'hot')
    roomChannel('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?pageNo=1&pageSize=50&tag=0&type=107&sign=d10b1a7240ca597d9b776cc539d8c759', 'new')
    roomChannel('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=0&genderType=0&pageNo=1&pageSize=20&sign=15c0833a2467ae28854de2e3581e9ba0', 'hot')
    roomChannel('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=107&genderType=0&pageNo=1&pageSize=20&sign=da814340721e98253bde11db2987abaf', 'new')
    roomChannel('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=0&genderType=0&pageNo=2&pageSize=20&sign=1f3d198b5838b113864b26d4a9037170', 'hot')
    roomChannel('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=107&genderType=0&pageNo=2&pageSize=20&sign=4c4065d621e003f06b3465aa97377189', 'new')
    roomChannel('https://hongrenshuo.com.cn/api/v170/room/channel/adv/syndication/timeline?tag=0&type=0&genderType=0&pageNo=3&pageSize=20&sign=409c7e91513fb335bd2e7de498542b01', 'hot')
    '''
    roomChannel('hot'); roomChannel('new');
  conn.close(); print('\n所有账号已上限');