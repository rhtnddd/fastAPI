from ch09.db_connect import get_db, engine, Base
import ch09.model.student as student_model
import ch09.model.department as department_model


def run_crud_practice():
    with get_db() as db:
        print("\n--- 1. CREATE (데이터 생성) ---")
        # 부서와 학생 객체를 생성하고 세션에 추가합니다.
        new_dept = department_model.Department(name="인공지능과", personnel=30)
        db.add(new_dept)
        db.commit()  # DB에 확정
        db.refresh(new_dept)  # DB에서 생성된 ID값을 객체로 다시 불러옴

        new_student = student_model.Student(name="김학생", gender=student_model.Gender.MALE, department_id=new_dept.id)
        db.add(new_student)
        db.commit()
        print(f"✅ 학생 추가 완료: {new_student.name} (ID: {new_student.id})")

        print("\n--- 2. READ (데이터 조회) ---")
        # .filter()로 조건 검색, .first()로 단건 조회, .all()로 전체 조회를 합니다.
        target_student = db.query(student_model.Student).filter(student_model.Student.name == "김학생").first()
        print(f"✅ 조회된 학생: {target_student.name}, 소속 학과 ID: {target_student.department_id}")

        print("\n--- 3. UPDATE (데이터 수정) ---")
        # 💡 [핵심] ORM에서는 update() 함수를 쓰지 않습니다! 객체의 속성만 바꾸고 commit()하면 알아서 수정됩니다. (영속성/더티 체킹)
        target_student.name = "이학생"  # 이름 변경
        db.commit()
        print(f"✅ 학생 이름 수정 완료: 김학생 -> {target_student.name}")

        print("\n--- 4. DELETE (데이터 삭제) ---")
        # session.delete()에 삭제할 객체를 통째로 넘겨줍니다.
        db.delete(target_student)
        db.commit()

        # 정말 삭제되었는지 확인
        check_deleted = db.query(student_model.Student).filter(student_model.Student.name == "이학생").first()
        if check_deleted is None:
            print("✅ 학생 데이터가 성공적으로 삭제되었습니다.")


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    run_crud_practice()