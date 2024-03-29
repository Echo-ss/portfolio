
# 하둡을 사용하여 빅데이터 분석
   하둡 클러스터를 생성하고 Hive 스크립트를 실행하여 로그 데이터 로드/처리를 합니다.
* * *

#### 기술스택
   AWS EMR(Hadoop cluster, HiveQL), Amazon S3
   
### 샘플 데이터
    - Amazon 프로젝트 기반 샘플 로그
    - SmartCar_Master, SmartCar_Item_buylist
    
### 프로젝트의 이유는?
   AWS를 이용해서 간단한 클러스터 설치/운영으로 시간 소요 없이 바로 동작과 퍼포먼스를 경험하고 데이터 로드 및 처리를 해보고 싶어서 AWS 기반의 프로젝트 중 '하둡을 사용하여 빅데이터 분석' 을 진행 및 다른 샘플 로그를 추가도 해서 진행.
   
### 프로젝트 후의 얻은 것
* * *
   VMware나 ec2 micro 인스턴스만 쓰다가 AWS를 제대로 이용해보니 시간이나 활용도 면에서 절약 및 편리하게 사용할 수 있었습니다. 많은 기업들이 AWS를 활용하는 이유를 느낄 수 있었고 표준 SQL 만 할 수 있어도 Hive/HiveQL 스크립트를 다루는데 어렵지 않음을 경험할 수 있어 좋았습니다. 샘플 로그를 활용하면서 어떤 데이터가 제공되면 좋을까 고민하고 원하던 결과를 얻을 때 좋은 고민을 해볼수록 결과에서 얻는 기쁨이 크다는 걸 느꼈습니다.

### 1. 사전 조건 설정
    - Amazon S3 버킷 생성
    name : emr-project
    region : 아시아 태평양(서울), ap-northeast-2
    
    - SSH Key 페어 생성
    name : emrssh


### 2. EMR 클러스터 시작
    - 클러스터 생성 - 빠른 옵션
    
    일반구성
       클러스터 이름 : emr_test
       로깅 체크 : 체크 (emr의 모든 로깅 정보를 남겨줍니다.)
       S3 폴더 : s3://aws-logs-250187480162-ap-northeast-2/elasticmapreduce/
    소프트웨어 구성
       릴리스 : emr-5.24.1
       애플리케이션ㅋ : Core Hadoop: Hadoop 2.8.5 with Ganglia 3.7.2, Hive 2.3.4, Hue 4.4.0, Mahout 0.13.0, Pig 0.17.0, and Tez 0.9.1
    하드웨어 구성
       인스턴스 유형 : m4.large (범용 부분으로 바꿈, 메모리 기반 m 사용)
       인스턴스 개수 : 3(1개의 마스터 및 2개의 코어 노드)
    보안 및 엑세스
       EC2 키 페어 : emrssh 선택
       권한 : 기본값

### 3. SSH 연결 허용
   클라이언트에서 클러스터에 대한 SSH 연결 허용 작업을 합니다.
   
    클러스터 EC2 인스턴스에 대한 인바운드 SSH 연결 허용하려면
    -> Amazon EMR 콘솔 열기
    -> 클러스터 이름 선택
    -> 하단, ElasticMapReduce-master 선택
    -> 인바운드 선택 - 편집 - 새 인바운드 규칙 추가 - SSH / 내 IP / 저장
    -> ElasticMapReduce-slave 도 위와 같게
    
### 4. Hive 스크립트를 단계로 실행하여 데이터 처리
   EMR GUI 활용과 CGI 활용으로 둘다 해본다.
   
   [EMR GUI로 해보기]
    
    - Amazon EMR 콘솔 열기
    - 해당 클러스터가 '대기'상태 인지 확인
    - 단계 탭 선택 - 단계 추가
    단계 유형 : Hive 프로그램
    이름 : Hive 프로그램
    스크립트 S3 위치: s3://ap-northeast-2.elasticmapreduce.samples/cloudfront/code/Hive_CloudFront.q
    입력 S3 위치: s3://ap-northeast-2.elasticmapreduce.samples
    출력 S3 위치: s3://emr-project
    인수
    실패 시 작업 : 계속
    - 추가
    
    결과 : s3://emr-project/os_requests > 000000_0 -> 다운로드 -> 열기
    (Hive_CloudFront.q 스크립트 안에 출력 시 분석한 쿼리로 나오게 했기 때문에 아래처럼 OS별 값이 나옵니다.)
    
    Android855
    Linux813
    MacOS852
    OSX799
    Windows883
    iOS794
 
   [CLI로 해보기_접속]
   
    - 버킷 생성(sc_master and sc_item, hql 업로드 경로)
   
    - Amazon EMR 콘솔 열기
    - 요약 탭에서 SSH 부분 클릭(연결 방법이 나옴)
    - 터미널 프로그램 열기
    - 호스트 : ec2-##-###-###-###.ap-northeast-2.compute.amazonaws.com
    - 포트 : 22
    - 사용자 키 선택하여 접속
    
    WARNING! The remote SSH server rejected X11 forwarding request.

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

    https://aws.amazon.com/amazon-linux-ami/2018.03-release-notes/
    5 package(s) needed for security, out of 10 available
    Run "sudo yum update" to apply all updates.
                                                                    
    EEEEEEEEEEEEEEEEEEEE MMMMMMMM           MMMMMMMM RRRRRRRRRRRRRRR    
    E::::::::::::::::::E M:::::::M         M:::::::M R::::::::::::::R   
    EE:::::EEEEEEEEE:::E M::::::::M       M::::::::M R:::::RRRRRR:::::R 
      E::::E       EEEEE M:::::::::M     M:::::::::M RR::::R      R::::R
      E::::E             M::::::M:::M   M:::M::::::M   R:::R      R::::R
      E:::::EEEEEEEEEE   M:::::M M:::M M:::M M:::::M   R:::RRRRRR:::::R 
      E::::::::::::::E   M:::::M  M:::M:::M  M:::::M   R:::::::::::RR   
      E:::::EEEEEEEEEE   M:::::M   M:::::M   M:::::M   R:::RRRRRR::::R  
      E::::E             M:::::M    M:::M    M:::::M   R:::R      R::::R
      E::::E       EEEEE M:::::M     MMM     M:::::M   R:::R      R::::R
    EE:::::EEEEEEEE::::E M:::::M             M:::::M   R:::R      R::::R
    E::::::::::::::::::E M:::::M             M:::::M RR::::R      R::::R
    EEEEEEEEEEEEEEEEEEEE MMMMMMM             MMMMMMM RRRRRRR      RRRRRR
    
    [hadoop@ip-##-###-###-### ~]$ 
    
   [스크립트 실행/]
   
    ※ 해당 스크립트 안에는 LOAD DATA 부분의 경로가 INPUT=s3://emr-project 인자를 받고 하위경로가 지정 되어있어 있습니다.
    [hadoop@ip-##-###-###-### ~]$ hive-script --run-hive-script --args -f s3://emr-project/sc_master.hql -d INPUT=s3://emr-project
    /usr/bin/hive

    Logging initialized using configuration in file:/etc/hive/conf.dist/hive-log4j2.properties Async: false
    OK
    Time taken: 1.239 seconds
    OK
    Time taken: 0.803 seconds
    Loading data to table default.smartcar_master
    OK
    Time taken: 1.801 seconds


    hive> SELECT * FROM smartcar_master limit 10;
    OK
    A0001	여	32	미혼	서울	프리랜서	1000	2009	F
    A0002	남	53	미혼	충남	주부	2500	2015	A
    A0003	여	62	기혼	대전	회사원	2500	2012	B
    A0004	남	31	미혼	광주	공무원	2000	2010	D
    A0005	남	67	미혼	대구	공무원	1700	2002	C
    A0006	여	30	미혼	인천	전문직	2000	2016	D
    A0007	남	61	미혼	전남	개인사업	1700	2003	E
    A0008	여	20	미혼	충북	개인사업	1500	2013	G
    A0009	여	60	미혼	경남	프리랜서	3500	2015	D
    A0010	여	69	미혼	제주	개인사업	1200	2003	A
    Time taken: 3.437 seconds, Fetched: 10 row(s)


    [hadoop@ip-##-###-###-### ~]$ hive-script --run-hive-script --args -f s3://emr-project/sc_item.hql -d INPUT=s3://emr-project
    /usr/bin/hive

    Logging initialized using configuration in file:/etc/hive/conf.dist/hive-log4j2.properties Async: false
    OK
    Time taken: 1.044 seconds
    OK
    Time taken: 0.447 seconds
    Loading data to table default.smartcar_item_buylist
    OK
    Time taken: 1.862 seconds


    hive> SELECT * FROM smartcar_item_buylist limit 10;
    OK
    M0014	Item-018	2	201606
    G0035	Item-015	3	201606
    I0090	Item-009	3	201606
    K0095	Item-018	5	201606
    Y0042	Item-020	2	201606
    W0023	Item-030	2	201606
    Y0036	Item-023	3	201606
    T0026	Item-028	1	201606
    Q0044	Item-008	1	201606
    Q0056	Item-014	5	201606
    Time taken: 2.598 seconds, Fetched: 10 row(s)
    
   [어떤 데이터를 필요로 할까?]
   
   **위 처럼 고민해보는 이유는?** 
   데이터 엔지니어/분석가의 기술과 작업 범위에 따른 이해관계로 인해 커뮤니케이션이 잘 안될 때가 있고 작업 요청이 반복 될 수 있다고 합니다. 이것은 엔지니어와 분석가 뿐만 아니라 분석가와 현업 등 데이터를 필요로 하는 곳이라면 존재할거라 생각합니다.
   이를 좁히기 위해 데이터 엔지니어로서 뭘 해야 원할한 커뮤니케이션이 되고 제대로 된 데이터를 제공할 수 있을까 생각했을 때 필요로 하는 데이터에 대해서 생각해보는 연습을 하고 기술적 역량의 범위를 넓히면 되겠다 생각을 하게 되어 데이터를 아래처럼 뽑아봤습니다.
     
     - 성별로 가장 많이 팔린 Item은?
     
     # hive> SELECT t.sex, t.sc_sum, t.item
      > FROM(SELECT m.sex, SUM(i.score) as sc_sum, RANK() OVER (PARTITION BY m.sex ORDER BY SUM(i.score) DESC) sc_rank, i.item FROM smartcar_master m , smartcar_item_buylist i WHERE m.car_number = i.car_number GROUP BY m.sex, i.item) t
      > WHERE sc_rank = 1;
      OK
      남		 4993 Item-020
      여		 5235 Item-012
      Time taken: 5.998 seconds, Fetched: 2 row(s)
