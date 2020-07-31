from user_init import User
from typing import Callable, Tuple
from pymysql.connections import Connection as _Connection
from datetime import date

#1.차량 목록 확인(판패가능 차량만)
def available_car_list(db:_Connection) -> None:
    cursor = db.cursor()
    print("#" * 50)
    print('차량번호\t브랜드\t연식\t모델\t 색상')
    print("#" * 50)
    show_tb = 'select car_no, brand, year, model, color from Car where c_no IS NULL'
    rows = cursor.execute(show_tb)
    for row in cursor.fetchall():
        print('\t'.join(map(str,list(row))))


#2. 차량 구매
def buy_car(db: _Connection, cur_user: User) -> bool:
    cursor = db.cursor()
    while True:
        # 구매 가능 차량 목록 보여주기
        available_car_list(db)
        # 구매할 차량 선택하기
        try:
            print("구입할 차량의 번호 선택, 0. 뒤로가기")
            car_num=int(input('입력 : '))
            if car_num == 0:
                return False
            choice = input(str(car_num)+" 번을 구매하시겠습니까 (y/n) : ")
            if choice =='y':
                print("멋진 차 구매 성공!! 좋은 하루 보내세요")
                # 구매 전의 차량은 고객 번호가 매칭 되어 있지 않고 판매자 번호만 매칭 된 상태이므로
                # 구매 후 차량은 고객 번호를 매칭 해줌
                buy_car_updateSql="update Car set c_no = %s where car_no = %s"
                cursor.execute(buy_car_updateSql,(cur_user.c_no, car_num))
                db.commit()
                
                # 해당 차량의 판매자 번호를 가져오기
                car_sno_selectSql="select s_no from Car where car_no=%s"
                cursor.execute(car_sno_selectSql, car_num)
                car_sno = cursor.fetchone()[0]

                #Invoice 테이블에 현재 user의 c_no와 팔린 차의 s_no를 넣어줘.        
                invoice_insertSql="insert into Invoice(s_no,c_no) values(%s, %s)"
                cursor.execute(invoice_insertSql, (car_sno, cur_user.c_no))
                db.commit()
                
            else:
                print("구매를 취소하셨습니다")
                return False
        except Exception as e:
            print('잘못된 입력입니다')
            continue


def cal_july() -> list:
    # 프로그램에서 가정하는 상황 : 7월 한달 동안 서비스 신청 가능
    year_month = '2020-07-'
    days = [_ for _ in range(1, 32)]
    july = []
    # mysql의 날짜 데이터는 DATE 형식이며 %Y-%m-%d의 출력 형태를 맞춰주기 위해
    for day in days:
        tmp = str(day)
        if day > 0 and day < 10:
            tmp = '0' + tmp
        july.append(year_month + tmp)

    return july


# 3. 서비스 신청
def get_parts(db: _Connection) -> Tuple:
    cursor = db.cursor()
    while True:
        print('어떤 부품을 수리할지 선택하세요 \n1. Handle 2. Wheel 3. Door 0. 뒤로가기')
        parts_select = int(input('입력 : '))
        if parts_select == 0:
            return None
        part = 'select * from Parts where p_no=%s'
        cursor.execute(part,parts_select)
        parts=cursor.fetchall()
        p_num=int(parts[0][0])
        p_name=parts[0][1]
        p_count=int(parts[0][2])
        
        # 부품의 갯수가 0보다 크면 수리 가능하며 선택 시 
        # 사용했다고 간주하여 존재하는 부품 수를 하나 줄임
        if p_count > 0:
            p_cnt_minus_updateSql='update Parts SET p_cnt=p_cnt-1 where p_no=%s'
            cursor.execute(p_cnt_minus_updateSql,parts_select)
            db.commit()
            print("수리가 가능합니다")
            parts_result_tuple = (p_num, p_name, p_count)
            return parts_result_tuple
        else:
            print("수리 불가능합니다. 죄송합니다")
            return None


def get_available_mechanic_and_work_date(db: _Connection, cur_user: User) -> Tuple:
    cursor = db.cursor()

    # 7월 한달 데이터에 대해 조회한다
    july = cal_july()

    # 모든 정비사 조회
    mno_lst = []
    mno_selectSql='select distinct m_no from Work'
    rows=cursor.execute(mno_selectSql)
    result = cursor.fetchall()
    for row in result:
        mno_lst.append(row[0])

    mno_available_date = dict()
    # 정비사 별로 모든 데이터를 가져와서 그 중 날짜를 가져옴
    # 7월 달 모든 날짜에서 정비사 별로 가져온 작업이 잡힌 날짜를 빼면
    # 정비사 별로 작업 가능한 날짜를 보여주고 고객에게 선택시킴
    for mno in mno_lst:
        work_selectSql='select * from Work where m_no=%s'
        rows=cursor.execute(work_selectSql, (mno))
        tmp_work_date_lst = []
        for row in cursor.fetchall():
            for idx, item in enumerate(list(row)):
                if idx == 2:
                    tmp_work_date_lst.append(str(item))
        tmp_available_date_lst = set(july.copy()) - set(tmp_work_date_lst)
        mno_available_date[mno] = sorted(list(tmp_available_date_lst))

    for key, val in mno_available_date.items():
        print('정비사 {}번의 작업 가능 날짜는 다음과 같습니다'.format(key))
        for item in val:
            print('<{}>'.format(item), end = ' ')
        print()
    
    print('수리받고자 하는 정비사 번호와 해당하는 정비사에 대한 작업 가능 날짜를 선택해주세요')
    print('입력 예시 : 1,2020-07-02')
    m_no_work_date_list = input().strip().split(',')
    
    m_no = int(m_no_work_date_list[0])
    work_date = m_no_work_date_list[1]

    print('작업 신청 내역')
    print('정비사 번호 : {} / 작업 예정 날짜 : {}'.format(m_no, work_date))
    year_month_day_list = work_date.split('-')
    year_month_day_list = list(map(int, year_month_day_list))
    work_date = date(year_month_day_list[0], year_month_day_list[1], year_month_day_list[2])    
    m_no_work_date_result_tuple = (m_no, work_date)

    return m_no_work_date_result_tuple    


def insert_service_and_work(db: _Connection, cur_user: User, parts_result_tuple: Tuple, m_no_work_date_result_tuple: Tuple) -> None:
    cursor = db.cursor()
    
    # 수리 서비스 테이블에 작업 내역을 저장
    m_no = m_no_work_date_result_tuple[0]
    work_date = m_no_work_date_result_tuple[1]
    p_no = parts_result_tuple[0]
    p_name = parts_result_tuple[1]
    p_cnt = parts_result_tuple[2]
    his=str(cur_user.c_no) + '/' + p_name + '/'+ str(work_date)
    his_sql='insert into `Repair-or-Service`(history,c_no,p_no) values(%s,%s,%s)' 
    cursor.execute(his_sql,(his,cur_user.c_no,p_no))
    db.commit()

    # 작업 테이블에 내역 저장 후 작업 신청 완료
    work_sql='select service_no from `Repair-or-Service` where history=%s'
    cursor.execute(work_sql,his) 
    serv_no=cursor.fetchone()[0]
    work_inser_sql='insert into Work values(%s,%s,%s)'
    cursor.execute(work_inser_sql,(serv_no,m_no,work_date))
    db.commit()
    print('서비스 신청이 완료 되었습니다.')


if __name__ == '__main__':
    print('this is customer_module')
else:
    pass