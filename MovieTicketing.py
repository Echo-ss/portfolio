class movie :
    m = ['캡틴마블', '걸캅스', '엑시트']
    mtime = {'캡틴마블':['09:00', '13:00', '15:00', '17:00'],'걸캅스':['09:30', '13:30', '15:30', '17:30'],'엑시트':['10:00', '13:00', '15:00', '17:00']}
    
    def __init__(self, choice_movie_number):
        self.choice_movie_number = choice_movie_number

    # 영화 시간 선택
    def choice_time(self):
        mname = movie.m[self.choice_movie_number-1]
        print(mname, end=' ')
        times = movie.mtime[mname]
        print(times)

        for i in times:
            print(i)
        print("영화 관람 시간을 선택하세요.(ex. 1,2,3,4)", end=' ')
        try:
            number = int(input())
            print("\n\n")
            while ((type(number)==int) and (number <= 0 or number > 4)):
                print("잘 못 입력했습니다.. 관람 시간을 다시 선택하세요.", end=' ')
                number = int(input())
        except ValueError:
            print("선택하지 앖았습니다. 종료됩니다.")
            exit(0)
            

        # 관람 시간times[number-1]
        return number-1


        # 관람 인원 (인원수 및 어른, 청소년, 어린이 계산)
    def people_price(self, rem_seat):
        self.rem_seat = rem_seat
        print("관람하실 인원을 입력해 주세요.", end=' ')

        try:
            people_num = int(input())
            while ((type(people_num)==int) & (people_num <= 0 or people_num > self.rem_seat)):
	            print("인원은 양수이고 남은 좌석(", self.rem_seat, ")을 초과할 수 없습니다. 다시 입력해 주세요", end=' ')
	            people_num = int(input())

            print("어린이는 몇 명인가요?", end=' ')
            kid_num = int(input())
            while ((type(kid_num)==int) & (kid_num < 0 or kid_num > people_num)):
	            print("인원은 양수이고 총 인원수를 초과할 수 없습니다. 어린이는 몇 명인가요?", end=' ')
	            kid_num = int(input())
        
            people_sum = people_num - kid_num

            print("청소년은 몇 명인가요?", end=' ')
            teen_num = int(input())
            print("\n\n")
            while ((type(teen_num)==int) & (teen_num < 0 or teen_num > people_sum)):
	            print("인원은 양수이고 총 인원수를 초과할 수 없습니다. 청소년은 몇 명인가요?", end=' ')
	            teen_num = int(input())
        except ValueError:
            print("올바르지 않은 입력입니다. 종료됩니다.")
            exit(0)

        adult_num = people_num - kid_num - teen_num

        return people_num, adult_num, teen_num, kid_num

# 좌석
class movie_seat(movie) :
    #영화관(1, 2, 3)별로 클래스의 초기화를 진행합니다. 또한 시간대별로 좌석 클래스도 초기화해줍니다. 
    #captain_time_Seat1 = ([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 0, 0]]) 
    captain_time_Seat1 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    captain_time_Seat2 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    captain_time_Seat3 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    captain_time_Seat4 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    girl_time_Seat1 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]) 
    girl_time_Seat2 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    girl_time_Seat3 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    girl_time_Seat4 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    exit_time_Seat1 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]) 
    exit_time_Seat2 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    exit_time_Seat3 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    exit_time_Seat4 = ([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
 
    def __init__(self, choice_movie_number, ntime):
        self.choice_movie_number = choice_movie_number
        self.ntime = ntime

        #좌석 묻기
    def seat(self,ntime, t_seat):
        self.ntime = ntime
        self.t_seat = t_seat

        print ("X는 예매가 완료된 좌석입니다.")
        for i in range(5):
            for j in range(5):
                if t_seat[i][j] == 0:
                    if i == 0:
                        print('A'+ str(j+1), end=' ')
                    if i == 1:
                        print('B'+ str(j+1), end=' ')
                    if i == 2:
                        print('C'+ str(j+1), end=' ')
                    if i == 3:
                        print('D'+ str(j+1), end=' ')
                    if i == 4:
                        print('E'+ str(j+1), end=' ')
                elif t_seat[i][j] == 1:
                    print("X", end=' ')
            print("\n")
        return

    # 좌석 선택
    def seat_select(self, t_seat, num):
        self.t_seat = t_seat
        self.num = num
        for k in range(self.num):
                i = int(input("예약할 좌석의 열(1, 2, 3, 4, 5)를 입력하세요. 1열은 A를 의미합니다.\n"))
                j = int(input("예약할 좌석의 행(1, 2, 3, 4, 5)을 입력하세요\n"))
                if self.t_seat[i-1][j-1] == 1: #예외를 처리
                    print("이미 예매된 좌석입니다. 다시 예매를 진행하세요.")
                    self.seat_select(self.t_seat, self.num)
                else:
                    self.t_seat[i-1][j-1] = 1
        print("예매가 완료되었습니다.", end="\n\n")
        return

    # 총 수입 구하기
    def sum_price(self, adult, teen, kid):
        self.adult = adult
        self.teen = teen
        self.kid = kid
        price_sum = 0
        
        if self.kid > 0:
            price_sum += (5000 * self.kid)
        if self.teen > 0:
            price_sum += (9000 * self.teen)
        if self.adult > 0:
            price_sum += (12000 * self.adult)
        
        return price_sum

    # 좌석 수 체크
    def seat_check(self):
        t_check = 0
        if self.choice_movie_number == 1:
            if self.ntime == 0:
                t_seat = movie_seat.captain_time_Seat1
            elif self.ntime == 1:
                t_seat = movie_seat.captain_time_Seat2
            elif self.ntime == 2:
                t_seat = movie_seat.captain_time_Seat3
            elif self.ntime == 3:
                t_seat = movie_seat.captain_time_Seat4

        if self.choice_movie_number == 2:
            if self.ntime == 0:
                t_seat = movie_seat.girl_time_Seat1
            elif self.ntime == 1:
                t_seat = movie_seat.girl_time_Seat2
            elif self.ntime == 2:
                t_seat = movie_seat.girl_time_Seat3
            elif self.ntime == 3:
                t_seat = movie_seat.girl_time_Seat4

        if self.choice_movie_number == 3:
            if self.ntime == 0:
                t_seat = movie_seat.exit_time_Seat1
            elif self.ntime == 1:
                t_seat = movie_seat.exit_time_Seat2
            elif self.ntime == 2:
                t_seat = movie_seat.exit_time_Seat3
            elif self.ntime == 3:
                t_seat = movie_seat.exit_time_Seat4

        for i in range(5):
            for j in range(5):
                if t_seat[i][j] == 1:
                    t_check += 1

        return t_check, t_seat




# 메인 메뉴
if __name__ == '__main__':
    adults = 0
    teens = 0
    kids = 0
    mflag = 0
    while True:
        print("□□□□□□□□□□□□□□□□□□□□")
        print("□              M Ticketing           □")
        print("□□□□□□□□□□□□□□□□□□□□")
        print("          1. 영화 예매")
        print("          2. 상영 시간 표 보여주기")
        print("          3. 총 수입")
        print("          Q. 종료", end="\n\n")

        print("선택하실 메뉴의 번호 또는 종료 Q를 입력해주세요.(ex. 1,2,3,Q)", end=' ')
        choice_menu = str(input())
        print("\n\n")

        # 영화 예매
        if choice_menu == '1':
            print("□□□□□□□□□□□□□□□□□□□□")
            print("□            MOVIE CHOICE            □")
            print("□□□□□□□□□□□□□□□□□□□□")
            print("             1. 캡틴마블")
            print("             2. 걸캅스")
            print("             3. 엑시트", end="\n\n")
            print("※ 다른 숫자나 문자를 입력 시 종료됩니다.")
            print("영화를 선택하세요.(ex. 1,2,3)", end=' ')
            try:
                choice_movie = int(input())
                print("\n")
                while ((type(choice_movie)==int) and (choice_movie < 0 or choice_movie > 3)):
                    print("잘 못 입력했습니다.. 영화를 다시 선택하세요.", end=' ')
                    choice_movie = int(input())
            except ValueError:
                print("선택하지 않았거나 잘못 입력하여 종료됩니다.")
                exit(0)

            movie1 = movie(choice_movie)                            # 객체 생성하고 movie 클래스에 영화 번호 넘기기
            ntime = movie1.choice_time()                            # 영화 시간 선택 메소드 실행 후 return 값 저장 
            movie2 = movie_seat(choice_movie, ntime)                # 객체 생성하고 movie_seat 클랙스에 영화 번호, 선택시간 넘기기
            t_check, t_seat = movie2.seat_check()                   # 좌석 체크 메소드 실행 후 return 값 저장
            if t_check == 25:
                print("해당 시간대에 예매할 좌석이 없습니다. 다시 예매해 주세요.", end="\n\n")
                continue
            rem_seat = 25 - t_check
            num, adult, teen, kid = movie1.people_price(rem_seat)   # 관람 인원 메소드 실행 후 return 값 저장
            adults += adult                                         # 표 값 미리 계산하기 위한 작업
            teens += teen
            kids += kid
        

            movie2.seat(ntime, t_seat)                              # 좌석 묻기 메소드 실행( 좌석 보여 줌)

            movie2.seat_select(t_seat, num)                         # 좌석 선택 메소드 실행
            mflag = 1                                               # 예매건이 있으므로 수입이 난 걸 의미하는 mflag = 1 로 저장

        # 상영 시간 표 보여주기
        elif choice_menu == '2':
            print("□□□□□□□□□□□□□□□□□□□□")
            print("□            MOVIE SCHEDULE          □")
            print("□□□□□□□□□□□□□□□□□□□□")
            for i in movie.mtime.keys():
                print(i, end=' ')
                print(movie.mtime[i])
            print(" ")

        # 총 수입
        elif choice_menu == '3':
            cnt = 1
            print(" 관리자 모드가 필요합니다. 패스워드를 입력해주세요.", end=' ')
            admin_mode = input()
            while admin_mode != 'goodjob8est':
                if cnt == 3:
                    print("패스워드를 세번 틀리셨습니다. 프로그램 종료합니다.")
                    exit(0)
                cnt += 1
                print("틀렸습니다. 패스워드를 다시 입력해주세요. 틀린 횟수,", cnt-1, end=' ')
                admin_mode = input()
                
            print("□□□□□□□□□□□□□□□□□□□□")
            print("□            Gross income            □")
            print("□□□□□□□□□□□□□□□□□□□□")
            if mflag == 0:
                print("총 수입 : 0 원")
                print(" ")
            else:
                print("총 수입 : ", movie2.sum_price(adults, teens, kids), "원")
                print(" ")

        # 종료
        elif choice_menu == 'Q' or choice_menu == 'q':
            exit(0)

        else:
            print("잘 못 입력하셨습니다. 다시 입력바랍니다.")
