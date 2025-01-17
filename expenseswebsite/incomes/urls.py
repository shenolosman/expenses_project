from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="incomes"),
    path("add-income", views.add_income, name="add-income"),
    path("edit-income/<int:id>", views.income_edit, name="income-edit"),
    path("delete-income/<int:id>", views.income_delete, name="income-delete"),
    path("search-incomes", csrf_exempt(views.search_incomes), name="search-incomes"),
]
