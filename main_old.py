import csv
import random
import os
from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from faker import Faker

# ==========================================
# 0. МОДЕЛІ ДАНИХ (Діаграма класів з Лаб 1)
# ==========================================
Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    title = Column(String)

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

class InterviewResult(Base):
    __tablename__ = 'interview_results'
    id = Column(Integer, primary_key=True)
    score = Column(Float)
    feedback = Column(String)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    vacancy_id = Column(Integer, ForeignKey('vacancies.id'))

# ==========================================
# 1. РІВЕНЬ ДОСТУПУ ДО ДАНИХ (DAL)
# ==========================================
class IRepository(ABC):
    @abstractmethod
    def read_csv(self, file_path): pass
    
    @abstractmethod
    def save_record(self, v_title, c_name, c_email, score, feedback): pass

class SqlAlchemyRepository(IRepository):
    def __init__(self, session):
        self.session = session

    def read_csv(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def save_record(self, v_title, c_name, c_email, score, feedback):
        # Логіка для коректного збереження (перевірка на існуючі записи)
        vacancy = self.session.query(Vacancy).filter_by(title=v_title).first()
        if not vacancy:
            vacancy = Vacancy(title=v_title)
            self.session.add(vacancy)
            self.session.flush()

        candidate = self.session.query(Candidate).filter_by(email=c_email).first()
        if not candidate:
            candidate = Candidate(name=c_name, email=c_email)
            self.session.add(candidate)
            self.session.flush()

        result = InterviewResult(
            score=float(score), 
            feedback=feedback, 
            candidate_id=candidate.id, 
            vacancy_id=vacancy.id
        )
        self.session.add(result)
        self.session.commit()

# ==========================================
# 2. РІВЕНЬ БІЗНЕС-ЛОГІКИ (BLL)
# ==========================================
class IRecruitingService(ABC):
    @abstractmethod
    def import_data_from_csv(self, file_path): pass

class RecruitingService(IRecruitingService):
    def __init__(self, repository: IRepository):
        # Впровадження залежності (DI) через інтерфейс
        self.repository = repository

    def import_data_from_csv(self, file_path):
        print(f"BLL: Початок обробки файлу {file_path}...")
        raw_rows = self.repository.read_csv(file_path)
        
        for row in raw_rows:
            self.repository.save_record(
                row['vacancy_title'],
                row['candidate_name'],
                row['candidate_email'],
                row['tech_score'],
                row['feedback']
            )
        print(f"BLL: Успішно імпортовано {len(raw_rows)} записів.")

# ==========================================
# 3. ПРЕЗЕНТАЦІЙНИЙ РІВЕНЬ (Тільки інтерфейс)
# ==========================================
class IRecruitingView(ABC):
    @abstractmethod
    def render(self): pass

# ==========================================
# 4. МОДУЛЬ ГЕНЕРАЦІЇ ДАНИХ (CLI)
# ==========================================
class DataGenerator:
    @staticmethod
    def create_csv(filename="data.csv", rows=1000):
        fake = Faker()
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['vacancy_title', 'candidate_name', 'candidate_email', 'tech_score', 'feedback'])
            for _ in range(rows):
                writer.writerow([
                    fake.job(), fake.name(), fake.unique.email(),
                    random.randint(0, 100), fake.sentence()
                ])
        print(f"Генератор: Створено файл {filename} з {rows} рядками.")

# ==========================================
# 5. ТОЧКА ВХОДУ ТА IoC КОНТЕКСТ
# ==========================================
if __name__ == "__main__":
    import sys

    # Команда для генерації: python main.py --generate
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        DataGenerator.create_csv("recruiting_data.csv", 1000)
    else:
        # 1. Ініціалізація БД (DAL)
        engine = create_engine('sqlite:///cornerstone_lab.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db_session = Session()

        # 2. IoC/DI: Збірка шарів
        # Створюємо репозиторій, впроваджуємо сесію БД
        repo = SqlAlchemyRepository(db_session)
        
        # Створюємо сервіс, впроваджуємо репозиторій через інтерфейс
        service = RecruitingService(repository=repo)

        # 3. Запуск процесу
        if os.path.exists("recruiting_data.csv"):
            service.import_data_from_csv("recruiting_data.csv")
        else:
            print("Помилка: Файл 'recruiting_data.csv' не знайдено. Запустіть спочатку з флагом --generate")