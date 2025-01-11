from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences

# Create your views here.


def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = (
            Expense.objects.filter(
                description__icontains=search_str, owner=request.user
            )
            | Expense.objects.filter(amount__startswith=search_str, owner=request.user)
            | Expense.objects.filter(date__startswith=search_str, owner=request.user)
            | Expense.objects.filter(category__icontains=search_str, owner=request.user)
        )

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="/authentication/login")
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    currency = UserPreferences.objects.get(user=request.user).currency
    # currency = "SEK"
    context = {
        "expenses": expenses,
        "page_obj": page_obj,
        "categories": categories,
        "currency": currency,
    }

    return render(request, "expenses/index.html", context)


# @login_required(login_url="/authentication/login")
def add_expenses(request):

    categories = Category.objects.all()
    context = {"categories": categories, "values": request.POST}

    if request.method == "GET":
        return render(request, "expenses/add_expenses.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/add_expenses.html", context)

        description = request.POST["description"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/add_expenses.html", context)

        category = request.POST["category"]
        if not category:
            messages.error(request, "Category is required")
            return render(request, "expenses/add_expenses.html", context)

        date = request.POST["date"]
        if not date:
            date = now()
        Expense.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            category=category,
            date=date,
        )
        messages.success(request, "Expense saved successfully")

        return redirect("expenses")


def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {"expense": expense, "values": expense, "categories": categories}

    if request.method == "GET":
        return render(request, "expenses/edit-expense.html", context)
    else:
        amount = request.POST["amount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/edit-expense.html", context)

        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/edit-expense.html", context)

        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.owner = request.user
        expense.save()

        messages.success(request, "Expense updated successfully")
        return redirect("expenses")


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")
    return redirect("expenses")
