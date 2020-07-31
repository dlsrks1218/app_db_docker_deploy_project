import user_init as ui
import customer_module as cm
import salesperson_module as sm

def start():
    print('='*45)
    print('Welcome to Car Sales & Service Center') 
    print('='*45)

    # mysql 연결 객체 - db
    db = ui.get_connect('mysql', 'mydb')
    # 현재 사용자의 로그인 정보 - 고객인지 판매자인지, 접속된 아이디와 이름
    cur_user = ui.User(0,0,'','')
    
    while True:
        # 로그인 되지 않은 초기 상태로 로그인 혹은 회원가입
        if cur_user.c_no == 0  and cur_user.s_no == 0:
            print('\n1. 로그인 2. 회원 가입 0. 종료')
            menu = int(input('입력 : '))
            if menu == 0:
                db.close()
                print('안녕히 가세요')
                exit()
            elif menu == 1:
                cur_user = ui.sign_in(db, cur_user)
                cur_user.show()
            elif menu == 2:
                cur_user = ui.sign_up(db, cur_user)
                cur_user.show()
            else:
                print('올바른 메뉴 번호를 입력해주세요.')
                continue    
        # 고객 혹은 판매자로 로그인 된 상태
        else:
            # customer로 로그인 후 고객용 ui 보여주기
            if cur_user.c_no != 0 and cur_user.s_no == 0:
                print('======고객용 서비스======')
                print('1. 자동차 목록 조회 2. 자동차 구매 3. 서비스 신청 4.로그아웃 0. 종료 : ')
                menu = int(input('입력 : '))
                if menu == 1:
                    cm.available_car_list(db)
                elif menu == 2:
                    cm.buy_car(db, cur_user)
                elif menu == 3:
                    # 필요한 부품의 갯수가 여유 있는지 체크
                    parts_tuple = cm.get_parts(db)
                    # 부품 선택 도중 취소 시 continue로 다시 고객용 서비스 고르기 화면으로 돌아감
                    if parts_tuple == None:
                        continue
                    # 부품이 존재한 상태에, 7월 한달 도중 정비사가 일이 없어 선택 가능한 날을 조회
                    m_no_work_date_tuple = cm.get_available_mechanic_and_work_date(db, cur_user)
                    # 부품과 정비사, 작업 날짜를 데이터베이스에 입력
                    cm.insert_service_and_work(db, cur_user, parts_tuple, m_no_work_date_tuple)
                elif menu == 4:
                    # 현재 로그인 정보를 비워 로그아웃 수행
                    cur_user = cur_user.logout()
                    print('로그아웃합니다.')
                if menu == 0:
                    print('안녕히 가세요')
                    exit()
            # salesperson으로 로그인 후 판매자용 ui 보여주기
            elif cur_user.s_no != 0 and cur_user.c_no == 0:
                print('======판매자용 서비스======')
                print('1. 고객 관리 2. 차량 관리 3. 주문 관리 4. 로그아웃 0. 종료')
                menu = int(input('입력 : '))
                if menu == 1:
                    # 고객 정보 조회(R),수정(U),삭제(D) (등록은 고객만 수행)
                    sm.manage_customer(db, cur_user)
                elif menu == 2:
                    # 차량 정보 등록(C),조회(R),수정(U),삭제(D)
                    sm.manage_car(db, cur_user)
                elif menu == 3:
                    # 주문 내역 정보 조회(R)
                    sm.manage_invoice(db)
                elif menu == 4:
                    cur_user = cur_user.logout()
                    print('로그아웃합니다.')
                if menu == 0:
                    print('안녕히 가세요')
                    exit()


if __name__ == '__main__':
    start()