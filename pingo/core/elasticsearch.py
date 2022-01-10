import abc
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from core.functions import PrintExceptionError
from .mixins import DynamicQuerySetMixin
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger("error_logger")


def get_count(values):
    return len(values)


class PaginatedElasticSearchAPIView(APIView):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            print("generate_q_expression")
            print(q)
            search = self.document_class.search().query(q).extra(from_=0, size=100)
            response = search.execute()
            print("search.execute")
            print(response)

            serializer = self.serializer_class(response, many=True)
            return Response(serializer.data, status=200)
        except Exception as error:
            print(PrintExceptionError(error))
            return Response(PrintExceptionError(error), status=500)


class ElasticSearchViewSet(DynamicQuerySetMixin, ViewSet):
    serializer_class = None
    document_class = None
    generate_q_expression = None
    omit_fields = None

    def search(self, request, *args, **kwargs):
        try:
            data = self.search_data(request, *args, **kwargs)

            if self.omit_fields is None:
                serializer = self.serializer_class(data, many=True)
            else:
                serializer = self.serializer_class(data, context={"omit_fields": self.omit_fields}, many=True)
            return Response(serializer.data, status=200)
        except Exception as error:
            print(PrintExceptionError(error))
            return Response(PrintExceptionError(error), status=500)

    def search_data(self, request, *args, **kwargs):
        self.get_omit_fields()

        search = self.document_class.search().query(self.generate_q_expression).extra(from_=0, size=100)
        response = search.execute()
        print(f'Found search_data: {response.hits.total.value} hit(s) for query')
        return response
        # df = pd.DataFrame([hit.to_dict() for hit in search.scan()])
        # print(df)
        #
        # elastic_docs = search["hits"]
        # print(elastic_docs)

        # fields = {}
        # item_ids = []
        # for num, doc in enumerate(response["hits"]["hits"]):
        #     source_data = doc["_source"]
        #     print(source_data)
        #     for key, val in enumerate(source_data):
        #         print(val, "--->", source_data[val])
        #
        #         try:
        #             if val == "item":
        #                 item_ids.append(source_data[val].id)
        #             fields[val].append(source_data[val])
        #         except KeyError:
        #             fields[val] = [source_data[val]]
        #
        # fields["item_id"] = item_ids
        # print(fields)
        #
        # df = pd.DataFrame(data=fields)
        # print(df)
        # sk = df.groupby(["item", "user"]).item.agg(get_count).sort_values(ascending=False)[:3]
        # print(sk)
        # print("end of search: data")
        #
        # return response
