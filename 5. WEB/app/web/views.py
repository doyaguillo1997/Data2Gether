from django import template
from django.core.serializers import serialize
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import loader

from app.accounts.services.account_service import get_account
from app.external_sources.cadastres.models import Road
from app.external_sources.cadastres.services.cadastre_importer import CadastreImporter
from app.external_sources.cadastres.services.cadastre_service import CadastreService
from app.external_sources.csv.models import Load
from app.external_sources.csv.services.csv_importer import CsvImporter
from app.external_sources.csv.services.csv_service import get_loads
from app.external_sources.csv.services.csv_service import get_loads_resume
from app.external_sources.idealista.services.idealista_service import get_historic
from app.external_sources.idealista.services.idealista_service import get_predictions
from app.geo.services.geo_service import get_zone
from app.models.services.model_predict import createDataFrame
from app.models.services.model_predict import predict_and_save
from app.models.services.model_predict import predict_one
from app.web.forms import AddressCadastreForm
from app.web.forms import UploadFileForm
from app.web.services.web_service import get_geo_elements
from app.web.services.web_service import get_wallet


def index(request):

    context = {}
    context["segment"] = "index"

    html_template = loader.get_template("index.html")
    return HttpResponse(html_template.render(context, request))


def pages(request: HttpRequest):
    """Load pages templates

    Args:
        request (HttpRequest):

    Returns:
        HttpResponse: html page
    """
    context = {}

    try:

        load_template = request.path.split("/")[-1]
        context["segment"] = load_template

        # Profile needs a form
        if load_template == "profile.html":
            context["form"] = UploadFileForm()
        if load_template == "address_form.html":
            context["form"] = AddressCadastreForm()
            context["roads"] = serialize("json", Road.objects.all())

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("page-404.html")
        return HttpResponse(html_template.render(context, request))

    except Exception:

        html_template = loader.get_template("page-500.html")
        return HttpResponse(html_template.render(context, request))


# AJAX


def get_map_data(request: HttpRequest):
    """Get the information related to the maps

    Args:
        request (HttpRequest):

    Returns:
        JsonResponse: 200 with the information
    """
    geo_id = request.GET.get("id", None)

    geo_parent = get_zone(geo_id)
    historic = list(get_historic(geo_id))
    predictions = list(get_predictions(geo_id))
    data = {
        "geoParent": {
            "name": geo_parent.name,
            "level": geo_parent.level.level,
            "centroid": {
                "lng": geo_parent.centroid.x,
                "lat": geo_parent.centroid.y,
            },
        },
        "polygons": serialize("polygons_geojson", get_geo_elements(geo_id)),
        "historic": serialize("json", historic),
        "predictions": serialize("json", predictions),
        "lastHistoric": serialize("json", [historic[len(historic) - 1]]),
    }

    return JsonResponse(
        data,
        safe=False,
        status=200,
    )


def get_profile_data(request: HttpRequest):
    """Get the information related to the profile

    Args:
        request (HttpRequest):

    Returns:
        JsonResponse: 200 with the information
    """
    account_id = request.GET.get("id", None)

    account = get_account(account_id)
    loads = get_loads_resume(account_id)

    data = {
        "name": account.name,
        "loads": loads,
        "countLoad": len(loads),
        "countProperties": sum(load["count"] for load in loads),
    }

    return JsonResponse(
        data,
        safe=False,
        status=200,
    )


def get_wallet_data(request: HttpRequest):
    """Get wallet ifnormation

    Args:
        request (HttpRequest):

    Returns: JsonResponse: 200 with the wallet if not exceptions, else 500
    """
    load_id = request.GET.get("loadId", None)
    if not load_id:
        account_id = request.GET.get("accountId", None)
        load_id = Load.objects.filter(account=account_id).first().id
    try:
        wallet = get_wallet(load_id)
        account_loads = list(get_loads(wallet["account_id"]).values("name", "id"))
        data = {
            "wallet": wallet,
            "total_buyed_price": sum(
                [property["buyed_price"] for property in wallet["properties"]]
            ),
            "total_estimated_price": sum(
                [property["estimated_price"] for property in wallet["properties"]]
            ),
            "loads": account_loads,
        }

        return JsonResponse(
            data,
            safe=False,
            status=200,
        )
    except:
        return JsonResponse(
            "",
            safe=False,
            status=500,
        )


def load_cadastre_info(request: HttpRequest):
    """Load cadastral information about a load

    Args:
        request (HttpRequest):

    Returns:
        JsonResponse: 200 with the number of properties with this new information
    """
    load_id = request.GET.get("id", None)

    load = Load.objects.filter(id=load_id).first()
    if load is None:
        return JsonResponse(
            None,
            safe=False,
            status=404,
        )

    try:
        cadastre_importer = CadastreImporter(load)

        return JsonResponse(
            cadastre_importer.cadastres_loaded,
            safe=False,
            status=200,
        )
    except:
        return JsonResponse(
            "",
            safe=False,
            status=500,
        )


def create_load(request: HttpRequest):
    """Create new load

    Args:
        request (HttpRequest):

    Returns:
        HttpResponse: reload page if form is valid else 500 page
    """
    form = UploadFileForm(request.POST, request.FILES)

    if form.is_valid():
        account = get_account(form.data["account"])
        mapper = {
            "external_id": form.data["external_id"],
            "RC": form.data["rc"],
            "buyed_price": form.data["buyed_price"],
        }
        CsvImporter(account, form.data["name"], mapper, request.FILES["file"])

        # Reload the page
        return redirect("/profile.html")
    else:
        return redirect("/page-500.html")


def estimate_property(request: HttpRequest):
    """Estimate price of a property

    Args:
        request (HttpRequest):

    Returns:
        HttpResponse: reload page if form is valid else 500 page
    """
    form = AddressCadastreForm(request.POST)
    if form.is_valid():
        try:
            road = Road.objects.get(pk=form.data["road"])
            service = CadastreService()
            address = (
                f"{road.name} ({road.type}), Nº{form.data['number']}, "
                + f"Bl {form.data['block']}, Esc {form.data['stairs']}, "
                + f"Piso {form.data['floor']}, Puerta {form.data['door']}"
            )
            cadastre = service.get_cadastre_by_address(
                "Madrid",
                "Madrid",
                road.type,
                road.name,
                form.data["number"],
                form.data["block"],
                form.data["stairs"],
                form.data["floor"],
                form.data["door"],
            )

            rc = cadastre.cadastral_reference

            estimated_price = predict_one(
                "GOATModel_RandomForestRegressor.pkl", cadastre
            )
            cadastre.delete()

            html_template = loader.get_template("estimated_price.html")
            return HttpResponse(
                html_template.render(
                    {
                        "estimated_price": round(estimated_price, 2),
                        "address": address,
                        "rc": rc,
                    },
                    request,
                )
            )
        except:
            html_template = loader.get_template("estimated_price_error.html")
            return HttpResponse(html_template.render({}, request))
    else:
        return redirect("/page-500.html")


def predict_load(request: HttpRequest):
    """Predict properties in load

    Args:
        request (HttpRequest):

    Returns:
        JsonResponse: 200 if not exceptions, else 500
    """
    load_id = request.GET.get("id", None)

    load = Load.objects.filter(id=load_id).first()
    if load is None:
        return JsonResponse(
            None,
            safe=False,
            status=404,
        )
    try:
        data = createDataFrame(load_id)
        predict_and_save(data)

        return JsonResponse(
            "",
            safe=False,
            status=200,
        )
    except:
        return JsonResponse(
            "",
            safe=False,
            status=500,
        )
