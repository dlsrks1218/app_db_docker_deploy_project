# 로그인 모듈
import pymysql as pm
from typing import Callable, Tuple
from pymysql.connections import Connection as _Connection


# 등록 혹은 로그인 후 현재 사용자 인지를 위해 클래스를 생성
class User:
    def __init__(self, c_no, s_no, name, id):
        self.c_no = c_no
        self.s_no = s_no
        self.name = name
        self.id = id
    
    def logout(self):
        self.c_no = 0
        self.s_no = 0
        self.name = ''
        self.id = ''
        print('로그아웃 되었습니다.')
        return self

    def show(self):
        cur_state = ''
        if self.c_no == 0 and self.s_no == 1:
            cur_state = '판매자'
        elif self.s_no == 0 and self.c_no == 1:
            cur_state = '고객'
        print(
            """
어서오세요.
현재 접속중인 {}의 정보입니다.
이름 : {}
ID : {}
            """.format(cur_state, self.name, self.id)
        )


def get_connect(hostname: str, db_name: str) -> _Connection:
    """mysql db Connection 객체를 반환

    Args:
        hostname(str): host name
        db_name (str): database name

    Returns:
        _Connection: Callable[..., _Connection]
    """
    db = pm.connect(host=hostname, port=3306, user='root', db=db_name, charset='utf8')
    return db


def check_value(id_or_pw: str, id_or_pw_flag: int, db: _Connection) -> int:
    cursor = db.cursor()
    value = ''
    if id_or_pw_flag == 0:
        value = 'id'
        selectSql = 'select * from Account where id=%s'
    elif id_or_pw_flag == 1:
        value = 'pw'
        selectSql = 'select * from Account where pw=%s'
    cursor.execute(selectSql, (id_or_pw))
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    elif len(result) == 1:
        return 1
    else:
        if value == 'pw':
            return 1
        else:
            print('중복된 id가 존재합니다')
            return -1
    

def check_customer_or_salesperson(id: str, db: _Connection) -> int:
    cursor = db.cursor()
    selectSql = 'select c_no, s_no from Account where id=%s'
    cursor.execute(selectSql, (id))
    result = cursor.fetchone()
    # Customer
    if result[0] == 1:
        return 0
    # Salesperson
    elif result[1] == 1:
        return 1
    # db.close()


def sign_in(db: _Connection, cur_user: User) -> User:
    # c_no, ticket_cnt, name, age, address, phone, id_no, id
    cursor = db.cursor()
    while True:
        id = input('아이디를 입력해주세요 : ')
        if check_value(id, 0, db) == 1:
            pw_try_cnt = 0
            while True:
                if pw_try_cnt > 2:
                    print('{}회 틀리셨습니다. 프로그램을 종료합니다'.format(pw_try_cnt))
                    exit()
                pw = input('비밀번호를 입력해주세요 : ')
                if check_value(pw, 1, db) == 1:
                    if check_customer_or_salesperson(id, db) == 0:
                        customer_selectSql = 'select * from Customer c, Account a where a.id=%s and a.pw=%s and c.c_no=a.c_no'
                        cursor.execute(customer_selectSql, (id, pw))
                        result = cursor.fetchone()
                        cur_user.c_no = result[0]
                        cur_user.name = result[2]
                        cur_user.id = id
                        # cur_user = User(result[0][0], 0, result[0][2], id)
                        return cur_user
                    elif check_customer_or_salesperson(id, db) == 1:
                        sales_person_selectSql = 'select * from Salesperson s, Account a where a.id=%s and a.pw=%s and s.s_no=a.s_no'
                        cursor.execute(sales_person_selectSql, (id, pw))
                        result = cursor.fetchone()
                        cur_user.s_no = result[0]
                        cur_user.name = result[1]
                        cur_user.id = id
                        # cur_user = User(0, result[0][0], result[0][1], id)
                        return cur_user
                else:
                    print('비밀번호가 틀렸습니다(3회 실패시 종료)')
                    pw_try_cnt += 1
                    continue
        else:
            print('해당하는 정보가 없습니다')
            menu =int(input(('1. 정보를 다시 입력하시겠습니까?\n2. 회원 가입을 하시겠습니까?\n0. 뒤로가기')))
            if menu == 1:
                continue
            elif menu == 2:
                return cur_user
            elif menu == 0:
                break


def sign_up(db: _Connection, cur_user: User) -> User:
    cursor = db.cursor()
    while True:
        menu = int(input('1. 고객으로 등록\n2. 판매자로 등록\n0. 뒤로가기'))
        if menu == 0:
            break
        while True:
            print('ID(최대 20자), PW(최대 20자)을 입력해주세요\n예시 : dlsrks1218,dlsrks123')
            id_pw_input = input('입력 : ')
            id_pw_input_lst = id_pw_input.strip().split(',')
            if check_value(id_pw_input_lst[0], 0, db) == 0:
                # 고객으로 등록
                if menu == 1:
                    print('고객님의 정보를 입력해주세요.')
                    print('이름, 나이, 주소, 전화번호, 주민번호\n입력 형식은 다음과 같습니다.')
                    print('예시 : 임종현,22,서울시 용산구,010-4554-1234,991212-1692212')
                    user_input = input('입력 : ')
                    user_input_lst = user_input.strip().split(',')
                    customer_insertSql = 'insert into Customer(ticket_cnt, name, age, address, phone, id_no) values(0, %s, %s, %s, %s, %s)'
                    cursor.execute(customer_insertSql, (user_input_lst[0], user_input_lst[1], user_input_lst[2], user_input_lst[3], user_input_lst[4]))
                    db.commit()
                    customer_no_selectSql = 'select c_no from Customer where name=%s'
                    cursor.execute(customer_no_selectSql, user_input_lst[0])
                    customer_no = cursor.fetchone()[0]
                    customer_id_insertSql = 'insert into Account(id, pw, c_no) values(%s, %s, %s)'
                    cursor.execute(customer_id_insertSql, (id_pw_input_lst[0], id_pw_input_lst[1], customer_no))
                    db.commit()
                    print('회원 가입이 완료되었습니다.')
                    # 회원가입 후 바로 로그인됨
                    cur_user.c_no = customer_no
                    cur_user.name = user_input_lst[0]
                    cur_user.id = id_pw_input_lst[0]
                    return cur_user
                # 판매자로 등록
                elif menu == 2:
                    sales_person_name = input('이름을 입력해주세요 : ')
                    sales_person_insertSql = 'insert into Salesperson(name) values(%s)'
                    cursor.execute(sales_person_insertSql, sales_person_name)
                    db.commit()
                    sales_person_no_selectSql = 'select s_no from Salesperson where name=%s'
                    cursor.execute(sales_person_no_selectSql, sales_person_name)
                    sales_person_no = cursor.fetchone()[0]
                    sales_person_id_insertSql = 'insert into Account(id, pw, s_no) values(%s, %s, %s)'
                    cursor.execute(sales_person_id_insertSql, (id_pw_input_lst[0], id_pw_input_lst[1], sales_person_no))
                    db.commit()
                    print('회원 가입이 완료되었습니다.')
                    cur_user.s_no = sales_person_no
                    cur_user.name = sales_person_name
                    cur_user.id = id_pw_input_lst[0]
                    return cur_user
            # 데이터 이미 존재하며, 1. 틀렸거나(잘못썼거나), 2.현 사용자가 회원가입이 안되있을 시
            # -> 회원가입 실패 시 이전 화면으로 돌려주거나 다시 입력하거나
            else:
                print('이미 {}에 해당하는 아이디가 존재합니다'.format(id_pw_input_lst[0]))
                print('1. 정보를 다시 입력하시겠습니까?\n0. 뒤로가기')
                menu = int(input('입력 : '))
                if menu == 1:
                    continue
                elif menu == 0:
                    return cur_user


if __name__ == '__main__':
    print('this is user_init')
else:
    pass