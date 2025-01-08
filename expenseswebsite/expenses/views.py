from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.


@login_required(login_url="/authentication/login")
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    context = {"expenses": expenses}

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
    expense= Expense.objects.get(pk=id)
    context = {"expense": expense, "values": expense}
    
    if request.method == "GET":
        return render(request, "expenses/edit-expense.html", context)
    else:
        messages.info(request, "Expense updated successfully")
        return render(request, "expenses/edit-expense.html", context)       
        

def expense_delete(request, id):
    expense= Expense.objects.get(pk=id)    
    return render(request, "expenses/delete-expense.html")