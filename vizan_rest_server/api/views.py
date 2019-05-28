import base64
import io
import json
import os
import tempfile
import traceback

import pandas as pd
from django.views.static import serve
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .json_utils import CobraSolutionDecoder
from .models import Analysis, Analysis2
from .serializers import AnalysisSerializer, Analysis2Serializer
from .vizan_utils import perform_visualisation

from xml.parsers.expat import ExpatError


# Create your views here.


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = Analysis.objects.all()
        serializer = AnalysisSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            svg = base64.b64decode(serializer.validated_data["svg"])
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
                with tempfile.NamedTemporaryFile(mode="w") as intermediate_file:
                    with tempfile.NamedTemporaryFile(mode="wb") as svg_file:
                        svg_file.write(svg)
                        svg_file.seek(0)
                        vizan_kwargs = {
                            'model_filename': io.StringIO(serializer.validated_data['model']),
                            'svg_filename': svg_file.name,
                            'analysis_type': serializer.validated_data.get("analysis_type", None) or 'FBA',
                            'output_filename': output_file.name,
                            'intermediate_filename': intermediate_file.name,
                        }
                        perform_visualisation(**vizan_kwargs)
                        output_filename = output_file.name
            with open(output_filename, "rb") as f:
                result_svg = f.read()
            os.remove(output_filename)
            result_svg_encoded = base64.b64encode(result_svg)
            res = {
                'result': result_svg_encoded.decode("utf-8")
            }
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Analysis2List(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = Analysis2.objects.all()
        serializer = Analysis2Serializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Analysis2Serializer(data=request.data)
        if serializer.is_valid():
            try:
                with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
                    with tempfile.NamedTemporaryFile(mode="w") as intermediate_file:
                        analysis_type = serializer.validated_data.get("analysis_type", None) or 'FBA'
                        analysis_results = serializer.validated_data.get('analysis_results', None)
                        if analysis_results is not None:
                            with open(serializer.validated_data['analysis_results'].temporary_file_path()) as f:
                                if analysis_type == 'FBA':
                                    analysis_results = json.load(f, cls=CobraSolutionDecoder)
                                if analysis_type == 'FVA':
                                    analysis_results = pd.read_json(f, typ='frame'),
                        vizan_kwargs = {
                            'model_filename': serializer.validated_data['model'].temporary_file_path(),
                            'svg_filename': serializer.validated_data['svg'].temporary_file_path(),
                            'analysis_type': analysis_type,
                            'analysis_results': analysis_results,
                            'output_filename': output_file.name,
                            'intermediate_filename': intermediate_file.name,
                        }
                        try:
                            perform_visualisation(**vizan_kwargs)
                        except ExpatError as exc:
                            traceback.print_exc()
                            return Response({'svg': ['Error while parsing SVG: {}'.format(exc.args)]},
                                            status=status.HTTP_400_BAD_REQUEST)
                        except Exception as inst:
                            return unknown_exception_logging(inst, "perform_visualisation",
                                                             status.HTTP_500_INTERNAL_SERVER_ERROR)
                return serve(request, os.path.basename(output_file.name), os.path.dirname(output_file.name))
            except Exception as inst:
                return unknown_exception_logging(inst, "after_valid_serializer", status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def unknown_exception_logging(inst, place, res_status):
    errors = {"server": {
        "place": place,
        "exc_type": str(type(inst)),  # the exception instance
        "exc_args": inst.args,
        "traceback": traceback.format_exc()
    }}  # arguments stored in .args
    print(errors)
    traceback.print_exc()
    return Response(errors, status=res_status)
