# DataPipeline_
데이터 파이프라인 구성을 해보고 flow를 경험해보자
###### private으로 진행했기 때문에 활용하기 위한 public으로 하나 더 만듦. 

### 솔루션과의 유사점과 차이점은?
    *유사점
       : [에이전트-분산처리시스템-수집서버-매니저(분석시스템)] 등과 같은 흐름과 유사함.
    *차이점
       : 솔루션은 확장성이 클라우드에 비해 떨어진다. On-Premises 이기에 하드웨어적 장애는 불가피하다.


# 데이터 생성

###### 사전 구성
#### 1. AWS 구성(5개의 vm 인스턴스 생성)
    - aws 가입
    - 서비스 -> EC2 선택 -> 리전(지역) 은 서울로 (다른 지역은 느리기 때문에) ->
    - 인스턴스 시작 선택
     1 단계 : Amazon Machine Image(AMI) 선택 : Ubuntu Server 16.04 LTS (HVM), SSD Volume Type 선택(Ubuntu Server 16.04 LTS (HVM),EBS General Purpose (SSD) Volume Type. Support available from Canonical 64비트(x86))
     2 단계 : 인스턴스 유형 선택 : t2.micro ( 프리 티어 사용 가능 ) 선택 -> 다음 : 인스턴스 세부 정보 구성 선택
     3 단계 : 인스턴스 세부정보 구성 : 인스턴스 개수(5개로 변경) -> 검토 및 시작
     7 단계 : 인스턴스 시작 검토 : 시작하기 버튼 누르면 기존 키 페어 선택 또는 새 키 페어 생성 창이 뜨고 SSH 키값을 생성하라고 한다. -> 첫번째 '기존 키 페어 선택' 리스트(새 키 페어 생성) -> 키 페어 이름(echo_ss_dp) -> 키 페어 다운 -> 인스턴스 시작 선택 -> 인스턴스 보기 선택
     
     
#### 2.VM 인스턴스 접속하기
    [윈도우 환경]
    - 터미널 프로그램 열기 [xshell 기준]
    - 새 세션 만들기
     [연결] 탭
     이     름 : 용도 이름과 같게함
     프로토콜 : SSH
     호 스 트 : 퍼블릭IP
     포     트 : 22
     [연결] 탭 -> [사용자 인증]
     방         법 : Public Key 선택
     사용자 이름 : ubuntu
     사용자   키 : 키_파일 선택
    - 만들어진 세션 선택, 접속


### 1. logstash 설치 및 설정
* * *
#### twitter_logstash 구성
   - twitter_logstash 접속
          
    $ sudo apt-get update  //apt-get, ubuntu에서 사용하는 패키지 관리자의 소스 리스트를 최신화 하는 작업 

   - install JDK 1.8
    
    $ sudo apt-get install openjdk-8-jdk -y // 사용될 빅데이터 분석 플랫폼은 거의 자바 기반이므로 설치
    $ java -version // 버전 확인
    openjdk version "1.8.0_212"
    OpenJDK Runtime Environment (build 1.8.0_212-8u212-b03-0ubuntu1.16.04.1-b03)
    OpenJDK 64-Bit Server VM (build 25.212-b03, mixed mode)

   - install logstash
   
     검색창에 "install logstash 5.5"
     * elasticsearch 장점 중의 하나인 문서가 잘되어있는 것인데 이 문서를 보며 활용하는 방법으로 설치해보자.

     Installing Logstash (Optional) | Beats Platform Reference [5.5] | Elastic 클릭
     > deb (devian package) // Ubuntu와 호환성을 갖는 패키지 바이너리 형태
    
    $ JDK는 이미 설치했기 때문에 skip
    $ curl -L -O https://artifacts.elastic.co/downloads/logstash/logstash-5.5.3.deb // curl 를 이용해서 다운로드
    $ ls // 다운 받은 파일 확인
    logstash-5.5.3.deb
    $ sudo dpkg -i logstash-5.5.3.deb // 설치

   - configure logstash jvm heap size
     
     logstash 기동 시 쓰는 jvm의 환경변수 설정하기 위해서이다. 그리고 For aws instance of t2. generation 해당하는 설정
   
    $ sudo vim /etc/logstash/jvm.options  // 파일 수정 작업 시 항상 백업하는 습관을 들여 놓는다.
    [Org]
    -Xms256m
    -Xmx1g
    [Modify]
    -Xms256m
    -Xmx256m

#### logstash 설정
   - configure logstash
     패키지로 설치 했기에 환경변수 파일이 모두 모인 /etc/ 하위에 logstash가 생김. 해당 디렉토리엔 jvm.options 파일이나 각종 properties 등 존재한다.
     하위 conf.d 는 실질적으로 어떤 데이터를 어디서 가져오고 어디로 전송하는지 configure 를 설정하는 디폴트 디렉토리이다.
   
    $ sudo vim /etc/logstash/conf.d/logstash.conf
    input {
      twitter {
                consumer_key => "OSgSJBCTmczN9Ui257BmkMgln"
                consumer_secret => "YjK8TopBtqJvvvDacy1NchsfsEW0LT4tOFAI6ZJ35x4kjGquXr"
                oauth_token => "1135827943870029829-f2nFqJ7XjfyKB5jcg3O2nWRtcbxbB4"
                oauth_token_secret => "QFmUzs4eyDfybKQNBDoBUBYzoEfGlyA1SWyQH7CrQJ8Kh"
                keywords => ["news","food","data"]
                full_tweet => true
      }
    }

    output {
        file {
               path => "/tmp/twitter-%{+YYYY-MM-dd}.json"  # kafka로 전송할 건데 시스템에 파일로 떨구는 이유는 api key가 제대로 설정 되어서 로그를 제대로 받아오는지 확인해야하기 때문에. 그리고 kafka 구성까지 완료 후에 데이터 확인을 하기에는 시간이 걸리니 데이터 확인을 먼저 하기 위해 임시 설정이다.
               codec => json_lines // 구분자를 new line으로 잡겠다
        }
    }

   **※ kafka 구성 후에 수정한다.** 
     - Modify logstash.conf
     - kafka 로 전송하기 위한 output 설정

    $ sudo vim /etc/logstash/conf.d/logstash.conf
    output {
       kafka {
               topic_id => "twitter"
               bootstrap_servers => "172.31.42.242:9092"  # kafka 의 broker 정보를 입력하는데 kafka 서버의 ip와 port
               acks => "1"
               codec => json_lines
       }
    }

### 2. logstash TEST
* * *
   - start logstash

    $ sudo service logstash start
    $ ls -lrt /tmp/
    $ sudo vim /tmp/twitter-2019-06-04.json
    $ sudo service logstash stop
    $ sudo jps  // logstash 정지 상태 확인
    18196 Jps  // jps는 자바프로세스 확인하는 명령어. jps만 나오면 정지 상태이며 만약, Main 이런게 보인다면 기동 상태이다. 


   - check twitter log
   
    $ tail -f /tmp/twitter*.json  // 실시간일 때 tail -f 로 보면 유용하다. 하지만 이미 이전에 정지 하였기 때문에 tail/less 옵션없이 확인해도 무방하다. 대용량 파일은 vim/vi로 열지 말것..
    $ less /tmp/twitter*.json

   - kafka를 구성을 위해 stop logstash
   
     이전에 정지 하였기 때문에 생략한다.
   
   
   
# 데이터 수집 - kafka

### 1. Kafka 설치 및 구성
* * *
   - 데이터 buffering을 위한 kafka 구성
   
   > kafka를 쓰는 이유?
   >> : 데이터를 꺼내서 뒷단의 elasticsearch 에 밀어넣고 분석을 하려하는데 elasticsearch가 장애난 상황이라면! 데이터를 전송하는 logstash는 잘못된 응답을 받으면서도 데이터를 전송해서 데이터 유실이 발생한다. 하지만 kafka의 버퍼링으로 중단된 시간만큼 데이터를 모아두고 장애 해결 후 이어서 worker/consumer가 데이터를 꺼내갈 수 있도록 해준다.
      이런 버퍼링 역할이 큰 강점이다.

   - install JDK 1.8

    $ sudo apt-get update // update를 안해주면 아래 jdk install 할 때 404 에러가 뜨면서 진행되지 않음
    $ sudo apt-get install openjdk-8-jdk -y
    $ java -version
    
   - download apache-kafka
     
     검색창에 "download apache kafka"
     첫번째 보이는 download 부분 링크 클릭
     바이너리 다운로드 부분에서 .tgz 를 왼쪽 클릭 링크 복사하여 아래처럼 wget 이용해 다운로드 받는다.

    $ wget https://archive.apache.org/dist/kafka/0.11.0.1/kafka_2.11-0.11.0.1.tgz
    $ ls -ltr // 다운로드 파일 확인
    -rw-rw-r-- 1 ubuntu ubuntu 42031343 Sep 12  2017 kafka_2.11-0.11.0.1.tgz
    $ tar xvzf ./kafka_2.11-0.11.0.1.tgz // 압축풀기
    $ ls -ltr // 디렉토리 확인 
    drwxr-xr-x 6 ubuntu ubuntu     4096 Sep  5  2017 kafka_2.11-0.11.0.1

   - start zookeeper
  
   > zookeeper 역할?
   >> : 앞서 kafka 버퍼링 역할 설명이 있었다. zookieeper는 kafka의 데이터를 worker/consumer가 어떤 메시지까지 가져갔는지의 알 수 있는 트랜잭션 로그, offset 정보를 저장한다.
        zookeeper는 offset에 대한 코드 관리와 kafka cluster health check. 이 두가지 역할을 위해 kafka와 항상 같이 설치 된다.
   
    $ ln -s kafka_2.11-0.11.0.1 kafka // 심볼릭 링크를 만들어 편하게 디렉토리 접근하기
    $ ls -ltr // 심볼릭 링크 확인
    lrwxrwxrwx 1 ubuntu ubuntu       19 Jun  4 17:44 kafka -> kafka_2.11-0.11.0.1
    $ cd kafka
    $ ./bin/zookeeper-server-start.sh config/zookeeper.properties &   // zookeeper-server-start.sh를 사용하면서 이 명령어에서 어떤 config를 참조할지 명시한 명령어이다. & 는 백그라운드로 돌리기 위함이다.
    -생략
    [2019-06-04 18:24:57,645] INFO binding to port 0.0.0.0/0.0.0.0:2181 (org.apache.zookeeper.server.NIOServerCnxnFactory)
    zookeeper.properties 내용 중 포트 2181 로 주소가 바인딩 되어 쓸 수 있다는 걸 알 수 있다.

   **※ cannot allocate memory 발생 시 해결방법**
   
    $ vim /home/ubuntu/kafka/bin/zookeeper-server-start.sh
    export KAFKA_HEAP_OPTS="-Xmx512M -Xms512M"  // 복사 후 kafka-server-start.sh 최상단에 붙여넣기
    * 1G였으면 512M, 512M -> 128M
    * 최상단에 넣는 이유는,  KAFKA_HEAP_OPTS 값이 정의 되어있지 않으면 기본값을 물고 올라오기 때문이다. 

   > zookeeper.properties 설명

    dataDir=/tmp/zookeeper  // offset 정보를 관리하기 위해서 디스크에 저장하는 경로 설정
    clientPort=2181  // 서비스 바인딩 포트
    maxClientCnxns=0  // 0:무제한

   > kafka cluster 구성을 하려면?
   >> https://kafka.apache.org/ -> Quickstart -> Step 6: Setting up a multi-broker cluster 참조


   - start kafka broker
   
    $ ./bin/kafka-server-start.sh config/server.properties &

   - if exist insufficient memory exception
   
    $ vim ./bin/kafka-server-start.sh
    export KAFKA_HEAP_OPTS="-Xmx256M -Xms256M"  // 최상단에 붙여넣기

   - check zookeeper, kafka listening port

    $ sudo netstat -anp | egrep "9092|2181"
    tcp6       0      0 :::9092                 :::*                    LISTEN      18696/java      
    tcp6       0      0 :::2181                 :::*                    LISTEN      18440/java      


### 2. topic 생성 및 확인
* * *
   - create topic

     데이터를 저장하기 위한 논리단위 topic 과 partition

    $ ./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitter
    ※ create 명령어를 받아서 저장하고 전송할 zookeeper 를 호출해서 topic을 생성
    ※ --replication-factor : 복제 수,  복제가 필요한 이유 복제가 없으면 여러대 kafka 서버 중 한 서버가 죽었을 때 그 서버가 가진 데이터는 유실된다. 복제가 있으면 겹치지 않은 partition 정보를 다른 서버로 failover하기 위해서 필요하다. failover 되면 연속적으로 데이터를 잃어올 수 있게 된다.
    ※ -- partitions : 서버 갯수에 따라 설정해 놓으면 분산 처리 효과를 받을 수 있다.


   - check topic

    $ ./bin/kafka-topics.sh --list --zookeeper localhost:2181
    -생략-
    [2019-06-04 20:56:12,139] INFO Established session 0x16b24179fbb0003 with negotiated timeout 30000 for client /127.0.0.1:47298 (org.apache.zookeeper.server.ZooKeeperServer)
    twitter
    -생략-
    $ ./bin/kafka-topics.sh --describe --zookeeper localhost:2181
    -생략-
    [2019-06-04 20:57:17,728] INFO Established session 0x16b24179fbb0004 with negotiated timeout 30000 for client /127.0.0.1:47300 (org.apache.zookeeper.server.ZooKeeperServer)
    Topic:twitter	PartitionCount:1	ReplicationFactor:1	Configs:
	  Topic: twitter	Partition: 0	Leader: 0	Replicas: 0	Isr: 0

   - change topic retention byte
   
    $ ./bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name twitter --alter --add-config retention.bytes=100000000  // 100M
    ※ retention 은 데이터 사이즈/시간 두가지 단위로 설정 가능하다. 기본 72 이거나 ..168시간 topric 당 1G
    ※ 기본으로 진행하면 kafka 디스크가 full 나기 때문에 위처럼 topic에 대한 alter를 해준다..
    ※ 100M 지정 후 kafka의 데이터 저장이 100M가 넘으면 가장 오래된 것부터 사라진다. 
    [2019-06-04 21:05:31,605] INFO Established session 0x16b24179fbb0005 with negotiated timeout 30000 for client /127.0.0.1:47302 (org.apache.zookeeper.server.ZooKeeperServer)
    Completed Updating config for entity: topic 'twitter'.[2019-06-04 21:05:31,765] INFO Processing notification(s) to /config/changes (kafka.common.ZkNodeChangeNotificationListener)

### 3. kafka message TEST
* * *
   - test producing message
 
   console 명령어를 통해 메세지를 생성하고 메세지가 잘 수신되는지 test
   
    $ ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic twitter

   - test consuming message
  
    $ ./bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic twitter

   - inbound add [ kafka, elasticsearch ]
   
     방화벽 쪽을 허용해줘야 logstash start 후 데이터들을 저장 할 수 있다.
     amazon 인스턴스에서 kafka_server를 클릭 -> [설명] 탭 클릭 -> 보안그룹 : launch-wizard-1 클릭 -> 그룹ID 복사 -> [인바운드] 탭 클릭 -> 편집 클릭 -> 규칙 추가 -> 유형:모든 트래픽 -> 소스:그룹ID 붙여넣기 -> 저장
     ###### ※ amazon 인스턴스 -> 작업 -> 네트워킹 -> 보안그룹 변경으로도 가능하다.

   - start twitter_logstash //  *Modify logstash.conf 수정 후 실행한다.
   
    $ sudo service logstash start
    logstatsh 가 start 되면 consumer 쪽에 데이터가 보인다면 kafka에 잘 저장되고 있다는 것이다.
    $ sudo service logstash stop
    $ sudo jps // logstash 정지 상태 확인
    ※ 만약 제대로 정지 안되거나 이상 상태(process information unavailable)라면 
    $ cd /tmp/hsperfdata_logstash/PID 값 삭제 또는 mv
    $ sudo jps  // 다시 확인 



# 데이터 저장, 처리 - elasicsearch

### 1. elasticsearch 설치 및 설정
* * *
   - pre-requisite

     Launch 1~3 VM for elasticsearch  // 1대로 진행해보기
     JDK 1.8.x

   - install elasticsearch
     
     검색창에 "install elasticsearch 5.5"
     
     **Download and install the .tar.gz package**
     The .tar.gz archive for elasticsearch v5.6.0 can be downloaded and installed as follows.
     
    $ curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.3.tar.gz // wget 으로 해도 된다.
    $ sha1sum elasticsearch-5.5.3.tar.gz   // 1)
    $ tar -xzf elasticsearch-5.5.3.tar.gz
    $ cd elasticsearch-5.5.3/  // 2)

   ###### 1) Compare the SHA produced by shalsum or shasum with the published SHA  //
   ###### 2) The directory is known as $  //

   - configure logstash jvm heap size  // vm 인스턴스의 memory가 작기 때문에 기본값에서 낮춰야한다.

    $ vi config/jvm.options
    [Org]
    -Xms2g
    -Xmx2g
    [modify]
    -Xms512m
    -Xmx512m

   - test running
   
    $ ./bin/elasticsearch
    [2019-06-05T09:49:37,734][INFO ][o.e.n.Node               ] initialized
    [2019-06-05T09:49:37,735][INFO ][o.e.n.Node               ] [fwkYvyj] starting ...
    [2019-06-05T09:49:38,032][INFO ][o.e.t.TransportService   ] [fwkYvyj] publish_address {127.0.0.1:9300}, bound_addresses {[::1]:9300}, {127.0.0.1:9300}
    [2019-06-05T09:49:41,143][INFO ][o.e.c.s.ClusterService   ] [fwkYvyj] new_master {fwkYvyj}{fwkYvyjZQSKME0kmX22VZg {6G0tVFLaTGO0TeRk1gKzXw}{127.0.0.1}{127.0.0.1:9300}, reason: zen-disco-elected-as-master ([0] nodes joined)
    [2019-06-05T09:49:41,198][INFO ][o.e.h.n.Netty4HttpServerTransport] [fwkYvyj] publish_address {127.0.0.1:9200}, bound_addresses {[::1]:9200}, {127.0.0.1:9200}
    [2019-06-05T09:49:41,198][INFO ][o.e.n.Node               ] [fwkYvyj] started
    [2019-06-05T09:49:41,201][INFO ][o.e.g.GatewayService     ] [fwkYvyj] recovered [0] indices into cluster_state

   **※ elasticsearch 'max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144] 에러 발생 해결방법**
   > memory에 동적으로 할당되는 커널 파라메터 값이 기본값보다 작아서 발생한 에러이다. 그렇기 때문에 elasticsearch 기본값인  [262144] 으로 변경해야한다. t2 타입의 자원이 작아서 자동 할당 값이 작은 것이지 production live 환경에서는 최소 메모리 30G 이상은 쓰기에 기본값보다 높게 자동 할당 될것이다.
   
    $ sudo sysctl -w vm.max_map_count=262144
    $ sudo sysctl -p  // published
    $ sudo sysctl vm.max_map_count  // 값 확인

   - configure elasticsearch

    $ vi config/elasticsearch.yml
    cluster.name: es-twitter-cluster
    node.name: node-1
    network.host: 0.0.0.0

   - run elasticearch
   
    $ ./bin/elasticsearch &

   - check elasticsearch
   
    $ curl -XGET localhost:9200
    $ curl -XGET localhost:9200/_cluster/health?pretty


### 2. consumer_logstash 구성
* * *
###### kafka 에서 데이터를 받아서 elasticsearch 로 밀어넣을 것이기에 twitter_logstash configure 와는 다르다.

   - install JDK 1.8.x
   - Install Logstash
   - configure logstash jvm heap size
   
    $ sudo vim /etc/logstash/jvm.options
    [Org]
    -Xms256m
    -Xmx1g
    [Modify]
    -Xms128m
    -Xmx128m
 
 #### logstash 설정 
   - configure logstash
  
    $ sudo vim /etc/logstash/conf.d/logstash.conf
    input {
      kafka {
              bootstrap_servers => "172.31.42.242:9092"  // 서버간의 통신은 privite IP 여야한다.
              codec => json_lines
              consumer_threads => 1
              group_id => twitter_log_to_es
              topics => "twitter"
      }
    }

    output {
       elasticsearch {
                       codec => json
                       hosts => "172.31.42.124:9200"
                       index => "twitter-%{+YYYYMMdd}"
                       workers => 1
       }
    }

   - start logstash

    $ sudo service logstash start  // 시작하면 kafka에서 데이터를 받아 elasticsearch로 밀어넣는다.

   - elasticsearch total fields limit  // logstash 에서 생성하고 있는 index명을 찾아서 아래 구성에 맞게 바꾼다. 

     검색창에 "elasticsearch total fields limit"
     https://discuss.elastic.co/t/total-fields-limit-setting/53004

   ###### ※ elasticsearch 에서 해당 명령어를 해야한다.
   
    $ curl -XPUT http://localhost:9200/twitter_20190605/_settings -d'
    {
	     "index.mapping.total_fields.limit":3000
    }'

    {"error":{"root_cause":[{"type":"index_not_found_exception","reason":"no such index","resource.type":"index_or_alias","resource.id":"twitter_20190605","index_uuid":"_na_","index":"twitter_20190605"}],"type":"index_not_found_exception","reason":"no such index","resource.type":"index_or_alias","resource.id":"twitter_20190605","index_uuid":"_na_","index":"twitter_20190605"},"status":404}



# 데이터 조회 - kibana

### 1. kibana 설치
* * *
   - install kibana

     kibana가 elasticsearch 를 조회해감
     ※ 자바가 필요없음. JDK 설치 X
     검색창에 "install kibana 5.5"
     
    
   - configure kibana

    $ sudo vim /etc/kibana/kibana.yml
    server.port: 5601
    server.host: "0.0.0.0"   // 서비스할 바인딩 ip
    elasticsearch.url: "http://${elasticsearch ip}:9200"  // elasticsearch

   - inbound add
     
     amazon 인스턴스에서 kafka_server를 클릭 -> [설명] 탭 클릭 -> 보안그룹 : launch-wizard-1 클릭 -> 그룹ID 복사 -> [인바운드] 탭 클릭 -> 편집 클릭 -> 규칙 추가 -> 유형:사용자 지정TCP규칙 -> 포트:5601 ->소스:My ip -> 저장
     ###### ※kibana는 랜섬웨어 공격에 취약하기 때문에 inbound add를 해주어야한다.

   - start kibana
     
    $ sudo service kibana start

   - connect kibana site
   
    http://${kibana ip}:5601


   - ** *kibana/elasticsearch 호환성 문제가 생기기 때문에 버전을 맞춰줘야한다.**

     elasticsearch 프로세스 죽이고 /tmp/하위 pid 값도 삭제 후 다시 설치


   **※ kafka 에러 'Failed to acquire lock on file .lock in /tmp/kafka-logs'**
  
    $ ./bin/kafka-server-stop.sh
    $ sudo rm -rf /tmp/kafka-logs  // kafka-logs 디렉토리를 삭제 또는 mv로 이름 바꾸기



