

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from database import Base, async_engine, async_session_factory, session_factory, sync_engine
from models import ResumesOrm, WorkersOrm, Workload


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            # worker_jack = WorkersOrm(user_name="Jack")
            # worker_michael = WorkersOrm(user_name="Michael")
            # worker_kamila = WorkersOrm(user_name="Kamila")
            # worker_alice = WorkersOrm(user_name="Alice")
            # worker_anton = WorkersOrm(user_name="Anton")
            worker_anna = WorkersOrm(user_name="Anna")
            worker_peter = WorkersOrm(user_name="Peter")
            worker_carl = WorkersOrm(user_name="Carl")
            session.add_all([worker_anna, worker_peter, worker_carl])
            # flush отправляет запрос в базу данных
            # После flush каждый из работников получает первичный ключ id, который отдала БД
            session.flush()
            session.commit()



    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            # print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkersOrm, worker_id)
            worker_michael.user_name = new_username
            session.commit()

    @staticmethod
    def delete_worker():
        with session_factory() as session:
            id_3 = session.query(WorkersOrm).get(7)
            session.delete(id_3)
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = ResumesOrm(
                title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)
            resume_jack_2 = ResumesOrm(
                title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
            resume_michael_1 = ResumesOrm(
                title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
            resume_michael_2 = ResumesOrm(
                title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2,
                             resume_michael_1, resume_michael_2])
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = session.execute(query)
            result = result.all()
            print(result)

    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
            )
            res = session.execute(query)
            result = res.scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)
            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_with_joined_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_with_selectin_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)







class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_workers():
        async with async_session_factory() as session:
            worker_jack = WorkersOrm(username="Jack")
            worker_michael = WorkersOrm(username="Michael")
            session.add_all([worker_jack, worker_michael])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_workers():
        async with async_session_factory() as session:
            query = select(WorkersOrm)
            result = await session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    async def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        async with async_session_factory() as session:
            worker_michael = await session.get(WorkersOrm, worker_id)
            worker_michael.username = new_username
            await session.refresh(worker_michael)
            await session.commit()

    @staticmethod
    async def insert_resumes():
        async with async_session_factory() as session:
            resume_jack_1 = ResumesOrm(
                title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)
            resume_jack_2 = ResumesOrm(
                title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
            resume_michael_1 = ResumesOrm(
                title="Python Data Engineer", compensation=250000, workload=Workload.parttime, worker_id=2)
            resume_michael_2 = ResumesOrm(
                title="Data Scientist", compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2,
                             resume_michael_1, resume_michael_2])
            await session.commit()

    @staticmethod
    async def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        async with async_session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    # 1 вариант использования cast
                    # cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                    # 2 вариант использования cast (предпочтительный способ)
                    func.avg(ResumesOrm.compensation).cast(Integer).label("avg_compensation"),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(func.avg(ResumesOrm.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)

    @staticmethod
    async def insert_additional_resumes():
        async with async_session_factory() as session:
            resumes = [
                {"title": "Python Senior Dev", "compensation": 600000, "workload": "fulltime", "worker_id": 8},
                {"title": "Machine Learning Engineer", "compensation": 200000, "workload": "parttime", "worker_id": 9},
                {"title": "Python Data Scientists", "compensation": 100000, "workload": "parttime", "worker_id": 10},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 11},
                {"title": "Python Junior Dev", "compensation": 40000, "workload": "fulltime", "worker_id": 12},
                {"title": "Python middle Dev", "compensation": 300000, "workload": "fulltime", "worker_id": 13},

            ]
            insert_resumes = insert(ResumesOrm).values(resumes)
            await session.execute(insert_resumes)
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func():
        """
        WITH helper2 AS (
            SELECT *, compensation-avg_workload_compensation AS compensation_diff
            FROM
            (SELECT
                w.id,
                w.username,
                r.compensation,
                r.workload,
                avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
            FROM resumes r
            JOIN workers w ON r.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC;
        """
        async with async_session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label(
                        "avg_workload_compensation"),
                )
                # .select_from(r)
                .join(r, r.worker_id == w.id).subquery("helper1")
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.user_name,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
                )
                .cte("helper2")
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )

            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.all()
            print(f"{len(result)=}. {result=}")

