import base64
import io
import json
import os
import tempfile

from django.views.static import serve
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .json_utils import CobraSolutionDecoder
from .models import Analysis, Analysis2
from .serializers import AnalysisSerializer, Analysis2Serializer
from .vizan_utils import perform_visualisation


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
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
                with tempfile.NamedTemporaryFile(mode="w") as intermediate_file:
                    analysis_results = serializer.validated_data.get('analysis_results', None)
                    if analysis_results is not None:
                        # analysis_file = analysis_results.temporary_file_path()
                        with open(serializer.validated_data['analysis_results'].temporary_file_path()) as f:
                            analysis_results = json.load(f, cls=CobraSolutionDecoder)
                    vizan_kwargs = {
                        'model_filename': serializer.validated_data['model'].temporary_file_path(),
                        'svg_filename': serializer.validated_data['svg'].temporary_file_path(),
                        'analysis_type': serializer.validated_data.get("analysis_type", None) or 'FBA',
                        'analysis_results': analysis_results,
                        'output_filename': output_file.name,
                        'intermediate_filename': intermediate_file.name,
                    }
                    perform_visualisation(**vizan_kwargs)
            return serve(request, os.path.basename(output_file.name), os.path.dirname(output_file.name))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
