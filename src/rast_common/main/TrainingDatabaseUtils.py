from datetime import datetime
from typing import Tuple
from pandas import DataFrame

from .TrainingDatabase import read_training_data_from_db_between_using_sqlalchemy, \
    read_all_training_data_from_db_using_sqlalchemy


def read_all_performance_metrics_from_db(db_path: str, begin_end: Tuple[str, str] = ()) -> Tuple[DataFrame, dict]:
    """
    Example call:

    `read_all_performance_metrics_from_db(r"db/trainingdata_2021-04-06.db", ("2021 03 30", "2021 04 05"))`
    :param db_path: Path to SQLite database file
    :param begin_end: Optional tuple to filter within the specified begin and end datetime.
    :return: DataFrame with performance metrics
    and dictionary with the request types mapping created using ordinal encoding
    """

    known_request_types = {}

    begin = datetime.now()

    if len(begin_end) > 0:
        training_data = read_training_data_from_db_between_using_sqlalchemy(db_path, begin_end[0], begin_end[1])
    else:
        training_data = read_all_training_data_from_db_using_sqlalchemy(db_path)

    def gen_rows():
        for row in training_data:
            time_stamp = row.timestamp

            weekday = time_stamp.weekday()

            # we are only interested in the time of day, not the date
            # time = time_stamp.timetz()
            # milliseconds = time.microsecond / 1000000
            # time_of_day_in_seconds = milliseconds + time.second + time.minute * 60 + time.hour * 3600
            # time_of_request = time_of_day_in_seconds

            time_of_request = time_stamp.timestamp()

            request_type = row.request_type

            if request_type not in known_request_types:
                known_request_types[request_type] = len(known_request_types)

            request_type_as_int = known_request_types[request_type]

            new_obj = (
                time_of_request,
                weekday,
                row.number_of_parallel_requests_start,
                row.number_of_parallel_requests_end,
                row.number_of_parallel_requests_finished,
                request_type_as_int,
                float(row.system_cpu_usage),
                row.requests_per_second,
                row.requests_per_minute,
                row.switch_id,
                row.bytes_per_second_transmitted_through_switch,
                row.packets_per_second_transmitted_through_switch,
                float(row.request_execution_time_ms) / 1000,
            )

            yield new_obj

    df = DataFrame.from_records(
        gen_rows(),
        columns=[
            'Timestamp',
            'WeekDay',
            'PR 1',
            'PR 2',
            'PR 3',
            'Request Type',
            'CPU (System)',
            'RPS',
            'RPM',
            "Switch ID",
            "BPS transmitted",
            "PPS transmitted",
            'Response Time s'
        ]
    )

    print(f"read_all_performance_metrics_from_db finished in {(datetime.now() - begin).total_seconds()} s")

    # print("== " + path + "==")
    # print(df.describe())
    # print("Number of response time outliers: %i" % len(detect_response_time_outliers(df)))

    return df, known_request_types
