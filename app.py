from datetime import date
from unicodedata import name
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.student).all()

@router_v1.get('/students/{student_id}')
async def get_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.student).filter(models.student.id == student_id).first()

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newstudent = models.student(name=student['name'], sername=student['sername'], id=student['id'], date=student['date'], gender=student['gender'])
    db.add(newstudent)
    db.commit()
    db.refresh(newstudent)
    response.status_code = 201
    return newstudent

@router_v1.put('/students/{student_id}')
async def update_student(student_id: int, student: dict, response: Response, db: Session = Depends(get_db)):
    try:
        db_student = db.query(models.student).filter(models.student.id == student_id).first()
        if db_student:
            db_student.name = student.get('name', db_student.name)
            db_student.sername = student.get('sername', db_student.sername)
            db_student.date = student.get('date', db_student.date)
            db_student.gender = student.get('gender', db_student.gender)

            db.commit()
            db.refresh(db_student)
            return db_student
        else:
            response.status_code = 404
            return {'message': f'Student with ID {student_id} not found'}
    except Exception as e:
        response.status_code = 500
        return {'message': f'Internal Server Error: {str(e)}'}
    
@router_v1.delete('/students/{student_id}')
async def delete_student(student_id: int, response: Response, db: Session = Depends(get_db)):
    try:
        db_student = db.query(models.student).filter(models.student.id == student_id).first()
        if db_student:
            db.delete(db_student)
            db.commit()
            return {'message': f'Student with ID {student_id} deleted successfully'}
        else:
            response.status_code = 404
            return {'message': f'Student with ID {student_id} not found'}
    except Exception as e:
        response.status_code = 500
        return {'message': f'Internal Server Error: {str(e)}'}
    
# @router_v1.patch('/students/{student_id}')
# async def update_student(student_id: int, student: dict, db: Session = Depends(get_db)):
#     pass

# @router_v1.delete('/students/{student_id}')
# async def delete_student(student_id: int, db: Session = Depends(get_db)):
#     pass

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
