import argparse
import csv
from collections import defaultdict
from datetime import datetime


def main():
    """
    1. Найти самый ветреный месяц - (месяц и средняя скорость ветра)
    2. Найти самый холодный месяц - (месяц и средняя температура)
    3. Найти самый холодный день - (день и средняя температура)
    4. Найти самый тёплый месяц - (месяц и средняя температура)
    5. Найти самый тёплый день - (день и средняя температура)
    6. Найти самую дождливую неделю - (период и количество осадков)

    """
    parser = argparse.ArgumentParser(description="Weather analytics")
    parser.add_argument('input_filename', help="input csv file name")
    args = parser.parse_args()
    input_filename = args.input_filename

    days_in_year = defaultdict(set)

    wind_sum_by_days = defaultdict(float)   # sum of measurements in day to calculate day-average value
    wind_avg_by_days = defaultdict(float)   # day-average wind
    wind_measure_by_days = defaultdict(int) # num of measurements in day

    temp_sum_by_days = defaultdict(float)
    temp_avg_by_days = defaultdict(float)
    temp_measure_by_days = defaultdict(int)

    rain_by_days = defaultdict(float)
    weeks = defaultdict(set)
    rain_by_weeks = defaultdict(int)
    measure_prev = None
    prev_measure_time = None

    with open(input_filename, mode='r', encoding='utf-8-sig') as csv_file:
        i = 1


        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if i <= 7:
                i += 1
                continue

            daytime = row[0]
            year = daytime[6:10]
            month = daytime[3:10]
            day = daytime[:10]

            days_in_year[year].add(daytime[:10])

            try:
                wind = float(row[7])
                wind_measure_by_days[day] += 1
            except:
                wind = 0
            wind_sum_by_days[day] += wind

            try:
                temp = float(row[1])
                temp_measure_by_days[day] += 1
            except:
                temp = 0
            temp_sum_by_days[day] += temp

            # rain
            measure = row[24]
            try:
                measure_int = int(measure)
            except:
                measure_int = None
            day_form = datetime.strptime(daytime, '%d.%m.%Y %H:%M')
            if measure_prev and prev_measure_time and measure != '' and row[23] != '':

                seconds = (day_form  - prev_measure_time).total_seconds()
                hours = seconds / 3600
                if hours <= 6:
                    if measure_int > measure_prev:
                        if row[23] == 'Следы осадков':
                            rain = 0.1*0.1
                        else:
                            try:
                                rain = float(row[23])
                            except:
                                rain = 0

                        rain_by_days[day] += rain
                        week = day_form.isocalendar()[1]
                        weeks[week].add(day)
            if measure_int:
                measure_prev = measure_int
                prev_measure_time = day_form




    #print(rain_by_days)

    wind_months = defaultdict(float)
    wind_days = defaultdict(int)
    for day, sum_wind in wind_sum_by_days.items():
        wind_avg_by_days[day] = sum_wind / wind_measure_by_days[day]
        month = day[3:]
        wind_months[month] += sum_wind / wind_measure_by_days[day]
        wind_days[month] += 1

    temp_months = defaultdict(float)
    temp_days = defaultdict(int)
    for day, sum_temp in temp_sum_by_days.items():
        temp_avg_by_days[day] = sum_temp / temp_measure_by_days[day]
        month = day[3:]
        temp_months[month] += sum_temp / temp_measure_by_days[day]
        temp_days[month] += 1


    for day,rain in rain_by_days.items():
        day_form = datetime.strptime(day, '%d.%m.%Y')
        week = day_form.isocalendar()[1]
        rain_by_weeks[week] += rain




    for year, days in days_in_year.items():
        if len(days) < 355:
            print(f'Year {year}: not enough data')
        else:
            print(f'Year {year}:')

            """ Most windy month
            """
            for month, sumwind in wind_months.items():
                wind_months[month] = wind_months[month] / wind_days[month]

            max_wind = -1
            max_wind_month = None
            for month, sumwind in wind_months.items():
                if month[3:] == year:
                    if sumwind > max_wind:
                        max_wind = sumwind
                        max_wind_month = month
            print(f'Most windy month: 01.{max_wind_month} ({round(max_wind ,1)})')

            """ Finding hottests and coldests
                day
                 """
            max_d_temp = float("-inf")
            max_temp_date = None
            min_d_temp = float("inf")
            min_temp_date = None
            for day, sumtemp in temp_avg_by_days.items():
                if sumtemp > max_d_temp:
                    max_d_temp = sumtemp
                    max_temp_date = day
                if sumtemp < min_d_temp:
                    min_d_temp = sumtemp
                    min_temp_date = day

            """ Finding hottests and coldests
                month
                """
            for month, sumtemp in temp_months.items():
                temp_months[month] = temp_months[month] / temp_days[month]
            max_temp = float("-inf")
            max_temp_month = None
            min_temp = float("inf")
            min_temp_month = None
            for month, sumtemp in temp_months.items():
                if month[3:] == year:
                    if sumtemp > max_temp:
                        max_temp = sumtemp
                        max_temp_month = month
                    if sumtemp < min_temp:
                        min_temp = sumtemp
                        min_temp_month = month

            print(f'Coldest month: 01.{min_temp_month} ({round(min_temp,1)})')
            print(f'Coldest day: {min_temp_date} ({round(min_d_temp,1)})')
            print(f'Hottest month: 01.{max_temp_month} ({round(max_temp,1)})')
            print(f'Hottest day: {max_temp_date} ({round(max_d_temp,1)})')

            """ Most rainy week
            """
            maxweek = None
            maxrain = -1
            for week, sumrain in rain_by_weeks.items():
                if sumrain > maxrain:
                    maxrain = sumrain
                    maxweek = week
            d = year+'-W' +str(maxweek)
            r = datetime.strptime(d + '-1', "%Y-W%W-%w")
            print(f'Most rainy week: {r} ({round(maxrain, 1)})')


if __name__ == '__main__':
    main()

