from user_init import User
from typing import Callable, Tuple
from pymysql.connections import Connection as _Connection

def total_car_list(db:_Connection) -> None: 
    cursor = db.cursor()
    print("#" * 45)
    print('차량번호\t브랜드\t연식\t모델명\t색상')
    print("#" * 45)
    show_tb = 'select car_no, brand, year, model, color from Car'
    rows = cursor.execute(show_tb)
    for row in cursor.fetchall():
        print('\t'.join(map(str,list(row))))


def total_customer_list(db: _Connection) -> None:
    cursor = db.cursor()
    print("#" * 45)
    print('고객번호\t이름\t나이\t주소\t전화번호')
    print("#" * 45)
    show_cus = 'select c_no,name,age, address, phone from Customer'
    rows = cursor.execute(show_cus)
    for row in cursor.fetchall():
        print('\t'.join(map(str,list(row))))


def manage_customer(db:_Connection, cur_user: User) -> None:
    cursor = db.cursor()
    while True:
        print('1. 고객정보 조회 2. 고객정보 변경 3. 고객정보 삭제 0. 뒤로가기')
        menu = int(input('입력 : '))
        if menu == 1:
            # 고객정보 출력
            total_customer_list(db)
                
        elif menu == 2:
            #고객정보 출력 후 변경할 고객번호 선택하기
            total_customer_list(db)

            update_customer_no=int(input("변경할 고객번호 입력해주세요\n"))
            print('어떤 정보를 변경하시겠습니까\n')
            change_attribute = int(input('1. 이름 2. 나이 3. 주소 4. 전화번호'))
            value = input('값을 입력해주세요 : ')
            # 고객 - 이름 수정
            if change_attribute ==1:
                change_name_updateSql = 'update Customer set name = %s where c_no= %s'
                cursor.execute(change_name_updateSql,(value, update_customer_no))
                db.commit()
            # 고객 - 나이 수정
            elif change_attribute == 2:
                change_age_updateSql = 'update Customer set age = %s where c_no= %s'
                cursor.execute(change_age_updateSql,(int(value), update_customer_no))
                db.commit()
            # 고객 - 주소 수정
            elif change_attribute == 3:
                change_addr_updateSql='update Customer set address = %s where c_no=%s'
                cursor.execute(change_addr_updateSql,(value, update_customer_no))
                db.commit()

            # 고객 - 전화번호 수정
            elif change_attribute == 4:
                change_phone_updateSql='update Customer set phone = %s where c_no=%s'
                cursor.execute(change_phone_updateSql,(value, update_customer_no))
                db.commit()

        elif menu == 3:
            # 모든 고객 조회
            total_customer_list(db)

            delete_customer_no = input("삭제할 고객 번호를 입력해주세요(c_no) : ")
            customer_deleteSql = "DELETE FROM Customer WHERE c_no = %s"
            cursor.execute(customer_deleteSql, delete_customer_no)
            db.commit()
            print("해당 차량 정보가 삭제되었습니다")

        elif menu == 0:
            break

        else:
            print('올바른 번호를 입력해주세요')
            continue    


def manage_car(db:_Connection, cur_user: User) -> None:
    cursor = db.cursor()
    while True:
        print('1. 차량조회 2. 차량등록 3. 차량삭제 0. 뒤로가기')
        menu = int(input('입력 : '))
        if menu == 1:
            # 전체 차량 조회
            total_car_list(db)
        elif menu == 2:
            # 새로운 차량 등록
            print('등록할 차량 정보를 입력해주세요')
            print('브랜드, 연식, 모델명, 색상')
            print('입력 예시 : Tesla,2020,ModelX,white')
            user_input = input('입력 : ')
            user_input_lst = user_input.strip().split(',')
            # Car 테이블에 데이터 입력
            sql = "INSERT INTO Car(s_no, brand, year, model, color) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(sql, (cur_user.s_no, user_input_lst[0], user_input_lst[1], user_input_lst[2], user_input_lst[3]))
            db.commit()
            print("해당 차량 정보가 입력되었습니다")            
            
        elif menu == 3:
            # 전체 차량 조회
            total_car_list(db)
            # 차량 삭제
            delete_car_no = int(input("삭제할 차량 번호를 입력해주세요(car_no) : "))
            car_deleteSql = "DELETE FROM Car WHERE car_no = %s"
            cursor.execute(car_deleteSql, (delete_car_no))
            db.commit()
            print("해당 차량 정보가 삭제되었습니다")

        elif menu == 0:
            break

        else:
            print('올바른 번호를 입력해주세요')
            continue


def manage_invoice(db: _Connection) -> None:
    cursor = db.cursor()
    while True:
        print('1. 주문내역 조회 0. 뒤로가기')
        menu = int(input('입력 : '))
        if menu == 1:
            sql = "SELECT * FROM Invoice"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("#" * 45)
            print('주문 번호\t판매자 번호\t고객 번호')
            print("#" * 45)
            for row in cursor.fetchall():
                print('\t'.join(map(str,list(row))))
        elif menu == 0:
            break
        else:
            print('올바른 번호를 입력해주세요.')
            continue


if __name__ == '__main__':
    print('this is salesperson_module')
else:
    pass