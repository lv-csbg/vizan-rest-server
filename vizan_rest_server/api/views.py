from .models import Analysis
from .serializers import AnalysisSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import io
from .vizan_utils import perform_visualisation
import tempfile


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
