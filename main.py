from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List

# DATABASE CONFIGURATION

DATABASE_URL = "sqlite:///./benchmarks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# DATABASE MODEL

class DBBenchmark(Base):

    __tablename__ = "benchmarks"

    id = Column(Integer, primary_key=True, index=True)

    benchmark_name = Column(
        String,
        nullable=False
    )

    platform = Column(
        String,
        nullable=False
    )

    score = Column(
        Integer,
        nullable=False
    )

    cv_percent = Column(
        Float,
        nullable=False
    )


Base.metadata.create_all(bind=engine)


# PYDANTIC SCHEMAS

class BenchmarkBase(BaseModel):

    benchmark_name: str

    platform: str

    score: int

    cv_percent: float


class BenchmarkCreate(BenchmarkBase):
    pass


class BenchmarkUpdate(BenchmarkBase):
    pass


class BenchmarkResponse(BenchmarkBase):

    id: int

    class Config:

        from_attributes = True


# DATABASE SESSION

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# FASTAPI APP

app = FastAPI(
    title="Benchmark Results API"
)


# CREATE

@app.post(
    "/benchmarks/",
    response_model=BenchmarkResponse,
    status_code=201
)
def create_benchmark(
    benchmark: BenchmarkCreate,
    db: Session = Depends(get_db)
):

    db_benchmark = DBBenchmark(
        benchmark_name=benchmark.benchmark_name,
        platform=benchmark.platform,
        score=benchmark.score,
        cv_percent=benchmark.cv_percent
    )

    db.add(db_benchmark)

    db.commit()

    db.refresh(db_benchmark)

    return db_benchmark


# READ ALL

@app.get(
    "/benchmarks/",
    response_model=List[BenchmarkResponse]
)
def read_benchmarks(
    db: Session = Depends(get_db)
):

    return db.query(DBBenchmark).all()


# READ ONE

@app.get(
    "/benchmarks/{benchmark_id}",
    response_model=BenchmarkResponse
)
def read_benchmark(
    benchmark_id: int,
    db: Session = Depends(get_db)
):

    benchmark = (
        db.query(DBBenchmark)
        .filter(DBBenchmark.id == benchmark_id)
        .first()
    )

    if benchmark is None:

        raise HTTPException(
            status_code=404,
            detail="Benchmark not found"
        )

    return benchmark


# UPDATE

@app.put(
    "/benchmarks/{benchmark_id}",
    response_model=BenchmarkResponse
)
def update_benchmark(
    benchmark_id: int,
    updated: BenchmarkUpdate,
    db: Session = Depends(get_db)
):

    benchmark = (
        db.query(DBBenchmark)
        .filter(DBBenchmark.id == benchmark_id)
        .first()
    )

    if benchmark is None:

        raise HTTPException(
            status_code=404,
            detail="Benchmark not found"
        )

    benchmark.benchmark_name = updated.benchmark_name
    benchmark.platform = updated.platform
    benchmark.score = updated.score
    benchmark.cv_percent = updated.cv_percent

    db.commit()

    db.refresh(benchmark)

    return benchmark


# DELETE

@app.delete(
    "/benchmarks/{benchmark_id}",
    status_code=204
)
def delete_benchmark(
    benchmark_id: int,
    db: Session = Depends(get_db)
):

    benchmark = (
        db.query(DBBenchmark)
        .filter(DBBenchmark.id == benchmark_id)
        .first()
    )

    if benchmark is None:

        raise HTTPException(
            status_code=404,
            detail="Benchmark not found"
        )

    db.delete(benchmark)

    db.commit()

    return None 