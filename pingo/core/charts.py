# https://towardsdatascience.com/django-pandas-and-chart-js-for-a-quick-dashboard-e261bce38bee
import random
import io
from dataclasses import dataclass, field
from typing import List
import pandas as pd
from django_pandas.io import read_frame
import numpy as np
import logging
from django.db.models import F
from palettable.lightbartlein.diverging import BlueDarkRed12_6 as palette
import csv
from io import StringIO
import json

logger = logging.getLogger("error_logger")

csv_settings = {
    'delimiter': ',',
    'doublequote': True,
    'lineterminator': '\r\n',
    'quotechar': '"',
    'skipinitialspace': True,
    'quoting': csv.QUOTE_MINIMAL,
    'strict': True
}


def filter_objects(model, fields=None, exclude=None, foreign_info=None, **kwargs):
    if not fields:
        fields = [field.name for field in model._meta.get_fields()]

    if exclude:
        fields = [field for field in fields if field not in exclude]

    print(kwargs)
    if foreign_info:
        foreign_key = foreign_info[0]
        foreign_name = foreign_info[1]
        if kwargs is not None:
            records = model.objects.filter(**kwargs).values_list(*fields).annotate(foreign_key=F(foreign_name))
        else:
            records = model.objects.all().values_list(*fields).annotate(foreign_key=F(foreign_name))
        fields.append(foreign_key)
    else:
        if kwargs is not None:
            records = model.objects.filter(**kwargs).values_list(*fields)
        else:
            records = model.objects.all()

    return records


# https://towardsdatascience.com/django-pandas-and-chart-js-for-a-quick-dashboard-e261bce38bee
def objects_to_df(qs, fields=None, date_cols=None):
    # records = filter_objects(model, fields, exclude, foreign_info, **kwargs)

    df = pd.DataFrame(list(qs), columns=fields)
    print(df)
    print("objects_to_df")
    if date_cols:
        strftime = date_cols.pop(0)
        for date_col in date_cols:
            df[date_col] = df[date_col].apply(lambda x: x.strftime(strftime))

    return df


def objects_to_csv(model, fields=None, exclude=None, date_cols=None, foreign_info=None, **kwargs):
    records = filter_objects(model, fields, exclude, foreign_info, **kwargs)

    if records.count():
        df = read_frame(records)  # インスタンスを渡す

        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue()

    return None


def jsonfield_to_list(js_field):
    detail = json.dumps(js_field)
    detail_parsed = json.loads(str(detail))
    keys = []
    values = []
    for key, value in detail_parsed.items():
        keys.append(key)
        values.append(value)

    return {"values": values, "keys": keys}


def qs_to_csv(queryset, json_fields, exclude_fields):
    logger.error(json_fields)
    count = 0
    rows = []
    header = []
    for obj in queryset:
        row = []

        # loop through all the fields in the current post object
        for field in obj._meta.fields:
            if field.name not in exclude_fields:
                if field.name in json_fields:
                    json_contents = jsonfield_to_list(getattr(obj, field.name))
                    logger.error(json_contents)
                    row.extend(json_contents["values"])
                    if count == 0:
                        header.extend(json_contents["keys"])
                else:
                    row.append(getattr(obj, field.name))
                    if count == 0:
                        header.append(field.name)

        if count == 0:
            rows.append(header)
            count += 1

        rows.append(row)

    file = StringIO()
    writer = csv.writer(file, **csv_settings)
    writer.writerows(rows)
    csv_data = file.getvalue()
    StringIO().close()

    return csv_data


def csv_to_db():
    df = pd.read_csv('supermarket_sales.csv')  # use pandas to read the csv
    records = df.to_records()  # convert to records

    # loop through and create a purchase object using django
    for record in records:
        purchase = Purchase(
            city=record[3],
            customer_type=record[4],
            gender=record[5],
            product_line=record[6],
            unit_price=record[7],
            quantity=record[8],
            tax=record[9],
            total=record[10],
            date=datetime.strptime(record[11], '%m/%d/%Y').date(),
            time=record[12],
            payment=record[13],
            cogs=record[14],
            profit=record[16],
            rating=record[17],
        )
        purchase.save()


def get_random_colors(num, colors=[]):
    while len(colors) < num:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        if color not in colors:
            colors.append(color)

    return colors


def get_colors():
    try:
        return palette.hex_colors
    except:
        return get_random_colors(6)


@dataclass
class Chart:
    datasets: List = field(default_factory=list)
    labels: List = field(default_factory=list)
    palette: List = field(default_factory=get_colors)
    tableData: List = field(default_factory=list)

    def from_lists(self, values, labels, stacks):
        self.datasets = []

        if len(self.palette) < len(values):
            self.palette = get_random_colors(num=len(values), colors=self.palette)

        for i in range(len(stacks)):
            self.datasets.append(
                {
                    'name': stacks[i],
                    'backgroundColor': self.palette[i],
                    'data': values[i],
                }
            )

        if len(values) == 1:
            self.datasets[0]['backgroundColor'] = self.palette[:1]

        self.labels = labels

    def from_table(self, values, labels, stacks):
        tableData = []

        for j in range(len(stacks)):
            row_data = []
            row_data.append(stacks[j])
            for i in range(len(labels)):
                row_data.append(values[j][i])

            tableData.append(row_data)

    def from_df(self, df, values, labels, stacks=None, aggfunc=np.sum,
                round_values=0, fill_value=0, sort_by=None, margins=False,
                sort_ascending=False, Top_n=None, df_type="List"):
        pivot = pd.pivot_table(
            df,
            values=values,
            index=stacks,
            columns=labels,
            aggfunc=aggfunc,
            fill_value=0,
            margins=margins
        )

        if sort_by:
            if df_type == "Table":
                pivot = pivot.sort_values(by=sort_by, ascending=sort_ascending)
            else:
                pivot = pivot.sort_values(axis=1, by=sort_by, ascending=sort_ascending)

        if Top_n:
            if df_type == "List":
                pivot = pivot.iloc[:, 0:Top_n]
            elif df_type == "Table":
                pivot = pivot.iloc[1:, 0:Top_n]
            elif df_type == "Ranking":
                pivot = pivot.iloc[:, 0:Top_n]

        pivot = pivot.round(round_values)

        values = pivot.values.tolist()
        labels = pivot.columns.tolist()
        stacks = pivot.index.tolist()

        self.from_lists(values, labels, stacks)

    def from_df_topranking(self, df, values, labels, stacks=None, aggfunc=np.sum,
                           round_values=0, fill_value=0, sort_by=None,
                           sort_ascending=False, Top_n=None):
        pivot = pd.pivot_table(
            df,
            values=values,
            index=stacks,
            columns=labels,
            aggfunc=aggfunc,
            fill_value=0
        )
        print(pivot)
        if sort_by:
            pivot = pivot.sort_values(axis=1, by=sort_by, ascending=sort_ascending)
        if Top_n:
            pivot = pivot.iloc[:, 0:Top_n]

        pivot = pivot.round(round_values)

        values = pivot.values.tolist()
        labels = pivot.columns.tolist()
        stacks = pivot.index.tolist()

        self.from_lists(values, labels, stacks)

    def get_presentation(self):
        return {
            'labels': self.labels,
            'datasets': self.datasets
        }

    def get_presentation_table(self):
        return {
            'table': self.tableData
        }
