import asyncio
import os
import sys

from queries.orm import SyncORM, AsyncORM
# from queries.core import SyncCore, AsyncCore
sys.path.insert(1, os.path.join(sys.path[0], '..'))

#
# SyncCore.create_tables()
# SyncCore.insert_workers()
# SyncCore.select_workers()
# SyncCore.update_worker()
# SyncCore.insert_resumes()
# SyncCore.select_resumes_avg_compensation()
# SyncCore.insert_additional_resumes()
# SyncCore.join_cte_subquery_window_func()


# ORM
# SyncORM.create_tables()
# SyncORM.insert_workers()
# SyncORM.select_workers()
# SyncORM.update_worker()
# SyncORM.insert_resumes()
# SyncORM.select_resumes_avg_compensation()
# SyncORM.insert_additional_resumes()
# SyncORM.join_cte_subquery_window_func()
# SyncORM.select_workers_with_lazy_relationship()
# SyncORM.select_workers_with_joined_relationship()
# SyncORM.select_workers_with_selectin_relationship()
# SyncORM.select_workers_with_condition_relationship()
# SyncORM.select_workers_with_condition_relationship_contains_eager()
# SyncORM.select_workers_with_relationship_contains_eager_with_limit()
# SyncORM.convert_workers_to_dto()
# SyncORM.add_vacancies_and_replies()
# SyncORM.select_resumes_with_all_relationships()

# ========== ASYNC ==========
# CORE
# await AsyncCore.create_tables()
# await AsyncCore.insert_workers()
# await AsyncCore.select_workers()
# await AsyncCore.update_worker()
# await AsyncCore.insert_resumes()
# await AsyncCore.select_resumes_avg_compensation()
# await AsyncCore.insert_additional_resumes()
# await AsyncCore.join_cte_subquery_window_func()

# ORM
async def main():
    # await AsyncORM.create_tables()
    # await AsyncORM.insert_workers()
    # await AsyncORM.select_workers()
    # await AsyncORM.update_worker()
    # await AsyncORM.insert_resumes()
    # await AsyncORM.select_resumes_avg_compensation()
    # await AsyncORM.insert_additional_resumes()
    # await AsyncORM.join_cte_subquery_window_func()
    # await AsyncORM.select_workers_with_lazy_relationship()
    # await AsyncORM.select_workers_with_joined_relationship()
    await AsyncORM.select_workers_with_selectin_relationship()
    # await AsyncORM.select_workers_with_condition_relationship()
    # await AsyncORM.select_workers_with_condition_relationship_contains_eager()
    # await AsyncORM.select_workers_with_relationship_contains_eager_with_limit()
    # await AsyncORM.convert_workers_to_dto()
    # await AsyncORM.add_vacancies_and_replies()
    # await AsyncORM.select_resumes_with_all_relationships()

if __name__ == "__main__":
    asyncio.run(main())
