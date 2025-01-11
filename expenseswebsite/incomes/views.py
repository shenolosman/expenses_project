from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import IncomeSource, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences

# Create your views here.


def search_incomes(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        incomes = (
            Income.objects.filter(description__icontains=search_str, owner=request.user)
            | Income.objects.filter(amount__startswith=search_str, owner=request.user)
            | Income.objects.filter(date__startswith=search_str, owner=request.user)
            | Income.objects.filter(source__icontains=search_str, owner=request.user)
        )

        data = incomes.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="/authentication/login")
def index(request):
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    source = IncomeSource.objects.all()
    currency = UserPreferences.objects.get(user=request.user).currency
    # currency = "SEK"
    context = {
        "incomes": incomes,
        "page_obj": page_obj,
        "source": source,
        "currency": currency,
    }

    return render(request, "incomes/index.html", context)


# @login_required(login_url="/authentication/login")
def add_income(request):

    sources = IncomeSource.objects.all()
    context = {"sources": sources, "values": request.POST}
    # import pdb
    # pdb.set_trace()
    if request.method == "GET":
        return render(request, "incomes/add_income.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "incomes/add_income.html", context)

        description = request.POST["description"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "incomes/add_income.html", context)

        source = request.POST["source"]
    
        if not source:
            messages.error(request, "Source is required")
            return render(request, "incomes/add_income.html", context)

        date = request.POST["date"]
        if not date:
            date = now()
        Income.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            source=source,
            date=date,
        )
        messages.success(request, "Record saved successfully")

        return redirect("incomes")


def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = IncomeSource.objects.all()
    context = {"income": income, "values": income, "sources": sources}

    if request.method == "GET":
        return render(request, "incomes/edit-income.html", context)
    else:
        amount = request.POST["amount"]
        description = request.POST["description"]
        source = request.POST["source"]
        date = request.POST["date"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "incomes/edit-income.html", context)

        if not description:
            messages.error(request, "Description is required")
            return render(request, "incomes/edit-income.html", context)

        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        income.owner = request.user
        income.save()

        messages.success(request, "Income updated successfully")
        return redirect("incomes")


def income_delete(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income removed")
    return redirect("incomes")
