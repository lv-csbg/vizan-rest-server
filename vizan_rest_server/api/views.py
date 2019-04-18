from .models import Analysis, Analysis2
from .serializers import AnalysisSerializer, Analysis2Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import io
from .vizan_utils import perform_visualisation
import tempfile
from django.views.static import serve
import os


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
            model_stream = io.StringIO(serializer.validated_data["model"])
            fp = tempfile.NamedTemporaryFile(mode="w")
            with fp:
                fp.write(svg.decode("utf-8"))
                # read data from file
                fp.seek(0)
                perform_visualisation(model_stream, fp.name, analysis_type=serializer.validated_data["analysis_type"])
                fp.close()
            with open('prod_subst_0.svg', "rb") as f:
                result_svg = f.read()
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
            vizan_kwargs = {
                'model_filename': serializer.validated_data['model'].temporary_file_path(),
                'svg_filename': serializer.validated_data['svg'].temporary_file_path(),
                'analysis_type': serializer.validated_data.get("analysis_type", None) or 'FBA'
            }
            perform_visualisation(**vizan_kwargs)
            output_file_path = 'prod_subst_0.svg'
            return serve(request, os.path.basename(output_file_path), os.getcwd())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
