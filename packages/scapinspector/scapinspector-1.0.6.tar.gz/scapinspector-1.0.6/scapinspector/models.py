import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey,DateTime ,DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import db

Base = declarative_base()

class Version(Base):
    __tablename__ = 'version'
    id            = Column(Integer, primary_key=True)
    version       = Column(String(255))
    description   = Column(String(255))
    created       = Column(DateTime(timezone=True), default=func.now())

class Results(Base):
    __tablename__ = 'results'
    id            = Column(Integer,primary_key=True)
    server        = Column(String(255))
    group         = Column(String(255))
    profile       = Column(String(255))
    score         = Column(DECIMAL(18,4))
    high          = Column(DECIMAL(18,4))
    medium        = Column(DECIMAL(18,4))
    low           = Column(DECIMAL(18,4))
    unknown       = Column(DECIMAL(18,4))
    scanned       = Column(DateTime(timezone=True), default=func.now())
    

class Benchmark(Base):
    __tablename__ = 'benchmarks'
    id            = Column(Integer, primary_key=True)
    ref_id        = Column(String(255))
    title         = Column(String(2048))
    description   = Column(String(10000))
    file          = Column(String(2048))
    description   = Column(String(2048))
    created       = Column(DateTime(timezone=True), default=func.now())


class Profile(Base):
    __tablename__ = 'profiles'
    id            = Column(Integer, primary_key=True)
    ref_id        = Column(String(255))
    title         = Column(String(2048))
    file          = Column(String(2048))
    description   = Column(String(10000))
    benchmark_id  = Column(Integer, ForeignKey(Benchmark.id))
    benchmark     = relationship(Benchmark)
    created       = Column(DateTime(timezone=True), default=func.now())

class Rule(Base):
    __tablename__ = 'rules'
    id            = Column(Integer, primary_key=True)
    ref_id        = Column(String(255))
    title         = Column(String(2048))
    description   = Column(String(10000))
    created       = Column(DateTime(timezone=True), default=func.now())


class Group(Base):
    __tablename__ = 'groups'
    id            = Column(Integer, primary_key=True)
    ref_id        = Column(String(255))
    title         = Column(String(2048))
    description   = Column(String(10000))
    #rule_id = Column(Integer, ForeignKey(Rule.id))
    #rule=relationship(Rule)
    parent_id     = Column(Integer, ForeignKey('groups.id'))
    parent        = relationship('Group', remote_side=[id])
    benchmark_id  = Column(Integer, ForeignKey(Benchmark.id))
    benchmark     = relationship(Benchmark)
    created       = Column(DateTime(timezone=True), default=func.now())

class Group_Rule(Base):
    __tablename__ = 'group_rule'
    id            = Column(Integer, primary_key=True)
    ref_id        = Column(String(255))
    rule_id = Column(Integer, ForeignKey(Rule.id))
    rule=relationship(Rule)
    parent_id     = Column(Integer, ForeignKey('groups.id'))
    parent        = relationship(Group)
    created       = Column(DateTime(timezone=True), default=func.now())


class Select(Base):
    __tablename__ = 'select'
    id            = Column(Integer, primary_key=True)
    ref_id        = Column(String(255))
    selected      = Column(String(10))
    rule_id       = Column(Integer, ForeignKey(Rule.id))
    rule          = relationship(Rule)
    profile_id    = Column(Integer, ForeignKey(Profile.id))
    profile       = relationship(Profile)
    created       = Column(DateTime(timezone=True), default=func.now())

def get_benchmarks():
    dbc=db.get_db()
    session=dbc['session']
    results=session.query(Benchmark).order_by(Benchmark.id)
    return results

def build(drop=False):
    """Build the tables for the benchmark/xccdf model"""
    conn=db.get_db()
    engine=conn['engine']
    Base.metadata.reflect(engine)
    if True == drop:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
